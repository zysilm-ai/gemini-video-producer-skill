# Continuity Rules (v4.0)

> **When to Read**: Phase 2 (Scene Breakdown) - when planning scene continuity and spatial relationships.

Basic film continuity rules to maintain spatial and directional consistency across scenes and segments.

---

## The 180-Degree Rule

The **axis of action** is an imaginary line between two subjects (or along the direction of movement). The camera should stay on one side of this line to maintain consistent screen direction.

### In pipeline.json

```json
"continuity": {
  "axis_of_action": "established",
  "spatial_notes": "Axis between characters A and B at table"
}
```

### Values

| Value | Meaning |
|-------|---------|
| `"established"` | Camera stays on one side of the axis throughout scene |
| `"crossing-allowed"` | Intentional axis crossing (disorientation, confusion) |
| `"not-applicable"` | No clear axis (single subject, landscape) |

### When Breaking the Rule is Intentional

- **Horror**: Disorientation effect
- **Action**: Chaos of battle
- **Transition**: Neutral shot (subject facing camera) resets the axis

### Visual Diagram

```
        [Character A]
             |
    ---------|--------- AXIS LINE
             |
        [Character B]

Camera positions: ALWAYS stay on one side of this line
```

---

## Screen Direction

Characters and objects should maintain consistent movement/facing direction across cuts.

### In pipeline.json

```json
"continuity": {
  "screen_direction": "left-to-right"
}
```

### Values

| Value | Meaning |
|-------|---------|
| `"left-to-right"` | Subject moves/faces toward frame right |
| `"right-to-left"` | Subject moves/faces toward frame left |
| `"neutral"` | Subject faces camera or direction unimportant |

### Maintaining Direction

- If character exits frame right, they should enter next shot from frame left
- Chase sequences: Pursuer and pursued maintain consistent relative direction
- Conversations: Each character maintains their facing direction

### Screen Direction in Prompts

Include direction explicitly in generation prompts:
- `"character faces right, looking toward frame right"`
- `"character running left-to-right"`
- `"subject in profile facing left"`

---

## Continuity Checklist

When planning scenes, verify:

- [ ] Screen direction is consistent with previous scene (unless intentional change)
- [ ] 180-degree axis is established and maintained
- [ ] Character positions are logical (no teleportation)
- [ ] Lighting direction is consistent within scene
- [ ] Props/objects maintain position between segments

---

## Common Continuity Mistakes

### Screen Direction Flip
**Problem**: Character faces left in one shot, right in the next
**Solution**:
1. Plan direction in scene-breakdown.md
2. Include direction in prompts
3. Use neutral shots (facing camera) to reset

### 180-Degree Rule Violation
**Problem**: Spatial relationships confusing, characters seem to swap positions
**Solution**:
1. Establish axis in continuity notes
2. Keep camera on one side of the imaginary line
3. Use neutral shot to reset if crossing is needed

### Spatial Teleportation
**Problem**: Character positions don't match between segments
**Solution**:
1. Extract end frame from previous segment as reference
2. Include position descriptions in prompts
3. Maintain consistent environmental elements

### Lighting Direction Inconsistency
**Problem**: Shadows flip direction between segments
**Solution**:
1. Establish lighting direction in philosophy.md
2. Include lighting in prompts
3. Match lighting direction to keyframe when chaining

---

## Continuity Notes Template

For each scene in scene-breakdown.md:

```markdown
### Continuity Notes
- **Screen Direction**: [left-to-right/right-to-left/neutral]
- **180 Rule**: [axis description or "not applicable"]
- **Spatial Setup**: [Character/object positions]
- **Lighting Direction**: [key light direction]
- **Props Tracking**: [important props and their positions]
```

---

## Cross-Scene Continuity Map

Create a continuity map in scene-breakdown.md:

```markdown
## Continuity Summary

### Screen Direction Map
| Scene | Direction | Notes |
|-------|-----------|-------|
| Scene 1 | left-to-right | Character enters from left |
| Scene 2 | neutral | Facing camera (resets direction) |
| Scene 3 | right-to-left | Intentional reversal for return journey |

### 180 Rule Considerations
- Scene 1-2: Axis between protagonist and antagonist
- Scene 3: Single subject, no axis needed
- Intentional crossing in Scene 4 for disorientation
```

---

## Genre-Specific Continuity

| Genre | Continuity Approach |
|-------|---------------------|
| **Action** | Relaxed - chaos allows some breaking |
| **Horror** | Intentional breaks for disorientation |
| **Comedy** | Strict - clarity helps timing |
| **Drama** | Strict - emotional geography matters |
| **Anime** | Stylized - can break with purpose |
| **Documentary** | Observational - natural continuity |
