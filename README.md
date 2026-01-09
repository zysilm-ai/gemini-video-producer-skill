# Gemini Video Producer Skill

[![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://opencode.ai)
[![Google Labs](https://img.shields.io/badge/Google_Labs-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://labs.google)
[![MCP](https://img.shields.io/badge/MCP_Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://modelcontextprotocol.io)

A Claude Code / OpenCode skill for AI video production using **Google Whisk** via **MCP Playwright** browser automation. Creates any video type: promotional, educational, narrative, social media, animations, game trailers, music videos, and more.

## Example Output

> **Created with one prompt:** *"photorealistic battlefield, first person"*
>
> Generated a **24-second continuous shot** exceeding Whisk's 8-second limit. The skill automatically broke down 3 scenes, chained video segments with extracted keyframes for seamless continuity, and concatenated them into a single fluid output.

## Installation

```bash
/plugin marketplace add zysilm-ai/gemini-video-producer-skill
```

Or manually clone to `~/.claude/skills/` or `.claude/skills/`

## Quick Start

Simply describe what video you want:

```
You: Create a first-person battlefield experience

Claude: I'll help you create that video. Let me start by establishing
a Production Philosophy and breaking down the scenes...
```

Claude will:
- Auto-install MCP Playwright if missing
- Navigate to Whisk and check login status
- Guide you through the production workflow
- Generate assets, keyframes, and videos with your approval
- Concatenate final output

**Prerequisites:** Claude Code or OpenCode CLI, Google account with Whisk access (labs.google)

## Overview

This skill guides you through creating professional AI-generated videos with a structured, iterative workflow:

1. **Production Philosophy** - Define visual style, motion language, and narrative approach
2. **Scene Breakdown** - Decompose video into scenes with motion requirements
3. **Asset Definition** - Define characters, backgrounds, styles, and objects
4. **Pipeline Generation** - Create detailed prompts for all assets and scenes
5. **Asset Generation** - Create backgrounds and character references
6. **Keyframe Generation** - Generate the first keyframe to establish visual style
7. **Scene Execution** - Generate videos sequentially, extracting last frames for continuity
8. **Final Concatenation** - Combine all scene videos into single output

The philosophy-first approach ensures visual coherence across all scenes.

## Key Features

- **Cloud-Based** - No GPU required, uses Google Whisk
- **Reference Slots** - Upload character, scene, and style references for consistency
- **MCP Automation** - Claude directly controls browser via MCP Playwright
- **Self-Healing** - Adapts to UI changes through semantic understanding
- **Video-First Pipeline** - Perfect visual continuity between scenes
- **Zero Setup** - MCP Playwright auto-installs if missing, just log in to Google

## Whisk Reference Slots

Whisk uses three reference image slots that map to our asset types:

| Whisk Slot | German Label | Our Asset Type | Purpose |
|------------|--------------|----------------|---------|
| **Subject** | Motiv | Characters | Person/creature reference for identity |
| **Scene** | Szene | Backgrounds | Location/environment reference |
| **Style** | Stil | Styles | Visual treatment reference |

## Architecture

```
Claude reads pipeline.json
    |
Claude -> MCP Playwright -> Google Whisk (labs.google/fx/tools/whisk)
    |
Claude updates pipeline.json status
    |
Claude moves downloads to correct output paths
    |
Claude concatenates videos to output.mp4
```

**Benefits:**
- Self-healing: Claude adapts to UI changes by semantic understanding
- No brittle CSS selectors that break when Whisk updates
- Simpler codebase - no Python Playwright code to maintain
- Real-time adaptation to page state

## Supported Video Types

- **Promotional** - Product launches, brand stories, ads
- **Educational** - Tutorials, explainers, courses
- **Narrative** - Short films, animations, music videos
- **Social Media** - Platform-optimized content (TikTok, Reels, Shorts)
- **Corporate** - Demos, presentations, training
- **Game Trailers** - Action sequences, atmosphere, gameplay hints
- **Immersive** - First-person experiences, POV content

## Output Structure

```
output/{project-name}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration
├── assets.json                # Asset definitions
├── scene-breakdown.md         # Scene plan
├── pipeline.json              # Execution pipeline
├── output.mp4                 # FINAL CONCATENATED VIDEO
├── assets/
│   ├── characters/
│   ├── backgrounds/
│   ├── styles/
│   └── objects/
├── keyframes/
│   ├── scene-01-start.png    # Generated keyframe
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

## Directory Structure

```
gemini-video-producer-skill/
├── SKILL.md                   # Claude Code skill instructions
├── README.md                  # This file
├── references/
│   ├── prompt-engineering.md
│   ├── style-systems.md
│   └── troubleshooting.md
└── output/                    # Generated projects
    └── {project-name}/
        ├── pipeline.json
        ├── output.mp4
        └── ...
```

## Contributing

Contributions welcome! Areas for improvement:

- Additional video generation backends
- Audio generation integration
- Batch processing tools
- More video styles and templates

## License

MIT License - See LICENSE.txt

## Acknowledgments

- [Claude Code](https://claude.ai/code) - AI coding assistant
- [OpenCode](https://opencode.ai) - Open source AI coding agent
- [MCP Playwright](https://github.com/anthropics/mcp-playwright) - Browser automation via MCP
- [Google Whisk](https://labs.google/fx/tools/whisk) - AI image and video generation
