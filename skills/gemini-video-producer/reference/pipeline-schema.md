# Pipeline Schema Reference (v7.0)

## Overview

Version 7.0 introduces the unified keyframe-driven approach where **all segments** use "Video aus Frames" with start and end keyframe images.

**Key Changes from v4.0:**
- Removed `mode: initial | extend` field (replaced by `type`)
- Added `type: initial | extend` to indicate keyframe generation strategy
- Removed `link_phrase` field (no longer needed)
- Added explicit `start_keyframe` and `end_keyframe` per segment
- Added `start_keyframe_source` for extend-type segments

## Full Schema Example

```json
{
  "version": "7.0",
  "project_name": "project-name",
  "config": {
    "segment_duration": 8,
    "use_keyframe_mode": true,
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
      "prompt": "Isolated dark crimson warship with organic protrusions, clean dark background",
      "output": "references/enemy_vessel.png",
      "status": "pending"
    },
    "space_nebula": {
      "type": "background",
      "subject_name": "Space Nebula",
      "prompt": "Deep space vista with colorful nebula, scattered stars, cinematic wide composition",
      "output": "references/backgrounds/nebula.png",
      "status": "pending"
    }
  },
  "scenes": [
    {
      "id": "scene-01",
      "title": "Fleet Assembly",
      "duration_target": 16,
      "transition_to_next": "cut",
      "camera_style": "dolly forward",
      "narrative_state": {
        "start": "Human fleet assembled, preparing for battle",
        "end": "Fleet powered up, shields active, ready to engage"
      },
      "segments": [
        {
          "id": "seg-01-A",
          "type": "initial",
          "start_keyframe": {
            "prompt": "Wide shot of massive fleet in V-formation against colorful nebula backdrop. Silver-blue warships with glowing cyan engines, flagship prominent at center. Dramatic rim lighting, cinematic 16:9 composition.",
            "output": "scene-01/keyframes/seg-A-start.png",
            "status": "pending"
          },
          "end_keyframe": {
            "prompt": "Medium shot approaching flagship, warships passing by camera. Flagship fills lower third of frame, engines pulsing blue. Same nebula backdrop, dramatic lighting.",
            "output": "scene-01/keyframes/seg-A-end.png",
            "status": "pending"
          },
          "motion_prompt": "Slow dolly push forward through the fleet formation, silver-blue warships drifting majestically past camera, cyan engines pulsing with rhythmic light, approaching the flagship...",
          "anchor_moment": "camera settling with flagship centered in frame",
          "output_video": "scene-01/seg-A.mp4",
          "status": "pending"
        },
        {
          "id": "seg-01-B",
          "type": "extend",
          "start_keyframe_source": "seg-01-A.end_keyframe",
          "end_keyframe": {
            "prompt": "Close-up of flagship bow, shields fully activated with crackling blue energy. Weapon ports glowing, ready to fire. Dramatic backlighting from nebula.",
            "output": "scene-01/keyframes/seg-B-end.png",
            "status": "pending"
          },
          "motion_prompt": "Camera continues pushing forward, flagship growing larger in frame, shields flickering to life with crackling blue energy, weapon ports beginning to glow...",
          "anchor_moment": "flagship bow fills frame, shields fully active",
          "output_video": "scene-01/seg-B.mp4",
          "status": "pending"
        }
      ]
    }
  ]
}
```

## Schema Fields

### Root Level
| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version ("7.0") |
| `project_name` | string | Project identifier |
| `config` | object | Pipeline configuration |
| `metadata` | object | File references |
| `references` | object | Reference images for style consistency |
| `scenes` | array | Scene definitions |

### Config
| Field | Type | Description |
|-------|------|-------------|
| `segment_duration` | number | Target seconds per segment (Flow limit: 8) |
| `use_keyframe_mode` | boolean | Enable keyframe-driven Video aus Frames |
| `use_references` | boolean | Enable reference images for style consistency |

### References
| Field | Type | Description |
|-------|------|-------------|
| `type` | string | "reference" \| "character" \| "object" \| "background" |
| `subject_name` | string | Human-readable name |
| `prompt` | string | Generation prompt |
| `output` | string | Output file path |
| `status` | string | "pending" \| "completed" \| "error" |

### Scenes
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique scene identifier |
| `title` | string | Human-readable scene title |
| `duration_target` | number | Target duration in seconds |
| `transition_to_next` | string | "cut" \| "fade" \| null |
| `camera_style` | string | Primary camera movement |
| `narrative_state` | object | Start/end narrative context |
| `segments` | array | Video segments for this scene |

### Segments

#### Initial-Type Segment (First segment of scene)
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique segment identifier |
| `type` | string | "initial" - generates both keyframes |
| `start_keyframe` | object | Start keyframe definition |
| `end_keyframe` | object | End keyframe definition |
| `motion_prompt` | string | Camera/subject motion between keyframes |
| `anchor_moment` | string | Holdable ending description |
| `output_video` | string | Output video path |
| `status` | string | "pending" \| "completed" \| "error" |

#### Extend-Type Segment (Continuation segment)
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique segment identifier |
| `type` | string | "extend" - uses previous segment's end as start |
| `start_keyframe_source` | string | Reference to source (e.g., "seg-01-A.end_keyframe") |
| `end_keyframe` | object | End keyframe definition |
| `motion_prompt` | string | Camera/subject motion between keyframes |
| `anchor_moment` | string | Holdable ending description |
| `output_video` | string | Output video path |
| `status` | string | "pending" \| "completed" \| "error" |

### Keyframe Object
| Field | Type | Description |
|-------|------|-------------|
| `prompt` | string | Detailed visual description for image generation |
| `output` | string | Output file path |
| `status` | string | "pending" \| "completed" \| "error" |

## Segment Type Logic

| Type | Start Keyframe | End Keyframe | Use Case |
|------|----------------|--------------|----------|
| `initial` | Generate new | Generate new | First segment of any scene |
| `extend` | Use previous end | Generate new | All continuation segments |

**Keyframe Chain Example:**
```
Scene 1:
  seg-01-A (initial): [start-A] → [end-A]
  seg-01-B (extend):  [end-A]   → [end-B]    (end-A reused as start)
  seg-01-C (extend):  [end-B]   → [end-C]    (end-B reused as start)

Scene 2:
  seg-02-A (initial): [start-D] → [end-D]    (new scene, new initial)
```

## Segment Calculation

```
segments_needed = ceil(scene_duration / 8)
```

| Scene Duration | Segments |
|----------------|----------|
| 1-8 seconds | 1 |
| 9-16 seconds | 2 |
| 17-24 seconds | 3 |
| 25-32 seconds | 4 |

## Keyframe Count Calculation

```
For each scene:
  initial_segment: 2 keyframes (start + end)
  extend_segments: 1 keyframe each (end only)

Total keyframes = 2 + (num_extend_segments)
                = 2 + (total_segments - 1)
                = total_segments + 1
```

| Scene Segments | Keyframes Needed |
|----------------|------------------|
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |
| 4 | 5 |

## Example: Resolving start_keyframe_source

When processing an extend-type segment:

```json
{
  "id": "seg-01-B",
  "type": "extend",
  "start_keyframe_source": "seg-01-A.end_keyframe"
}
```

The main agent should:
1. Parse the source reference: `seg-01-A.end_keyframe`
2. Look up `seg-01-A` in the segments array
3. Get its `end_keyframe.output` path
4. Use that path as `start_keyframe_path` when calling segment-generator

## Migration from v4.0

| v4.0 Field | v7.0 Equivalent |
|------------|-----------------|
| `mode: "initial"` | `type: "initial"` + `start_keyframe` + `end_keyframe` |
| `mode: "extend"` | `type: "extend"` + `start_keyframe_source` + `end_keyframe` |
| `link_phrase` | Removed (not needed with keyframe approach) |
| `first_keyframe` (scene level) | Moved to first segment's `start_keyframe` |
