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

# AI Video Producer (Whisk Edition) v4.0

Create professional AI-generated videos through a structured, iterative workflow using Google Whisk via MCP Playwright.

## Prerequisites & Setup

**Required:**
- Google account with access to Google Labs (labs.google)
- Internet connection

**MCP Playwright:** If not installed, run automatically:
```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

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
- **"Manual approval"** - User approves each phase before proceeding
- **"Automatic approval"** - LLM proceeds automatically, user only reviews final output

| Mode | User Interaction | Best For |
|------|------------------|----------|
| **Manual** | Checkpoint at each phase | First-time projects, precise control |
| **Automatic** | Only final review | Trusted workflow, quick generation |

**Store the selected mode** and apply it to all checkpoints throughout the workflow.

## Architecture

```
Claude reads pipeline.json (v4.0 with shot types, genre, continuity)
    |
Claude -> MCP Playwright -> Google Whisk (labs.google/fx/tools/whisk)
    |
Claude updates pipeline.json status
    |
Claude verifies shot type and continuity via VLM
    |
Claude moves downloads to correct output paths
    |
Claude concatenates videos to output.mp4
```

## Sub-Agent Architecture (Context Management)

This skill uses **sub-agents** for efficient memory management. Each generation task runs in a fresh context, preventing memory bloat and improving reliability.

### Why Sub-Agents?

| Problem | Solution |
|---------|----------|
| Context fills with irrelevant history | Each sub-agent starts fresh |
| Long workflows cause errors | Isolated tasks, isolated failures |
| Memory of asset A not needed for asset B | Stateless execution |
| Parallel generation impossible | Independent sub-agents can run in parallel |

### Agent Responsibilities

| Phase | Agent Type | Context Needed |
|-------|------------|----------------|
| **0-3** (Planning) | Main Agent | User intent, iteration, approval |
| **4** (Assets) | Sub-agents (parallel) | Just asset prompt + MCP instructions |
| **5+6** (Videos) | Sub-agents (per segment) | Just scene data + asset paths |
| **7** (Concat) | Main Agent | Just file paths |

### Sub-Agent Workflow

```
Main Agent (planning phases)
    │
    ├── pipeline.json complete
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  PHASE 4: PARALLEL ASSET GENERATION                 │
│                                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ Asset 1 │ │ Asset 2 │ │ Asset 3 │ │ Asset N │  │
│  │SubAgent │ │SubAgent │ │SubAgent │ │SubAgent │  │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘  │
│       │           │           │           │        │
│       ▼           ▼           ▼           ▼        │
│   [success]   [success]   [retry→ok]  [success]   │
└─────────────────────────────────────────────────────┘
    │
    ├── All assets complete
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  PHASE 5+6: VIDEO GENERATION (sequential per scene) │
│                                                     │
│  Scene 1: seg-A ──► seg-B ──► seg-C                │
│  Scene 2: seg-A ──► seg-B                          │
│  (seg-B depends on seg-A for frame extraction)     │
└─────────────────────────────────────────────────────┘
    │
    ▼
Main Agent (concatenation)
```

### Sub-Agent Instructions

Sub-agents receive complete, self-contained instructions:

- **Asset Generation**: See `references/subagents/asset-generation.md`
- **Video Generation**: See `references/subagents/video-generation.md`

### Spawning Sub-Agents

**For Asset Generation (Parallel):**
```
Spawn multiple sub-agents simultaneously, one per asset:

Sub-agent prompt template:
"Generate an asset using Google Whisk.

 ASSET INFO:
 - Type: {asset_type}
 - Prompt: {prompt}
 - Output Path: {output_path}

 INSTRUCTIONS: [content from references/subagents/asset-generation.md]

 AUTO-RETRY: Up to 2 retries on failure.
 Return: status, output_path"
```

**For Video Generation (Sequential per scene):**
```
Spawn one sub-agent per segment, wait for completion before next:

Sub-agent prompt template:
"Generate keyframe and video using Google Whisk.

 SEGMENT INFO:
 - Scene: {scene_id}, Segment: {segment_id}
 - Keyframe Prompt: {keyframe_prompt}
 - Motion Prompt: {motion_prompt}
 - Character Assets: {character_paths}
 - Background Asset: {background_path}
 - Keyframe Output: {keyframe_output_path}
 - Video Output: {video_output_path}
 - Previous Video: {previous_video_path} (for seg-B+)

 INSTRUCTIONS: [content from references/subagents/video-generation.md]

 VLM REVIEW: Required for keyframe selection.
 AUTO-RETRY: Up to 2 retries on failure.
 Return: status, keyframe_path, video_path"
```

### Error Handling

- **Auto-retry**: Sub-agents retry up to 2 times on failure
- **Failure reporting**: Sub-agent returns clear error message
- **Main agent action**: Update pipeline.json, log error, continue or stop based on approval mode

## Whisk Reference Slots

| Whisk Slot | German Label | Our Asset Type | Purpose |
|------------|--------------|----------------|---------|
| **Subject** | Motiv | Characters | Person/creature reference for identity |
| **Scene** | Szene | Backgrounds | Location/environment reference |
| **Style** | Stil | Styles | Visual treatment reference |

## MCP Playwright Operations

### Login Check & Flow

```
1. Navigate: mcp__playwright__browser_navigate(url="https://labs.google/fx/tools/whisk")
2. Snapshot: mcp__playwright__browser_snapshot()
3. If cookie consent ("Auf labs.google/fx werden..."): Click "Ausblenden"
4. If on landing page: Click "Tool aufrufen" to enter workspace
5. If not logged in: Inform user to log in manually
```

### Asset Image Generation

```
1. Expand reference panel: Click "Bilder hinzufügen"
2. Upload references to appropriate slots (Subject/Scene/Style) if needed
3. Type prompt: mcp__playwright__browser_type(element="Prompt input", ref="<ref>", text="<prompt>")
4. Generate: mcp__playwright__browser_click(element="Prompt senden", ref="<ref>")
5. Wait: mcp__playwright__browser_wait_for(time=15)
6. Whisk generates 2 images - review both
7. Download chosen image and move to pipeline output path
8. Update pipeline.json status
```

### Combined Keyframe + Video Generation (RECOMMENDED)

**This is the efficient workflow for scene generation with asset references for consistency.**

**TESTED WORKFLOW - Follow these exact MCP operations:**

```
STEP 1: START FRESH SESSION
===========================
Navigate to Whisk and start a new chat for each scene:
1. mcp__playwright__browser_navigate(url="https://labs.google/fx/tools/whisk")
2. mcp__playwright__browser_snapshot() - verify page loaded
3. If needed, click "Neuer Chat" to clear previous context

STEP 2: UPLOAD ASSET REFERENCES (Critical for consistency!)
===========================================================
Check pipeline.json for scene's required assets and upload each:

For CHARACTER (Subject/Motiv slot):
a. Take snapshot to find the Subject slot with heading "Motiv"
b. Click on the slot area (look for image placeholder under "Motiv")
c. Click "Bild" or image upload option when it appears
d. Use browser_file_upload with absolute path to character asset
   Example: mcp__playwright__browser_file_upload(paths=["D:/Project/.../assets/characters/zelda.jpg"])

For BACKGROUND (Scene/Szene slot):
a. Click on the Scene slot area under heading "Szene"
b. Click "Bild" or image upload option
c. Use browser_file_upload with absolute path to background asset
   Example: mcp__playwright__browser_file_upload(paths=["D:/Project/.../assets/backgrounds/spring_of_power.jpg"])

For STYLE (Style/Stil slot) - Optional:
a. Click on the Style slot area under heading "Stil"
b. Upload style reference if specified in pipeline

STEP 3: GENERATE KEYFRAMES
==========================
1. Take snapshot to find the prompt textbox
2. Type KEYFRAME prompt: mcp__playwright__browser_type(
     element="Prompt textbox",
     ref="<textbox_ref>",
     text="<first_keyframe.prompt from pipeline.json>"
   )
3. Click "Prompt senden" button to generate
4. Wait for generation: mcp__playwright__browser_wait_for(time=20)
5. Whisk generates 2 keyframe options

STEP 4: VLM REVIEW & SELECTION
==============================
1. Take screenshot: mcp__playwright__browser_take_screenshot()
2. Use VLM to assess BOTH keyframes:
   - Character consistency with uploaded references
   - Background consistency with scene reference
   - Composition and shot type match
   - Overall quality and style consistency
3. Decide which keyframe (left or right) is better
4. Note: Left keyframe typically has lower ref numbers

STEP 5: ANIMATE TO VIDEO
========================
1. Take snapshot to find "Animieren" button on CHOSEN keyframe
2. Click "Animieren" (Animate) button on the better keyframe
3. Animation view opens with a new textbox asking "Was für eine Animation möchten Sie sehen?"
4. Take snapshot to find the animation textbox
5. Type MOTION prompt: mcp__playwright__browser_type(
     element="Animation prompt textbox",
     ref="<textbox_ref>",
     text="<segments[0].motion_prompt from pipeline.json>"
   )
6. Click "Prompt senden" to start video generation
7. Wait for video: mcp__playwright__browser_wait_for(time=120)
   NOTE: Video generation takes 2-3 minutes! Progress shows as percentage.
8. Take snapshot to verify video is complete (shows play controls, duration "0:08")

STEP 6: DOWNLOAD VIDEO
======================
1. Take snapshot to find "DOWNLOAD download" button on the video
2. Click the DOWNLOAD button - a menu appears with options
3. Click "Herunterladen" (Download) option for MP4 format
4. Check MCP output for downloaded filename:
   "Downloaded file Whisk_xxx.mp4 to .playwright-mcp/Whisk-xxx.mp4"

STEP 7: DOWNLOAD KEYFRAME
=========================
1. Click "close" button to exit animation view and return to main storyboard
2. Take snapshot - both generated keyframes are visible with download buttons
3. Click "download" button on the CHOSEN keyframe (the one you animated)
4. Check MCP output for downloaded filename:
   "Downloaded file Whisk_xxx.jpeg to .playwright-mcp/Whisk-xxx.jpeg"

STEP 8: MOVE FILES TO OUTPUT PATHS
==================================
Move downloads from .playwright-mcp/ to correct locations:
```powershell
# Move video
Move-Item ".playwright-mcp/Whisk-xxx.mp4" "output/project/scene-03/seg-A.mp4" -Force

# Move keyframe
Move-Item ".playwright-mcp/Whisk-xxx.jpeg" "output/project/keyframes/scene-03-start.jpg" -Force
```

STEP 9: UPDATE STATUS & CONTINUE
================================
1. Update pipeline.json status for keyframe and segment to "completed"
2. For next segment (seg-B+), extract last frame as reference:
   ffmpeg -sseof -1 -i "scene-XX/seg-A.mp4" -frames:v 1 "scene-XX/extracted/after-seg-A.png"
3. Start new Whisk chat for next scene/segment
```

**Key insight:** Asset references in Whisk slots ensure character and environment consistency across all generated content. Always upload character AND background references before generating!

### Key MCP Tools

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_snapshot` | Get page accessibility tree |
| `browser_click` | Click element by ref |
| `browser_type` | Type text into input |
| `browser_file_upload` | Upload files |
| `browser_wait_for` | Wait for text/time |

---

## Workflow Phases

### Phase 0: Setup Check

```
1. Navigate to https://labs.google/fx/tools/whisk
2. Handle cookie consent if needed
3. Verify login status
4. If not logged in, guide user through login
```

### Phase 1: Production Philosophy (REQUIRED)

**Before starting this phase, read:**
- `references/genre-presets.md` - Genre preset options and configurations
- `references/templates/philosophy.md` - Templates for philosophy.md and style.json

**Create these files:**
- `{output_dir}/philosophy.md` - Production philosophy document
- `{output_dir}/style.json` - Style configuration with genre preset

**CHECKPOINT:** Get user approval before proceeding.

### Phase 2: Scene Breakdown (REQUIRED)

**Before starting this phase, read:**
- `references/shot-types.md` - Shot type definitions and Whisk modifiers
- `references/shot-progressions.md` - Shot progression patterns
- `references/camera-movements.md` - Camera movement options
- `references/continuity-rules.md` - Continuity guidelines
- `references/templates/scene-breakdown.md` - Template for scene-breakdown.md

**Create:** `{output_dir}/scene-breakdown.md`

**Segment Calculation:** `segments_needed = ceil(scene_duration / 8)`

| Scene Duration | Segments Needed |
|----------------|-----------------|
| 1-8 seconds | 1 |
| 9-16 seconds | 2 |
| 17-24 seconds | 3 |
| 25-32 seconds | 4 |

**CHECKPOINT:** Get user approval before proceeding.

### Phase 2.5: Asset Definition (REQUIRED)

**Before starting this phase, read:**
- `references/asset-prompts.md` - Professional asset prompt writing guide

**Create:** `{output_dir}/assets.json`

Define reusable assets using professional reference formats:

| Asset Type | Format | Key Requirements |
|------------|--------|------------------|
| **Characters** | Character Model Sheet (turnaround) | Multiple views (front, 3/4, side, back), T-pose/A-pose, neutral expression, white background |
| **Backgrounds** | Environment Concept Art | No characters visible, establishes location/mood, composition space for subjects |
| **Styles** | Style Reference Image | No characters, demonstrates color palette/lighting/texture, captures visual treatment |
| **Objects** | Prop Reference Sheet | Multiple views, detail callouts, scale reference with human silhouette |

**CHECKPOINT:** Get user approval before proceeding.

### Phase 3: Pipeline Generation (REQUIRED)

**Before starting this phase, read:**
- `references/pipeline-schema.md` - v4.0 schema definition and examples

**Create:** `{output_dir}/pipeline.json`

The v4.0 pipeline schema includes:
- `genre_preset` - One of: action, horror, comedy, drama, anime, documentary
- `config.continuity_mode` - "strict" or "relaxed"
- `scenes[].shot_progression` - Pattern for shot type sequencing
- `scenes[].continuity` - Screen direction, axis of action, spatial notes
- `first_keyframe.shot_type` - Professional shot type
- `segments[].shot_type` - Shot type per segment
- `segments[].camera_movement` - Camera movement type

**CHECKPOINT:** Get user approval before proceeding.

### Phase 4: Asset Execution (Sub-Agents - Parallel)

**Uses sub-agents for memory efficiency. See `references/subagents/asset-generation.md`**

**Spawn sub-agents in PARALLEL for all assets:**

1. **Extract all pending assets** from pipeline.json (characters, backgrounds, styles, objects)

2. **For each asset, spawn a sub-agent** with this prompt:
   ```
   Generate an asset using Google Whisk.

   ASSET INFO:
   - Type: {asset_type}
   - Prompt: "{prompt}"
   - Output Path: {project_base_path}/{output_path}

   [Include full content from references/subagents/asset-generation.md]

   AUTO-RETRY: Up to 2 retries on failure.
   Return: status (success/failure), final output path
   ```

3. **Wait for all sub-agents** to complete

4. **For each result:**
   - On success: Update pipeline.json status to "completed"
   - On failure: Log error, mark as "failed" in pipeline.json

5. **Verify all assets exist** at their output paths

**CHECKPOINT:** Review assets visually, get user approval before proceeding.

### Phase 5+6: Combined Keyframe & Video Generation (Sub-Agents - Sequential)

**Uses sub-agents for memory efficiency. See `references/subagents/video-generation.md`**

**Spawn sub-agents SEQUENTIALLY per segment (seg-B depends on seg-A for frame extraction):**

For each scene in pipeline.json:
  For each segment in scene.segments with status "pending":

1. **Extract segment info from pipeline.json:**
   - scene_id, segment_id
   - first_keyframe.prompt (for seg-A) or continuation prompt
   - segment.motion_prompt
   - character asset paths (resolve from assets section)
   - background asset path (resolve from assets section)
   - keyframe_output_path, video_output_path
   - previous_video_path (for seg-B+)

2. **Spawn sub-agent** with this prompt:
   ```
   Generate keyframe and video using Google Whisk.

   SEGMENT INFO:
   - Scene: {scene_id}, Segment: {segment_id}
   - Keyframe Prompt: "{keyframe_prompt}"
   - Motion Prompt: "{motion_prompt}"
   - Character Assets: {character_paths}
   - Background Asset: {background_path}
   - Keyframe Output: {keyframe_output_path}
   - Video Output: {video_output_path}
   - Previous Video: {previous_video_path} (for frame extraction, seg-B+ only)

   [Include full content from references/subagents/video-generation.md]

   VLM REVIEW: Required - select better keyframe before animating.
   AUTO-RETRY: Up to 2 retries on failure.
   Return: status, keyframe_path, video_path
   ```

3. **Wait for sub-agent** to complete

4. **On result:**
   - Success: Update pipeline.json status to "completed"
   - Failure: Log error, optionally retry or mark as "failed"

5. **Continue to next segment** (seg-B needs seg-A's video for frame extraction)

**Segment Dependencies:**
```
Scene 1: seg-A ──► seg-B ──► seg-C (sequential - frame extraction dependency)
Scene 2: seg-A ──► seg-B           (can start after Scene 1 seg-A if needed)
```

**CHECKPOINT:** After all segments complete, review videos, get user approval.

### Phase 7: Final Concatenation

1. Concatenate segments within each scene:
   ```bash
   ffmpeg -i "seg-A.mp4" -i "seg-B.mp4" -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0" "scene.mp4"
   ```

2. Concatenate scenes with transitions:
   ```bash
   ffmpeg -i "scene-01/scene.mp4" -i "scene-02/scene.mp4" -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0" "output.mp4"
   ```

3. Final output: `{output_dir}/output.mp4`

**DONE:** Present final video to user.

---

## File Download Handling

**CRITICAL:** Downloads go to `.playwright-mcp/` directory. Always:

1. After clicking download, check the download result in MCP output
2. Note the downloaded filename
3. Create target directory if needed
4. Move file to correct pipeline output path
5. Verify file exists at destination

```powershell
New-Item -ItemType Directory -Force -Path "output/project/assets/backgrounds"
Move-Item -Path ".playwright-mcp/whisk-generated-xyz.png" -Destination "output/project/assets/backgrounds/battlefield.png" -Force
```

## Output Directory Structure

```
{output_dir}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration + genre preset
├── scene-breakdown.md         # Scene plan with shot types + continuity
├── assets.json                # Asset definitions
├── pipeline.json              # v4.0 execution pipeline
├── output.mp4                 # FINAL VIDEO
├── assets/
│   ├── characters/
│   ├── backgrounds/
│   ├── styles/
│   └── objects/
├── keyframes/
│   └── scene-XX-start.png
└── scene-XX/
    ├── seg-X.mp4
    ├── scene.mp4
    └── extracted/
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cookie consent page | Click "Ausblenden" (Hide) button |
| Not logged in | Guide user to log in manually |
| On landing page | Click "Tool aufrufen" to enter workspace |
| Generation stuck | Wait longer, check snapshot for progress |
| Element ref not found | Take new snapshot, refs change on page update |
| Shot type mismatch | Add stronger shot type modifiers to prompt |
| Screen direction flip | Check continuity notes, use neutral shots to reset |
| Video generation slow | Wait 2-3 minutes, progress shows as percentage |
| Element outside viewport | Click close button or navigate back, take new snapshot |
| Click intercepted by overlay | Use browser_run_code with force:true or wait for overlay to close |
| Download menu appears | Click "Herunterladen" for MP4, "GIF" for animated gif |
| Keyframe not visible after animation | Close animation view first, then download from main view |
| Character inconsistent | Upload character reference to Subject (Motiv) slot BEFORE generating |
| Background wrong | Upload background reference to Scene (Szene) slot BEFORE generating |
| Previous context affecting generation | Start new Whisk chat for each scene |

For detailed troubleshooting, read: `references/troubleshooting.md`

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Segment Duration | 8 seconds per generation (Whisk limit) |
| Image Resolution | Up to 1024x1024 |
| Video Resolution | Up to 1080p |
| GPU Required | None (cloud-based) |
| Shot Types | 8 professional types |
| Genre Presets | 6 (Action, Horror, Comedy, Drama, Anime, Documentary) |
| Camera Movements | 11 types |

## Reference Files

All reference documentation is in the `references/` directory:

| File | Purpose |
|------|---------|
| `shot-types.md` | Shot type definitions and Whisk modifiers |
| `shot-progressions.md` | Shot progression patterns |
| `camera-movements.md` | Camera movement options |
| `genre-presets.md` | Genre preset configurations |
| `continuity-rules.md` | Continuity guidelines |
| `vlm-checklists.md` | Review checklists |
| `pipeline-schema.md` | v4.0 schema definition |
| `templates/philosophy.md` | Philosophy and style templates |
| `templates/scene-breakdown.md` | Scene breakdown template |
| `prompt-engineering.md` | Prompt writing guidance |
| `troubleshooting.md` | Detailed troubleshooting |

See `references/README.md` for the full index.
