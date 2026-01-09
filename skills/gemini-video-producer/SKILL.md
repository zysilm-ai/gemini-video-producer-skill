---
name: ai-video-producer
description: >
  AI video production workflow using Google Whisk via MCP Playwright browser automation.
  Creates any video type: promotional, educational, narrative, social media,
  animations, game trailers, music videos, product demos, and more. Use when
  users want to create videos with AI, need help with video storyboarding,
  keyframe generation, or video prompt writing. Follows a philosophy-first
  approach: establish visual style and production philosophy, then execute
  scene by scene with user feedback at each stage. Requires MCP Playwright
  server and a Google account with Whisk access (labs.google).
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, TodoWrite, mcp__playwright__*
---

# AI Video Producer (Whisk Edition)

Create professional AI-generated videos through a structured, iterative workflow using Google Whisk via MCP Playwright.

## Prerequisites & Setup

**Required:**
- Google account with access to Google Labs (labs.google)
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

## MANDATORY WORKFLOW REQUIREMENTS

**YOU MUST FOLLOW THESE RULES:**

1. **ALWAYS use TodoWrite** at the start to create a task list for the entire workflow
2. **NEVER skip phases** - complete each phase in order before proceeding
3. **ALWAYS create required files** - philosophy.md, style.json, scene-breakdown.md, and pipeline.json are REQUIRED
4. **ALWAYS break videos into multiple scenes** - minimum 2 scenes for any video over 5 seconds
5. **ALWAYS ask user for approval** before proceeding to the next phase
6. **NEVER generate without a complete pipeline.json** - plan ALL prompts first, execute second
7. **ALWAYS use MCP Playwright** for Whisk interaction - no Python scripts
8. **ALWAYS move downloads to correct locations** - files download to `.playwright-mcp/`, must be moved to pipeline output paths
9. **ALWAYS review generated outputs using VLM** - view images after each stage, assess quality
10. **ALWAYS ask about Approval Mode** at the very start (see below)

## Approval Mode Selection (FIRST STEP)

**At the very beginning of the workflow, ask the user to choose an approval mode:**

Use AskUserQuestion with these options:
- **"Manual approval"** - User approves each phase before proceeding (philosophy, scenes, assets, pipeline, keyframes, videos)
- **"Automatic approval"** - LLM proceeds automatically, user only reviews final output

| Mode | User Interaction | Best For |
|------|------------------|----------|
| **Manual** | Checkpoint at each phase | First-time projects, precise control, learning the workflow |
| **Automatic** | Only final review | Trusted workflow, quick generation, batch production |

**Store the selected mode** and apply it to all checkpoints throughout the workflow.

### Standard Checkpoint Format (ALL PHASES)

**Checkpoint behavior depends on the selected Approval Mode:**

#### Manual Approval Mode (default)
1. Show the output to user (file path or display content)
2. Ask for approval using AskUserQuestion:
   - **"Approve"** - Proceed to next step
   - User can select **"Other"** to specify what needs to be changed
3. **If user does not approve:**
   - User specifies what to change
   - Make the requested adjustments
   - Show updated result → Ask again → Repeat until approved
4. **Do NOT proceed to next phase until approved**

#### Automatic Approval Mode
1. Show the output to user (file path or display content)
2. **LLM reviews the output using VLM capability** (for images/videos)
3. If LLM assessment is positive → Proceed automatically
4. If LLM detects issues → Fix and regenerate before proceeding
5. **User only reviews final output at the end**

## Architecture

```
Claude reads pipeline.json
    |
Claude -> MCP Playwright -> Google Whisk (labs.google/fx/tools/whisk)
    |
Claude updates pipeline.json status
    |
Claude moves downloads to correct output paths
```

**Benefits:**
- Self-healing: Claude adapts to UI changes by semantic understanding
- No brittle CSS selectors that break when Whisk updates
- Simpler codebase - no Python Playwright code to maintain
- Real-time adaptation to page state

## Whisk Reference Slots

Whisk uses three reference image slots that map to our asset types:

| Whisk Slot | German Label | Our Asset Type | Purpose |
|------------|--------------|----------------|---------|
| **Subject** | Motiv | Characters | Person/creature reference for identity |
| **Scene** | Szene | Backgrounds | Location/environment reference |
| **Style** | Stil | Styles | Visual treatment reference |

This is a perfect match for our asset-based workflow!

## MCP Playwright Operations Reference

### Login Check & Flow

```
1. Navigate to Whisk:
   mcp__playwright__browser_navigate(url="https://labs.google/fx/tools/whisk")

2. Take snapshot to check state:
   mcp__playwright__browser_snapshot()

3. If cookie consent appears (German: "Auf labs.google/fx werden..."):
   - Click "Ausblenden" (Hide) or accept button

4. Check if logged in:
   - Look for "Tool aufrufen" button on landing page
   - Or look for profile image button if already in tool
   - If login form appears: inform user to log in manually

5. If on landing page:
   - Click "Tool aufrufen" (Access tool) button to enter the workspace

6. If not logged in:
   - Inform user: "Please log in to your Google account in the browser window"
   - Wait for login: mcp__playwright__browser_wait_for(text="Whisk", time=120)
```

### Image Generation (with Reference Slots)

Whisk generates images using up to three reference slots plus a text prompt:

```
1. Ensure in Whisk workspace:
   - URL should be: labs.google/fx/.../whisk/project
   - If on landing page, click "Tool aufrufen"

2. Expand the reference panel (if collapsed):
   - Click "Bilder hinzufügen" (Add images) button to show slots

3. Upload reference images to appropriate slots:

   a. For CHARACTER reference (Motiv/Subject slot):
      - Click on the "person" slot area
      - Click "Bild hochladen" (Upload image) button
      - mcp__playwright__browser_file_upload(paths=["assets/characters/<id>.png"])

   b. For BACKGROUND reference (Szene/Scene slot):
      - Click on the "location_on" slot area
      - Click "Bild hochladen" (Upload image) button
      - mcp__playwright__browser_file_upload(paths=["assets/backgrounds/<id>.png"])

   c. For STYLE reference (Stil/Style slot):
      - Click on the "stylus_note" slot area
      - Click "Bild hochladen" (Upload image) button
      - mcp__playwright__browser_file_upload(paths=["assets/styles/<id>.png"])

4. Type the generation prompt:
   mcp__playwright__browser_type(
     element="Prompt input textbox",
     ref="<textbox_ref>",
     text="<detailed_prompt_description>",
     submit=false
   )

5. Click generate button:
   mcp__playwright__browser_click(element="Prompt senden", ref="<ref>")

6. Wait for generation (15-60 seconds):
   mcp__playwright__browser_wait_for(time=30)
   mcp__playwright__browser_snapshot()  # Check if image appeared

7. Download the generated image:
   - Right-click on generated image or find download button
   - mcp__playwright__browser_click(element="Download button", ref="<ref>")
   - Wait for download

8. Move file to correct location:
   - Downloaded to: .playwright-mcp/<filename>.png
   - Move to: <pipeline_output_path>
   - Use PowerShell: Move-Item -Path "source" -Destination "dest"

9. Update pipeline.json status to "completed"

10. Clear slots for next generation:
    - Click X on each reference slot to remove
    - Or start new project
```

### Video Generation (Animate Image)

Whisk animates existing images to create videos:

```
1. First, generate or have a keyframe image ready

2. Navigate to video mode:
   - Click "videocam_auto" button in toolbar

3. Find the generated image in the gallery:
   - Images appear in the workspace after generation
   - Click on the image you want to animate

4. Look for animation/video option:
   - Find "Animate" or video generation button
   - Click to start video generation

5. Wait for video generation (60-180 seconds):
   mcp__playwright__browser_wait_for(time=60)
   mcp__playwright__browser_snapshot()

6. Download the video:
   - Find video in the video gallery (videocam_auto mode)
   - Click download button
   - Wait for completion

7. Move to correct output path:
   - Downloaded to: .playwright-mcp/<filename>.mp4
   - Move to: scene-XX/seg-X.mp4

8. Extract last frame for next segment:
   ```powershell
   ffmpeg -sseof -1 -i "scene-01/seg-A.mp4" -frames:v 1 "scene-01/extracted/after-seg-A.png"
   ```

9. Update pipeline.json status
```

### Whisk-Specific Tips

- **Reference slots are optional**: You can use 0, 1, 2, or all 3 slots
- **Character consistency**: Always use the same character asset in the Subject slot
- **Style consistency**: Upload your style anchor to the Style slot for consistent look
- **Clear slots between generations**: Remove references when generating different content
- **Check video mode**: Videos appear in a separate gallery (videocam_auto button)

### Key MCP Tools

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_snapshot` | Get page accessibility tree (preferred over screenshot) |
| `browser_click` | Click element by ref |
| `browser_type` | Type text into input, optionally submit |
| `browser_file_upload` | Upload files |
| `browser_wait_for` | Wait for text/time |
| `browser_take_screenshot` | Visual screenshot (for user review) |

## Pipeline Architecture

### Scene and Segment Model

Videos are structured hierarchically:
- **Scenes** contain one or more **segments**
- Each **scene** has a generated starting keyframe (new visual context)
- **Segments** within a scene chain via extracted frames (seamless continuity)
- **Transitions** between scenes are applied programmatically (cut, fade, dissolve)

```
Scene 1 (20 sec target → 3 segments)
├── Keyframe: scene-01-start.png (GENERATED)
├── Segment A (8 sec) → extract frame
├── Segment B (8 sec) → extract frame
└── Segment C (4 sec)

[TRANSITION: fade/cut/dissolve]

Scene 2 (8 sec target → 1 segment)
├── Keyframe: scene-02-start.png (GENERATED - new visual context)
└── Segment A (8 sec)
```

**Why this model:**
- Scenes = narrative units (different camera, location, or perspective)
- Segments = technical chunks needed due to 8-second generation limit
- Keyframes generated per scene (not per segment) - establishes visual context
- Transitions between scenes are real cinematic choices (not just frame chaining)

## Workflow Phases

### Phase 0: Setup Check

```
1. Navigate to https://labs.google/fx/tools/whisk
2. Handle cookie consent if needed
3. Verify login status
4. If not logged in, guide user through login
```

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
- **Segment Duration**: 8 seconds (Whisk video limit)
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

### Phase 2.5: Asset Definition (REQUIRED)

Create `{output_dir}/assets.json` to define reusable assets that maintain consistency across all scenes.

**assets.json schema:**
```json
{
  "characters": {
    "<id>": {
      "description": "Full physical description: hair, eyes, build, clothing, distinguishing features...",
      "identity_ref": "assets/characters/<id>.png"
    }
  },
  "backgrounds": {
    "<id>": {
      "description": "Environment description: setting, lighting, atmosphere...",
      "ref_image": "assets/backgrounds/<id>.png"
    }
  },
  "styles": {
    "<id>": {
      "description": "Visual style description: art style, color treatment, mood...",
      "ref_image": "assets/styles/<id>.png"
    }
  },
  "objects": {
    "<id>": {
      "description": "Recurring prop description: appearance, details...",
      "ref_image": "assets/objects/<id>.png"
    }
  }
}
```

**Asset Types:**

| Type | Purpose | Example |
|------|---------|---------|
| **Characters** | People/creatures - CRITICAL for identity consistency | "protagonist", "sidekick", "villain" |
| **Backgrounds** | Locations/environments | "city_street", "temple_courtyard", "spaceship_bridge" |
| **Styles** | Visual treatment references | "ghibli_pastoral", "noir_cinematic", "cyberpunk_neon" |
| **Objects** | Recurring props/items | "magic_sword", "protagonist_car", "robot_companion" |

**Character Asset Prompt Guidelines:**
- Include full physical description (hair color/style, eye color, build, facial features)
- Describe signature outfit and accessories
- Mention "character sheet, A-pose, full body, white background" for clean references
- Include multiple views if needed: "front view, side view, back view"

**CHECKPOINT:** Get user approval before proceeding.

---

## Character Consistency Rules (CRITICAL)

### The Character Drift Problem

Without proper character references, AI video models cause "identity drift" - clothing colors change, styles shift, characters become unrecognizable across scenes. The drift is **cumulative**: by Scene 4-5, characters may look completely different from Scene 1.

### When to Include Character References

**CRITICAL RULE:** Include character references for ANY scene where the character is visible, even partially.

| What's Visible | Include Character Reference? | Example |
|----------------|------------------------------|---------|
| Full body | **YES** | Wide shot of character walking |
| Upper body only | **YES** | Medium shot conversation |
| **Hands only** | **YES** | Close-up of hands holding object |
| **Clothing only (no face)** | **YES** | Back view of character running |
| Character's belongings | Optional | Close-up of character's bag |
| No character elements | NO | Landscape, building exterior |

**Common Mistake:** Close-up of hands without character reference → clothing color/style becomes inconsistent.

### Scene Type Classification

Every scene must be classified as one of:
- **`character`**: ANY part of a character is visible (even hands, clothing, or back view)
- **`landscape`**: No character elements visible at all

### Keyframe Type Selection (CRITICAL)

| Scene Type | Transition | Keyframe Type | Why |
|------------|------------|---------------|-----|
| `character` | ANY | **ALWAYS generated** | Must re-anchor character identity |
| `landscape` | cut/fade/dissolve | generated | New visual context |
| `landscape` | continuous | extracted OK | No identity to preserve |

**RULE:** NEVER use extracted keyframes for character scenes. Even for "continuous" transitions, character scenes MUST use generated keyframes with character references.

### Reference Chain Rules

| Asset Type | Chain Behavior |
|------------|----------------|
| **Character Identity** | ALWAYS use original asset from `assets/characters/` (never chain from keyframes) |
| **Background** | Can chain from previous scene's background for continuity |
| **Style** | ALWAYS apply with style asset reference |

**Key Rule:** Never chain keyframes as character references - always use original character assets.

---

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
    "characters": {
      "<id>": {
        "prompt": "Full physical description with character sheet styling...",
        "output": "assets/characters/<id>.png",
        "status": "pending"
      }
    },
    "backgrounds": {
      "<id>": {
        "prompt": "Environment description with atmosphere...",
        "output": "assets/backgrounds/<id>.png",
        "status": "pending"
      }
    },
    "styles": {
      "<id>": {
        "prompt": "Visual style reference description...",
        "output": "assets/styles/<id>.png",
        "status": "pending"
      }
    },
    "objects": {
      "<id>": {
        "prompt": "Recurring prop description...",
        "output": "assets/objects/<id>.png",
        "status": "pending"
      }
    }
  },
  "scenes": [
    {
      "id": "scene-01",
      "title": "Scene Title",
      "scene_type": "character",
      "duration_target": 20,
      "transition_to_next": "cut",
      "first_keyframe": {
        "type": "generated",
        "prompt": "Detailed visual description for scene start...",
        "characters": ["protagonist"],
        "background": "location_id",
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
      "title": "Landscape Scene",
      "scene_type": "landscape",
      "duration_target": 8,
      "transition_to_next": null,
      "first_keyframe": {
        "type": "generated",
        "prompt": "Environment establishing shot...",
        "background": "location_id",
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
- `config.segment_duration`: Whisk's max video length (8 seconds)
- `assets`: Defines reusable assets (characters, backgrounds, styles, objects) - mirrors assets.json
- `scenes[].scene_type`: **NEW** - `"character"` or `"landscape"` (determines keyframe rules)
- `scenes[].duration_target`: Desired scene length → determines segment count: `ceil(duration / 8)`
- `scenes[].transition_to_next`: Transition to apply before next scene (`cut`, `fade`, `dissolve`, `wipe`, or `null` for last scene)
- `scenes[].first_keyframe.type`: **NEW** - `"generated"` or `"extracted"` (see Character Consistency Rules)
- `scenes[].first_keyframe.characters`: **NEW** - Array of character asset IDs to reference (REQUIRED if scene_type is "character")
- `scenes[].first_keyframe.background`: **NEW** - Optional background asset ID
- `scenes[].segments[]`: Technical video chunks that chain seamlessly within the scene

**Keyframe Type Rules:**
| Scene Type | Keyframe Type | Character References |
|------------|---------------|----------------------|
| `character` | ALWAYS `"generated"` | REQUIRED - array of character IDs |
| `landscape` | `"generated"` or `"extracted"` | Not needed |

**CHECKPOINT:** Get user approval before proceeding.

### Phase 4: Asset Execution (MCP)

For each asset in pipeline.json:

1. **Navigate to Whisk** (if not already there)
2. **Generate image:**
   - Type: "Generate an image: <asset_prompt>"
   - Submit and wait for generation
3. **Download image:**
   - Click download button
   - Wait for download to complete
4. **Move to correct path:**
   ```powershell
   New-Item -ItemType Directory -Force -Path "<parent_dir>"
   Move-Item -Path ".playwright-mcp/<downloaded_file>" -Destination "<output_path>"
   ```
5. **Update pipeline.json:** Set status to "completed"
6. **Start new chat** for next generation (keeps context clean)

**CHECKPOINT:** Review assets with VLM, get user approval.

### Phase 5: Scene Keyframes Generation (MCP)

For each scene in pipeline.json:

1. **Generate scene's starting keyframe** using Whisk image generation
2. **Download and move** to `keyframes/scene-XX-start.png`
3. **Update pipeline.json** scene's `first_keyframe.status` to "completed"

**Note:** Each scene needs its own generated keyframe because scenes represent distinct visual contexts (different camera, location, perspective, etc.)

**CHECKPOINT:** Review all scene keyframes with VLM, get user approval.

### Phase 6: Segment Execution (MCP)

For each scene in pipeline.json:
  For each segment in scene.segments:

1. **Determine start frame:**
   - If first segment of scene → use scene's `first_keyframe`
   - Else → use extracted frame from previous segment

2. **Start new chat**

3. **Upload start frame:**
   - Click attach/upload button
   - Use `browser_file_upload` with appropriate frame path

4. **Type motion prompt:**
   - "Create a video from this image: <segment.motion_prompt>"

5. **Wait for video generation** (60-180 seconds)

6. **Download video**

7. **Move to correct path** (e.g., `scene-01/seg-A.mp4`)

8. **Extract last frame** (if not the last segment in this scene):
   ```powershell
   ffmpeg -sseof -1 -i "scene-01/seg-A.mp4" -frames:v 1 "scene-01/extracted/after-seg-A.png"
   ```

9. **Update pipeline.json** segment status to "completed"

**Execution Flow Example:**
```
Scene 1 (3 segments):
  seg-A: upload scene-01-start.png → generate → extract frame
  seg-B: upload after-seg-A.png → generate → extract frame
  seg-C: upload after-seg-B.png → generate → (no extraction, last segment)

Scene 2 (1 segment):
  seg-A: upload scene-02-start.png → generate → (no extraction, last segment)
```

**CHECKPOINT:** Get user approval on videos.

### Phase 7: Final Concatenation with Transitions

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

---

## Motion Prompt Structure

### I2V Motion Prompt Format

Use this structured format for video motion prompts:

```
[SUBJECT] [ACTION VERB] [BODY PART DETAILS], [ENVIRONMENTAL INTERACTION], camera [CAMERA MOVEMENT]
```

**Example:** "soldier sprints through trench, legs driving forward, rifle bouncing against chest, mud splashing from boots, camera tracking from behind at shoulder height"

### I2V Motion Rules

1. **Separate subject motion from camera motion** - describe both explicitly
2. **Describe physical body movements** - "legs pumping", "arms swinging", not just "running"
3. **Include environmental interaction** - "boots splashing through mud", "hair flowing in wind"
4. **Avoid POV/first-person** - I2V struggles with perspective-based motion
5. **Use motion verbs** - "sprinting" not "in motion"
6. **One action per segment** - don't overload with multiple complex actions in 8 seconds

### Positional Language for Multi-Character Scenes

When multiple characters appear, use explicit positioning to maintain spatial consistency:

| Position | Phrase |
|----------|--------|
| Left side | "On the left:" |
| Right side | "On the right:" |
| Center | "In the center:" |
| Foreground | "In the foreground:" |
| Background | "In the background:" |

**Example:**
"On the left: samurai in red armor raises katana. On the right: ninja in black crouches defensively. In the background: temple burning with orange flames. Camera slowly pushes in from wide shot."

### Motion Quality Vocabulary

| Type | Words |
|------|-------|
| **Speed** | glacially, gradually, steadily, quickly, explosively |
| **Smooth** | fluid, graceful, seamless, flowing |
| **Sharp** | precise, snappy, crisp, sudden |
| **Heavy** | weighted, powerful, forceful, impactful |
| **Light** | delicate, airy, subtle, ethereal |

---

## VLM Review Checklists

### For Character Assets
- [ ] Appearance matches description (hair, eyes, clothing, distinguishing features)
- [ ] Pose is neutral and usable as reference (A-pose or T-pose)
- [ ] Style matches production philosophy
- [ ] No artifacts, distortions, or extra limbs
- [ ] Background is clean (white/neutral)

### For Keyframes
- [ ] Characters match their asset references (identity preserved)
- [ ] Character positions match prompt descriptions
- [ ] Background/environment matches philosophy
- [ ] Lighting is consistent with style.json
- [ ] Composition allows for intended motion
- [ ] No text or watermarks in frame

### For Videos
- [ ] Motion matches prompt description
- [ ] Characters remain consistent throughout (no identity drift)
- [ ] No sudden jumps, flickers, or artifacts
- [ ] Camera movement is smooth
- [ ] Environmental interactions look natural

---

## Output Directory Structure

```
{output_dir}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration
├── scene-breakdown.md         # Scene planning document
├── assets.json                # Asset definitions (NEW)
├── pipeline.json              # Execution pipeline with all prompts
├── output.mp4                 # FINAL VIDEO (with transitions)
│
├── assets/
│   ├── characters/            # Character reference sheets
│   │   └── protagonist.png
│   ├── backgrounds/           # Environment references
│   │   └── location.png
│   ├── styles/                # Visual style references (NEW)
│   │   └── style_anchor.png
│   └── objects/               # Recurring props (NEW)
│       └── item.png
│
├── keyframes/
│   ├── scene-01-start.png     # Generated (scene 1 start)
│   └── scene-02-start.png     # Generated (scene 2 start)
│
├── scene-01/
│   ├── seg-A.mp4              # Segment videos
│   ├── seg-B.mp4
│   ├── seg-C.mp4
│   ├── scene.mp4              # Concatenated scene (intermediate)
│   └── extracted/             # Internal extracted frames
│       ├── after-seg-A.png
│       └── after-seg-B.png
│
├── scene-02/
│   ├── seg-A.mp4
│   └── scene.mp4
└── ...
```

**Key Points:**
- `assets.json` defines all reusable assets (characters, backgrounds, styles, objects)
- `assets/` folders mirror the asset types in assets.json
- `keyframes/` contains only **generated** keyframes (one per scene)
- `scene-XX/extracted/` contains **extracted** frames (internal, for segment chaining)
- `scene-XX/scene.mp4` is the intermediate concatenated scene (before transitions)

## TodoWrite Templates

At the START of the workflow, create the appropriate todo list based on selected approval mode:

### Manual Approval Mode

```
1. Ask user to select approval mode (Manual/Automatic)
2. MCP: Navigate to Whisk, check login
3. Create philosophy.md and style.json
4. Get user approval on production philosophy
5. Create scene-breakdown.md (with scenes and segments)
6. Get user approval on scene breakdown
7. Create assets.json (characters, backgrounds, styles, objects)
8. Get user approval on asset definitions
9. Create pipeline.json (v3.0 schema with scene_type, characters)
10. Get user approval on pipeline.json
11. MCP: Generate assets, VLM review, get user approval
12. MCP: Generate scene keyframes, VLM review, get user approval
13. MCP: Generate segment videos (nested loop: scenes → segments)
14. Get user approval on videos
15. Concatenate segments within each scene
16. Concatenate scenes with transitions into output.mp4
17. Provide final summary
```

### Automatic Approval Mode

```
1. Ask user to select approval mode (Manual/Automatic)
2. MCP: Navigate to Whisk, check login
3. Create philosophy.md and style.json
4. Create scene-breakdown.md (with scenes and segments)
5. Create assets.json (characters, backgrounds, styles, objects)
6. Create pipeline.json (v3.0 schema with scene_type, characters)
7. MCP: Generate assets, VLM review (auto-proceed if good)
8. MCP: Generate scene keyframes, VLM review (auto-proceed if good)
9. MCP: Generate segment videos (nested loop: scenes → segments)
10. Concatenate segments within each scene
11. Concatenate scenes with transitions into output.mp4
12. Present final output to user for review
```

**Key Differences:**
- Manual mode has explicit user approval checkpoints at each phase
- Automatic mode relies on VLM review and only shows final output to user
- Both modes use VLM to review generated assets and keyframes
- LLM should fix and regenerate if VLM detects issues in either mode

## File Download Handling

**CRITICAL:** Downloads go to `.playwright-mcp/` directory. Always:

1. After clicking download, check the download result in MCP output
2. Note the downloaded filename
3. Create target directory if needed
4. Move file to correct pipeline output path
5. Verify file exists at destination

```powershell
# Example
New-Item -ItemType Directory -Force -Path "output/project/assets/backgrounds"
Move-Item -Path ".playwright-mcp/whisk-generated-xyz.png" -Destination "output/project/assets/backgrounds/battlefield.png" -Force
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cookie consent page | Click "Ausblenden" (Hide) button |
| Not logged in | Guide user to log in to Google account manually |
| On landing page | Click "Tool aufrufen" to enter workspace |
| Generation stuck | Wait longer, check snapshot for progress |
| Download not working | Try right-clicking image or find download button |
| Element ref not found | Take new snapshot, refs change on page update |
| Rate limited | Wait 1-2 minutes between generations |
| Reference slot not clearing | Click X button on slot or start new project |
| Video not appearing | Check video gallery (videocam_auto button) |

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Segment Duration | 8 seconds per generation (Whisk video limit) |
| Image Resolution | Up to 1024x1024 |
| Video Resolution | Up to 1080p |
| Rate Limiting | ~2-3 generations per minute |
| GPU Required | None (cloud-based) |

**Key Terminology:**
- **Scene** = A narrative/cinematic unit (any duration). Represents a continuous shot or distinct visual context. Each scene requires a generated starting keyframe.
- **Segment** = A technical 8-second video chunk within a scene. Multiple segments chain together seamlessly via extracted frames to form longer scenes.
