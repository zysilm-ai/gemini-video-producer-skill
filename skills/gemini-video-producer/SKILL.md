---
name: flow-video-producer
description: Produces AI videos using Google Flow via MCP Playwright. Creates promotional, narrative, educational, or social media videos of any length by chaining 8-second segments with Extend mode for seamless continuity. Use when users want to create videos, need video storyboarding, or want AI-generated video content.
---

# Flow Video Producer

Create AI videos of any length using Google Flow. Videos are broken into scenes and 8-second segments, chained seamlessly using Flow's Extend feature.

## Architecture

```
MAIN AGENT (this skill)
    │
    ├── reference-generator  → Subject/character/background images
    ├── keyframe-generator   → Scene starting compositions
    └── segment-generator    → Video segments (initial + extend)
```

Sub-agents are spawned via Task tool. Each has fresh context and returns status JSON.

## Core Concept: Extend Mode

**Problem:** Each video generation is stateless - no memory of camera trajectory or subject identity.

**Solution:** Use Flow's **Extend** feature instead of frame extraction:
- Analyzes last ~1 second of previous video (not just last frame)
- Preserves motion vectors, camera direction, subject identity
- Each extension adds 8 seconds, chainable for unlimited length

| Mode | When | Input |
|------|------|-------|
| `initial` | First segment of scene | Keyframe image |
| `extend` | All continuation segments | Previous video |

## Workflow

### Phase 0: Setup
Navigate to `https://labs.google/fx/flow`, verify login.

### Phase 1: Philosophy
Create `philosophy.md` and `style.json`. See [reference/templates.md](reference/templates.md).

**Get user approval.**

### Phase 2: Scene Breakdown
Create `scene-breakdown.md` with scenes and segments. See [reference/templates.md](reference/templates.md).

**Get user approval.**

### Phase 3: Pipeline
Create `pipeline.json`. See [reference/pipeline-schema.md](reference/pipeline-schema.md).

**Get user approval.**

### Phase 4: References
Spawn `reference-generator` for each reference (parallel):

```
Task(
  subagent_type="reference-generator",
  prompt='Generate reference. Task: {"type": "reference", "reference_id": "...", ...}',
  description="Generate [name] reference"
)
```

Types: `reference` (isolated subject), `character`, `object`, `background`

**Get user approval.**

### Phase 5: Keyframes
Spawn `keyframe-generator` for each scene (parallel):

```
Task(
  subagent_type="keyframe-generator",
  prompt='Generate keyframe. Task: {"scene_id": "scene-01", "prompt": "...", ...}',
  description="Generate scene-01 keyframe"
)
```

**Get user approval.**

### Phase 6: Segments
Spawn `segment-generator` sequentially within each scene:

```
# First segment: initial mode
Task(
  subagent_type="segment-generator",
  prompt='Generate segment. Task: {"segment_id": "seg-01-A", "mode": "initial", ...}',
  description="Generate seg-01-A (initial)"
)

# Following segments: extend mode
Task(
  subagent_type="segment-generator",
  prompt='Generate segment. Task: {"segment_id": "seg-01-B", "mode": "extend", "previous_video_path": "...", ...}',
  description="Generate seg-01-B (extend)"
)
```

**Get user approval.**

### Phase 7: Concatenation
Use `scripts/merge_videos.py`:

```bash
# Merge segments into scene
python scripts/merge_videos.py -o scene-01/scene.mp4 scene-01/seg-A.mp4 scene-01/seg-B.mp4

# Merge scenes into final
python scripts/merge_videos.py -o output.mp4 scene-01/scene.mp4 scene-02/scene.mp4
```

## Rules

1. **Always use TodoWrite** to track progress
2. **Never skip phases** - complete in order
3. **Always get user approval** before proceeding to next phase
4. **Never generate without pipeline.json** - plan first, execute second
5. **Use sub-agents for generation** - reference-generator, keyframe-generator, segment-generator
6. **Update pipeline.json** after each sub-agent returns

## Sub-Agents

### reference-generator
Generates images for visual consistency.
- **Types:** reference (isolated), character, object, background
- **Input:** type, reference_id, subject_name, prompt, output_path, style_context
- **Uses:** Flow "Bild erstellen" mode

### keyframe-generator
Generates scene starting compositions.
- **Input:** scene_id, prompt, output_path, style_context
- **Uses:** Flow "Bild erstellen" mode

### segment-generator
Generates 8-second video segments.
- **Modes:**
  - `initial` - from keyframe image (Video aus Frames)
  - `extend` - from previous video (Extend feature)
- **Input:** segment_id, mode, motion_prompt, output_video_path, [start_frame_path | previous_video_path]
- **Uses:** Flow Veo 3.1 Quality

## Flow Settings

When configuring Flow (via Settings button):
- **Model:** Veo 3.1 - Quality (NOT Fast)
- **Outputs:** 1 (NOT 2)
- **Aspect:** 16:9 Landscape

## Output Structure

```
output/{project}/
├── philosophy.md
├── style.json
├── scene-breakdown.md
├── pipeline.json
├── output.mp4              ← FINAL VIDEO
├── references/
├── keyframes/
├── scene-01/
│   ├── seg-A.mp4
│   ├── seg-B.mp4
│   └── scene.mp4
└── scene-02/
    └── ...
```

## References

- **Pipeline schema:** [reference/pipeline-schema.md](reference/pipeline-schema.md)
- **Veo prompts:** [reference/veo-prompts.md](reference/veo-prompts.md)
- **Templates:** [reference/templates.md](reference/templates.md)
