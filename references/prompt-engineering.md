# Prompt Engineering Guide for AI Video Production

This guide covers advanced prompt writing techniques for both image generation and video generation using Google Whisk.

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

## Structured Motion Prompts for I2V

### The Motion Prompt Formula

For Image-to-Video generation, use this structured format:

```
[SUBJECT] [ACTION VERB] [BODY PART DETAILS], [ENVIRONMENTAL INTERACTION], camera [CAMERA MOVEMENT]
```

This structure ensures you describe:
1. **Who/what** is moving
2. **How** they're moving (specific body mechanics)
3. **Interaction** with the environment
4. **Camera** behavior (often overlooked!)

### Examples

**Action Scene:**
```
warrior lunges forward, right arm thrusting sword ahead, left arm pulled back for balance,
cape billowing behind, dust kicking up from boots, camera tracking from side at waist height
```

**Subtle Movement:**
```
woman turns head slowly to the left, eyes shifting first then chin following,
hair swaying gently with movement, soft shadows moving across face,
camera holds steady on medium close-up
```

**Environmental Interaction:**
```
child runs through tall grass, arms brushing against stalks,
grass parting and swaying in wake, pollen catching sunlight,
camera following at child's height
```

**Character Emotion:**
```
man's expression shifts from confusion to understanding,
eyebrows rising, lips parting slightly, shoulders relaxing downward,
warm light gradually brightening on face, camera slowly pushes in
```

### I2V-Specific Rules

1. **Separate subject motion from camera motion** - Describe both explicitly
2. **Describe physical body movements** - "legs pumping", "arms swinging", not just "running"
3. **Include environmental interaction** - "boots splashing through mud", "hair flowing in wind"
4. **Avoid POV/first-person** - I2V models struggle with perspective-based motion
5. **Use motion verbs** - "sprinting" not "in motion"
6. **One action per segment** - Don't overload with multiple complex actions in 8 seconds
7. **Match the keyframe** - If character is standing, don't describe them sitting

### Positional Language for Multi-Character Scenes

When multiple characters appear, use explicit positioning to maintain spatial consistency:

| Position | Phrase | Use When |
|----------|--------|----------|
| Left side | "On the left:" | Character positioned in left third |
| Right side | "On the right:" | Character positioned in right third |
| Center | "In the center:" | Character positioned in middle |
| Foreground | "In the foreground:" | Element closer to camera |
| Background | "In the background:" | Element further from camera |

**Multi-Character Example:**
```
On the left: samurai in red armor raises katana overhead, muscles tensing.
On the right: ninja in black crouches defensively, arms raised to block.
In the background: temple burning with orange flames, smoke rising.
Camera slowly pushes in from wide shot to medium.
```

This explicit positioning helps maintain character placement across regenerations and prevents confusion about who is doing what.

---

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

Whisk doesn't use traditional negative prompts. Instead, use explicit constraints:

**Instead of**: `negative_prompt: "blurry, low quality, distorted"`
**Use**: "Sharp focus, high quality, anatomically correct proportions. Avoid any blur or distortion."

**Instead of**: `negative_prompt: "text, watermark, logo"`
**Use**: "Clean image without any text, watermarks, or logos visible."

---

## Shot Type Prompt Modifiers (v4.0)

Use these prompt modifiers to achieve professional shot types. Add these phrases to your prompts based on the `shot_type` field in pipeline.json.

### Shot Type Modifier Library

| Shot Type | Primary Modifier | Alternative Modifiers |
|-----------|------------------|----------------------|
| `wide` | "wide establishing shot, full environment visible" | "extreme wide shot", "environment dominant, subject small in frame" |
| `medium` | "medium shot, waist-up framing" | "mid-shot showing upper body", "character from waist up" |
| `close-up` | "close-up shot, face filling frame" | "tight shot on face", "emotional close-up" |
| `extreme-close-up` | "extreme close-up on [feature]" | "macro shot", "[feature] filling entire frame" |
| `pov` | "first-person POV, character's viewpoint" | "subjective camera", "POV shot, hands at frame edges" |
| `over-shoulder` | "over-the-shoulder shot, shoulder in foreground" | "OTS framing", "looking past [A] at [B]" |
| `two-shot` | "two-shot framing, both characters visible" | "dual subject composition", "[A] and [B] in frame together" |
| `insert` | "insert shot of [object]" | "detail shot", "close-up cutaway to [object]" |

### Camera Movement Modifier Library

| Movement | Prompt Modifier | Notes |
|----------|-----------------|-------|
| `static` | "camera holds steady" | Good for dialogue, tension |
| `push-in` | "camera slowly pushes in" | Builds intensity |
| `pull-out` | "camera pulls back to reveal" | Shows context |
| `pan-left` | "camera pans left" | Following action |
| `pan-right` | "camera pans right" | Following action |
| `track-left` | "camera tracks left" | Bodily movement |
| `track-right` | "camera tracks right" | Bodily movement |
| `crane-up` | "camera cranes up" | Reveals, power |
| `crane-down` | "camera descends" | Intimacy |
| `handheld` | "handheld camera feel" | Urgency, documentary |
| `steadicam` | "smooth steadicam movement" | Fluid following |

### Genre-Specific Prompt Modifiers

Add these to your prompts based on the `genre_preset` field:

**Action:**
```
dynamic action shot, high energy, dramatic lighting, motion blur on fast movement, dust and debris particles
```

**Horror:**
```
ominous atmosphere, deep shadows, unsettling mood, something wrong in the frame, dread-inducing lighting
```

**Comedy:**
```
comedic timing, bright cheerful lighting, exaggerated expression, clear staging for gag, reaction shot emphasis
```

**Drama:**
```
cinematic drama, emotional lighting, intimate framing, naturalistic atmosphere, character-focused composition
```

**Anime:**
```
anime illustration style, clean lines, vibrant colors, dramatic anime lighting, expressive character animation
```

**Documentary:**
```
documentary style, naturalistic lighting, authentic atmosphere, observational camera, real-world setting
```

### Combining Shot Type + Camera + Genre

Build complete prompts by combining modifiers:

**Example: Action wide shot with tracking camera**
```
wide establishing shot showing the entire battlefield,
soldiers visible small in frame against smoke-filled sky,
camera tracks right following explosion debris,
dynamic action shot, dramatic lighting, dust particles
```

**Example: Horror close-up with slow push-in**
```
close-up shot, face filling frame,
character's eyes wide with terror, sweat on brow,
camera slowly pushes in,
ominous atmosphere, deep shadows, dread-inducing lighting
```

**Example: Comedy two-shot with static camera**
```
two-shot framing, both characters visible at table,
camera holds steady for comedic timing,
bright cheerful lighting, clear staging for visual gag
```

### Shot Type Best Practices

1. **Match shot type to narrative purpose**: Wide shots orient, close-ups emote
2. **Progress through shots**: Use `shot_progression` patterns (wide → medium → close-up)
3. **Combine with camera movement**: Static close-ups for dialogue, tracking for action
4. **Genre consistency**: Horror avoids comfortable framing, comedy uses clear staging
5. **Composition notes matter**: Add rule of thirds, headroom guidance
6. **Screen direction**: Include facing/movement direction for continuity
