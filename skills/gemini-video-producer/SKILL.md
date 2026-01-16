---
name: ai-video-producer
description: >
  AI video production workflow using Google Flow via MCP Playwright browser automation.
  Creates any video type: promotional, educational, narrative, social media,
  animations, game trailers, music videos, product demos, and more. Use when
  users want to create videos with AI, need help with video storyboarding,
  keyframe generation, or video prompt writing. Follows a philosophy-first
  approach: establish visual style and production philosophy, then execute
  scene by scene with user feedback at each stage. Requires MCP Playwright
  server and a Google account with Flow access (Google AI Pro or Ultra subscription).
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, TodoWrite, Task, Bash
---

# AI Video Producer (MCP Edition)

Create professional AI-generated videos through a structured, iterative workflow using Google Flow via MCP Playwright.

## Architecture Overview

This skill uses a **main agent + sub-agents architecture** for efficient context management:

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN AGENT (this skill)                 │
│  - Handles all user interaction and approvals                  │
│  - Creates philosophy.md, style.json, scene-breakdown.md       │
│  - Generates pipeline.json                                      │
│  - Orchestrates sub-agents via Task tool                       │
│  - Updates pipeline.json status after each sub-agent returns   │
│  - Runs FFmpeg concatenation                                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Task tool spawns isolated agents
                            │ with instructions from .claude/agents/
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│reference-gen  │   │keyframe-gen   │   │segment-gen    │
├───────────────┤   ├───────────────┤   ├───────────────┤
│ Images for    │   │ Scene start   │   │ Video clips   │
│ consistency   │   │ compositions  │   │ initial/extend│
│ (subjects,    │   │ (one per      │   │ (8 sec each)  │
│ backgrounds)  │   │ scene)        │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Implementation Note:** Sub-agents are spawned using `subagent_type="general-purpose"` with the full instructions from `.claude/agents/*.md` files embedded in the prompt. This achieves the same isolation benefits while using Claude Code's built-in agent system.

## Prerequisites & Setup

**Required:**
- Google account with Flow access (Google AI Pro or Ultra subscription)
- Internet connection

**MCP Playwright:** If not installed, run automatically:
```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

**No Python scripts required!** Claude directly controls the browser via MCP.

### Auto-Setup Check

At workflow start, verify MCP Playwright is available:
1. Try calling `mcp__playwright__browser_snapshot()`
2. If tools unavailable, offer to install: `claude mcp add playwright -- npx @playwright/mcp@latest`
3. After install, user must restart Claude Code for MCP to load

## Google Flow Overview

**URL:** `https://labs.google/fx/flow`

Flow is a project-based AI filmmaking tool with these generation modes:

| Mode | German Label | Model | Purpose |
|------|--------------|-------|---------|
| Text to Image | "Bild erstellen" | Nano Banana Pro | Generate assets, keyframes, references |
| Video from Frames | "Video aus Frames" | Veo 3.1 - Quality | Generate video segments from start frame |
| Text to Video | "Video aus Text" | Veo 3.1 - Quality | Generate video from text only |
| Ingredients to Video | "Video aus Elementen" | Veo 2 | Generate video with reference images for subject consistency |
| Frames to Video | "Frames zu Video" | Veo 3.1 | Interpolate between start AND end frames |
| **Extend** | "Erweitern" | Veo 3.1 | **Continue from last second of previous clip** |

**Key Interface Elements:**
- Mode selector dropdown (combobox) to switch between generation types
- Text input field for prompts
- "add" buttons for uploading reference images/frames
- "Erstellen" (Create) button to start generation
- Generated content appears in the gallery (Videos/Images tabs)
- Settings button ("tune" / "Einstellungen") to configure model and output count
- **Extend button** on generated videos to continue the action

**REQUIRED Video Settings (configure via Settings button):**
- **Model:** Veo 3.1 - Quality (NOT Veo 3.1 - Fast)
- **Outputs per prompt:** 1 (NOT 2)
- **Aspect ratio:** Querformat 16:9 (Landscape)

## Continuity Architecture

**Problem:** AI video generation is stateless. Each generation starts fresh with no memory of:
- Camera trajectory (was moving left, should continue left)
- Subject identity (this specific ship, not a similar one)
- Narrative state (enemy is losing, human fleet is winning)
- Action continuity (explosion should continue expanding)

**Solution:** This skill uses multiple continuity techniques:

### 1. Extend-Based Segment Chaining
Instead of generating new videos from extracted frames, use Flow's **Extend** feature:
- Extend analyzes the **last second** (not just last frame) of the previous clip
- Preserves motion vectors, camera direction, and subject identity
- Each extension adds 7-8 seconds, chainable up to 148 seconds

### 2. Reference Images for Subject Consistency
Generate "hero images" of key subjects and use as **Ingredients**:
- Human flagship reference (isolated, clean background)
- Enemy vessels reference
- Key characters/objects
- Use same references across ALL segments

### 3. Explicit Prompt Linking
Every continuation prompt MUST reference the previous state:
- "Continuing from the previous shot..."
- "Maintaining the camera's forward momentum..."
- "The [subject], still [previous state], now..."

### 4. Anchor Moments
End each segment with a "holdable" moment for clean extensions:
- "camera holds on the explosion for a beat"
- "ship maintains course, engines steady"
- "camera settles into stable tracking"

### 5. Narrative State Tracking
Track what has happened narratively in pipeline.json:
- Who is winning/losing
- What has been destroyed
- Where the camera is spatially

## MANDATORY WORKFLOW REQUIREMENTS

**YOU MUST FOLLOW THESE RULES:**

1. **ALWAYS use TodoWrite** at the start to create a task list for the entire workflow
2. **NEVER skip phases** - complete each phase in order before proceeding
3. **ALWAYS create required files** - philosophy.md, style.json, scene-breakdown.md, and pipeline.json are REQUIRED
4. **ALWAYS break videos into multiple scenes** - minimum 2 scenes for any video over 5 seconds
5. **ALWAYS ask user for approval** before proceeding to the next phase
6. **NEVER generate without a complete pipeline.json** - plan ALL prompts first, execute second
7. **ALWAYS use sub-agents for generation** - use Task tool to spawn reference-generator, keyframe-generator, segment-generator
8. **ALWAYS update pipeline.json** after each sub-agent returns with status
9. **ALWAYS move downloads to correct locations** - files download to `.playwright-mcp/`, sub-agents handle this

## Sub-Agent Definitions

Three sub-agents are defined in `.claude/agents/`:

### reference-generator
- **Purpose:** Generate visual reference images for video production (subjects, characters, objects, backgrounds)
- **Input:** type (reference|character|object|background), reference_id, subject_name, prompt, output_path, project_dir, style_context
- **Output:** JSON with status, type, reference_id, subject_name, output_path, message
- **Uses:** Flow "Bild erstellen" mode (Nano Banana Pro)
- **Types:**
  - `reference`: Isolated subjects for "Ingredients to Video" (MUST have clean background)
  - `character`: Character designs and poses
  - `object`: Props, vehicles, items
  - `background`: Environment images, settings

### keyframe-generator
- **Purpose:** Generate ONE scene starting keyframe via Flow
- **Input:** scene_id, prompt, output_path, project_dir, style_context
- **Output:** JSON with status, scene_id, output_path, message
- **Uses:** Flow "Bild erstellen" mode (Nano Banana Pro)

### segment-generator
- **Purpose:** Generate video segments via Flow using TWO modes:
  - **First segment of scene:** "Video aus Frames" from keyframe
  - **Continuation segments:** "Extend" from previous segment
- **Input:** segment_id, scene_id, motion_prompt, mode (initial|extend), previous_video_path, start_frame_path, output_video_path, project_dir, anchor_moment
- **Output:** JSON with status, segment_id, scene_id, output_video_path, message
- **Uses:** Flow "Video aus Frames" OR "Extend" feature (Veo 3.1 Quality)

**CRITICAL:** Continuation segments MUST use Extend mode, NOT new generations from extracted frames.

## How to Invoke Sub-Agents

Use the Task tool with the appropriate `subagent_type` and provide the task details in the prompt:

```
Task(
  subagent_type="reference-generator",
  prompt='''
  Generate a subject reference image.

  Task:
  {
    "type": "reference",
    "reference_id": "hero_ship",
    "subject_name": "Hero Battleship",
    "prompt": "Massive silver-blue battleship with angular hull, twin engine pods glowing cyan",
    "isolation_style": "centered on black space background, dramatic three-quarter view",
    "output_path": "output/project/references/hero_ship.png",
    "project_dir": "D:/Project/gemini-video-producer-skill/output/project",
    "style_context": {
      "art_style": "cinematic realistic sci-fi",
      "lighting": "dramatic rim lighting"
    }
  }
  ''',
  description="Generate hero_ship reference"
)
```

**Available Sub-Agent Types:**
- `reference-generator` - for references, characters, objects, backgrounds
- `keyframe-generator` - for scene starting keyframes
- `segment-generator` - for video segments (initial and extend modes)

**Parallel Execution:** For independent tasks, spawn multiple sub-agents in a single message:

```
# References can be generated in parallel
Task(subagent_type="reference-generator", prompt="[reference 1 task]", description="Generate reference 1")
Task(subagent_type="reference-generator", prompt="[reference 2 task]", description="Generate reference 2")
Task(subagent_type="reference-generator", prompt="[background task]", description="Generate background")
```

**Sequential Execution:** Segments within a scene must be sequential (frame chaining):
```
# Segment A first (uses keyframe)
result_A = Task(subagent_type="general-purpose", prompt="[segment-generator instructions] + seg A task...")

# Segment B uses extracted frame from A
result_B = Task(subagent_type="general-purpose", prompt="[segment-generator instructions] + seg B task...")
```

## Pipeline Architecture

### Scene and Segment Model (with Continuity)

Videos are structured hierarchically with **continuity-preserving connections**:
- **References** = isolated subject images used across ALL generations for identity consistency
- **Scenes** = narrative units with distinct visual context (requires new keyframe)
- **Segments** = technical chunks within scenes, connected via **Extend** (NOT frame extraction)

```
REFERENCES (generated once, used everywhere)
├── ref-human-flagship.png (isolated ship on clean background)
├── ref-enemy-dreadnought.png
└── ref-fighter-squadron.png

Scene 1 (20 sec target → 3 segments)
├── Keyframe: scene-01-start.png (GENERATED, establishes visual context)
├── Segment A (8 sec) - mode: "initial" from keyframe
│   └── anchor: "camera holds steady on fleet formation"
├── Segment B (8 sec) - mode: "extend" from Segment A
│   └── prompt: "Continuing the forward motion, the camera..."
│   └── anchor: "flagship fills frame, shields flickering"
└── Segment C (8 sec) - mode: "extend" from Segment B
    └── prompt: "Maintaining momentum, the camera pushes past..."

[TRANSITION: cut - intentional scene break]

Scene 2 (32 sec target → 4 segments)
├── Keyframe: scene-02-start.png (NEW visual context - battle)
├── Segment A (8 sec) - mode: "initial" from keyframe
├── Segment B (8 sec) - mode: "extend" from Segment A
├── Segment C (8 sec) - mode: "extend" from Segment B
└── Segment D (8 sec) - mode: "extend" from Segment C
```

**Why this model:**
- **References** maintain subject identity across the entire video
- **Extend mode** preserves camera trajectory, motion vectors, and action continuity
- **Anchor moments** at segment ends ensure clean extension points
- **Prompt linking** tells the AI what state to continue from
- **Scenes** are intentional narrative breaks where continuity resets are acceptable

## Workflow Phases

### Phase 0: Setup Check

```
1. Navigate to https://labs.google/fx/flow (use MCP directly for initial check)
2. Handle cookie consent if needed
3. Verify login status (look for project list or user avatar)
4. If not logged in, guide user through login
5. Create a new project or use existing one
```

**Note:** This phase is done by the main agent directly to verify MCP is working.

### Phase 1: Production Philosophy (REQUIRED)

Create both files before proceeding:
- `{output_dir}/philosophy.md`
- `{output_dir}/style.json`

**philosophy.md template:**
```markdown
# Production Philosophy: [Project Name]

## Visual Identity
- **Art Style**: [e.g., cinematic realistic, anime, painterly]
- **Color Palette**: [primary colors, mood, temperature]
- **Lighting**: [natural, dramatic, soft, high-contrast]
- **Composition**: [rule of thirds, centered, dynamic angles]

## Motion Language
- **Movement Quality**: [smooth/fluid, dynamic/energetic, subtle/minimal]
- **Pacing**: [fast cuts, slow contemplative, rhythmic]
- **Camera Style**: [static, tracking, handheld, cinematic sweeps]

## Subject Consistency
- **Characters/Products**: [detailed descriptions]
- **Environment**: [setting details]
- **Props/Elements**: [recurring visual elements]

## Constraints
- **Avoid**: [unwanted elements]
- **Maintain**: [elements that must stay consistent]
```

**style.json template:**
```json
{
  "project_name": "Project Name",
  "visual_style": {
    "art_style": "description",
    "color_palette": "description",
    "lighting": "description",
    "composition": "description"
  },
  "motion_language": {
    "movement_quality": "description",
    "pacing": "description",
    "camera_style": "description"
  },
  "subject_consistency": {
    "main_subject": "detailed description",
    "environment": "detailed description"
  },
  "constraints": {
    "avoid": ["list", "of", "things"],
    "maintain": ["list", "of", "things"]
  }
}
```

**CHECKPOINT:** Get user approval before proceeding.

### Phase 2: Scene Breakdown (REQUIRED)

Create `{output_dir}/scene-breakdown.md`:

```markdown
# Scene Breakdown: [Project Name]

## Overview
- **Total Duration**: [X seconds]
- **Number of Scenes**: [N]
- **Segment Duration**: 8 seconds (Flow Veo limit)
- **Video Type**: [promotional/narrative/educational/etc.]

## Key Subjects (for Reference Generation)
List all subjects that need visual consistency:
- **Subject 1**: [e.g., "Human flagship - silver-blue angular dreadnought with cyan engines"]
- **Subject 2**: [e.g., "Enemy vessels - dark crimson ships with organic protrusions"]
- **Subject 3**: [e.g., "Fighter squadron - small angular craft"]

## Camera Path Plan
[Describe the overall camera journey through the video]
- **Scene 1**: Camera starts [position], moves [direction] through [subject]
- **Scene 1→2 Transition**: [CUT/FADE] - intentional [perspective change/location change]
- **Scene 2**: Camera [movement pattern] through [action]
- **Scene 2→3 Transition**: [CUT/FADE]
- **Scene 3**: Camera [final movement] to [ending composition]

---

## Scene 1: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [cut/fade/dissolve/wipe]
**Camera Style**: [single clear style: tracking/dolly/crane/static]

**Narrative State at Start**: [What the viewer should understand]
**Narrative State at End**: [What has changed]

**Starting Keyframe**:
[Detailed visual description for the generated keyframe that starts this scene]

**Segments** (with Extend-based continuity):
1. **Seg A** (0-8s) [mode: initial]:
   - Motion: [Motion description for first 8 seconds]
   - Anchor: [How this segment ends - holdable moment for extension]

2. **Seg B** (8-16s) [mode: extend]:
   - Link: "Continuing from Seg A, maintaining [speed/direction]..."
   - Motion: [Motion description continuing the action]
   - Anchor: [How this segment ends]

3. **Seg C** (16-Xs) [mode: extend]:
   - Link: "Maintaining momentum from Seg B..."
   - Motion: [Motion description for remaining seconds]
   - Anchor: [Final holdable moment before scene transition]

---

## Scene 2: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [null - last scene]
**Camera Style**: [camera movement type]

**Narrative State at Start**: [State carried from Scene 1]
**Narrative State at End**: [Final state]

**Starting Keyframe**:
[Detailed visual description - this is a NEW scene so needs its own keyframe]

**Segments**:
1. **Seg A** (0-8s) [mode: initial]:
   - Motion: [Motion description]
   - Anchor: [Holdable ending]

---
```

**Planning Guidelines:**

| When to Create a New Scene |
|----------------------------|
| Camera angle/perspective changes significantly |
| Location or setting changes |
| Time jump occurs |
| Subject/focus changes |
| You want a cinematic transition (fade, dissolve) |

| When to Add Segments (Same Scene) |
|-----------------------------------|
| Continuous action exceeds 8 seconds |
| Same camera perspective continues |
| No narrative break needed |

**Segment Calculation:** `segments_needed = ceil(scene_duration / 8)`

| Scene Duration | Segments Needed |
|----------------|-----------------|
| 1-8 seconds | 1 |
| 9-16 seconds | 2 |
| 17-24 seconds | 3 |
| 25-32 seconds | 4 |

**CHECKPOINT:** Get user approval before proceeding.

### Phase 3: Pipeline Generation (REQUIRED)

Create `{output_dir}/pipeline.json`:

**Pipeline Schema v4.0 (with Continuity Features):**
```json
{
  "version": "4.0",
  "project_name": "project-name",
  "config": {
    "segment_duration": 8,
    "use_extend_mode": true,
    "use_references": true
  },
  "metadata": {
    "created_at": "ISO timestamp",
    "philosophy_file": "philosophy.md",
    "style_file": "style.json",
    "scene_breakdown_file": "scene-breakdown.md"
  },
  "references": {
    "human_flagship": {
      "type": "reference",
      "subject_name": "Human Flagship",
      "prompt": "Isolated silver-blue angular dreadnought warship, clean dark background, dramatic rim lighting",
      "output": "references/human_flagship.png",
      "status": "pending"
    },
    "enemy_vessel": {
      "type": "reference",
      "subject_name": "Enemy Vessel",
      "prompt": "Isolated dark crimson warship with organic protrusions, clean dark background, dramatic lighting",
      "output": "references/enemy_vessel.png",
      "status": "pending"
    },
    "space_nebula": {
      "type": "background",
      "subject_name": "Space Nebula",
      "prompt": "Deep space vista with colorful purple and blue nebula, scattered stars, cinematic wide composition",
      "output": "references/backgrounds/nebula.png",
      "status": "pending"
    }
  },
  "scenes": [
    {
      "id": "scene-01",
      "title": "Scene Title",
      "duration_target": 24,
      "transition_to_next": "cut",
      "camera_style": "dolly forward",
      "narrative_state": {
        "start": "Human fleet assembled, preparing for battle",
        "end": "Fleet powered up, shields active, ready to engage"
      },
      "first_keyframe": {
        "prompt": "Detailed visual description for scene start...",
        "output": "keyframes/scene-01-start.png",
        "status": "pending"
      },
      "segments": [
        {
          "id": "seg-01-A",
          "mode": "initial",
          "motion_prompt": "Slow dolly push forward through the fleet formation...",
          "anchor_moment": "camera holds steady, flagship centered in frame",
          "output_video": "scene-01/seg-A.mp4",
          "status": "pending"
        },
        {
          "id": "seg-01-B",
          "mode": "extend",
          "link_phrase": "Continuing the forward momentum from the previous shot",
          "motion_prompt": "The camera continues pushing forward, now tracking alongside the flagship...",
          "anchor_moment": "flagship fills frame, shields flickering to life",
          "output_video": "scene-01/seg-B.mp4",
          "status": "pending"
        },
        {
          "id": "seg-01-C",
          "mode": "extend",
          "link_phrase": "Maintaining the tracking movement",
          "motion_prompt": "Camera maintains pace alongside the flagship as weapon ports begin to glow...",
          "anchor_moment": "camera settles into stable position, fleet ready",
          "output_video": "scene-01/seg-C.mp4",
          "status": "pending"
        }
      ]
    },
    {
      "id": "scene-02",
      "title": "Different Scene",
      "duration_target": 8,
      "transition_to_next": null,
      "camera_style": "dynamic tracking",
      "narrative_state": {
        "start": "Battle has begun, fleets engaged",
        "end": "Enemy defeated, human fleet victorious"
      },
      "first_keyframe": {
        "prompt": "New visual context description...",
        "output": "keyframes/scene-02-start.png",
        "status": "pending"
      },
      "segments": [
        {
          "id": "seg-02-A",
          "mode": "initial",
          "motion_prompt": "Motion description...",
          "anchor_moment": "holdable ending moment",
          "output_video": "scene-02/seg-A.mp4",
          "status": "pending"
        }
      ]
    }
  ]
}
```

**Schema v4.0 Changes:**
- `config.use_extend_mode`: Enable Extend-based segment chaining (default: true)
- `config.use_references`: Enable reference images for subject consistency (default: true)
- `references`: Subject reference images for "Ingredients to Video" feature
- `scenes[].camera_style`: Single camera movement type for the entire scene
- `scenes[].narrative_state`: What the viewer should understand at start/end
- `segments[].mode`: "initial" (from keyframe) or "extend" (from previous segment)
- `segments[].link_phrase`: How this segment connects to previous (for extend mode)
- `segments[].anchor_moment`: Holdable ending for clean extension point

### Veo Motion Prompt Guidelines

Motion prompts for video segments MUST follow this official Veo structure:

**Structure:** `[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`

| Component | Description | Example |
|-----------|-------------|---------|
| **Cinematography** | Camera movement, shot type, lens | "Slow dolly push forward", "Wide tracking shot", "Close-up with shallow depth of field" |
| **Subject** | Main visual focus with details | "A massive silver-blue warship with glowing cyan engines", "A young woman's face" |
| **Action** | ONE primary motion/change | "rotates its turrets into firing position", "looks out the window at passing lights" |
| **Context** | Setting, environment, surroundings | "against a backdrop of colorful nebula in deep space", "inside a bus at night during a rainstorm" |
| **Style & Ambiance** | Mood, lighting, visual quality | "Tense pre-battle atmosphere, dramatic rim lighting, photorealistic cinematic quality" |

**Prompt Requirements:**
- **Length:** 100-150 words (3-6 sentences)
- **ONE action per segment:** Don't describe 5 things happening simultaneously
- **Specific camera language:** Use "dolly", "tracking", "pan", "crane", "push", "pull back" - not vague "camera moves"
- **Motion focus:** Describe what MOVES, not static descriptions

**Good Example:**
```
Slow dolly push forward through a massive fleet formation in deep space. Sleek silver-blue warships with angular hulls drift majestically past camera, their cyan engines pulsing with rhythmic blue light. Turrets on the nearest destroyer slowly rotate into firing position as shield generators flicker to life with crackling blue energy. The ships hold perfect V-formation against a backdrop of distant stars and colorful nebula. Tense pre-battle atmosphere, epic cinematic scale, photorealistic sci-fi with dramatic rim lighting on metal hulls.
```

**Bad Example (too many actions, vague camera):**
```
Battle erupts in full fury. Blue and red laser beams crisscross the frame. A battleship fires broadsides. Explosions ripple. Fighters weave between ships. Debris scatters everywhere. Camera tracks through chaos.
```
↑ This has 6+ simultaneous actions and "camera tracks through chaos" is vague.

**Fixed Version:**
```
Dynamic tracking shot following a massive human battleship as it unleashes a devastating broadside. Blue energy bolts erupt from its flanking cannons, streaking across the void toward an enemy cruiser. Orange explosions bloom on the target's shields, rippling with impact energy. Debris and sparks scatter into space. The battleship's hull fills the foreground, weapon ports flashing in sequence. Intense combat lighting with contrasting blue and orange, chaotic but readable action, cinematic sci-fi blockbuster quality.
```

**Common Mistakes to Avoid:**
| Mistake | Problem | Fix |
|---------|---------|-----|
| Multiple simultaneous actions | Veo can't render 5 things at once clearly | Focus on ONE primary action |
| Static descriptions | "Ships in space" describes an image, not video | Add motion: "Ships drift forward, engines pulsing" |
| Vague camera direction | "Camera moves dynamically" | Use specific: "Tracking shot following the ship" |
| Too short (30-50 words) | Lacks detail for quality output | Expand to 100-150 words |
| Missing style/mood | Generic output | Add atmosphere: "Tense, dramatic rim lighting" |

**CHECKPOINT:** Get user approval before proceeding.

### Phase 4: Reference Generation (via sub-agents)

**Purpose:** Generate all visual reference images needed for video production:
- **Subject references** (isolated, for "Ingredients to Video")
- **Characters** (design reference)
- **Objects** (props, vehicles)
- **Backgrounds** (environments)

For each reference in pipeline.json, spawn a `reference-generator` sub-agent:

```
Task(
  subagent_type="reference-generator",
  prompt='''
  Generate a subject reference image.

  Task:
  {
    "type": "reference",
    "reference_id": "human_flagship",
    "subject_name": "Human Flagship",
    "prompt": "Massive silver-blue angular dreadnought warship with glowing cyan engines",
    "isolation_style": "centered on clean dark space background, dramatic rim lighting, three-quarter view",
    "output_path": "<project_dir>/references/human_flagship.png",
    "project_dir": "<project_directory>",
    "style_context": {
      "art_style": "cinematic photorealistic sci-fi",
      "lighting": "dramatic rim lighting"
    }
  }
  ''',
  description="Generate human_flagship reference"
)
```

**Type-Specific Requirements:**

| Type | Isolation | Background | Use Case |
|------|-----------|------------|----------|
| `reference` | REQUIRED | Black/neutral | Upload to "Ingredients to Video" |
| `character` | Recommended | Simple | Character design reference |
| `object` | Recommended | Simple | Prop/item reference |
| `background` | N/A | Full scene | Environment reference |

**Parallel Execution:** All references are independent - spawn all in parallel.

After each sub-agent returns:
1. Parse the returned JSON
2. Update pipeline.json: Set reference's status to "completed" or "error"

**CHECKPOINT:** Review reference images, get user approval. Subject references will be used as "Ingredients" in video generation.

### Phase 5: Scene Keyframes Generation (via sub-agents)

**First, read the agent instructions:**
```
Read(".claude/agents/keyframe-generator.md")
```

For each scene in pipeline.json, spawn a `general-purpose` sub-agent with embedded instructions:

```
Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/keyframe-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "scene_id": "<scene_id>",
    "prompt": "<keyframe_prompt>",
    "output_path": "<full_keyframe_path>",
    "project_dir": "<project_directory>",
    "style_context": {
      "art_style": "<from style.json>",
      "color_palette": "<from style.json>",
      "lighting": "<from style.json>"
    }
  }
  ''',
  description="Generate <scene_id> keyframe"
)
```

**Parallel Execution:** Keyframes are independent - spawn all in parallel:

```python
Task(subagent_type="general-purpose", prompt="[keyframe-generator.md] + scene-01 task", description="Generate scene-01 keyframe")
Task(subagent_type="general-purpose", prompt="[keyframe-generator.md] + scene-02 task", description="Generate scene-02 keyframe")
```

After each sub-agent returns:
1. Parse the returned JSON
2. Update pipeline.json: Set scene's `first_keyframe.status` to "completed" or "error"

**CHECKPOINT:** Review all scene keyframes (read the image files), get user approval.

### Phase 6: Segment Execution (via sub-agents with Extend)

**First, read the agent instructions:**
```
Read(".claude/agents/segment-generator.md")
```

For each scene in pipeline.json:
  For each segment in scene.segments:

**CRITICAL: Use Extend mode for continuation segments (NOT new generations from frames)**

```
# Scene 1 segments - SEQUENTIAL with EXTEND

# Segment A: Initial generation from keyframe
seg_A_result = Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/segment-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "segment_id": "seg-01-A",
    "scene_id": "scene-01",
    "mode": "initial",
    "motion_prompt": "<motion_prompt>. End with: <anchor_moment>",
    "start_frame_path": "<project_dir>/keyframes/scene-01-start.png",
    "output_video_path": "<project_dir>/scene-01/seg-A.mp4",
    "project_dir": "<project_directory>",
    "narrative_context": "<scene.narrative_state.start>"
  }
  ''',
  description="Generate seg-01-A (initial)"
)

# Segment B: EXTEND from Segment A (preserves motion, camera, subjects)
seg_B_result = Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/segment-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "segment_id": "seg-01-B",
    "scene_id": "scene-01",
    "mode": "extend",
    "previous_video_path": "<project_dir>/scene-01/seg-A.mp4",
    "link_phrase": "<link_phrase from pipeline.json>",
    "motion_prompt": "<motion_prompt>. End with: <anchor_moment>",
    "output_video_path": "<project_dir>/scene-01/seg-B.mp4",
    "project_dir": "<project_directory>",
    "narrative_context": "Continuing from previous segment..."
  }
  ''',
  description="Generate seg-01-B (extend)"
)

# Segment C: EXTEND from Segment B
seg_C_result = Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/segment-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "segment_id": "seg-01-C",
    "scene_id": "scene-01",
    "mode": "extend",
    "previous_video_path": "<project_dir>/scene-01/seg-B.mp4",
    "link_phrase": "<link_phrase from pipeline.json>",
    "motion_prompt": "<motion_prompt>. End with: <anchor_moment>",
    "output_video_path": "<project_dir>/scene-01/seg-C.mp4",
    "project_dir": "<project_directory>",
    "narrative_context": "<scene.narrative_state.end>"
  }
  ''',
  description="Generate seg-01-C (extend)"
)
```

**Execution Flow with Extend:**
```
Scene 1 (3 segments) - Sequential chain using EXTEND:
  seg-A: mode=initial, start_frame=keyframe → generate 8s video
  seg-B: mode=extend, previous_video=seg-A.mp4 → extend by 8s (preserves motion!)
  seg-C: mode=extend, previous_video=seg-B.mp4 → extend by 8s

Scene 2 (4 segments) - Can start in parallel with Scene 1:
  seg-A: mode=initial, start_frame=keyframe → generate 8s video
  seg-B: mode=extend, previous_video=seg-A.mp4 → extend by 8s
  seg-C: mode=extend, previous_video=seg-B.mp4 → extend by 8s
  seg-D: mode=extend, previous_video=seg-C.mp4 → extend by 8s
```

**Why Extend is Better Than Frame Extraction:**

| Old Approach (Frame Extraction) | New Approach (Extend) |
|--------------------------------|----------------------|
| Extracts last frame as image | Analyzes last SECOND of video |
| Loses motion vectors | Preserves camera trajectory |
| Loses action momentum | Continues ongoing actions |
| Subject may drift | Maintains subject identity |
| Camera may jump | Smooth camera continuation |

**Prompt Construction for Extend Mode:**
```
Full prompt = link_phrase + " " + motion_prompt + " " + anchor_moment

Example:
"Continuing the forward momentum from the previous shot, the camera
tracks alongside the flagship as its shield generators flicker to life
with crackling blue energy. The massive hull fills the frame as weapon
ports begin to glow. Camera holds steady on the ship's bow, shields
fully active."
```

After each sub-agent returns:
1. Parse the returned JSON
2. Update pipeline.json: Set segment's status to "completed" or "error"
3. If extend failed, retry or fall back to frame extraction mode

**CHECKPOINT:** Get user approval on videos.

### Phase 7: Final Concatenation

**This phase is handled by the main agent directly (not sub-agents).**

Use the `scripts/merge_videos.py` script to concatenate videos. This script uses moviepy and handles resolution differences automatically.

**Merge Script Location:** `scripts/merge_videos.py`

**Usage:**
```bash
python scripts/merge_videos.py -o <output_file> <input1> <input2> [input3] ...
```

**Step 1: Concatenate segments within each scene (seamless)**

For each scene, merge its segments:

```bash
# Scene 1: combine segments
cd {output_dir}
python {skill_dir}/scripts/merge_videos.py -o scene-01/scene.mp4 scene-01/seg-A.mp4 scene-01/seg-B.mp4

# Scene 2: combine segments
python {skill_dir}/scripts/merge_videos.py -o scene-02/scene.mp4 scene-02/seg-A.mp4 scene-02/seg-B.mp4 scene-02/seg-C.mp4 scene-02/seg-D.mp4

# Scene 3: combine segments
python {skill_dir}/scripts/merge_videos.py -o scene-03/scene.mp4 scene-03/seg-A.mp4 scene-03/seg-B.mp4
```

**Step 2: Combine all scenes into final video**

Merge all scene videos into the final output:

```bash
python {skill_dir}/scripts/merge_videos.py -o output.mp4 scene-01/scene.mp4 scene-02/scene.mp4 scene-03/scene.mp4
```

**Script Features:**
- Automatically resizes videos to match the first video's resolution
- Handles any number of input videos (2 or more)
- Uses libx264 codec for compatibility
- Returns JSON status with duration and resolution info

**Script Options:**
| Option | Description |
|--------|-------------|
| `-o, --output` | Output video file path (required) |
| `--codec` | Video codec (default: libx264) |
| `--fps` | Output FPS (default: first video's FPS) |
| `--no-resize` | Don't resize videos to match first |

**Step 3: Clean up and finalize**

1. Remove intermediate files (scene.mp4 per scene) - optional
2. Update pipeline.json to mark project complete

**Final output:** `{output_dir}/output.mp4`

## Output Directory Structure

```
{output_dir}/
├── philosophy.md
├── style.json
├── scene-breakdown.md
├── pipeline.json
├── output.mp4                      <- FINAL VIDEO
├── references/                     <- All visual references
│   ├── hero_ship.png               <- Subject reference (for Ingredients)
│   ├── enemy_vessel.png            <- Subject reference
│   ├── characters/                 <- Character designs
│   │   └── captain.png
│   ├── objects/                    <- Props and items
│   │   └── artifact.png
│   └── backgrounds/                <- Environment images
│       └── nebula.png
├── keyframes/
│   ├── scene-01-start.png          <- Generated scene start
│   └── scene-02-start.png          <- Generated scene start
├── scene-01/
│   ├── seg-A.mp4                   <- Segment videos
│   ├── seg-B.mp4
│   ├── seg-C.mp4
│   └── scene.mp4                   <- Concatenated scene
├── scene-02/
│   ├── seg-A.mp4
│   └── scene.mp4
└── ...
```

**Key Points:**
- `references/` contains all visual reference images (subjects, characters, objects, backgrounds)
- `keyframes/` contains **scene starting compositions** (one per scene)
- `scene-XX/` contains segment videos and concatenated scene video

## TodoWrite Template

```
1. Check MCP Playwright availability
2. Navigate to Flow and verify login
3. Create philosophy.md
4. Create style.json
5. Get user approval on philosophy
6. Create scene-breakdown.md (with scenes and segments)
7. Get user approval on scene breakdown
8. Create pipeline.json (v4.0 with references and segments)
9. Get user approval on pipeline
10. Spawn reference-generator sub-agents (parallel) - subjects, characters, objects, backgrounds
11. Update pipeline.json with reference results
12. Review references, get user approval
13. Spawn keyframe-generator sub-agents (parallel)
14. Update pipeline.json with keyframe results
15. Review keyframes, get user approval
16. Spawn segment-generator sub-agents (sequential per scene, parallel across scenes)
17. Update pipeline.json with segment results
18. Get user approval on videos
19. Concatenate segments within each scene
20. Concatenate scenes into output.mp4
21. Provide final summary
```

## Error Handling

When a sub-agent returns an error:
1. Log the error in pipeline.json (update status to "error", add error message)
2. Inform the user of the failure
3. Offer to retry: spawn a new sub-agent for the failed task
4. Continue with other independent tasks if possible

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Segment Duration | 8 seconds per generation (Flow Veo limit) |
| Image Resolution | Up to 1024x1024 (Nano Banana Pro) |
| Video Resolution | Up to 1080p (4K with AI Ultra) |
| Rate Limiting | Credits-based (100 credits per Quality video) |
| GPU Required | None (cloud-based) |
| Image Model | Nano Banana Pro |
| Video Model | Veo 3.1 - Quality |
| Outputs per Prompt | 1 |

**Key Terminology:**
- **Scene** = A narrative/cinematic unit (any duration). Represents a continuous shot or distinct visual context. Each scene requires a generated starting keyframe.
- **Segment** = A technical 8-second video chunk within a scene. Multiple segments chain together seamlessly via extracted frames to form longer scenes.
- **Sub-agent** = Isolated agent instance spawned via Task tool. Has fresh context, returns result to main agent.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Sub-agent returns error | Check error message, retry with fresh sub-agent |
| Rate limited / Out of credits | Wait or upgrade subscription, then retry |
| Generation stuck | Sub-agent will timeout and return error |
| File not found | Check .playwright-mcp/ directory manually |
| Pipeline out of sync | Re-read pipeline.json, update status fields |
| Not logged in | Guide user to log in at labs.google/fx/flow |
| Generation mode wrong | Verify correct mode selected in dropdown |

