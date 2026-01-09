# Reference Files Index

This directory contains reference documentation for the Gemini Video Producer Skill v4.0.

---

## When to Read Each File

| Phase | File | Purpose |
|-------|------|---------|
| **Phase 1** | `genre-presets.md` | Select genre for project |
| **Phase 1** | `templates/philosophy.md` | Create philosophy.md and style.json |
| **Phase 2** | `shot-types.md` | Plan shot types for scenes |
| **Phase 2** | `shot-progressions.md` | Plan shot sequences |
| **Phase 2** | `camera-movements.md` | Plan camera movements |
| **Phase 2** | `continuity-rules.md` | Plan continuity |
| **Phase 2** | `templates/scene-breakdown.md` | Create scene-breakdown.md |
| **Phase 2.5** | `asset-prompts.md` | Write professional asset prompts |
| **Phase 3** | `pipeline-schema.md` | Create pipeline.json |
| **Phases 4-6** | `vlm-checklists.md` | Review generated content |
| **Troubleshooting** | `troubleshooting.md` | Resolve issues |
| **Prompts** | `prompt-engineering.md` | Write effective prompts |
| **Style** | `style-systems.md` | Configure visual styles |

---

## File Descriptions

### Core References

| File | Lines | Description |
|------|-------|-------------|
| `shot-types.md` | ~120 | 8 professional shot type definitions with Whisk modifiers |
| `shot-progressions.md` | ~80 | 4 shot progression patterns for scene sequencing |
| `camera-movements.md` | ~100 | 11 camera movement types with genre guidance |
| `genre-presets.md` | ~220 | 6 genre presets with full configuration JSON |
| `continuity-rules.md` | ~150 | 180-degree rule, screen direction, continuity checklist |
| `asset-prompts.md` | ~350 | Professional asset prompt writing (model sheets, prop sheets, environments, styles) |
| `pipeline-schema.md` | ~200 | v4.0 schema definition with examples |
| `vlm-checklists.md` | ~150 | Review checklists for assets, keyframes, videos |

### Templates

| File | Description |
|------|-------------|
| `templates/philosophy.md` | Templates for philosophy.md and style.json |
| `templates/scene-breakdown.md` | Template for scene-breakdown.md |

### Sub-Agent Instructions

| File | Description |
|------|-------------|
| `subagents/asset-generation.md` | Complete MCP workflow for asset generation sub-agents |
| `subagents/video-generation.md` | Complete MCP workflow for video generation sub-agents |

**Why sub-agents?** Each generation task runs in a fresh context, preventing memory bloat and enabling parallel execution. See main README for architecture details.

### Existing References

| File | Description |
|------|-------------|
| `prompt-engineering.md` | Motion prompts, shot type modifiers |
| `style-systems.md` | Visual style configuration |
| `troubleshooting.md` | Common issues and solutions |

---

## Quick Reference

### Shot Types
`wide` | `medium` | `close-up` | `extreme-close-up` | `pov` | `over-shoulder` | `two-shot` | `insert`

### Shot Progressions
`establishing-to-intimate` | `action-sequence` | `dialogue-coverage` | `reveal`

### Camera Movements
`static` | `push-in` | `pull-out` | `pan-left` | `pan-right` | `track-left` | `track-right` | `crane-up` | `crane-down` | `handheld` | `steadicam`

### Genre Presets
`action` | `horror` | `comedy` | `drama` | `anime` | `documentary`

### Screen Direction
`left-to-right` | `right-to-left` | `neutral`

### 180-Degree Rule
`established` | `crossing-allowed` | `not-applicable`

---

## Usage Pattern

At each workflow phase, read the relevant reference files:

```
Phase 1: Production Philosophy
├── Read: genre-presets.md (select genre)
└── Read: templates/philosophy.md (create files)

Phase 2: Scene Breakdown
├── Read: shot-types.md (plan shots)
├── Read: shot-progressions.md (plan sequences)
├── Read: camera-movements.md (plan camera)
├── Read: continuity-rules.md (plan continuity)
└── Read: templates/scene-breakdown.md (create file)

Phase 3: Pipeline Generation
└── Read: pipeline-schema.md (create pipeline.json)

Phases 4-6: Execution
└── Read: vlm-checklists.md (review content)
```
