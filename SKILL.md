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
- MCP Playwright server installed: `claude mcp add playwright -- npx @playwright/mcp@latest`
- Google account with Gemini access
- Internet connection

**No Python scripts required!** Claude directly controls the browser via MCP.

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

## Pipeline Modes

### Video-First Mode (Recommended)
Generate only the first keyframe, then generate videos sequentially.
Each video's last frame becomes the next scene's start keyframe.

```
KF-A (generated) -> Scene 1 -> KF-B (extracted) -> Scene 2 -> KF-C (extracted)
```

**Pros:** Perfect visual continuity between scenes
**Cons:** Less control over specific end poses

### Keyframe-First Mode
Generate all keyframes first, then generate videos between keyframe pairs.

```
KF-A ---------> Scene 1 <--------- KF-B
KF-B ---------> Scene 2 <--------- KF-C
```

**Pros:** Precise control over start and end frames
**Cons:** Potential inconsistency between independently generated keyframes

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
- **Video Type**: [promotional/narrative/educational/etc.]

---

## Scenes

### Scene 1: [Title]
**Duration**: [X seconds]
**Purpose**: [What this scene communicates]

**Visual Description**:
[Detailed description of what appears]

**Motion Description**:
[Specific actions and movements]

**Camera**: [static/tracking/pan/zoom]

**Transition to Next**: [cut/fade/continuous]

---

### Scene 2: [Title]
...
```

**Scene Count Guidelines:**
| Total Length | Scenes |
|--------------|--------|
| 1-8 seconds | 1 |
| 9-15 seconds | 2 |
| 16-24 seconds | 3 |
| 25-32 seconds | 4 |
| 32+ seconds | 5+ |

**CHECKPOINT:** Get user approval before proceeding.

### Phase 3: Pipeline Generation (REQUIRED)

Create `{output_dir}/pipeline.json`:

**Video-First Schema:**
```json
{
  "version": "2.0",
  "project_name": "project-name",
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
  "first_keyframe": {
    "id": "KF-A",
    "type": "character|landscape",
    "prompt": "Detailed visual description...",
    "output": "keyframes/KF-A.png",
    "status": "pending"
  },
  "scenes": [
    {
      "id": "scene-01",
      "motion_prompt": "Motion description...",
      "start_keyframe": "KF-A",
      "output_video": "scene-01/video.mp4",
      "output_keyframe": "keyframes/KF-B.png",
      "status": "pending"
    }
  ]
}
```

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

### Phase 5: First Keyframe (MCP)

1. **Generate first keyframe image** using same MCP flow
2. **Download and move** to keyframes/KF-A.png
3. **Update pipeline.json** status

**CHECKPOINT:** Review keyframe with VLM, get user approval.

### Phase 6: Scene Execution (MCP)

For each scene in pipeline.json:

1. **Start new chat**
2. **Upload start keyframe:**
   - Click attach/upload button
   - Use `browser_file_upload` with keyframe path
3. **Type motion prompt:**
   - "Create a video from this image: <motion_prompt>"
4. **Wait for video generation** (can take 1-3 minutes)
5. **Download video**
6. **Move to correct path** (e.g., scene-01/video.mp4)
7. **Extract last frame** for next scene's keyframe:
   ```powershell
   ffmpeg -sseof -1 -i "scene-01/video.mp4" -frames:v 1 "keyframes/KF-B.png"
   ```
8. **Update pipeline.json** status

**CHECKPOINT:** Get user approval on videos.

### Phase 7: Final Concatenation

Concatenate all scene videos into a single output file:

1. **Create file list** for ffmpeg:
   ```powershell
   # Create concat list
   @"
   file 'scene-01/video.mp4'
   file 'scene-02/video.mp4'
   file 'scene-03/video.mp4'
   "@ | Out-File -FilePath "concat-list.txt" -Encoding ASCII
   ```

2. **Concatenate videos** (ffmpeg or Python fallback):
   ```powershell
   # Option A: ffmpeg (if available)
   ffmpeg -f concat -safe 0 -i "concat-list.txt" -c copy "output.mp4"
   ```
   ```python
   # Option B: Python/OpenCV fallback
   import cv2, os
   base, scenes = '.', ['scene-01/video.mp4', 'scene-02/video.mp4', 'scene-03/video.mp4']
   cap = cv2.VideoCapture(scenes[0])
   fps, w, h = cap.get(cv2.CAP_PROP_FPS), int(cap.get(3)), int(cap.get(4))
   cap.release()
   out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
   for s in scenes:
       cap = cv2.VideoCapture(s)
       while True:
           ret, f = cap.read()
           if not ret: break
           out.write(f)
       cap.release()
   out.release()
   ```

3. **Clean up** concat-list.txt (optional)

4. **Update pipeline.json** to mark project complete

**Final output:** `{output_dir}/output.mp4`

## Output Directory Structure

```
{output_dir}/
├── philosophy.md
├── style.json
├── scene-breakdown.md
├── pipeline.json
├── output.mp4              <- FINAL CONCATENATED VIDEO
├── assets/
│   ├── characters/
│   └── backgrounds/
├── keyframes/
│   ├── KF-A.png
│   ├── KF-B.png (extracted from scene-01)
│   └── KF-C.png (extracted from scene-02)
├── scene-01/
│   └── video.mp4
├── scene-02/
│   └── video.mp4
└── ...
```

## TodoWrite Template

### Video-First Mode
```
1. Ask user: Video-First or Keyframe-First?
2. MCP: Navigate to Gemini, check login
3. Create philosophy.md
4. Create style.json
5. Get user approval on philosophy
6. Create scene-breakdown.md
7. Get user approval on scene breakdown
8. Create pipeline.json
9. Get user approval on pipeline
10. MCP: Generate assets, download, move to correct paths
11. Review assets with VLM, get user approval
12. MCP: Generate first keyframe
13. Review first keyframe with VLM, get user approval
14. MCP: Generate scene videos sequentially
15. Get user approval on videos
16. Concatenate all videos into output.mp4
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
| Video Duration | 5-8 seconds per generation |
| Image Resolution | Up to 1024x1024 |
| Video Resolution | Up to 1080p |
| Rate Limiting | ~2-3 generations per minute |
| GPU Required | None (cloud-based) |
