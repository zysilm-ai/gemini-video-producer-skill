# Scene Breakdown Template

> **When to Read**: Phase 2 (Scene Breakdown) - when creating scene-breakdown.md.

---

## scene-breakdown.md Template

Create `{output_dir}/scene-breakdown.md` with this structure:

```markdown
# Scene Breakdown: [Project Name]

## Overview
- **Total Duration**: [X seconds]
- **Number of Scenes**: [N]
- **Segment Duration**: 8 seconds (Whisk video limit)
- **Video Type**: [promotional/narrative/educational/etc.]
- **Genre Preset**: [action/horror/comedy/drama/anime/documentary]

---

## Scene 1: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [cut/fade/dissolve/wipe]

### Shot Type Breakdown
| Segment | Shot Type | Camera Movement | Duration |
|---------|-----------|-----------------|----------|
| Keyframe | [wide/medium/close-up/etc.] | N/A | N/A |
| Seg A | [shot type] | [static/push-in/etc.] | 8s |
| Seg B | [shot type] | [camera movement] | 8s |
| Seg C | [shot type] | [camera movement] | Xs |

**Shot Progression**: [establishing-to-intimate/action-sequence/dialogue-coverage/reveal]

### Continuity Notes
- **Screen Direction**: [left-to-right/right-to-left/neutral]
- **180 Rule**: [axis description or "not applicable"]
- **Spatial Setup**: [Character/object positions]

### Starting Keyframe
**Shot Type**: [wide/medium/close-up/etc.]
**Composition**: [Rule of thirds placement, headroom notes]
[Detailed visual description for the generated keyframe that starts this scene]

### Segments
1. **Seg A** (0-8s):
   - **Shot Type**: [type]
   - **Camera**: [movement]
   - **Motion**: [Motion description for first 8 seconds]

2. **Seg B** (8-16s):
   - **Shot Type**: [type]
   - **Camera**: [movement]
   - **Motion**: [Motion description for next 8 seconds]

3. **Seg C** (16-Xs):
   - **Shot Type**: [type]
   - **Camera**: [movement]
   - **Motion**: [Motion description for remaining seconds]

---

## Scene 2: [Title]
**Duration**: [X seconds] → [ceil(X/8)] segments
**Purpose**: [What this scene communicates]
**Transition to Next**: [null - last scene]

### Shot Type Breakdown
| Segment | Shot Type | Camera Movement | Duration |
|---------|-----------|-----------------|----------|
| Keyframe | [type] | N/A | N/A |
| Seg A | [type] | [movement] | 8s |

**Shot Progression**: [pattern]

### Continuity Notes
- **Screen Direction**: [direction]
- **180 Rule**: [axis description]
- **Spatial Setup**: [positions]

### Starting Keyframe
**Shot Type**: [type]
**Composition**: [framing notes]
[Detailed visual description - this is a NEW scene so needs its own keyframe]

### Segments
1. **Seg A** (0-8s):
   - **Shot Type**: [type]
   - **Camera**: [movement]
   - **Motion**: [Motion description]

---

## Continuity Summary

### Screen Direction Map
| Scene | Direction | Notes |
|-------|-----------|-------|
| Scene 1 | [direction] | [notes] |
| Scene 2 | [direction] | [notes] |

### 180 Rule Considerations
- [Notes on axis of action throughout the project]
- [Any intentional rule breaks and justification]

---
```

---

## Planning Guidelines

### When to Create a New Scene

| Condition | Action |
|-----------|--------|
| Camera angle/perspective changes significantly | New scene |
| Location or setting changes | New scene |
| Time jump occurs | New scene |
| Subject/focus changes | New scene |
| You want a cinematic transition (fade, dissolve) | New scene |

### When to Add Segments (Same Scene)

| Condition | Action |
|-----------|--------|
| Continuous action exceeds 8 seconds | Add segment |
| Same camera perspective continues | Add segment |
| No narrative break needed | Add segment |

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

## Shot Progression Patterns

| Pattern | Sequence | Best For |
|---------|----------|----------|
| **establishing-to-intimate** | wide → medium → close-up | Scene openings, emotional build |
| **action-sequence** | wide → medium → close-up → wide | Fights, chases |
| **dialogue-coverage** | two-shot → OTS A → OTS B → close-ups | Conversations |
| **reveal** | ECU → medium → wide | Surprises, plot twists |

See `references/shot-progressions.md` for detailed patterns.

---

## Example Scene Breakdown

```markdown
## Scene 1: The Cute Encounter
**Duration**: 16 seconds → 2 segments
**Purpose**: Establish the protagonist meeting the cute pigeon
**Transition to Next**: cut

### Shot Type Breakdown
| Segment | Shot Type | Camera Movement | Duration |
|---------|-----------|-----------------|----------|
| Keyframe | medium | N/A | N/A |
| Seg A | medium | static | 8s |
| Seg B | close-up | push-in | 8s |

**Shot Progression**: establishing-to-intimate

### Continuity Notes
- **Screen Direction**: left-to-right
- **180 Rule**: Character on right, pigeon approaches from left
- **Spatial Setup**: Tram station platform, Lawson in background

### Starting Keyframe
**Shot Type**: medium
**Composition**: Character on right third, pigeon on left third
Anime illustration style, young person standing at Tokyo tram station platform,
warm golden afternoon light, holding small paper bakery bag, a single round
fluffy grey pigeon waddling toward them on the platform ground, Lawson
convenience store visible in background.

### Segments
1. **Seg A** (0-8s):
   - **Shot Type**: medium
   - **Camera**: static
   - **Motion**: Pigeon waddles closer, character's expression changes to
     delighted surprise, character leans down to look at the adorable pigeon

2. **Seg B** (8-16s):
   - **Shot Type**: close-up
   - **Camera**: push-in
   - **Motion**: Character tears off piece of madeleine, offers to pigeon,
     pigeon pecks happily, warm lighting begins to dim ominously
```
