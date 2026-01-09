# Gemini Video Producer Skill

[![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://opencode.ai)
[![Google Labs](https://img.shields.io/badge/Google_Labs-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://labs.google)
[![MCP](https://img.shields.io/badge/MCP_Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/v4.0-Academic_Film_Standards-blueviolet?style=for-the-badge)](SKILL.md)

A Claude Code / OpenCode skill for **professional AI video production** using **Google Whisk** via **MCP Playwright** browser automation. Now with **academic film production standards**: professional shot types, genre presets, and continuity rules.

## What's New in v4.0

- **8 Professional Shot Types**: wide, medium, close-up, extreme close-up, POV, over-shoulder, two-shot, insert
- **6 Genre Presets**: Action, Horror, Comedy, Drama, Anime, Documentary
- **Shot Progression Patterns**: establishing-to-intimate, action-sequence, dialogue-coverage, reveal
- **Continuity Rules**: 180-degree rule, screen direction, spatial consistency
- **11 Camera Movements**: static, push-in, pull-out, pan, track, crane, handheld, steadicam

## Example Output

> **Created with one prompt:** *"photorealistic battlefield, first person"*
>
> Generated a **24-second continuous shot** exceeding Whisk's 8-second limit. The skill automatically broke down scenes with proper **shot types** (POV throughout), **camera movements** (handheld), and **action-sequence progression**, then concatenated them into a single fluid output.

## Quick Start

Simply describe what video you want:

```
You: Create a horror short film with a jump scare reveal

Claude: I'll help you create that video using the horror genre preset.
Let me start by establishing a Production Philosophy with:
- Cold, desaturated visual style
- Reveal shot progression (ECU mystery -> wide context)
- Push-in camera movements for building dread
- Proper continuity for spatial consistency...
```

Claude will:
- Auto-install MCP Playwright if missing
- Navigate to Whisk and check login status
- Apply genre-appropriate shot types and camera movements
- Guide you through the production workflow with continuity checks
- Generate assets, keyframes, and videos with your approval
- Concatenate final output

**Prerequisites:** Claude Code or OpenCode CLI, Google account with Whisk access (labs.google)

## Overview

This skill guides you through creating professional AI-generated videos with a structured, iterative workflow based on **academic film production standards**:

1. **Production Philosophy** - Define visual style, motion language, and narrative approach
2. **Scene Breakdown** - Decompose video into scenes with **shot types**, **camera movements**, and **continuity notes**
3. **Asset Definition** - Define characters, backgrounds, styles, and objects
4. **Pipeline Generation** - Create detailed prompts with shot type modifiers and genre styling
5. **Asset Generation** - Create backgrounds and character references
6. **Keyframe Generation** - Generate starting keyframes with proper shot composition
7. **Scene Execution** - Generate videos with continuity verification
8. **Final Concatenation** - Combine all scene videos with appropriate transitions

The philosophy-first approach ensures visual coherence across all scenes.

## Key Features

- **Professional Film Grammar** - Shot types, progressions, and continuity rules from academic research
- **Genre Presets** - Pre-configured visual styles for Action, Horror, Comedy, Drama, Anime, Documentary
- **Sub-Agent Architecture** - Efficient context management with parallel asset generation
- **Cloud-Based** - No GPU required, uses Google Whisk
- **Reference Slots** - Upload character, scene, and style references for consistency
- **MCP Automation** - Claude directly controls browser via MCP Playwright
- **Self-Healing** - Adapts to UI changes through semantic understanding
- **Continuity Checking** - 180-degree rule, screen direction, spatial consistency
- **Zero Setup** - MCP Playwright auto-installs if missing, just log in to Google

## Sub-Agent Architecture (Context Management)

This skill uses a **sub-agent pattern** for efficient memory management - a key innovation for long-running AI workflows.

### The Problem

Traditional single-agent workflows suffer from:
- **Context bloat**: Memory fills with irrelevant generation history
- **Token waste**: Previous asset prompts not needed for current generation
- **Reliability issues**: Large contexts cause errors and confusion
- **No parallelization**: Sequential execution only

### The Solution

```
┌─────────────────────────────────────────────────────────────────┐
│  MAIN AGENT (Phases 0-3)                                        │
│  • Understands user intent                                      │
│  • Creates philosophy, scene breakdown, pipeline.json           │
│  • Orchestrates sub-agents                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Asset Sub-  │      │ Asset Sub-  │      │ Asset Sub-  │  PARALLEL
│ Agent #1    │      │ Agent #2    │      │ Agent #N    │  EXECUTION
│ (character) │      │ (background)│      │ (style)     │
└─────────────┘      └─────────────┘      └─────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  VIDEO SUB-AGENTS (Sequential per scene)                        │
│                                                                 │
│  Scene 1: [seg-A] ──► [seg-B] ──► [seg-C]                      │
│  Scene 2: [seg-A] ──► [seg-B]                                  │
│                                                                 │
│  Each sub-agent: fresh memory, complete instructions, VLM review│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  MAIN AGENT (Phase 7)                                           │
│  • Concatenates all videos                                      │
│  • Produces final output.mp4                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Benefits

| Feature | Benefit |
|---------|---------|
| **Fresh memory per task** | No context pollution between generations |
| **Parallel asset generation** | Generate all assets simultaneously |
| **Fault isolation** | One failure doesn't affect others |
| **Auto-retry** | Sub-agents retry up to 2x on failure |
| **VLM review in sub-agent** | Keyframe quality check before animation |
| **Stateless instructions** | Self-contained, reproducible tasks |

### Sub-Agent Files

```
references/subagents/
├── asset-generation.md    # Complete instructions for asset sub-agents
└── video-generation.md    # Complete instructions for video sub-agents
```

Each sub-agent receives:
- Specific task parameters (prompts, paths)
- Complete MCP workflow instructions
- VLM review checklist (for video sub-agents)
- Auto-retry logic

## Shot Types

| Shot Type | Use Case | Whisk Modifier |
|-----------|----------|----------------|
| **wide** | Establishing geography, scale | "wide establishing shot, full environment" |
| **medium** | Dialogue, character actions | "medium shot, waist-up framing" |
| **close-up** | Emotion, reactions | "close-up shot, face filling frame" |
| **extreme-close-up** | Intensity, detail | "extreme close-up on [feature]" |
| **pov** | Immersion, subjective | "first-person POV" |
| **over-shoulder** | Dialogue, spatial relationship | "over-the-shoulder shot" |
| **two-shot** | Relationships, comedy | "two-shot framing" |
| **insert** | Props, details | "insert shot of [object]" |

## Genre Presets

| Genre | Visual Style | Preferred Shots | Camera |
|-------|-------------|-----------------|--------|
| **Action** | High contrast, gritty | wide, medium, close-up impact | track, handheld |
| **Horror** | Cold, desaturated, shadows | medium, close-up, POV | push-in, static |
| **Comedy** | Warm, bright, clear | medium, two-shot, wide | static, motivated |
| **Drama** | Naturalistic, filmic | medium, close-up, OTS | push-in, steadicam |
| **Anime** | Vibrant, cel-shaded | all types, ECU eyes | push-in, pull-out |
| **Documentary** | Naturalistic, authentic | medium, wide, OTS | static, handheld |

## Shot Progression Patterns

| Pattern | Sequence | Best For |
|---------|----------|----------|
| **establishing-to-intimate** | wide -> medium -> close-up | Scene openings, emotional build |
| **action-sequence** | wide -> medium -> close-up -> wide | Fights, chases |
| **dialogue-coverage** | two-shot -> OTS A -> OTS B -> close-ups | Conversations |
| **reveal** | ECU -> medium -> wide | Surprises, plot twists |

## Whisk Reference Slots

Whisk uses three reference image slots that map to our asset types:

| Whisk Slot | German Label | Our Asset Type | Purpose |
|------------|--------------|----------------|---------|
| **Subject** | Motiv | Characters | Person/creature reference for identity |
| **Scene** | Szene | Backgrounds | Location/environment reference |
| **Style** | Stil | Styles | Visual treatment reference |

## How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        SKILL.md (~360 lines)                    │
│                     Core workflow instructions                   │
│                                                                 │
│  Phase 1 ──► Read: references/genre-presets.md                  │
│              Read: references/templates/philosophy.md           │
│                                                                 │
│  Phase 2 ──► Read: references/shot-types.md                     │
│              Read: references/shot-progressions.md              │
│              Read: references/camera-movements.md               │
│              Read: references/continuity-rules.md               │
│                                                                 │
│  Phase 3 ──► Read: references/pipeline-schema.md                │
│                                                                 │
│  Phase 4-6 ► Read: references/vlm-checklists.md                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Playwright Browser                        │
│                                                                 │
│  Claude ──► browser_navigate ──► Google Whisk                   │
│         ──► browser_snapshot ──► Page state                     │
│         ──► browser_click    ──► UI interaction                 │
│         ──► browser_type     ──► Prompt input                   │
│         ──► browser_upload   ──► Reference images               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      pipeline.json (v4.0)                        │
│                                                                 │
│  • genre_preset: action/horror/comedy/drama/anime/documentary   │
│  • shot_progression: establishing-to-intimate/action-sequence   │
│  • continuity: screen_direction, axis_of_action                 │
│  • segments[].shot_type + camera_movement                       │
└─────────────────────────────────────────────────────────────────┘
```

### Modular Reference Loading

The skill uses a **modular architecture** to optimize LLM context and attention:

1. **Core Instructions** (`SKILL.md` ~360 lines) - Always loaded, contains workflow phases
2. **Reference Files** (loaded on-demand) - Detailed documentation loaded only when needed

**Why this approach?**
- **Better LLM focus**: Smaller context = better attention on current task
- **On-demand loading**: Reference data loaded only at relevant phases
- **Maintainability**: Each reference file can be updated independently
- **Token efficiency**: ~78% reduction in base context size

### Workflow Execution

```
User Request
    │
    ▼
Phase 0: Setup Check
    │ Navigate to Whisk, verify login
    ▼
Phase 1: Production Philosophy
    │ Read: genre-presets.md, templates/philosophy.md
    │ Create: philosophy.md, style.json
    ▼
Phase 2: Scene Breakdown
    │ Read: shot-types.md, shot-progressions.md,
    │       camera-movements.md, continuity-rules.md
    │ Create: scene-breakdown.md
    ▼
Phase 3: Pipeline Generation
    │ Read: pipeline-schema.md
    │ Create: pipeline.json (v4.0)
    ▼
Phase 4-6: MCP Execution
    │ Read: vlm-checklists.md
    │ Generate: assets → keyframes → videos
    │ Verify: shot types, continuity via VLM
    ▼
Phase 7: Final Concatenation
    │ ffmpeg: segments → scenes → output.mp4
    ▼
Final Output
```

### Self-Healing Browser Automation

Claude uses **semantic understanding** rather than brittle CSS selectors:

```
❌ Old approach: document.querySelector('.btn-primary-xyz')
✅ MCP approach: browser_click(element="Generate button", ref="<snapshot_ref>")
```

**Benefits:**
- Adapts to UI changes automatically
- No code maintenance when Whisk updates
- Works across different languages (German UI labels supported)

## Supported Video Types

- **Promotional** - Product launches, brand stories, ads
- **Educational** - Tutorials, explainers, courses
- **Narrative** - Short films, animations, music videos
- **Social Media** - Platform-optimized content (TikTok, Reels, Shorts)
- **Corporate** - Demos, presentations, training
- **Game Trailers** - Action sequences, atmosphere, gameplay hints
- **Immersive** - First-person experiences, POV content
- **Horror** - Tension building, jump scares, atmospheric dread
- **Comedy** - Timing-based humor, reaction shots
- **Anime** - Stylized animation, expressive characters

## Output Structure

```
output/{project-name}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration + genre preset
├── assets.json                # Asset definitions
├── scene-breakdown.md         # Scene plan with shot types + continuity
├── pipeline.json              # v4.0 execution pipeline
├── output.mp4                 # FINAL CONCATENATED VIDEO
├── assets/
│   ├── characters/
│   ├── backgrounds/
│   ├── styles/
│   └── objects/
├── keyframes/
│   ├── scene-01-start.png    # Generated keyframe (with shot type)
│   └── scene-02-start.png    # Generated keyframe
├── scene-01/
│   ├── seg-A.mp4
│   └── scene.mp4
├── scene-02/
│   └── seg-A.mp4
└── ...
```

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Video Duration | 5-8 seconds per generation |
| Image Resolution | Up to 1024x1024 |
| Video Resolution | Up to 1080p |
| Reference Slots | 3 (Subject, Scene, Style) |
| GPU Required | None (cloud-based) |
| Shot Types | 8 professional types |
| Genre Presets | 6 (Action, Horror, Comedy, Drama, Anime, Documentary) |
| Camera Movements | 11 types |

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_snapshot` | Get page accessibility tree |
| `browser_click` | Click element by ref |
| `browser_type` | Type text into input |
| `browser_file_upload` | Upload references |
| `browser_wait_for` | Wait for generation |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cookie consent page | Click "Ausblenden" (Hide) button |
| Not logged in | Log in to Google manually in browser |
| On landing page | Click "Tool aufrufen" to enter workspace |
| Generation stuck | Wait longer, check snapshot for progress |
| Download not working | Try right-clicking image |
| Element ref not found | Take new snapshot, refs change on page update |
| Shot type mismatch | Add stronger shot type modifiers to prompt |
| Screen direction flip | Check continuity notes, use neutral shots to reset |

## Directory Structure

```
gemini-video-producer-skill/
├── skill.md                   # Core skill instructions
├── README.md                  # This file
├── assets/
│   └── example-style.json     # Style template with genre preset
├── references/
│   ├── README.md              # Reference file index
│   ├── shot-types.md          # 8 professional shot type definitions
│   ├── shot-progressions.md   # 4 shot progression patterns
│   ├── camera-movements.md    # 11 camera movement types
│   ├── genre-presets.md       # 6 genre preset configurations
│   ├── continuity-rules.md    # 180° rule, screen direction
│   ├── vlm-checklists.md      # Review checklists for VLM
│   ├── pipeline-schema.md     # v4.0 pipeline schema definition
│   ├── asset-prompts.md       # Professional asset prompt writing
│   ├── prompt-engineering.md  # Prompt writing guidance
│   ├── style-systems.md       # Visual style configuration
│   ├── troubleshooting.md     # Detailed troubleshooting
│   ├── subagents/             # Sub-agent instruction files
│   │   ├── asset-generation.md    # Asset generation sub-agent
│   │   └── video-generation.md    # Video generation sub-agent
│   └── templates/
│       ├── philosophy.md      # philosophy.md + style.json templates
│       └── scene-breakdown.md # scene-breakdown.md template
└── output/                    # Generated projects
    └── zelda-botw-story/      # Example project
```

## Contributing

Contributions welcome! Areas for improvement:

- Additional genre presets (Western, Musical, Noir, etc.)
- Advanced shot patterns (coverage planning, reaction shots)
- Audio generation integration
- Batch processing tools
- More video styles and templates

## License

MIT License - See LICENSE

## Acknowledgments

### Tools & Platforms
- [Claude Code](https://claude.ai/code) - AI coding assistant
- [OpenCode](https://opencode.ai) - Open source AI coding agent
- [MCP Playwright](https://github.com/microsoft/playwright-mcp) - Browser automation via Model Context Protocol
- [Google Whisk](https://labs.google/fx/tools/whisk) - AI image and video generation
