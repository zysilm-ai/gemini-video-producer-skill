# Flow Video Producer Skill

[![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://opencode.ai)
[![Google Flow](https://img.shields.io/badge/Google_Flow-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://labs.google/fx/flow)
[![MCP](https://img.shields.io/badge/MCP_Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://modelcontextprotocol.io)

A Claude Code / OpenCode skill for AI video production using **Google Flow** via **MCP Playwright** browser automation. Creates any video type: promotional, educational, narrative, social media, animations, game trailers, music videos, and more.

## Example Output

> **Created with one prompt:** *"interstellar battle, 1 minute with 30-second battle scene"*
>
> Generated a **64-second continuous video** far exceeding Flow's 8-second limit. The skill automatically broke down 3 scenes into 8 segments, used **keyframe-driven Video aus Frames** for precise visual control, and concatenated them into a single cinematic output.

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
- Use **Video aus Frames** with start/end keyframes for seamless continuity
- Concatenate final output

**Prerequisites:** Claude Code or OpenCode CLI, Google account with Flow access (AI Pro or Ultra subscription)

## Key Features

| Feature | Description |
|---------|-------------|
| **Keyframe-Driven** | Every segment uses explicit start/end keyframes for precise visual control |
| **Video aus Frames** | Unified approach where Flow interpolates between keyframe images |
| **Reference Images** | Generates subject references for consistent keyframe generation |
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
│ Subjects,     │   │ Start & end   │   │ Video clips   │
│ characters,   │   │ keyframes for │   │ via Video aus │
│ objects,      │   │ each segment  │   │ Frames mode   │
│ backgrounds   │   │ (1-2 per seg) │   │ (8 sec each)  │
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
| 3 | **Pipeline Generation** | Create `pipeline.json` v7.0 with keyframe + motion prompts |
| 4 | **Reference Generation** | Generate subjects, characters, objects, backgrounds (parallel) |
| 5 | **Keyframe Generation** | Generate start/end keyframes for each segment |
| 6 | **Segment Execution** | Generate videos via Video aus Frames with keyframes |
| 7 | **Final Concatenation** | Merge segments into scenes, scenes into output.mp4 |

## Continuity Architecture

**Problem:** AI video generation is stateless. Each generation starts fresh with no memory of camera trajectory, subject identity, or action continuity.

**Solution:** Unified keyframe-driven approach with explicit visual control.

### Keyframe-Driven Video Generation

Every segment is generated by interpolating between two keyframe images:

```
Segment A: [start-A] ──Video aus Frames──> [end-A]
Segment B: [end-A]   ──Video aus Frames──> [end-B]  (reuses A's end)
Segment C: [end-B]   ──Video aus Frames──> [end-C]  (reuses B's end)
```

**Benefits:**
- **Explicit visual anchors** - No ambiguity about what each segment shows
- **Perfect continuity** - End keyframe of segment N = start keyframe of segment N+1
- **Subject consistency** - Same visual elements appear in connected keyframes
- **Predictable results** - Flow interpolates between your defined compositions

### Reference Images for Style Consistency

Generate isolated "hero images" of key subjects:
- Used as **style guides** when generating keyframes
- Maintains subject identity across all segments
- Clean backgrounds for easy visual reference

## Segment Types

| Type | Start Keyframe | End Keyframe | When Used |
|------|----------------|--------------|-----------|
| **initial** | Generate new | Generate new | First segment of each scene |
| **extend** | Use previous end | Generate new | All continuation segments |

All segments use the same **Video aus Frames** mode in Flow - the only difference is where the start keyframe comes from.

## Pipeline Schema (v7.0)

```json
{
  "version": "7.0",
  "config": {
    "segment_duration": 8,
    "use_keyframe_mode": true,
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
      "segments": [
        {
          "id": "seg-01-A",
          "type": "initial",
          "start_keyframe": {
            "prompt": "Wide shot of fleet...",
            "output": "scene-01/keyframes/seg-A-start.png",
            "status": "pending"
          },
          "end_keyframe": {
            "prompt": "Medium shot approaching flagship...",
            "output": "scene-01/keyframes/seg-A-end.png",
            "status": "pending"
          },
          "motion_prompt": "Slow dolly push forward...",
          "status": "pending"
        },
        {
          "id": "seg-01-B",
          "type": "extend",
          "start_keyframe_source": "seg-01-A.end_keyframe",
          "end_keyframe": {
            "prompt": "Close-up of flagship shields...",
            "output": "scene-01/keyframes/seg-B-end.png",
            "status": "pending"
          },
          "motion_prompt": "Camera continues forward...",
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
- Focus on MOTION between keyframes (don't redescribe static elements)

## Output Structure

```
output/{project-name}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration
├── scene-breakdown.md         # Scene plan with segments
├── pipeline.json              # v7.0 execution pipeline
├── output.mp4                 # FINAL CONCATENATED VIDEO
├── references/                # Style reference images
│   ├── hero_ship.png          # Subject reference
│   ├── enemy_vessel.png       # Subject reference
│   └── backgrounds/           # Environment images
├── scene-01/
│   ├── keyframes/
│   │   ├── seg-A-start.png    # Segment A opening
│   │   ├── seg-A-end.png      # Segment A closing (= B start)
│   │   └── seg-B-end.png      # Segment B closing
│   ├── seg-A.mp4              # Video aus Frames output
│   ├── seg-B.mp4              # Video aus Frames output
│   └── scene.mp4              # Concatenated scene
├── scene-02/
│   ├── keyframes/
│   │   └── ...
│   └── ...
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
| `browser_file_upload` | Upload keyframes |
| `browser_wait_for` | Wait for generation completion |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Not logged in | Log in to Google at labs.google/fx/flow |
| Out of credits | Wait for reset or add credits at one.google.com/ai/credits |
| Generation stuck | Sub-agent will timeout and return error |
| Keyframe missing | Check keyframe generation status in pipeline.json |
| Wrong model selected | Sub-agents auto-configure Veo 3.1 Quality |
| Rate limited | Wait until quota resets (usually daily) |

## Directory Structure

```
flow-video-producer-skill/
├── skills/
│   └── gemini-video-producer/
│       ├── SKILL.md                 # Main skill (~175 lines)
│       └── reference/               # Progressive disclosure
│           ├── pipeline-schema.md   # Pipeline.json v7.0 schema
│           ├── veo-prompts.md       # Veo + keyframe prompt guidelines
│           └── templates.md         # File templates
├── .claude/
│   └── agents/                      # Sub-agent definitions
│       ├── reference-generator.md   # Images (subjects, characters, backgrounds)
│       ├── keyframe-generator.md    # Start/end keyframes for segments
│       └── segment-generator.md     # Video segments via Video aus Frames
├── scripts/
│   └── merge_videos.py              # Video concatenation
├── README.md                        # This file
└── output/                          # Generated projects
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
