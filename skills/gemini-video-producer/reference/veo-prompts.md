# Veo Motion Prompt Guidelines

## Structure

`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`

| Component | Description | Example |
|-----------|-------------|---------|
| **Cinematography** | Camera movement, shot type | "Slow dolly push forward", "Wide tracking shot" |
| **Subject** | Main visual focus with details | "A massive silver-blue warship with glowing cyan engines" |
| **Action** | ONE primary motion/change | "rotates its turrets into firing position" |
| **Context** | Setting, environment | "against a backdrop of colorful nebula in deep space" |
| **Style & Ambiance** | Mood, lighting, quality | "Tense pre-battle atmosphere, dramatic rim lighting" |

## Requirements

- **Length:** 100-150 words (3-6 sentences)
- **ONE action per segment** - Don't describe multiple simultaneous events
- **Specific camera language** - Use "dolly", "tracking", "pan", "crane", "push", "pull back"
- **Motion focus** - Describe what MOVES, not static descriptions
- **End with anchor moment** - Holdable beat for clean extensions

## Good Example

```
Slow dolly push forward through a massive fleet formation in deep space.
Sleek silver-blue warships with angular hulls drift majestically past camera,
their cyan engines pulsing with rhythmic blue light. Turrets on the nearest
destroyer slowly rotate into firing position as shield generators flicker
to life with crackling blue energy. The ships hold perfect V-formation
against a backdrop of distant stars and colorful nebula. Tense pre-battle
atmosphere, epic cinematic scale, photorealistic sci-fi with dramatic rim
lighting on metal hulls.
```

## Bad Example

```
Battle erupts in full fury. Blue and red laser beams crisscross the frame.
A battleship fires broadsides. Explosions ripple. Fighters weave between
ships. Debris scatters everywhere. Camera tracks through chaos.
```

**Problems:** 6+ simultaneous actions, vague camera direction

## Fixed Version

```
Dynamic tracking shot following a massive human battleship as it unleashes
a devastating broadside. Blue energy bolts erupt from its flanking cannons,
streaking across the void toward an enemy cruiser. Orange explosions bloom
on the target's shields, rippling with impact energy. Debris and sparks
scatter into space. The battleship's hull fills the foreground, weapon
ports flashing in sequence. Intense combat lighting with contrasting blue
and orange, cinematic sci-fi blockbuster quality.
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Multiple simultaneous actions | Focus on ONE primary action |
| Static descriptions ("Ships in space") | Add motion ("Ships drift forward, engines pulsing") |
| Vague camera ("Camera moves dynamically") | Specific ("Tracking shot following the ship") |
| Too short (30-50 words) | Expand to 100-150 words |
| Missing style/mood | Add atmosphere ("Tense, dramatic rim lighting") |

---

## Keyframe Prompt Guidelines

Keyframes define the visual start and end points for Video aus Frames generation. Each keyframe should be a complete, static composition that can stand alone as an image.

### Structure for Keyframe Prompts

`[Shot Type] + [Subject Position] + [Key Details] + [Environment] + [Style/Lighting]`

### Start Keyframe vs End Keyframe

| Aspect | Start Keyframe | End Keyframe |
|--------|----------------|--------------|
| **Purpose** | Establish the scene opening | Define the motion destination |
| **Composition** | Often wider, establishing | Often closer, resolved |
| **Subject** | Entering/approaching | Arrived/settled |
| **Energy** | Beginning, anticipation | Concluded, resolution |

### Keyframe Prompt Examples

**Start Keyframe:**
```
Wide shot of massive fleet in V-formation against colorful nebula backdrop.
Silver-blue warships with glowing cyan engines arranged in perfect symmetry,
flagship dreadnought prominent at formation center. Ships at distance,
establishing scale and grandeur. Dramatic rim lighting on angular hulls,
deep space environment with scattered stars. Cinematic 16:9 composition,
photorealistic sci-fi quality.
```

**Corresponding End Keyframe:**
```
Medium shot with flagship filling lower third of frame. Warships visible
passing by in periphery, motion implied by positioning. Flagship engines
pulsing bright cyan, shield emitters beginning to glow. Same nebula backdrop
visible behind ship. Camera has approached significantly from start position.
Dramatic lighting, cinematic composition, photorealistic detail.
```

### Keyframe Chain Design

When designing keyframes for chained segments, ensure visual continuity:

```
Segment A: [Wide fleet shot] ────motion────> [Medium flagship approach]
                                                      │
Segment B: [Medium flagship approach] ─motion─> [Close flagship shields]
           (reuses A's end keyframe)
                                                      │
Segment C: [Close flagship shields] ──motion──> [Weapon ports firing]
           (reuses B's end keyframe)
```

### Keyframe Quality Checklist

| Requirement | Description |
|-------------|-------------|
| **16:9 aspect** | Matches video output format |
| **Static composition** | No motion blur, sharp details |
| **Complete scene** | All key elements visible |
| **Style consistent** | Matches project visual style |
| **Logical sequence** | End keyframe follows naturally from motion |

### Common Keyframe Mistakes

| Mistake | Fix |
|---------|-----|
| Motion blur in composition | Describe frozen moment, sharp details |
| Missing key subjects | Include all elements that will be in the video |
| Inconsistent style between frames | Reference same lighting, color palette |
| Too similar start/end | Ensure visible difference for motion |
| Describing motion in keyframe | Keyframes are static - save motion for motion_prompt |

### Relationship: Keyframes vs Motion Prompt

| Element | Describes | Example |
|---------|-----------|---------|
| **Start Keyframe** | Opening frozen moment | "Wide shot of fleet in formation..." |
| **End Keyframe** | Closing frozen moment | "Medium shot with flagship prominent..." |
| **Motion Prompt** | How we get there | "Slow dolly push forward through fleet..." |

The motion prompt should NOT re-describe what's in the keyframes. It describes the journey between them:

**Good motion prompt (with keyframes):**
```
Slow dolly push forward, camera gradually approaching the flagship,
warships drifting past on either side, engines pulsing with rhythmic light,
smooth cinematic movement through the formation.
```

**Bad motion prompt (with keyframes):**
```
Wide shot of fleet in V-formation. Camera pushes forward. Ships have
cyan engines. Flagship is silver-blue. Camera ends on medium shot.
```
*Problems: Re-describes keyframe content, wastes prompt on static descriptions*
