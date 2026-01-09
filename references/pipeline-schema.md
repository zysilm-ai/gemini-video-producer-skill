# Pipeline Schema v4.0

> **When to Read**: Phase 3 (Pipeline Generation) - when creating pipeline.json.

The v4.0 pipeline schema includes shot types, genre presets, and continuity rules for professional video production.

---

## Complete Schema

```json
{
  "version": "4.0",
  "project_name": "project-name",
  "genre_preset": "action|horror|comedy|drama|anime|documentary",
  "config": {
    "segment_duration": 8,
    "default_transition": "cut",
    "continuity_mode": "strict|relaxed"
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
        "prompt": "Full physical description...",
        "output": "assets/characters/<id>.png",
        "status": "pending"
      }
    },
    "backgrounds": {
      "<id>": {
        "prompt": "Environment description...",
        "output": "assets/backgrounds/<id>.png",
        "status": "pending"
      }
    },
    "styles": {
      "<id>": {
        "prompt": "Visual style reference...",
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
      "shot_progression": "establishing-to-intimate",
      "continuity": {
        "screen_direction": "left-to-right",
        "axis_of_action": "established",
        "spatial_notes": "Character enters from left"
      },
      "first_keyframe": {
        "type": "generated",
        "shot_type": "wide",
        "prompt": "Detailed visual description...",
        "composition_notes": "Rule of thirds, subject on left",
        "characters": ["protagonist"],
        "background": "location_id",
        "output": "keyframes/scene-01-start.png",
        "status": "pending"
      },
      "segments": [
        {
          "id": "seg-01-A",
          "shot_type": "wide",
          "camera_movement": "static",
          "motion_prompt": "Motion description...",
          "output_video": "scene-01/seg-A.mp4",
          "status": "pending"
        }
      ]
    }
  ]
}
```

---

## Field Reference

### Root Level

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Must be `"4.0"` |
| `project_name` | string | Project identifier (used in paths) |
| `genre_preset` | string | One of: `action`, `horror`, `comedy`, `drama`, `anime`, `documentary` |
| `config` | object | Configuration settings |
| `metadata` | object | File references |
| `assets` | object | Reusable asset definitions |
| `scenes` | array | Scene definitions |

### Config Object

| Field | Type | Description |
|-------|------|-------------|
| `segment_duration` | number | Whisk's max video length (always 8) |
| `default_transition` | string | Default transition: `cut`, `fade`, `dissolve`, `wipe` |
| `continuity_mode` | string | `"strict"` enforces rules, `"relaxed"` allows flexibility |

### Scene Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique scene identifier (e.g., `"scene-01"`) |
| `title` | string | Human-readable scene title |
| `scene_type` | string | `"character"` or `"landscape"` |
| `duration_target` | number | Desired scene length in seconds |
| `transition_to_next` | string/null | Transition type or `null` for last scene |
| `shot_progression` | string | Pattern: `establishing-to-intimate`, `action-sequence`, `dialogue-coverage`, `reveal` |
| `continuity` | object | Continuity tracking |
| `first_keyframe` | object | Scene starting keyframe |
| `segments` | array | Video segments (8s each) |

### Continuity Object

| Field | Type | Description |
|-------|------|-------------|
| `screen_direction` | string | `"left-to-right"`, `"right-to-left"`, `"neutral"` |
| `axis_of_action` | string | `"established"`, `"crossing-allowed"`, `"not-applicable"` |
| `spatial_notes` | string | Free-form notes on spatial setup |

### Keyframe Object

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `"generated"` (always for character scenes) |
| `shot_type` | string | Professional shot type |
| `prompt` | string | Visual description for generation |
| `composition_notes` | string | Framing guidance |
| `characters` | array | Character asset IDs (required if scene_type is "character") |
| `background` | string | Optional background asset ID |
| `output` | string | Output path |
| `status` | string | `"pending"` or `"completed"` |

### Segment Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique segment ID (e.g., `"seg-01-A"`) |
| `shot_type` | string | Professional shot type |
| `camera_movement` | string | Camera movement type |
| `motion_prompt` | string | Motion description for video |
| `output_video` | string | Output video path |
| `status` | string | `"pending"` or `"completed"` |

---

## Keyframe Type Rules

| Scene Type | Keyframe Type | Character References |
|------------|---------------|----------------------|
| `character` | ALWAYS `"generated"` | REQUIRED - array of character IDs |
| `landscape` | `"generated"` or `"extracted"` | Not needed |

---

## Valid Shot Types

```
wide, medium, close-up, extreme-close-up, pov, over-shoulder, two-shot, insert
```

See `references/shot-types.md` for definitions.

---

## Valid Camera Movements

```
static, push-in, pull-out, pan-left, pan-right, track-left, track-right,
crane-up, crane-down, handheld, steadicam
```

See `references/camera-movements.md` for definitions.

---

## Valid Shot Progressions

```
establishing-to-intimate, action-sequence, dialogue-coverage, reveal
```

See `references/shot-progressions.md` for patterns.

---

## Segment Calculation

```
segments_needed = ceil(scene_duration / 8)
```

| Scene Duration | Segments Needed |
|----------------|-----------------|
| 1-8 seconds | 1 |
| 9-16 seconds | 2 |
| 17-24 seconds | 3 |
| 25-32 seconds | 4 |

---

## Example: Character Scene

```json
{
  "id": "scene-01",
  "title": "The Encounter",
  "scene_type": "character",
  "duration_target": 16,
  "transition_to_next": "cut",
  "shot_progression": "establishing-to-intimate",
  "continuity": {
    "screen_direction": "left-to-right",
    "axis_of_action": "established",
    "spatial_notes": "Hero on right, villain on left"
  },
  "first_keyframe": {
    "type": "generated",
    "shot_type": "wide",
    "prompt": "Wide establishing shot of dark alley, hero standing on right side facing left toward shadowy figure, neon signs reflecting on wet pavement",
    "composition_notes": "Hero on right third, villain silhouette on left third",
    "characters": ["hero", "villain"],
    "background": "alley",
    "output": "keyframes/scene-01-start.png",
    "status": "pending"
  },
  "segments": [
    {
      "id": "seg-01-A",
      "shot_type": "wide",
      "camera_movement": "static",
      "motion_prompt": "Wide shot holds steady as hero and villain face each other, tension building, slight movement as they assess each other",
      "output_video": "scene-01/seg-A.mp4",
      "status": "pending"
    },
    {
      "id": "seg-01-B",
      "shot_type": "close-up",
      "camera_movement": "push-in",
      "motion_prompt": "Close-up on hero's face, camera slowly pushes in as determination fills their expression, eyes narrowing",
      "output_video": "scene-01/seg-B.mp4",
      "status": "pending"
    }
  ]
}
```

---

## Example: Landscape Scene

```json
{
  "id": "scene-02",
  "title": "Sunset Vista",
  "scene_type": "landscape",
  "duration_target": 8,
  "transition_to_next": null,
  "shot_progression": "establishing-to-intimate",
  "continuity": {
    "screen_direction": "neutral",
    "axis_of_action": "not-applicable",
    "spatial_notes": "Static environment shot"
  },
  "first_keyframe": {
    "type": "generated",
    "shot_type": "wide",
    "prompt": "Wide establishing shot of mountain vista at sunset, golden light painting peaks, clouds streaking across orange sky",
    "composition_notes": "Horizon on lower third, sky dominant",
    "background": "mountains",
    "output": "keyframes/scene-02-start.png",
    "status": "pending"
  },
  "segments": [
    {
      "id": "seg-02-A",
      "shot_type": "wide",
      "camera_movement": "pan-right",
      "motion_prompt": "Wide vista with camera slowly panning right, revealing more of the mountain range as sun sets",
      "output_video": "scene-02/seg-A.mp4",
      "status": "pending"
    }
  ]
}
```
