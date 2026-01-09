# Shot Type Reference (v4.0)

> **When to Read**: Phase 2 (Scene Breakdown) - when planning shot types for scenes and segments.

Professional shot types with Whisk prompt modifiers. Shot types are **advisory** - they guide prompt generation to achieve professional framing.

---

## Shot Type Definitions

### WIDE / ESTABLISHING SHOT
- **Definition**: Shows full environment, subject occupies small portion of frame. Establishes location and spatial relationships.
- **When to Use**: Scene openings, location changes, showing scale, establishing geography
- **Whisk Prompt Modifiers**:
  - `"wide establishing shot, full environment visible"`
  - `"extreme wide shot showing entire location"`
  - `"subject small in frame, environment dominant"`
- **Composition**: Rule of thirds for horizon, subject positioned to show scale

### MEDIUM SHOT
- **Definition**: Shows subject from approximately waist up. Balances subject and environment.
- **When to Use**: Dialogue scenes, character actions, transitional shots, general coverage
- **Whisk Prompt Modifiers**:
  - `"medium shot, waist-up framing"`
  - `"mid-shot showing upper body and surroundings"`
  - `"character from waist up, environment visible"`
- **Composition**: Headroom appropriate, rule of thirds for subject placement

### CLOSE-UP (CU)
- **Definition**: Face and shoulders fill frame. Emphasizes emotion and reaction.
- **When to Use**: Emotional beats, important dialogue, reactions, revealing character detail
- **Whisk Prompt Modifiers**:
  - `"close-up shot, face filling frame"`
  - `"tight shot on face, shoulders visible"`
  - `"emotional close-up, emphasis on expression"`
- **Composition**: Eyes on upper third line, minimal headroom

### EXTREME CLOSE-UP (ECU)
- **Definition**: Single feature (eyes, hands, object) fills entire frame.
- **When to Use**: Maximum emotional intensity, important details, tension, horror
- **Whisk Prompt Modifiers**:
  - `"extreme close-up on [feature]"`
  - `"macro shot of [detail]"`
  - `"[feature] filling entire frame"`
- **Composition**: Feature centered or slightly off-center for tension

### POV (Point of View)
- **Definition**: Camera represents character's eyes, showing what they see.
- **When to Use**: Subjective experience, immersion, horror reveals, discovery, action
- **Whisk Prompt Modifiers**:
  - `"first-person POV, seeing through character's eyes"`
  - `"subjective camera, character's viewpoint"`
  - `"POV shot, hands visible at frame edges"`
- **Composition**: Slight camera tilt for organic feel, hands/body parts at edges optional

### OVER-THE-SHOULDER (OTS)
- **Definition**: Camera positioned behind one character, showing their shoulder/head and the subject they're looking at.
- **When to Use**: Dialogue scenes, confrontations, establishing spatial relationship between characters
- **Whisk Prompt Modifiers**:
  - `"over-the-shoulder shot, character's back visible"`
  - `"OTS framing, shoulder in foreground"`
  - `"looking past [character A] at [character B]"`
- **Composition**: Foreground character occupies 1/3, subject in remaining 2/3

### TWO-SHOT
- **Definition**: Two characters in frame together, typically in conversation or interaction.
- **When to Use**: Dialogue between two characters, showing relationship, comedy timing
- **Whisk Prompt Modifiers**:
  - `"two-shot framing, both characters visible"`
  - `"dual subject composition"`
  - `"[character A] and [character B] in frame together"`
- **Composition**: Both subjects balanced with equal or intentional unequal visual weight

### INSERT SHOT
- **Definition**: Close-up of object or detail relevant to the action.
- **When to Use**: Showing important props, detail work, information, cutaway
- **Whisk Prompt Modifiers**:
  - `"insert shot of [object]"`
  - `"detail shot focusing on [item]"`
  - `"close-up cutaway to [object]"`
- **Composition**: Object fills frame, clean background, clear lighting

---

## Shot Type Selection by Genre

| Genre | Primary Shots | Emphasis Shots | Avoid |
|-------|--------------|----------------|-------|
| **Action** | wide, medium | close-up (impact) | static ECU |
| **Horror** | medium, close-up, POV | ECU (dread) | comfortable two-shots |
| **Comedy** | medium, two-shot, wide | close-up (reaction) | dramatic ECU |
| **Drama** | medium, close-up, OTS | ECU (emotion) | unmotivated POV |
| **Anime** | all types | ECU (eyes), wide (world) | realistic handheld |
| **Documentary** | medium, wide, OTS | insert (evidence) | stylized POV |

---

## Quick Reference Table

| Shot Type | Whisk Modifier | Best For |
|-----------|----------------|----------|
| wide | `"wide establishing shot, full environment"` | Scene openings, scale |
| medium | `"medium shot, waist-up framing"` | Dialogue, actions |
| close-up | `"close-up shot, face filling frame"` | Emotion, reaction |
| extreme-close-up | `"extreme close-up on [feature]"` | Intensity, detail |
| pov | `"first-person POV"` | Immersion, action |
| over-shoulder | `"over-the-shoulder shot"` | Dialogue, relationship |
| two-shot | `"two-shot framing"` | Conversations, comedy |
| insert | `"insert shot of [object]"` | Props, details |
