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
                            │ Task tool spawns general-purpose agents
                            │ with embedded instructions from .claude/agents/
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ asset-generator│   │keyframe-generator│ │segment-generator│
│ (general-purpose)│ │ (general-purpose)│ │ (general-purpose)│
├───────────────┤   ├───────────────┤   ├───────────────┤
│ Fresh context │   │ Fresh context │   │ Fresh context │
│ MCP browser   │   │ MCP browser   │   │ MCP browser   │
│ Returns path  │   │ Returns path  │   │ Returns paths │
│ + status only │   │ + status only │   │ + status only │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Benefits:**
- Each generation has isolated memory (no context pollution)
- Browser automation details don't clutter main conversation
- Parallel execution possible for independent tasks
- Easy retry of individual failed generations
- Main agent stays focused on orchestration

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
| Text to Image | "Bild erstellen" | Nano Banana Pro | Generate assets and keyframes |
| Video from Frames | "Video aus Frames" | Veo 3.1 - Quality | Generate video segments from start frame |
| Text to Video | "Video aus Text" | Veo 3.1 - Quality | Generate video from text only |
| Video from Elements | "Video aus Elementen" | Veo 3.1 - Quality | Generate video with reference elements |

**Key Interface Elements:**
- Mode selector dropdown (combobox) to switch between generation types
- Text input field for prompts
- "add" buttons for uploading reference images/frames
- "Erstellen" (Create) button to start generation
- Generated content appears in the gallery (Videos/Images tabs)
- Settings button ("tune" / "Einstellungen") to configure model and output count

**REQUIRED Video Settings (configure via Settings button):**
- **Model:** Veo 3.1 - Quality (NOT Veo 3.1 - Fast)
- **Outputs per prompt:** 1 (NOT 2)
- **Aspect ratio:** Querformat 16:9 (Landscape)

## MANDATORY WORKFLOW REQUIREMENTS

**YOU MUST FOLLOW THESE RULES:**

1. **ALWAYS use TodoWrite** at the start to create a task list for the entire workflow
2. **NEVER skip phases** - complete each phase in order before proceeding
3. **ALWAYS create required files** - philosophy.md, style.json, scene-breakdown.md, and pipeline.json are REQUIRED
4. **ALWAYS break videos into multiple scenes** - minimum 2 scenes for any video over 5 seconds
5. **ALWAYS ask user for approval** before proceeding to the next phase
6. **NEVER generate without a complete pipeline.json** - plan ALL prompts first, execute second
7. **ALWAYS use sub-agents for generation** - use Task tool to spawn asset-generator, keyframe-generator, segment-generator
8. **ALWAYS update pipeline.json** after each sub-agent returns with status
9. **ALWAYS move downloads to correct locations** - files download to `.playwright-mcp/`, sub-agents handle this

## Sub-Agent Definitions

Three sub-agents are defined in `.claude/agents/`:

### asset-generator
- **Purpose:** Generate ONE asset image (character, background, object) via Flow
- **Input:** asset_id, prompt, output_path, project_dir
- **Output:** JSON with status, asset_id, output_path, message
- **Uses:** Flow "Bild erstellen" mode (Nano Banana Pro)

### keyframe-generator
- **Purpose:** Generate ONE scene starting keyframe via Flow
- **Input:** scene_id, prompt, output_path, project_dir, style_context
- **Output:** JSON with status, scene_id, output_path, message
- **Uses:** Flow "Bild erstellen" mode (Nano Banana Pro)

### segment-generator
- **Purpose:** Generate ONE video segment (8 seconds max) via Flow
- **Input:** segment_id, scene_id, motion_prompt, start_frame_path, output_video_path, project_dir, extract_end_frame, end_frame_path
- **Output:** JSON with status, segment_id, scene_id, output_video_path, end_frame_path, message
- **Uses:** Flow "Video aus Frames" mode (Veo 3.1 Fast)

## How to Invoke Sub-Agents

Use the Task tool with `subagent_type="general-purpose"` and embed the agent instructions from `.claude/agents/` in the prompt:

```
Task(
  subagent_type="general-purpose",
  prompt='''
  You are an asset-generator sub-agent. Follow these instructions:

  [Read and embed full contents of .claude/agents/asset-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "asset_id": "hero_character",
    "prompt": "A heroic knight in silver armor, standing tall, dramatic lighting",
    "output_path": "output/project/assets/characters/hero.png",
    "project_dir": "D:/Project/gemini-video-producer-skill/output/project"
  }
  ''',
  description="Generate hero character asset"
)
```

**IMPORTANT:** Before spawning sub-agents, use the Read tool to load the agent instructions:
- `Read(".claude/agents/asset-generator.md")` for asset generation
- `Read(".claude/agents/keyframe-generator.md")` for keyframe generation
- `Read(".claude/agents/segment-generator.md")` for segment generation

Then embed those instructions in the Task prompt.

**Parallel Execution:** For independent tasks, spawn multiple sub-agents in a single message:

```
# Assets can be generated in parallel (all use general-purpose with embedded instructions)
Task(subagent_type="general-purpose", prompt="[asset-generator instructions] + asset 1 task", description="Generate asset 1")
Task(subagent_type="general-purpose", prompt="[asset-generator instructions] + asset 2 task", description="Generate asset 2")
Task(subagent_type="general-purpose", prompt="[asset-generator instructions] + asset 3 task", description="Generate asset 3")
```

**Sequential Execution:** Segments within a scene must be sequential (frame chaining):
```
# Segment A first (uses keyframe)
result_A = Task(subagent_type="general-purpose", prompt="[segment-generator instructions] + seg A task...")

# Segment B uses extracted frame from A
result_B = Task(subagent_type="general-purpose", prompt="[segment-generator instructions] + seg B task...")
```

## Pipeline Architecture

### Scene and Segment Model

Videos are structured hierarchically:
- **Scenes** contain one or more **segments**
- Each **scene** has a generated starting keyframe (new visual context)
- **Segments** within a scene chain via extracted frames (seamless continuity)
- **Transitions** between scenes are applied programmatically (cut, fade, dissolve)

```
Scene 1 (20 sec target → 3 segments)
├── Keyframe: scene-01-start.png (GENERATED via keyframe-generator)
├── Segment A (8 sec) → extract frame (via segment-generator)
├── Segment B (8 sec) → extract frame (via segment-generator)
└── Segment C (4 sec) (via segment-generator, no extraction)

[TRANSITION: fade/cut/dissolve]

Scene 2 (8 sec target → 1 segment)
├── Keyframe: scene-02-start.png (GENERATED via keyframe-generator)
└── Segment A (8 sec) (via segment-generator)
```

**Why this model:**
- Scenes = narrative units (different camera, location, or perspective)
- Segments = technical chunks needed due to 8-second generation limit
- Keyframes generated per scene (not per segment) - establishes visual context
- Transitions between scenes are real cinematic choices (not just frame chaining)

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

---

## Scene 1: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [cut/fade/dissolve/wipe]

**Starting Keyframe**:
[Detailed visual description for the generated keyframe that starts this scene]

**Segments**:
1. **Seg A** (0-8s): [Motion description for first 8 seconds]
2. **Seg B** (8-16s): [Motion description for next 8 seconds]
3. **Seg C** (16-Xs): [Motion description for remaining seconds]

**Camera**: [static/tracking/pan/zoom/POV]

---

## Scene 2: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [null - last scene]

**Starting Keyframe**:
[Detailed visual description - this is a NEW scene so needs its own keyframe]

**Segments**:
1. **Seg A** (0-8s): [Motion description]

**Camera**: [camera style]

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

**Pipeline Schema v3.0:**
```json
{
  "version": "3.0",
  "project_name": "project-name",
  "config": {
    "segment_duration": 8
  },
  "metadata": {
    "created_at": "ISO timestamp",
    "philosophy_file": "philosophy.md",
    "style_file": "style.json",
    "scene_breakdown_file": "scene-breakdown.md"
  },
  "assets": {
    "backgrounds": {
      "<id>": {
        "prompt": "Detailed description...",
        "output": "assets/backgrounds/<id>.png",
        "status": "pending"
      }
    },
    "characters": {
      "<id>": {
        "prompt": "Detailed description...",
        "output": "assets/characters/<id>.png",
        "status": "pending"
      }
    }
  },
  "scenes": [
    {
      "id": "scene-01",
      "title": "Scene Title",
      "duration_target": 20,
      "transition_to_next": "cut",
      "first_keyframe": {
        "prompt": "Detailed visual description for scene start...",
        "output": "keyframes/scene-01-start.png",
        "status": "pending"
      },
      "segments": [
        {
          "id": "seg-01-A",
          "motion_prompt": "Motion description for first 8 seconds...",
          "output_video": "scene-01/seg-A.mp4",
          "status": "pending"
        },
        {
          "id": "seg-01-B",
          "motion_prompt": "Continuing motion for next 8 seconds...",
          "output_video": "scene-01/seg-B.mp4",
          "status": "pending"
        },
        {
          "id": "seg-01-C",
          "motion_prompt": "Final motion segment...",
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
      "first_keyframe": {
        "prompt": "New visual context description...",
        "output": "keyframes/scene-02-start.png",
        "status": "pending"
      },
      "segments": [
        {
          "id": "seg-02-A",
          "motion_prompt": "Motion description...",
          "output_video": "scene-02/seg-A.mp4",
          "status": "pending"
        }
      ]
    }
  ]
}
```

**Schema Notes:**
- `config.segment_duration`: Flow Veo's max video length (8 seconds)
- `scenes[].duration_target`: Desired scene length → determines segment count: `ceil(duration / 8)`
- `scenes[].transition_to_next`: Transition to apply before next scene (`cut`, `fade`, `dissolve`, `wipe`, or `null` for last scene)
- `scenes[].first_keyframe`: Generated image to establish scene's visual context
- `scenes[].segments[]`: Technical video chunks that chain seamlessly within the scene

**CHECKPOINT:** Get user approval before proceeding.

### Phase 4: Asset Execution (via sub-agents)

**First, read the agent instructions:**
```
Read(".claude/agents/asset-generator.md")
```

For each asset in pipeline.json, spawn a `general-purpose` sub-agent with embedded instructions:

```
Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/asset-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "asset_id": "<asset_id>",
    "prompt": "<asset_prompt>",
    "output_path": "<full_output_path>",
    "project_dir": "<project_directory>"
  }
  ''',
  description="Generate <asset_id> asset"
)
```

**Parallel Execution:** Assets are independent - spawn all sub-agents in parallel:

```python
# All assets can run simultaneously (embed same instructions in each)
Task(subagent_type="general-purpose", prompt="[asset-generator.md] + asset1 task", description="Generate asset 1")
Task(subagent_type="general-purpose", prompt="[asset-generator.md] + asset2 task", description="Generate asset 2")
Task(subagent_type="general-purpose", prompt="[asset-generator.md] + asset3 task", description="Generate asset 3")
```

After each sub-agent returns:
1. Parse the returned JSON
2. Update pipeline.json: Set asset's status to "completed" or "error"
3. If error, note it for user review

**CHECKPOINT:** Review assets (read the image files), get user approval.

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

### Phase 6: Segment Execution (via sub-agents)

**First, read the agent instructions:**
```
Read(".claude/agents/segment-generator.md")
```

For each scene in pipeline.json:
  For each segment in scene.segments:

**IMPORTANT: Segments within a scene MUST be sequential (frame chaining)**

```
# Scene 1 segments - SEQUENTIAL
seg_A_result = Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/segment-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "segment_id": "seg-01-A",
    "scene_id": "scene-01",
    "motion_prompt": "<motion_prompt>",
    "start_frame_path": "<project_dir>/keyframes/scene-01-start.png",
    "output_video_path": "<project_dir>/scene-01/seg-A.mp4",
    "project_dir": "<project_directory>",
    "extract_end_frame": true,
    "end_frame_path": "<project_dir>/scene-01/extracted/after-seg-A.png"
  }
  ''',
  description="Generate seg-01-A"
)

# Wait for seg_A to complete, then use its extracted frame
seg_B_result = Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/segment-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "segment_id": "seg-01-B",
    "scene_id": "scene-01",
    "motion_prompt": "<motion_prompt>",
    "start_frame_path": "<project_dir>/scene-01/extracted/after-seg-A.png",
    "output_video_path": "<project_dir>/scene-01/seg-B.mp4",
    "project_dir": "<project_directory>",
    "extract_end_frame": true,
    "end_frame_path": "<project_dir>/scene-01/extracted/after-seg-B.png"
  }
  ''',
  description="Generate seg-01-B"
)

# Last segment - no extraction needed
seg_C_result = Task(
  subagent_type="general-purpose",
  prompt='''
  [Embed full contents of .claude/agents/segment-generator.md here]

  ---
  NOW EXECUTE THIS TASK:
  {
    "segment_id": "seg-01-C",
    "scene_id": "scene-01",
    "motion_prompt": "<motion_prompt>",
    "start_frame_path": "<project_dir>/scene-01/extracted/after-seg-B.png",
    "output_video_path": "<project_dir>/scene-01/seg-C.mp4",
    "project_dir": "<project_directory>",
    "extract_end_frame": false,
    "end_frame_path": null
  }
  ''',
  description="Generate seg-01-C"
)
```

**Cross-Scene Parallelization:** Different scenes can run in parallel since they don't share frames:

```python
# Scene 1 and Scene 2 keyframes are ready - both scene segment chains can run in parallel
# (But segments WITHIN each scene must be sequential)
```

**Execution Flow:**
```
Scene 1 (3 segments) - Sequential chain:
  seg-A: start=keyframe → generate → extract frame
  seg-B: start=after-seg-A.png → generate → extract frame
  seg-C: start=after-seg-B.png → generate → (no extraction)

Scene 2 (1 segment) - Can run in parallel with Scene 1:
  seg-A: start=keyframe → generate → (no extraction)
```

After each sub-agent returns:
1. Parse the returned JSON
2. Update pipeline.json: Set segment's status to "completed" or "error"

**CHECKPOINT:** Get user approval on videos.

### Phase 7: Final Concatenation with Transitions

**This phase is handled by the main agent directly (not sub-agents).**

Two-step concatenation: first combine segments within each scene, then combine scenes with transitions.

**Step 1: Concatenate segments within each scene (seamless)**

For each scene, concatenate its segments without transitions:

```powershell
# Scene 1: combine segments
@"
file 'scene-01/seg-A.mp4'
file 'scene-01/seg-B.mp4'
file 'scene-01/seg-C.mp4'
"@ | Out-File -FilePath "scene-01/concat.txt" -Encoding ASCII

ffmpeg -f concat -safe 0 -i "scene-01/concat.txt" -c copy "scene-01/scene.mp4"
```

**Step 2: Combine scenes with transitions**

Apply transitions between scenes based on `transition_to_next` in pipeline.json:

| Transition | FFmpeg Implementation |
|------------|----------------------|
| `cut` | Simple concatenation (no filter) |
| `fade` | `xfade=transition=fade:duration=0.5` |
| `dissolve` | `xfade=transition=dissolve:duration=0.5` |
| `wipe` | `xfade=transition=wipeleft:duration=0.5` |

**For `cut` transitions only (simple case):**
```powershell
@"
file 'scene-01/scene.mp4'
file 'scene-02/scene.mp4'
"@ | Out-File -FilePath "concat-list.txt" -Encoding ASCII

ffmpeg -f concat -safe 0 -i "concat-list.txt" -c copy "output.mp4"
```

**For fade/dissolve/wipe transitions:**
```powershell
# Two scenes with fade (0.5 sec transition)
# offset = scene1_duration - transition_duration
ffmpeg -i "scene-01/scene.mp4" -i "scene-02/scene.mp4" `
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=15.5[v]" `
  -map "[v]" -c:v libx264 "output.mp4"

# Three scenes with different transitions
ffmpeg -i "scene-01/scene.mp4" -i "scene-02/scene.mp4" -i "scene-03/scene.mp4" `
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=15.5[v1]; `
                   [v1][2:v]xfade=transition=dissolve:duration=0.5:offset=23.5[v2]" `
  -map "[v2]" -c:v libx264 "output.mp4"
```

**Available xfade transitions:** `fade`, `dissolve`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `slideleft`, `slideright`, `pixelize`, `radial`, `smoothleft`, `smoothright`

**Step 3: Clean up and finalize**

1. Remove intermediate files (concat.txt, scene.mp4 per scene) - optional
2. Update pipeline.json to mark project complete

**Final output:** `{output_dir}/output.mp4`

## Output Directory Structure

```
{output_dir}/
├── philosophy.md
├── style.json
├── scene-breakdown.md
├── pipeline.json
├── output.mp4                      <- FINAL VIDEO (with transitions)
├── assets/
│   ├── characters/
│   └── backgrounds/
├── keyframes/
│   ├── scene-01-start.png          <- Generated (scene 1 start)
│   └── scene-02-start.png          <- Generated (scene 2 start)
├── scene-01/
│   ├── seg-A.mp4                   <- Segment videos
│   ├── seg-B.mp4
│   ├── seg-C.mp4
│   ├── scene.mp4                   <- Concatenated scene (intermediate)
│   └── extracted/                  <- Internal extracted frames
│       ├── after-seg-A.png
│       └── after-seg-B.png
├── scene-02/
│   ├── seg-A.mp4
│   └── scene.mp4
└── ...
```

**Key Points:**
- `keyframes/` contains only **generated** keyframes (one per scene)
- `scene-XX/extracted/` contains **extracted** frames (internal, for segment chaining)
- `scene-XX/scene.mp4` is the intermediate concatenated scene (before transitions)

## TodoWrite Template

```
1. Check MCP Playwright availability
2. Navigate to Flow and verify login
3. Create philosophy.md
4. Create style.json
5. Get user approval on philosophy
6. Create scene-breakdown.md (with scenes and segments)
7. Get user approval on scene breakdown
8. Create pipeline.json (v3.0 with nested segments)
9. Get user approval on pipeline
10. Spawn asset-generator sub-agents (parallel)
11. Update pipeline.json with asset results
12. Review assets, get user approval
13. Spawn keyframe-generator sub-agents (parallel)
14. Update pipeline.json with keyframe results
15. Review keyframes, get user approval
16. Spawn segment-generator sub-agents (sequential per scene, parallel across scenes)
17. Update pipeline.json with segment results
18. Get user approval on videos
19. Concatenate segments within each scene (ffmpeg)
20. Concatenate scenes with transitions into output.mp4
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

