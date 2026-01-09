# Philosophy and Style Templates

> **When to Read**: Phase 1 (Production Philosophy) - when creating philosophy.md and style.json.

---

## philosophy.md Template

Create `{output_dir}/philosophy.md` with this structure:

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

---

## style.json Template

Create `{output_dir}/style.json` with this structure:

```json
{
  "project_name": "Project Name",
  "version": "4.0",
  "genre_preset": "drama",
  "visual_style": {
    "art_style": "description",
    "color_palette": {
      "primary": ["color1", "color2", "color3"],
      "secondary": ["color4", "color5"],
      "accent": ["color6"],
      "avoid": ["colors to avoid"]
    },
    "lighting": {
      "type": "natural lighting, golden hour preferred",
      "direction": "upper-left as default",
      "quality": "soft shadows, volumetric when appropriate"
    },
    "composition": {
      "default": "rule of thirds",
      "emphasis": "center framing for key moments",
      "negative_space": "use for breathing room"
    }
  },
  "motion_language": {
    "movement_quality": "smooth and fluid, weighted and natural",
    "pacing": {
      "establishing": "slow, 5-8 seconds",
      "action": "dynamic, 3-5 seconds per beat",
      "emotional": "hold moments, let them breathe"
    },
    "camera_style": "steady tracking, occasional slow push-in",
    "avoid": ["shaky cam", "rapid unmotivated cuts", "excessive zoom"]
  },
  "shot_preferences": {
    "preferred_shots": ["medium", "close-up", "over-shoulder"],
    "emphasis_shots": ["extreme-close-up", "two-shot"],
    "default_progression": "establishing-to-intimate"
  },
  "subjects": {
    "main_character": {
      "type": "character",
      "description": "Describe your main character here",
      "outfit": "Describe typical clothing",
      "references": []
    },
    "environment": {
      "type": "location",
      "description": "Describe primary environment",
      "time_of_day": "golden hour",
      "weather": "clear with some clouds"
    }
  },
  "constraints": {
    "avoid": [
      "text or watermarks in frame",
      "anachronistic elements",
      "excessive lens flare"
    ],
    "maintain": [
      "consistent lighting direction within scenes",
      "character appearance and proportions",
      "color grade across all scenes",
      "screen direction unless intentionally crossing"
    ]
  }
}
```

---

## Example: Action Genre

```markdown
# Production Philosophy: Battlefield FPV

## Visual Identity
- **Art Style**: Photorealistic war photography, documentary feel
- **Color Palette**: Desaturated earth tones, muted greens and browns, dust-hazed skies
- **Lighting**: Harsh daylight through smoke, rim lighting on subjects
- **Composition**: Dynamic angles, slightly tilted horizons, immersive framing

## Motion Language
- **Movement Quality**: Urgent, visceral, handheld energy
- **Pacing**: Fast cuts during action, held moments of tension
- **Camera Style**: POV handheld throughout, shaky organic movement

## Subject Consistency
- **Characters/Products**: First-person soldier perspective, hands/weapon at frame edges
- **Environment**: Devastated urban battlefield, rubble, smoke, debris
- **Props/Elements**: Rifle barrel, debris particles, smoke wisps

## Constraints
- **Avoid**: Clean pristine surfaces, bright colors, static stable shots
- **Maintain**: POV perspective throughout, dust/smoke atmosphere, desaturated color grade
```

---

## Example: Anime Genre

```markdown
# Production Philosophy: Tokyo Pigeon Incident

## Visual Identity
- **Art Style**: Anime illustration, slice-of-life aesthetic, clean lines
- **Color Palette**: Warm golden afternoon tones, soft pastels, vibrant accents
- **Lighting**: Warm rim lighting, soft shadows, anime-style dramatic shifts
- **Composition**: Clear staging, character-focused, environmental detail

## Motion Language
- **Movement Quality**: Fluid anime motion, exaggerated expressions
- **Pacing**: Slice-of-life pacing for setup, sudden escalation for comedy
- **Camera Style**: Static for dialogue, dynamic push-in for emphasis

## Subject Consistency
- **Characters/Products**: Young person in casual clothes, round fluffy pigeon
- **Environment**: Tokyo tram station, Lawson convenience store, urban Japan
- **Props/Elements**: Bakery bag, madeleine pastry, pigeon flock

## Constraints
- **Avoid**: Photorealistic rendering, western animation style
- **Maintain**: Anime illustration consistency, expressive character animation
```

---

## Genre-Specific Guidelines

| Genre | Art Style | Color Palette | Lighting |
|-------|-----------|---------------|----------|
| Action | Gritty photorealistic | High contrast, desaturated shadows | Dramatic rim, hard |
| Horror | Unsettling, grainy | Cold, desaturated, sickly accents | Deep shadows, motivated |
| Comedy | Clean, bright | Warm, vibrant | Even, flattering |
| Drama | Naturalistic, filmic | Restrained, mood-appropriate | Motivated, emotional |
| Anime | Cel-shaded, clean | Vibrant, stylized | Dramatic rim, stylized |
| Documentary | Sharp, authentic | Naturalistic | Available light |

See `references/genre-presets.md` for complete genre configurations.
