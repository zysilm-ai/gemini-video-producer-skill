# Genre Presets (v4.0)

> **When to Read**: Phase 1 (Production Philosophy) - when selecting a genre for the project.

Select a genre preset to apply consistent visual language, shot preferences, and pacing guidelines. Set in `genre_preset` field at pipeline root level.

---

## ACTION

```json
{
  "genre": "action",
  "visual_style": {
    "color_temperature": "high contrast, cool shadows with warm highlights",
    "saturation": "punchy, slightly desaturated in shadows",
    "lighting_style": "dramatic rim lighting, hard shadows",
    "texture": "gritty, sharp detail"
  },
  "shot_preferences": {
    "preferred_shots": ["wide", "medium", "pov"],
    "emphasis_shots": ["close-up"],
    "default_progression": "action-sequence"
  },
  "pacing": {
    "cut_rhythm": "fast, rhythmic (2-4 second shots)",
    "hold_moments": "impact beats, aftermath"
  },
  "camera_movement": {
    "preferred": ["track-left", "track-right", "handheld", "steadicam"],
    "intensity": "dynamic, motivated by action"
  },
  "prompt_modifiers": [
    "dynamic action shot",
    "high energy",
    "dramatic lighting",
    "motion blur on fast movement",
    "dust and debris particles"
  ]
}
```

**Key Characteristics:**
- High energy, fast cuts
- Dynamic camera movements
- Dramatic rim lighting
- Impact-focused close-ups

---

## HORROR

```json
{
  "genre": "horror",
  "visual_style": {
    "color_temperature": "cold, desaturated with sickly accent colors",
    "saturation": "muted, with occasional oversaturated grotesque elements",
    "lighting_style": "high contrast, deep shadows, motivated sources",
    "texture": "grainy, unsettling detail"
  },
  "shot_preferences": {
    "preferred_shots": ["medium", "close-up", "pov"],
    "emphasis_shots": ["extreme-close-up"],
    "default_progression": "reveal"
  },
  "pacing": {
    "cut_rhythm": "slow build (4-8s), sudden release (1-2s)",
    "hold_moments": "dread building, aftermath of horror"
  },
  "camera_movement": {
    "preferred": ["push-in", "handheld", "static"],
    "intensity": "creeping, uncomfortable"
  },
  "prompt_modifiers": [
    "ominous atmosphere",
    "deep shadows",
    "unsettling mood",
    "something wrong in the frame",
    "dread-inducing lighting"
  ]
}
```

**Key Characteristics:**
- Cold, desaturated colors
- Deep shadows with motivated light sources
- Slow builds with sudden releases
- POV for subjective horror

---

## COMEDY

```json
{
  "genre": "comedy",
  "visual_style": {
    "color_temperature": "warm, inviting",
    "saturation": "vibrant, slightly exaggerated",
    "lighting_style": "bright, even, flattering",
    "texture": "clean, clear"
  },
  "shot_preferences": {
    "preferred_shots": ["medium", "two-shot", "wide"],
    "emphasis_shots": ["close-up", "insert"],
    "default_progression": "dialogue-coverage"
  },
  "pacing": {
    "cut_rhythm": "snappy (2-4s), timed to jokes",
    "hold_moments": "reaction beats, awkward pauses"
  },
  "camera_movement": {
    "preferred": ["static", "push-in", "pan-left", "pan-right"],
    "intensity": "motivated by gags, otherwise restrained"
  },
  "prompt_modifiers": [
    "comedic timing",
    "bright cheerful lighting",
    "exaggerated expression",
    "clear staging for gag",
    "reaction shot emphasis"
  ]
}
```

**Key Characteristics:**
- Warm, bright lighting
- Two-shots for timing
- Reaction close-ups
- Clean staging for gags

---

## DRAMA

```json
{
  "genre": "drama",
  "visual_style": {
    "color_temperature": "naturalistic, mood-appropriate",
    "saturation": "restrained, realistic",
    "lighting_style": "motivated, naturalistic, emotional",
    "texture": "filmic, subtle grain"
  },
  "shot_preferences": {
    "preferred_shots": ["medium", "close-up", "over-shoulder"],
    "emphasis_shots": ["extreme-close-up", "two-shot"],
    "default_progression": "establishing-to-intimate"
  },
  "pacing": {
    "cut_rhythm": "deliberate (4-8s), breathing room",
    "hold_moments": "emotional peaks, silences"
  },
  "camera_movement": {
    "preferred": ["push-in", "static", "steadicam"],
    "intensity": "subtle, emotionally motivated"
  },
  "prompt_modifiers": [
    "cinematic drama",
    "emotional lighting",
    "intimate framing",
    "naturalistic atmosphere",
    "character-focused composition"
  ]
}
```

**Key Characteristics:**
- Naturalistic, motivated lighting
- Intimate framing
- Deliberate pacing with breathing room
- Emotional close-ups

---

## ANIME

```json
{
  "genre": "anime",
  "visual_style": {
    "color_temperature": "vibrant, stylized",
    "saturation": "high, cel-shaded appearance",
    "lighting_style": "dramatic rim lights, stylized shadows",
    "texture": "clean lines, flat color fills"
  },
  "shot_preferences": {
    "preferred_shots": ["medium", "close-up", "wide"],
    "emphasis_shots": ["extreme-close-up", "pov"],
    "default_progression": "establishing-to-intimate"
  },
  "pacing": {
    "cut_rhythm": "variable - dynamic for action, held for emotion",
    "hold_moments": "emotional reactions, dramatic pauses"
  },
  "camera_movement": {
    "preferred": ["push-in", "pull-out", "pan-left", "pan-right", "static"],
    "intensity": "exaggerated for action, subtle for drama"
  },
  "prompt_modifiers": [
    "anime illustration style",
    "clean lines",
    "vibrant colors",
    "dramatic anime lighting",
    "expressive character animation"
  ]
}
```

**Key Characteristics:**
- Vibrant, cel-shaded colors
- Clean lines, flat fills
- ECU on eyes for emotion
- Dramatic rim lighting

---

## DOCUMENTARY

```json
{
  "genre": "documentary",
  "visual_style": {
    "color_temperature": "naturalistic, authentic",
    "saturation": "realistic, unmanipulated look",
    "lighting_style": "available light, motivated practicals",
    "texture": "sharp, detailed, observational"
  },
  "shot_preferences": {
    "preferred_shots": ["medium", "wide", "over-shoulder"],
    "emphasis_shots": ["close-up", "insert"],
    "default_progression": "establishing-to-intimate"
  },
  "pacing": {
    "cut_rhythm": "observational, unhurried (4-8s)",
    "hold_moments": "subject speaking, contemplative"
  },
  "camera_movement": {
    "preferred": ["static", "handheld", "pan-left", "pan-right"],
    "intensity": "observational, reactive"
  },
  "prompt_modifiers": [
    "documentary style",
    "naturalistic lighting",
    "authentic atmosphere",
    "observational camera",
    "real-world setting"
  ]
}
```

**Key Characteristics:**
- Naturalistic, available lighting
- Observational camera style
- Authentic, unmanipulated look
- Insert shots for evidence

---

## Genre Comparison Table

| Genre | Color | Lighting | Pacing | Key Movement |
|-------|-------|----------|--------|--------------|
| Action | High contrast | Rim lighting | Fast (2-4s) | track, handheld |
| Horror | Cold, desaturated | Deep shadows | Slow build, fast release | push-in, static |
| Comedy | Warm, vibrant | Bright, even | Snappy (2-4s) | static, pan |
| Drama | Naturalistic | Motivated, emotional | Deliberate (4-8s) | push-in, steadicam |
| Anime | Vibrant, stylized | Dramatic rim | Variable | push-in, pull-out |
| Documentary | Naturalistic | Available light | Observational (4-8s) | static, handheld |
