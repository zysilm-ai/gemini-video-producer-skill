# File Templates

## philosophy.md

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

## style.json

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

## scene-breakdown.md

```markdown
# Scene Breakdown: [Project Name]

## Overview
- **Total Duration**: [X seconds]
- **Number of Scenes**: [N]
- **Segment Duration**: 8 seconds (Flow limit)

## Key Subjects (for Reference Generation)
- **Subject 1**: [description for reference image]
- **Subject 2**: [description]

## Camera Path Plan
- **Scene 1**: Camera starts [position], moves [direction]
- **Scene 1→2 Transition**: [CUT/FADE]
- **Scene 2**: Camera [movement pattern]

---

## Scene 1: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [cut/fade/null]
**Camera Style**: [tracking/dolly/crane/static]

**Narrative State at Start**: [What viewer understands]
**Narrative State at End**: [What has changed]

**Segments**:

### Seg A [type: initial]
**Start Keyframe**: [Detailed visual description for opening composition]
**End Keyframe**: [Detailed visual description for closing composition]
**Motion**: [Camera/subject motion between keyframes]
**Anchor Moment**: [Holdable beat at segment end]

### Seg B [type: extend]
**Start Keyframe**: Uses Seg A end keyframe
**End Keyframe**: [Detailed visual description for closing composition]
**Motion**: [Camera/subject motion between keyframes]
**Anchor Moment**: [Holdable beat at segment end]

---

## Scene 2: [Title]
[Same structure as Scene 1]
```

## Keyframe Chain Planning

When planning keyframes, visualize the chain:

```
Scene 1:
  Seg A: [start-A] ──motion──> [end-A]
  Seg B: [end-A]   ──motion──> [end-B]  (reuses A's end)

Scene 2:
  Seg A: [start-C] ──motion──> [end-C]  (new scene, fresh start)
```

## When to Create New Scenes vs Add Segments

| New Scene | Add Segment |
|-----------|-------------|
| Camera angle changes significantly | Continuous action exceeds 8s |
| Location or setting changes | Same camera perspective |
| Time jump occurs | No narrative break needed |
| Subject/focus changes | |
| Want cinematic transition | |

## Keyframe Count per Scene

| Segments | Initial Type | Extend Type | Total Keyframes |
|----------|--------------|-------------|-----------------|
| 1 | 1 (2 keyframes) | 0 | 2 |
| 2 | 1 (2 keyframes) | 1 (1 keyframe) | 3 |
| 3 | 1 (2 keyframes) | 2 (2 keyframes) | 4 |
| 4 | 1 (2 keyframes) | 3 (3 keyframes) | 5 |
