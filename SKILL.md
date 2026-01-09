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

### Image Generation

```
1. Expand reference panel: Click "Bilder hinzufügen"
2. Upload references to appropriate slots (Subject/Scene/Style)
3. Type prompt: mcp__playwright__browser_type(element="Prompt input", ref="<ref>", text="<prompt>")
4. Generate: mcp__playwright__browser_click(element="Prompt senden", ref="<ref>")
5. Wait: mcp__playwright__browser_wait_for(time=30)
6. Download image and move to pipeline output path
7. Update pipeline.json status
```

### Video Generation

```
1. Navigate to video mode: Click "videocam_auto" button
2. Select image to animate
3. Click animate/generate button
4. Wait: mcp__playwright__browser_wait_for(time=60)
5. Download video and move to pipeline output path
6. Extract last frame: ffmpeg -sseof -1 -i "seg-A.mp4" -frames:v 1 "extracted/after-seg-A.png"
7. Update pipeline.json status
```

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

### Phase 4: Asset Execution (MCP)

**Before reviewing, read:** `references/vlm-checklists.md`

For each asset in pipeline.json:
1. Navigate to Whisk (if not already there)
2. Generate image using asset prompt
3. Download and move to correct path
4. Update pipeline.json status to "completed"
5. Start new chat for next generation

**CHECKPOINT:** Review assets with VLM, get user approval.

### Phase 5: Scene Keyframes Generation (MCP)

**Before reviewing, read:** `references/vlm-checklists.md`

For each scene in pipeline.json:
1. Generate scene's starting keyframe using Whisk
2. Upload character references to Subject slot (if character scene)
3. Upload background reference to Scene slot (if applicable)
4. Download and move to `keyframes/scene-XX-start.png`
5. Update pipeline.json status

**Verify shot type:** Ensure keyframe matches specified shot type.

**CHECKPOINT:** Review keyframes with VLM, get user approval.

### Phase 6: Scene Videos Generation (MCP)

**Before reviewing, read:** `references/vlm-checklists.md`

For each scene:
  For each segment:
    1. Use starting keyframe (segment A) or extracted frame (segments B+)
    2. Generate video with motion prompt
    3. Download and move to `scene-XX/seg-X.mp4`
    4. Extract last frame: `ffmpeg -sseof -1 -i "seg-X.mp4" -frames:v 1 "extracted/after-seg-X.png"`
    5. Update pipeline.json status

**Verify continuity:** Check screen direction and spatial consistency.

**CHECKPOINT:** Review videos with VLM, get user approval.

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
