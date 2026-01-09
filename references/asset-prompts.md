# Asset Prompt Writing Guide

> **When to Read**: Phase 2.5 (Asset Definition) - when writing prompts for characters, backgrounds, styles, and objects in assets.json.

This guide covers professional prompt writing for generating reusable reference assets that will be uploaded to Whisk's reference slots (Subject, Scene, Style).

---

## Asset Types Overview

| Asset Type | Whisk Slot | Purpose | Format |
|------------|------------|---------|--------|
| **Characters** | Subject (Motiv) | Identity consistency | Character Model Sheet |
| **Backgrounds** | Scene (Szene) | Environment reference | Environment Concept Art |
| **Styles** | Style (Stil) | Visual treatment | Style Reference Image |
| **Objects** | Subject (Motiv) | Prop consistency | Prop Reference Sheet |

---

## Character Assets: Model Sheet / Turnaround

Professional animation and film production uses **character model sheets** (also called turnaround sheets) - a single image containing multiple angles of the character.

### What a Character Model Sheet Contains

```
┌─────────────────────────────────────────────────────┐
│                  CHARACTER NAME                      │
│                                                     │
│    FRONT      3/4 VIEW     SIDE       BACK         │
│                                                     │
│     ┌─┐        ┌─┐         ┌─┐        ┌─┐         │
│    /│ │\      /│ │\        │ │        │ │         │
│     │ │        │ │         │ │        │ │         │
│    / \        / \         / \        / \          │
│                                                     │
│  [All views at consistent scale, T-pose or A-pose] │
└─────────────────────────────────────────────────────┘
```

### Character Model Sheet Requirements

1. **Multiple views in one image**: Front, 3/4, Side (profile), Back
2. **Neutral pose**: T-pose or A-pose (arms slightly away from body)
3. **Neutral expression**: No emotion, relaxed face
4. **Consistent scale**: All views same size/proportion
5. **Clean background**: White or neutral gray
6. **Full body visible**: Head to feet in frame
7. **Consistent lighting**: Same light direction across all views

### Character Model Sheet Prompt Template

```
Character model sheet turnaround of [CHARACTER DESCRIPTION],
multiple views showing front view, three-quarter view, side profile, and back view,
[POSE TYPE: T-pose/A-pose] with arms slightly away from body,
neutral expression, consistent proportions and scale across all views,
[ART STYLE] style, clean white background,
professional character design reference sheet for animation production
```

### Character Prompt Examples

**Hero Character:**
```
Character model sheet turnaround of a young male knight with blonde hair in ponytail and blue eyes,
wearing blue tunic with white trim and brown leather boots,
multiple views showing front view, three-quarter view, side profile, and back view,
A-pose with arms slightly away from body, neutral expression,
consistent proportions and scale across all views,
painterly anime style, clean white background,
professional character design reference sheet for animation production
```

**Creature/Non-Human:**
```
Character model sheet turnaround of a red-skinned aquatic humanoid female with fins and fish-like features,
elegant slender build, wearing ornate armor and blue scarf,
multiple views showing front view, three-quarter view, side profile, and back view,
A-pose standing straight, neutral expression,
consistent proportions and scale across all views,
painterly anime style, clean white background,
professional character design reference sheet for animation production
```

**Monster/Villain:**
```
Character model sheet of a massive corrupted mechanical creature,
amalgamation of spider-like robot limbs and swirling dark energy,
glowing magenta core, multiple views showing front view, side view, and three-quarter view,
consistent scale across all views,
dark fantasy style with horror elements, neutral gray background to show glowing elements,
professional creature design reference sheet
```

---

## Object Assets: Prop Reference Sheet

Professional prop design uses **prop sheets** or **object reference sheets** - a single image containing multiple views, scale reference, and detail callouts.

### What a Prop Reference Sheet Contains

```
┌─────────────────────────────────────────────────────┐
│                    PROP NAME                         │
│                                                     │
│   FRONT     SIDE      3/4 VIEW     SCALE REF       │
│                                                     │
│     │        ─          ╱│         │    ┌─┐       │
│     │        │         ╱ │         │   /   \      │
│     │        │        ╱  │         │    │ │       │
│     ▼        ▼       ▼   ▼         ▼    / \       │
│                                                     │
│   DETAIL CALLOUT:        MATERIAL NOTES:           │
│   [Close-up of           Steel, gold accents,      │
│    important feature]    glowing blue gems         │
└─────────────────────────────────────────────────────┘
```

### Prop Reference Sheet Requirements

1. **Multiple orthographic views**: Front, Side, Top (or 3/4 perspective)
2. **Scale reference**: Human silhouette or measurement indicator
3. **Detail callouts**: Close-ups of intricate parts, mechanisms, textures
4. **Consistent lighting**: Same light direction across all views
5. **Clean background**: White or neutral
6. **Material indication**: Show surface qualities (metal, wood, fabric, etc.)

### Prop Reference Sheet Prompt Template

```
Prop reference sheet of [OBJECT DESCRIPTION],
multiple views showing front view, side view, and three-quarter perspective,
[OPTIONAL: detail callout of [IMPORTANT FEATURE]],
scale reference with human silhouette,
clean white background, consistent lighting across all views,
[ART STYLE] style, professional prop design sheet for animation production
```

### Prop Prompt Examples

**Weapon:**
```
Prop reference sheet of a legendary sword with blue hilt and golden crossguard,
glowing blade with ancient symbols, purple gem in pommel,
multiple views showing front view, side view, and three-quarter perspective,
detail callout of the ornate hilt and crossguard design,
scale reference with human silhouette showing sword is roughly 3 feet long,
clean white background, consistent lighting across all views,
painterly fantasy style, professional prop design sheet for animation production
```

**Technology/Device:**
```
Prop reference sheet of an ancient tablet device with glowing cyan eye symbol,
stone and metal construction with circuit-like engravings,
multiple views showing front view, back view, and three-quarter perspective,
detail callout of the glowing screen interface,
scale reference showing tablet is handheld size,
clean white background, consistent lighting across all views,
sci-fi fantasy style, professional prop design sheet for animation production
```

**Vehicle/Large Object:**
```
Prop reference sheet of a massive mechanical elephant machine,
ancient technology aesthetic with glowing blue accents,
multiple views showing front view, side view, and three-quarter perspective,
detail callout of the head and trunk mechanism,
scale reference with human silhouette showing enormous scale,
clean white background, consistent lighting across all views,
fantasy mecha style, professional vehicle design sheet for animation production
```

---

## Background Assets: Environment Concept Art

Background assets serve as **scene references** for Whisk's Scene slot. They establish location, mood, and atmosphere.

### Background Asset Requirements

1. **No characters visible**: Pure environment/location
2. **Establishes location**: Clear sense of place
3. **Shows mood/atmosphere**: Lighting, weather, time of day
4. **Composition space**: Leave room for characters to be added
5. **Art style consistent**: Match project's visual philosophy

### Background Prompt Template

```
[SHOT TYPE] of [LOCATION DESCRIPTION],
no characters visible, [TIME OF DAY] lighting,
[ATMOSPHERE/MOOD DESCRIPTION],
[WEATHER if relevant], [KEY ENVIRONMENTAL DETAILS],
[ART STYLE] style, environment concept art for animation production
```

### Background Prompt Examples

**Peaceful Location:**
```
Wide establishing shot of a sacred mountain spring with clear pool,
no characters visible, golden hour lighting with ethereal glow,
ancient stone architecture and massive goddess statue in background,
serene mist rising from water, peaceful sacred atmosphere,
painterly anime style, Ghibli-inspired environment concept art
```

**Dramatic Location:**
```
Wide shot of a castle consumed by swirling dark energy,
no characters visible, ominous red and purple sky,
corrupted magical energy erupting from towers, fires burning below,
apocalyptic destruction atmosphere, lightning in clouds,
dark fantasy style, dramatic environment concept art
```

**Interior Location:**
```
Interior shot of ancient ruined temple hall,
no characters visible, dramatic shafts of golden light through broken ceiling,
crumbling stone columns overgrown with vines and moss,
dust particles visible in light beams, solemn abandoned atmosphere,
painterly anime style, architectural environment concept art
```

---

## Style Assets: Visual Treatment Reference

Style assets demonstrate the **visual treatment** (color palette, lighting style, texture quality) and are uploaded to Whisk's Style slot.

### Style Asset Requirements

1. **Focus on environment/atmosphere**: NOT characters
2. **Demonstrates color palette**: Show the colors you want
3. **Shows lighting style**: The quality and direction of light
4. **Exhibits texture quality**: Painterly, clean, grainy, etc.
5. **Captures mood**: The emotional tone of visuals

### Style Prompt Template

```
[ART STYLE] style reference image, no characters,
[ENVIRONMENT TYPE] demonstrating [COLOR PALETTE DESCRIPTION],
[LIGHTING STYLE] with [LIGHTING QUALITY],
[TEXTURE DESCRIPTION], [MOOD/ATMOSPHERE],
visual style reference for animation production
```

### Style Prompt Examples

**Painterly Anime Style:**
```
Painterly anime style reference image, no characters,
beautiful fantasy landscape demonstrating warm earth tones and soft greens,
golden hour natural lighting with visible light rays through atmosphere,
soft watercolor texture with visible brush strokes, nostalgic peaceful mood,
Ghibli-inspired visual style reference for animation production
```

**Dark Cinematic Style:**
```
Dark cinematic style reference image, no characters,
moody interior scene demonstrating desaturated cool colors with warm accent highlights,
dramatic chiaroscuro lighting with deep shadows and rim lighting,
film grain texture with high contrast, tense atmospheric mood,
noir-inspired visual style reference for film production
```

**Vibrant Action Style:**
```
Dynamic action style reference image, no characters,
explosive battlefield scene demonstrating high contrast saturated colors,
dramatic rim lighting with motion blur and particle effects,
sharp detailed texture with energy effects, intense powerful mood,
blockbuster action visual style reference for animation production
```

---

## Prompt Structure Summary

### Character Model Sheet
```
Character model sheet turnaround of [DESCRIPTION],
multiple views showing front, 3/4, side, back,
[POSE], neutral expression, consistent scale,
[STYLE], clean white background,
professional character design reference sheet
```

### Prop Reference Sheet
```
Prop reference sheet of [DESCRIPTION],
multiple views showing front, side, 3/4,
detail callout of [FEATURE], scale reference with human silhouette,
[STYLE], clean white background,
professional prop design sheet
```

### Background Environment
```
[SHOT TYPE] of [LOCATION],
no characters visible, [LIGHTING],
[ATMOSPHERE], [DETAILS],
[STYLE], environment concept art
```

### Style Reference
```
[STYLE] reference image, no characters,
[ENVIRONMENT] demonstrating [COLORS],
[LIGHTING], [TEXTURE], [MOOD],
visual style reference
```

---

## Common Mistakes to Avoid

| Mistake | Problem | Correct Approach |
|---------|---------|------------------|
| Portrait instead of model sheet | Only shows one angle | Request "multiple views" turnaround |
| Emotional expression | Hard to use as neutral reference | Specify "neutral expression" |
| Action pose | Limbs obscure body details | Use "T-pose" or "A-pose" |
| Busy background | Distracts from character | Always "clean white background" |
| Characters in backgrounds | Conflicts with scene composition | Specify "no characters visible" |
| Single angle for props | Missing important details | Request "multiple views" |
| No scale reference for props | Size unclear | Include "scale reference with human silhouette" |
| Describing style verbally | No visual reference for Whisk | Generate actual style image |

---

## Integration with Pipeline

Assets defined in `assets.json` should use these prompt templates. The prompts are then executed in Phase 4 and the resulting images are used as references in Phases 5-6.

```
Phase 2.5: Write asset prompts using this guide
    ↓
Phase 4: Generate assets in Whisk using prompts
    ↓
Phase 5: Upload assets to Whisk slots when generating keyframes
         - Characters → Subject slot
         - Backgrounds → Scene slot
         - Styles → Style slot
```
