# Flow Video Producer Skill

[![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://opencode.ai)
[![Google Flow](https://img.shields.io/badge/Google_Flow-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://labs.google/fx/flow)
[![MCP](https://img.shields.io/badge/MCP_Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://modelcontextprotocol.io)

A Claude Code / OpenCode skill for AI video production using **Google Flow** via **MCP Playwright** browser automation. Creates any video type: promotional, educational, narrative, social media, animations, game trailers, music videos, and more.

## Example Output

> **Created with one prompt:** *"interstellar battle, 1 minute with 30-second battle scene"*
>
> Generated a **64-second continuous video** far exceeding Flow's 8-second limit. The skill automatically broke down 3 scenes into 8 segments, used **Extend mode** for seamless motion continuity, and concatenated them into a single cinematic output.

## Installation

```bash
/plugin marketplace add zysilm-ai/flow-video-producer-skill
```

Or manually clone to `~/.claude/skills/` or `.claude/skills/`

## Quick Start

Simply describe what video you want:

```
You: Create an interstellar battle video, 1 minute long

Claude: I'll help you create that video. Let me start by establishing
a Production Philosophy and breaking down the scenes...
```

Claude will:
- Auto-install MCP Playwright if missing
- Navigate to Flow and check login status
- Guide you through the production workflow
- Generate references, keyframes, and videos with your approval
- Use **Extend mode** for seamless segment chaining
- Concatenate final output

**Prerequisites:** Claude Code or OpenCode CLI, Google account with Flow access (AI Pro or Ultra subscription)

## Key Features

| Feature | Description |
|---------|-------------|
| **Extend Mode** | Uses Flow's Extend feature for seamless segment chaining - preserves camera trajectory, motion vectors, and subject identity |
| **Reference Images** | Generates isolated subject references for visual consistency across all segments |
| **Sub-Agent Architecture** | Isolated agents for each generation task - no context pollution |
| **Cloud-Based** | No GPU required, uses Flow's Veo 3.1 Quality for video, Nano Banana Pro for images |
| **MCP Automation** | Claude directly controls browser via MCP Playwright |
| **Self-Healing** | Adapts to UI changes through semantic understanding |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN AGENT                              │
│  - Handles all user interaction and approvals                   │
│  - Creates philosophy.md, style.json, scene-breakdown.md        │
│  - Generates pipeline.json                                      │
│  - Orchestrates sub-agents via Task tool                        │
│  - Updates pipeline.json status after each sub-agent returns    │
│  - Runs video concatenation                                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Task tool spawns isolated agents
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│reference-gen  │   │keyframe-gen   │   │segment-gen    │
├───────────────┤   ├───────────────┤   ├───────────────┤
│ Subjects,     │   │ Scene start   │   │ Video clips   │
│ characters,   │   │ compositions  │   │ initial OR    │
│ objects,      │   │ (one per      │   │ extend mode   │
│ backgrounds   │   │ scene)        │   │ (8 sec each)  │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Benefits:**
- Each generation has isolated memory (no context pollution)
- Browser automation details don't clutter main conversation
- Parallel execution for independent tasks
- Easy retry of individual failed generations

## Workflow Phases

| Phase | Name | Description |
|-------|------|-------------|
| 0 | **Setup Check** | Verify MCP Playwright, navigate to Flow, check login |
| 1 | **Production Philosophy** | Create `philosophy.md` and `style.json` |
| 2 | **Scene Breakdown** | Create `scene-breakdown.md` with scenes and segments |
| 3 | **Pipeline Generation** | Create `pipeline.json` v4.0 with all prompts |
| 4 | **Reference Generation** | Generate subjects, characters, objects, backgrounds (parallel) |
| 5 | **Keyframe Generation** | Generate starting keyframe for each scene (parallel) |
| 6 | **Segment Execution** | Generate videos using initial + extend modes (sequential per scene) |
| 7 | **Final Concatenation** | Merge segments into scenes, scenes into output.mp4 |

## Continuity Architecture

**Problem:** AI video generation is stateless. Each generation starts fresh with no memory of camera trajectory, subject identity, or action continuity.

**Solution:** This skill uses multiple continuity techniques:

### 1. Extend-Based Segment Chaining
Instead of extracting frames, use Flow's **Extend** feature:
- Analyzes the **last second** (not just last frame) of previous clip
- Preserves motion vectors, camera direction, and subject identity
- Each extension adds ~8 seconds, chainable for long videos

### 2. Reference Images for Subject Consistency
Generate isolated "hero images" of key subjects:
- Used as **Ingredients** in Flow's video generation
- Maintains subject identity across all segments
- Clean backgrounds for easy visual parsing

### 3. Explicit Prompt Linking
Every continuation prompt references the previous state:
- Link phrases: "Continuing from the previous shot..."
- Anchor moments: "camera holds on the explosion for a beat"

## Segment Generation Modes

| Mode | When Used | Flow Feature | Benefit |
|------|-----------|--------------|---------|
| **initial** | First segment of each scene | Video aus Frames | Full control of starting composition |
| **extend** | All continuation segments | Extend | Perfect visual/motion continuity |

**Why Extend beats Frame Extraction:**

| Aspect | Frame Extraction | Extend Mode |
|--------|-----------------|-------------|
| Motion continuity | Often jarring | Seamless |
| Subject consistency | May drift | Preserved |
| Camera trajectory | Resets | Continues |
| Context analyzed | Single frame | Full 8 seconds |

## Pipeline Schema (v4.0)

```json
{
  "version": "4.0",
  "config": {
    "segment_duration": 8,
    "use_extend_mode": true,
    "use_references": true
  },
  "references": {
    "hero_ship": {
      "prompt": "Isolated silver battleship, clean background...",
      "output": "references/hero_ship.png",
      "status": "pending"
    }
  },
  "scenes": [
    {
      "id": "scene-01",
      "narrative_state": { "start": "...", "end": "..." },
      "first_keyframe": { "prompt": "...", "output": "...", "status": "pending" },
      "segments": [
        {
          "id": "seg-01-A",
          "mode": "initial",
          "motion_prompt": "...",
          "anchor_moment": "camera holds steady...",
          "status": "pending"
        },
        {
          "id": "seg-01-B",
          "mode": "extend",
          "link_phrase": "Continuing the forward momentum...",
          "motion_prompt": "...",
          "anchor_moment": "...",
          "status": "pending"
        }
      ]
    }
  ]
}
```

## Veo Motion Prompt Guidelines

Structure: **Cinematography + Subject + Action + Context + Style**

```
Slow dolly push forward through a massive fleet formation in deep space.
Sleek silver-blue warships with angular hulls drift majestically past camera,
their cyan engines pulsing with rhythmic blue light. Turrets on the nearest
destroyer slowly rotate into firing position. The ships hold perfect V-formation
against a backdrop of distant stars and colorful nebula. Tense pre-battle
atmosphere, epic cinematic scale, photorealistic sci-fi with dramatic rim lighting.
```

**Requirements:**
- 100-150 words per prompt
- ONE primary action per segment
- Specific camera language (dolly, tracking, pan, crane)
- End with anchor moment for clean extensions

## Output Structure

```
output/{project-name}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration
├── scene-breakdown.md         # Scene plan with segments
├── pipeline.json              # v4.0 execution pipeline
├── output.mp4                 # FINAL CONCATENATED VIDEO
├── references/                # All visual references
│   ├── hero_ship.png          # Subject reference (for Ingredients)
│   ├── enemy_vessel.png       # Subject reference
│   ├── characters/            # Character designs
│   ├── objects/               # Props and items
│   └── backgrounds/           # Environment images
├── keyframes/
│   ├── scene-01-start.png     # Scene starting compositions
│   ├── scene-02-start.png
│   └── scene-03-start.png
├── scene-01/
│   ├── seg-A.mp4              # Initial from keyframe
│   ├── seg-B.mp4              # Extended from seg-A
│   └── scene.mp4              # Concatenated scene
├── scene-02/
│   ├── seg-A.mp4
│   ├── seg-B.mp4
│   ├── seg-C.mp4
│   ├── seg-D.mp4
│   └── scene.mp4
└── scene-03/
    └── ...
```

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Segment Duration | 8 seconds per generation |
| Video Model | Veo 3.1 - Quality (100 credits/video) |
| Image Model | Nano Banana Pro |
| Video Resolution | Up to 1080p (4K with AI Ultra) |
| Image Resolution | Up to 1024x1024 |
| GPU Required | None (cloud-based) |
| Max Video Length | Unlimited (via segment chaining) |

## Supported Video Types

- **Promotional** - Product launches, brand stories, ads
- **Educational** - Tutorials, explainers, courses
- **Narrative** - Short films, animations, music videos
- **Social Media** - Platform-optimized content (TikTok, Reels, Shorts)
- **Corporate** - Demos, presentations, training
- **Game Trailers** - Action sequences, atmosphere, gameplay hints
- **Immersive** - First-person experiences, POV content
- **Sci-Fi/Action** - Space battles, explosions, dynamic sequences

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to Flow URL |
| `browser_snapshot` | Get page accessibility tree |
| `browser_click` | Click elements by ref |
| `browser_type` | Type prompts into inputs |
| `browser_file_upload` | Upload keyframes and references |
| `browser_wait_for` | Wait for generation completion |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Not logged in | Log in to Google at labs.google/fx/flow |
| Out of credits | Wait for reset or add credits at one.google.com/ai/credits |
| Generation stuck | Sub-agent will timeout and return error |
| Extend not available | Falls back to frame extraction mode |
| Wrong model selected | Sub-agents auto-configure Veo 3.1 Quality |
| Rate limited | Wait until quota resets (usually daily) |

## Directory Structure

```
flow-video-producer-skill/
├── skills/
│   └── gemini-video-producer/
│       └── SKILL.md           # Detailed skill instructions
├── .claude/
│   └── agents/                # Sub-agent definitions (3 agents)
│       ├── reference-generator.md   # Subjects, characters, objects, backgrounds
│       ├── keyframe-generator.md    # Scene starting compositions
│       └── segment-generator.md     # Video segments (initial + extend)
├── scripts/
│   └── merge_videos.py        # Video concatenation script
├── references/
│   ├── prompt-engineering.md
│   ├── style-systems.md
│   └── troubleshooting.md
├── README.md                  # This file
└── output/                    # Generated projects
```

## Contributing

Contributions welcome! Areas for improvement:

- Audio generation integration
- More sophisticated transitions between scenes
- Batch processing tools
- Additional video styles and templates
- Alternative video generation backends

## License

MIT License - See LICENSE.txt

## Acknowledgments

- [Claude Code](https://claude.ai/code) - AI coding assistant
- [OpenCode](https://opencode.ai) - Open source AI coding agent
- [MCP Playwright](https://github.com/anthropics/mcp-playwright) - Browser automation via MCP
- [Google Flow](https://labs.google/fx/flow) - AI video/image generation with Veo 3.1
