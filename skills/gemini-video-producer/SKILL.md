---
name: ai-video-producer
description: >
  AI video production workflow using Gemini via MCP Playwright browser automation.
  Creates any video type: promotional, educational, narrative, social media,
  animations, game trailers, music videos, product demos, and more. Use when
  users want to create videos with AI, need help with video storyboarding,
  keyframe generation, or video prompt writing. Follows a philosophy-first
  approach: establish visual style and production philosophy, then execute
  scene by scene with user feedback at each stage. Requires MCP Playwright
  server and a Google account with Gemini access.
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, TodoWrite, mcp__playwright__*
---

# AI Video Producer (MCP Edition)

Create professional AI-generated videos through a structured, iterative workflow using Gemini via MCP Playwright.

## Prerequisites & Setup

**Required:**
- Google account with Gemini access
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
7. **ALWAYS use MCP Playwright** for Gemini interaction - no Python scripts
8. **ALWAYS move downloads to correct locations** - files download to `.playwright-mcp/`, must be moved to pipeline output paths
9. **ALWAYS review generated outputs using VLM** - view images after each stage, assess quality

## Architecture

```
Claude reads pipeline.json
    |
Claude -> MCP Playwright -> Gemini Web Interface
    |
Claude updates pipeline.json status
    |
Claude moves downloads to correct output paths
```

**Benefits:**
- Self-healing: Claude adapts to UI changes by semantic understanding
- No brittle CSS selectors that break when Gemini updates
- Simpler codebase - no Python Playwright code to maintain
- Real-time adaptation to page state

## MCP Playwright Operations Reference

### Login Check & Flow

```
1. Navigate to Gemini:
   mcp__playwright__browser_navigate(url="https://gemini.google.com/app")

2. Take snapshot to check state:
   mcp__playwright__browser_snapshot()

3. If cookie consent appears:
   - Click "Accept all" button

4. Check if logged in:
   - Look for textbox "Prompt hier eingeben" or similar chat input
   - If present: logged in
   - If login form appears: inform user to log in manually

5. If not logged in:
   - Inform user: "Please log in to your Google account in the browser window"
   - Wait for login: mcp__playwright__browser_wait_for(text="Prompt", time=120)
```

### Image Generation

```
1. Ensure on Gemini chat page (navigate if needed)

2. Type prompt into chat:
   mcp__playwright__browser_type(
     element="Prompt input textbox",
     ref="<textbox_ref>",
     text="Generate an image: <prompt>",
     submit=true
   )

3. Wait for generation (15-60 seconds):
   mcp__playwright__browser_wait_for(time=30)
   mcp__playwright__browser_snapshot()  # Check if image appeared

4. Download the image:
   - Find download button in snapshot (usually "Download" or download icon)
   - mcp__playwright__browser_click(element="Download button", ref="<ref>")
   - Wait for download: mcp__playwright__browser_wait_for(textGone="downloading")

5. Move file to correct location:
   - Downloaded to: .playwright-mcp/<filename>.png
   - Move to: <pipeline_output_path>
   - Use PowerShell: Move-Item -Path "source" -Destination "dest"

6. Update pipeline.json status to "completed"
```

### Video Generation

```
1. Start new chat or continue existing:
   - Click "New chat" button if needed

2. For Image-to-Video (I2V):
   a. Upload start frame:
      - Click upload/attach button
      - mcp__playwright__browser_file_upload(paths=["<keyframe_path>"])

   b. Type video prompt:
      mcp__playwright__browser_type(
        element="Prompt input",
        ref="<ref>",
        text="Create a video: <motion_prompt>",
        submit=true
      )

3. For Text-to-Video (T2V):
   - Just type the prompt without uploading images

4. Wait for video generation (60-180 seconds):
   mcp__playwright__browser_wait_for(time=60)
   mcp__playwright__browser_snapshot()  # Check progress

5. Download the video:
   - Find video element and download button
   - Click download
   - Wait for completion

6. Move to correct output path

7. Extract last frame if needed for next scene:
   - Use ffmpeg or similar to extract last frame
   - Save as next keyframe
```

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
1. Navigate to https://gemini.google.com/app
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
- **Segment Duration**: 8 seconds (Gemini limit)
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
- `config.segment_duration`: Gemini's max video length (8 seconds)
- `scenes[].duration_target`: Desired scene length → determines segment count: `ceil(duration / 8)`
- `scenes[].transition_to_next`: Transition to apply before next scene (`cut`, `fade`, `dissolve`, `wipe`, or `null` for last scene)
- `scenes[].first_keyframe`: Generated image to establish scene's visual context
- `scenes[].segments[]`: Technical video chunks that chain seamlessly within the scene

**CHECKPOINT:** Get user approval before proceeding.

### Phase 4: Asset Execution (MCP)

For each asset in pipeline.json:

1. **Navigate to Gemini** (if not already there)
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

1. **Generate scene's starting keyframe** using Gemini image generation
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
1. MCP: Navigate to Gemini, check login
2. Create philosophy.md
3. Create style.json
4. Get user approval on philosophy
5. Create scene-breakdown.md (with scenes and segments)
6. Get user approval on scene breakdown
7. Create pipeline.json (v3.0 with nested segments)
8. Get user approval on pipeline
9. MCP: Generate assets, download, move to correct paths
10. Review assets with VLM, get user approval
11. MCP: Generate scene keyframes (one per scene)
12. Review keyframes with VLM, get user approval
13. MCP: Generate segment videos (nested loop: scenes → segments)
14. Get user approval on videos
15. Concatenate segments within each scene
16. Concatenate scenes with transitions into output.mp4
17. Provide final summary
```

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
Move-Item -Path ".playwright-mcp/Gemini-Generated-Image-xyz.png" -Destination "output/project/assets/backgrounds/battlefield.png" -Force
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cookie consent page | Click "Accept all" button |
| Not logged in | Guide user to log in manually |
| Generation stuck | Wait longer, check snapshot for progress |
| Download not working | Try clicking download button again |
| Element ref not found | Take new snapshot, refs change on page update |
| Rate limited | Wait 1-2 minutes between generations |

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Segment Duration | 8 seconds per generation (Gemini Veo limit) |
| Image Resolution | Up to 1024x1024 |
| Video Resolution | Up to 1080p |
| Rate Limiting | ~2-3 generations per minute |
| GPU Required | None (cloud-based) |

**Key Terminology:**
- **Scene** = A narrative/cinematic unit (any duration). Represents a continuous shot or distinct visual context. Each scene requires a generated starting keyframe.
- **Segment** = A technical 8-second video chunk within a scene. Multiple segments chain together seamlessly via extracted frames to form longer scenes.
