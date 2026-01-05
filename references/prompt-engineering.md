# Prompt Engineering Guide for AI Video Production

This guide covers advanced prompt writing techniques for both image generation (Gemini) and video generation (Veo).

## Prompt Anatomy

A well-structured prompt contains these components in order:

```
[Subject] + [Action] + [Environment] + [Style] + [Technical] + [Constraints]
```

### Component Breakdown

#### 1. Subject Description
Be specific about the main subject. Include:
- Physical appearance
- Clothing/accessories
- Pose or stance
- Emotional state

**Weak**: "A person standing"
**Strong**: "A young woman with long dark hair wearing a flowing white dress, standing with arms slightly raised, serene expression"

#### 2. Action/Motion
For video prompts, describe the motion trajectory:
- Starting position
- Motion path
- Ending position (if not using end frame)
- Speed and quality of movement

**Weak**: "She moves"
**Strong**: "She slowly raises her arms from her sides to above her head, palms facing upward, movement fluid and graceful"

#### 3. Environment
Set the scene with:
- Location type
- Time of day
- Weather/atmosphere
- Foreground/background elements

**Weak**: "Outside"
**Strong**: "Standing at the edge of a cliff overlooking a stormy ocean, dark clouds gathering on the horizon, wind-swept grass in the foreground"

#### 4. Style Specification
Define the visual treatment:
- Art style (cinematic, animated, stylized)
- Color treatment (warm, cool, monochromatic)
- Mood (dramatic, peaceful, tense)
- Reference styles (optional)

**Weak**: "Nice looking"
**Strong**: "Cinematic wide shot, golden hour lighting, film grain, shallow depth of field, warm color grade with teal shadows"

#### 5. Technical Details
Camera and composition:
- Shot type (wide, medium, close-up)
- Camera movement (static, tracking, pan)
- Angle (eye-level, low angle, bird's eye)
- Aspect ratio considerations

**Weak**: (omitted)
**Strong**: "Medium wide shot, slight low angle, camera slowly dollies forward, 16:9 cinematic aspect ratio"

#### 6. Constraints
What to avoid or maintain:
- Elements to exclude
- Consistency requirements
- Directional locks

**Weak**: (omitted)
**Strong**: "Character remains facing the ocean throughout, no rotation. Avoid any modern elements. Maintain consistent lighting direction from upper left."

## Image Prompt Examples

### Character Portrait
```
A weathered sea captain in his 60s with a gray beard and deep-set eyes,
wearing a dark wool peacoat and captain's hat,
standing at the helm of a wooden sailing ship,
stormy seas visible through rain-spattered windows behind him.
Dramatic lighting from a lantern, chiaroscuro effect,
cinematic portrait shot, shallow depth of field.
Photorealistic, film grain, muted color palette with warm lamp light.
```

### Environment/Establishing Shot
```
An ancient temple partially reclaimed by jungle,
massive stone pillars wrapped in vines and moss,
shafts of golden sunlight piercing through the canopy above,
mist rising from the jungle floor.
Wide establishing shot, rule of thirds composition,
subject space on right for character entry.
Cinematic, Uncharted game aesthetic, lush greens with warm golden accents.
```

### Product Shot
```
A sleek smartwatch with a dark titanium case,
displayed on a marble surface with soft reflections,
minimalist background with subtle gradient from dark gray to black.
Product photography lighting with key light from upper right,
perfect focus on watch face showing 10:10 time.
Clean, modern, Apple product photography style.
```

## Video Prompt Examples

### Action Sequence (Dual-Frame)
```
The warrior springs forward from a crouching position,
sword drawn back for a powerful horizontal slash,
motion blur on the blade as it arcs through the air.
Enemies in the background begin to react, some raising shields.
Dust and debris kicked up from the warrior's movement.
Dynamic camera follows the action with slight shake.
Cinematic action, 300 movie style slow-motion aesthetic.
Warrior remains facing right throughout the sequence.
```

### Ambient/Atmospheric (Single-Frame)
```
Gentle waves lap against the shore as the sun sets,
colors shifting from orange to deep purple across the sky,
a lone sailboat silhouette drifts slowly across the horizon.
Seabirds occasionally pass through frame.
Camera remains static, contemplative mood.
Golden hour transitioning to blue hour,
film photography aesthetic, slight lens flare from sun.
```

### Product Demo (Text-to-Video)
```
A smartphone rotates slowly on a minimalist white surface,
light catching the metallic edges and creating subtle reflections,
camera orbits 180 degrees around the device.
Clean, modern lighting with soft shadows.
Apple-style product video aesthetic,
smooth continuous motion, no sudden changes.
```

### Character Transformation (Dual-Frame)
```
Starting: Young woman in casual modern clothes, confused expression.
Ending: Same woman now in elegant period dress, confident pose.

The transformation happens through a spiral of glowing particles
that swirl around her, briefly obscuring view before revealing the change.
Magical sparkle effects, warm golden light emanates from the transformation.
Fantasy movie aesthetic, Disney-quality visual effects.
Character position remains center frame throughout.
```

## Motion Description Vocabulary

### Speed Modifiers
- **Very slow**: "glacially", "imperceptibly", "in slow-motion"
- **Slow**: "gradually", "gently", "leisurely"
- **Normal**: "steadily", "smoothly", "naturally"
- **Fast**: "quickly", "swiftly", "rapidly"
- **Very fast**: "instantly", "in a flash", "explosively"

### Quality Modifiers
- **Smooth**: "fluid", "graceful", "seamless", "flowing"
- **Sharp**: "precise", "snappy", "crisp", "sudden"
- **Heavy**: "weighted", "powerful", "forceful", "impactful"
- **Light**: "delicate", "airy", "subtle", "ethereal"

### Directional Terms
- "moves from left to right across frame"
- "rises up from below frame"
- "retreats into the background"
- "approaches camera"
- "circles clockwise around"
- "descends diagonally toward lower right"

## Common Mistakes

### Mistake 1: Ambiguous Action
**Bad**: "The character does something dramatic"
**Good**: "The character throws both arms wide, head tilted back, mouth open in a triumphant shout"

### Mistake 2: Contradicting Keyframes
**Bad**: (Start frame shows character on left, prompt says they enter from right)
**Good**: Ensure prompt matches the visual information in keyframes

### Mistake 3: Impossible Physics
**Bad**: "Character instantly teleports across the room" (without magical context)
**Good**: "Character dashes across the room in a blur of speed, leaving a motion trail"

### Mistake 4: Too Many Actions
**Bad**: "Character jumps, spins, draws sword, blocks attack, and counterstrikes"
**Good**: Focus on one clear action per 8-second segment

### Mistake 5: Missing Constraints
**Bad**: "Character turns around"
**Good**: "Character rotates 90 degrees to face right, revealing profile view. Face should remain visible throughout rotation."

## Style Consistency Tips

1. **Create a prompt template** for your project with fixed style elements
2. **Copy-paste style sections** across all prompts in a project
3. **Reference previous outputs** as style guides when possible
4. **Use the style.json** configuration with the generation scripts
5. **Review each output** against the Production Philosophy before proceeding

## Negative Prompting

Veo and Gemini don't use traditional negative prompts. Instead, use explicit constraints:

**Instead of**: `negative_prompt: "blurry, low quality, distorted"`
**Use**: "Sharp focus, high quality, anatomically correct proportions. Avoid any blur or distortion."

**Instead of**: `negative_prompt: "text, watermark, logo"`
**Use**: "Clean image without any text, watermarks, or logos visible."
