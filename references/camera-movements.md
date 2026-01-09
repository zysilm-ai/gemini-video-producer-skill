# Camera Movement Reference (v4.0)

> **When to Read**: Phase 2 (Scene Breakdown) - when planning camera movements for segments.

Camera movement types for the `camera_movement` field in segments. Each movement has specific emotional and narrative effects.

---

## Camera Movement Types

| Movement | Description | Whisk Prompt Modifier | Best For |
|----------|-------------|----------------------|----------|
| `static` | Camera holds position | `"camera holds steady"` | Dialogue, tension, letting action unfold |
| `push-in` | Camera moves toward subject | `"camera slowly pushes in"` | Building intensity, focusing attention |
| `pull-out` | Camera moves away from subject | `"camera pulls back to reveal"` | Reveals, showing context, endings |
| `pan-left` | Camera rotates left on axis | `"camera pans left"` | Following action, revealing space |
| `pan-right` | Camera rotates right on axis | `"camera pans right"` | Following action, revealing space |
| `track-left` | Camera moves bodily left | `"camera tracks left"` | Following moving subject |
| `track-right` | Camera moves bodily right | `"camera tracks right"` | Following moving subject |
| `crane-up` | Camera rises vertically | `"camera cranes up"` | Reveals, power, transcendence |
| `crane-down` | Camera descends vertically | `"camera descends"` | Intimacy, vulnerability, grounding |
| `handheld` | Organic, human movement | `"handheld camera feel"` | Urgency, documentary, chaos |
| `steadicam` | Smooth floating movement | `"smooth steadicam movement"` | Following action fluidly, immersion |

---

## Camera Movement by Genre

| Genre | Preferred Movements | Avoid |
|-------|--------------------|----- |
| **Action** | track, handheld, steadicam | long static holds |
| **Horror** | push-in, static, handheld | smooth steadicam |
| **Comedy** | static, pan, motivated push-in | dramatic crane |
| **Drama** | push-in, static, steadicam | flashy unmotivated moves |
| **Anime** | push-in, pull-out, pan | realistic handheld |
| **Documentary** | static, handheld, pan | cinematic crane |

---

## Movement Emotional Effects

### Building Intensity
- **push-in** - Creates focus, builds tension or intimacy
- **crane-up** - Elevates subject, creates power or transcendence

### Revealing Information
- **pull-out** - Reveals context, shows scale
- **crane-up** - Reveals geography, scope
- **pan** - Reveals space, connects elements

### Creating Energy
- **track-left/right** - Dynamic following motion
- **handheld** - Urgency, chaos, documentary feel
- **steadicam** - Smooth energy, flowing movement

### Creating Calm/Focus
- **static** - Allows audience to observe, creates stillness
- **crane-down** - Grounding, intimacy, vulnerability

---

## Speed Modifiers

Add these to prompts to control movement speed:

| Speed | Modifier | Use Case |
|-------|----------|----------|
| Very slow | `"glacially slow push-in"` | Dread, contemplation |
| Slow | `"slow push-in"` | Drama, intimacy |
| Moderate | `"steady push-in"` | General use |
| Fast | `"quick push-in"` | Action, urgency |
| Very fast | `"rapid push-in"` | Impact moments |

---

## Combining with Shot Types

| Shot Type | Best Camera Movements | Avoid |
|-----------|----------------------|-------|
| wide | pan, track, crane | push-in (defeats purpose) |
| medium | push-in, static, track | extreme movements |
| close-up | static, subtle push-in | pan, track |
| ECU | static | any movement |
| POV | handheld, track | static (feels unnatural) |
| OTS | static, subtle push-in | pan, crane |
