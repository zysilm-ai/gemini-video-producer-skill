# AI Video Producer Skill

[![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://opencode.ai)
[![Gemini](https://img.shields.io/badge/Google_Gemini-886FBF?style=for-the-badge&logo=googlegemini&logoColor=white)](https://gemini.google.com)
[![MCP](https://img.shields.io/badge/MCP_Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://modelcontextprotocol.io)

A Claude Code / OpenCode skill for AI video production using **Gemini** via **MCP Playwright** browser automation. Creates any video type: promotional, educational, narrative, social media, animations, game trailers, music videos, and more.

## Example

https://github.com/zysilm-ai/gemini-video-producer-skill/raw/main/doc/example.mp4

> **Created with one prompt:** *"photorealistic battlefield, first person"*
>
> This **24-second continuous shot** exceeds Gemini's 8-second limit per generation. The skill automatically breaks down scenes, chains video segments with extracted keyframes for seamless continuity, and concatenates them into a single fluid output.

## Overview

This skill guides you through creating professional AI-generated videos with a structured, iterative workflow:

1. **Production Philosophy** - Define visual style, motion language, and narrative approach
2. **Scene Breakdown** - Decompose video into scenes with motion requirements
3. **Pipeline Generation** - Create detailed prompts for all assets and scenes
4. **Asset Generation** - Create backgrounds and character references
5. **Keyframe Generation** - Generate the first keyframe to establish visual style
6. **Scene Execution** - Generate videos sequentially, extracting last frames for continuity
7. **Final Concatenation** - Combine all scene videos into single output

The philosophy-first approach ensures visual coherence across all scenes.

## Key Features

- **Cloud-Based** - No GPU required, uses Gemini's Veo 3.1 Fast
- **MCP Automation** - Claude directly controls browser via MCP Playwright
- **Self-Healing** - Adapts to UI changes through semantic understanding
- **Video-First Pipeline** - Perfect visual continuity between scenes
- **Simple Setup** - Just install MCP server and log in to Google

## Prerequisites

**Required:**
- Claude Code or OpenCode CLI
- MCP Playwright server
- Google account with Gemini access
- Internet connection

**Optional:**
- Python with OpenCV (for frame extraction fallback)
- ffmpeg (for video concatenation)

## Quick Start

### 1. Install MCP Playwright Server

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

### 2. Start Creating Videos

Simply describe what video you want:

```
You: Create a 15-second first-person battlefield experience

Claude: I'll help you create that video. Let me start by establishing
a Production Philosophy and breaking down the scenes...
```

Claude will:
- Navigate to Gemini and check login status
- Guide you through the production workflow
- Generate assets, keyframes, and videos with your approval
- Concatenate final output

## Architecture

```
Claude reads pipeline.json
    |
Claude -> MCP Playwright -> Gemini Web Interface
    |
Claude updates pipeline.json status
    |
Claude moves downloads to correct output paths
    |
Claude concatenates videos to output.mp4
```

**Benefits:**
- Self-healing: Claude adapts to UI changes by semantic understanding
- No brittle CSS selectors that break when Gemini updates
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

## Pipeline Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **Video-First** (Recommended) | Generate first keyframe only, then videos sequentially. Last frame of each video becomes next scene's start. | Visual continuity between scenes |
| **Keyframe-First** | Generate all keyframes independently, then videos between them. | Precise control over end poses |

## Output Structure

```
output/{project-name}/
├── philosophy.md              # Production philosophy
├── style.json                 # Style configuration
├── scene-breakdown.md         # Scene plan
├── pipeline.json              # Execution pipeline
├── output.mp4                 # FINAL CONCATENATED VIDEO
├── assets/
│   ├── characters/
│   └── backgrounds/
├── keyframes/
│   ├── KF-A.png              # First keyframe (generated)
│   ├── KF-B.png              # Extracted from scene-01
│   └── KF-C.png              # Extracted from scene-02
├── scene-01/
│   └── video.mp4
├── scene-02/
│   └── video.mp4
└── scene-03/
    └── video.mp4
```

## Technical Specs

| Parameter | Value |
|-----------|-------|
| Video Duration | 5-8 seconds per generation |
| Image Resolution | Up to 1024x1024 |
| Video Resolution | Up to 1080p |
| Rate Limiting | ~3 videos per day (Gemini free tier) |
| GPU Required | None (cloud-based) |

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_snapshot` | Get page accessibility tree |
| `browser_click` | Click element by ref |
| `browser_type` | Type text into input |
| `browser_file_upload` | Upload keyframes |
| `browser_wait_for` | Wait for generation |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cookie consent page | Click "Accept all" button |
| Not logged in | Log in to Google manually in browser |
| Generation stuck | Wait longer, check snapshot for progress |
| Download not working | Try clicking download button again |
| Element ref not found | Take new snapshot, refs change on page update |
| Rate limited | Wait until quota resets (usually daily) |

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
- [Google Gemini](https://gemini.google.com) - Video generation (Veo 3.1)
