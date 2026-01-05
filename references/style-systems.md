# Style Systems Guide

How to establish and maintain visual consistency across your AI video production.

## The Production Philosophy

The Production Philosophy is the foundation of visual consistency. It defines the "rules" that govern all visual decisions in your project.

### Why Philosophy First?

Without a defined philosophy:
- Each generation makes independent style decisions
- Visual elements drift between scenes
- The final video lacks cohesion
- Iteration becomes expensive (regenerating everything)

With a philosophy:
- All generations follow the same visual rules
- Consistency is built-in, not fixed later
- Faster iteration (change philosophy, not every prompt)
- Professional, cohesive results

## Philosophy Components

### 1. Visual Identity

Define the overall look and feel:

```markdown
## Visual Identity

**Art Style**: Cinematic realism with subtle painterly touches,
reminiscent of Roger Deakins cinematography meets Studio Ghibli
background art. Grounded in reality but with enhanced beauty.

**Color Palette**:
- Primary: Warm earth tones (amber, sienna, ochre)
- Secondary: Deep teals and slate blues
- Accent: Occasional warm golden highlights
- Avoid: Neon colors, pure blacks, harsh whites

**Lighting Philosophy**:
Natural light preferred. Golden hour is our default.
When indoors, motivated lighting from windows or practical sources.
Shadows are soft but present, never flat.
Light direction: consistently from upper-left unless scene demands otherwise.

**Composition Principles**:
- Wide shots for establishing, close-ups for emotion
- Rule of thirds for static compositions
- Center framing for powerful moments
- Negative space used intentionally for mood
```

### 2. Motion Language

Define how things move:

```markdown
## Motion Language

**Movement Quality**:
Our motion is smooth and deliberate. Characters move with weight
and intention. No sudden jerky movements unless expressing surprise
or violence.

**Pacing**:
- Establishing shots: Slow, contemplative (4-8 seconds static)
- Dialogue scenes: Medium pace, subtle movements
- Action sequences: Dynamic but not frenetic
- Emotional beats: Hold on expressions, let moments breathe

**Camera Movement**:
- Slow push-ins for tension building
- Smooth tracking for following action
- Static for emotional resonance
- Avoid: Shaky cam, rapid zooms, unmotivated movement

**Transitions**:
- Match cuts where possible
- Fade to black for time passage
- Direct cuts for same-time scene changes
```

### 3. Subject Consistency

Define recurring elements:

```markdown
## Subject Consistency

**Main Character: Elena**
- Age: Mid-20s
- Hair: Long, dark brown, often windswept
- Eyes: Deep green
- Build: Athletic, medium height
- Signature outfit: Earth-toned practical clothing, leather satchel
- Physical mannerisms: Touches hair when thinking, stands with weight on left foot
- Reference images: character-refs/elena-front.png, elena-side.png, elena-back.png

**Environment: The Valley**
- Lush temperate forest with ancient trees
- A winding river reflects the sky
- Distant mountains always visible on horizon
- Architecture: Stone ruins covered in moss and vines
- Weather: Usually clear with dramatic clouds
- Time of day: Varies, but golden hour preferred
```

### 4. Constraints and Rules

Define what to avoid:

```markdown
## Constraints

**Never Include**:
- Modern technology (cars, phones, power lines)
- Text or writing visible in frame (unless plot-relevant)
- Contemporary clothing on background characters
- Lens artifacts that break immersion (excessive flare, chromatic aberration)

**Always Maintain**:
- Consistent sun/light direction within a scene
- Character proportions and features
- Color grade across all scenes
- The established geography of locations

**Technical Standards**:
- Minimum 720p, prefer 1080p for hero shots
- Avoid banding in gradients (request smooth transitions)
- Sharp focus on subject, natural depth of field falloff
```

## Style Configuration (JSON)

Convert your philosophy into a machine-readable format:

```json
{
  "project_name": "Valley of Echoes",
  "version": "1.0",
  "visual_style": {
    "art_style": "Cinematic realism with subtle painterly touches",
    "color_palette": {
      "primary": ["amber", "sienna", "ochre"],
      "secondary": ["deep teal", "slate blue"],
      "accent": ["warm gold"],
      "avoid": ["neon", "pure black", "harsh white"]
    },
    "lighting": {
      "type": "natural, golden hour preferred",
      "direction": "upper-left default",
      "quality": "soft shadows, never flat"
    },
    "composition": {
      "wide_shots": "establishing, rule of thirds",
      "close_ups": "emotional beats, center framing for power",
      "negative_space": "intentional for mood"
    }
  },
  "motion_language": {
    "movement_quality": "smooth and deliberate, weighted",
    "pacing": {
      "establishing": "slow, 4-8 seconds",
      "dialogue": "medium, subtle",
      "action": "dynamic but controlled",
      "emotional": "hold, let moments breathe"
    },
    "camera_style": "slow push-ins, smooth tracking, static for emotion",
    "avoid": ["shaky cam", "rapid zooms", "unmotivated movement"]
  },
  "subjects": {
    "elena": {
      "type": "main_character",
      "description": "Mid-20s woman, long dark brown hair, green eyes, athletic build",
      "outfit": "earth-toned practical clothing, leather satchel",
      "references": ["character-refs/elena-front.png", "character-refs/elena-side.png"]
    },
    "the_valley": {
      "type": "environment",
      "description": "Lush temperate forest, ancient trees, winding river, distant mountains",
      "architecture": "stone ruins with moss and vines",
      "weather": "clear with dramatic clouds",
      "time_of_day": "golden hour preferred"
    }
  },
  "constraints": {
    "avoid": [
      "modern technology",
      "visible text unless plot-relevant",
      "contemporary clothing on NPCs",
      "excessive lens artifacts"
    ],
    "maintain": [
      "consistent lighting direction in scenes",
      "character proportions",
      "color grade",
      "location geography"
    ]
  }
}
```

## Using Style Configuration

### With Image Generation

```bash
python scripts/gemini_image.py \
  --prompt "Elena stands at the edge of the forest, looking toward distant mountains" \
  --style-ref outputs/style.json \
  --reference character-refs/elena-front.png \
  --output outputs/scene-01/keyframe-start.png
```

The script reads the style configuration and enhances your prompt with:
- Art style descriptors
- Color palette guidance
- Lighting specifications
- Motion quality hints

### With Video Generation

```bash
python scripts/veo_video.py \
  --prompt "Elena walks slowly into the forest, sunlight filtering through leaves" \
  --start-frame outputs/scene-01/keyframe-start.png \
  --style-ref outputs/style.json \
  --output outputs/scene-01/video.mp4
```

## Style Templates by Video Type

### Promotional Video
```json
{
  "visual_style": {
    "art_style": "clean, modern, professional",
    "color_palette": {
      "primary": ["brand colors here"],
      "secondary": ["complementary tones"],
      "accent": ["call-to-action highlight color"]
    },
    "lighting": "bright, even, flattering"
  },
  "motion_language": {
    "movement_quality": "smooth, confident, purposeful",
    "pacing": "dynamic, modern, 2-4 second shots",
    "camera_style": "orbiting product shots, smooth reveals"
  }
}
```

### Educational/Tutorial
```json
{
  "visual_style": {
    "art_style": "clear, uncluttered, focused",
    "color_palette": {
      "primary": ["neutral backgrounds"],
      "accent": ["highlight color for key elements"]
    },
    "lighting": "even, no harsh shadows, good visibility"
  },
  "motion_language": {
    "movement_quality": "steady, predictable, easy to follow",
    "pacing": "measured, allows for comprehension",
    "camera_style": "static or slow smooth movements"
  }
}
```

### Narrative/Cinematic
```json
{
  "visual_style": {
    "art_style": "cinematic, film-like, atmospheric",
    "color_palette": {
      "primary": ["mood-appropriate palette"],
      "contrast": "considered for dramatic effect"
    },
    "lighting": "motivated, dramatic when appropriate"
  },
  "motion_language": {
    "movement_quality": "character-driven, emotionally resonant",
    "pacing": "varied for emotional beats",
    "camera_style": "storytelling-focused, intentional choices"
  }
}
```

### Social Media (Short Form)
```json
{
  "visual_style": {
    "art_style": "bold, eye-catching, high contrast",
    "color_palette": {
      "primary": ["vibrant, saturated colors"],
      "accent": ["pop colors for attention"]
    },
    "lighting": "bright, energetic"
  },
  "motion_language": {
    "movement_quality": "dynamic, attention-grabbing",
    "pacing": "fast, hook in first 2 seconds",
    "camera_style": "dynamic angles, movement"
  }
}
```

## Maintaining Consistency Across Sessions

1. **Save your style configuration** in version control
2. **Use the same reference images** throughout the project
3. **Create a "style anchor" keyframe** that exemplifies your vision
4. **Review all outputs** against the Production Philosophy
5. **Update philosophy** if vision evolves (then regenerate affected assets)
