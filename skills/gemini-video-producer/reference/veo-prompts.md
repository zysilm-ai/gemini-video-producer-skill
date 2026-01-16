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

## Prompt Linking for Extend Mode

When using extend mode, construct prompts that reference continuation:

```
Full prompt = link_phrase + motion_prompt + anchor_moment

Example:
"Continuing the forward momentum from the previous shot, the camera
tracks alongside the flagship as its shield generators flicker to life
with crackling blue energy. The massive hull fills the frame as weapon
ports begin to glow. Camera holds steady on the ship's bow, shields
fully active."
```
