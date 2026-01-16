# Pipeline Schema Reference (v4.0)

## Full Schema Example

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
        }
      ]
    }
  ]
}
```

## Schema Fields

### Config
| Field | Type | Description |
|-------|------|-------------|
| `segment_duration` | number | Target seconds per segment (Flow limit: 8) |
| `use_extend_mode` | boolean | Enable Extend-based segment chaining |
| `use_references` | boolean | Enable reference images for subject consistency |

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
| `duration_target` | number | Target duration in seconds |
| `transition_to_next` | string | "cut" \| "fade" \| null |
| `camera_style` | string | Primary camera movement |
| `narrative_state` | object | Start/end narrative context |
| `first_keyframe` | object | Scene starting keyframe |
| `segments` | array | Video segments for this scene |

### Segments
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique segment identifier |
| `mode` | string | "initial" (from keyframe) \| "extend" (from previous) |
| `link_phrase` | string | Continuation language (extend mode only) |
| `motion_prompt` | string | Video generation prompt |
| `anchor_moment` | string | Holdable ending for clean extension |
| `output_video` | string | Output video path |
| `status` | string | "pending" \| "completed" \| "error" |

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
