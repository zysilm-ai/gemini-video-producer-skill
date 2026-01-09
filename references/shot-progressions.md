# Shot Progression Patterns (v4.0)

> **When to Read**: Phase 2 (Scene Breakdown) - when planning shot sequences within scenes.

Predefined patterns for shot type sequencing within a scene. Use these to guide the `shot_progression` field in pipeline.json.

---

## ESTABLISHING-TO-INTIMATE

```
wide → medium → close-up → (optional) extreme-close-up
```

- **Use**: Scene openings, building emotional connection, introducing characters/locations
- **Example**: City skyline → apartment building → character at window → character's face
- **Pacing**: Gradual, allows audience to orient then connect
- **Best For**: Drama, character introductions, emotional build-up

---

## ACTION-SEQUENCE

```
wide (geography) → medium (action) → close-up (impact) → wide (result)
```

- **Use**: Fight scenes, chase sequences, physical conflict, sports
- **Example**: Battlefield overview → soldier running → explosion impact → aftermath
- **Pacing**: Rhythmic, oriented around impact moments
- **Best For**: Action, thriller, sports, martial arts

---

## DIALOGUE-COVERAGE

```
establishing two-shot → OTS (A to B) → OTS (B to A) → reaction close-ups
```

- **Use**: Conversations, confrontations, interviews
- **Example**: Two characters at table → over A's shoulder → over B's shoulder → A reacts
- **Pacing**: Conversational, cuts on dialogue beats
- **Best For**: Drama, comedy, documentary interviews

---

## REVEAL

```
ECU/insert (mystery) → pull-out to medium → wide (context)
```

- **Use**: Surprises, plot reveals, horror moments, discoveries
- **Example**: Bloody knife → hand holding knife → person standing over body
- **Pacing**: Builds anticipation then releases
- **Best For**: Horror, thriller, mystery, plot twists

---

## Shot Progression Selection Guide

| Scene Purpose | Recommended Pattern |
|--------------|---------------------|
| Scene opening | `establishing-to-intimate` |
| Action/fight | `action-sequence` |
| Conversation | `dialogue-coverage` |
| Plot twist | `reveal` |
| Emotional climax | `establishing-to-intimate` (ending on ECU) |
| Chase scene | `action-sequence` (repeated) |
| Horror reveal | `reveal` |
| Character introduction | `establishing-to-intimate` |
| Interview segment | `dialogue-coverage` |

---

## Combining Patterns

For longer scenes, patterns can be combined:

**Example - Horror Chase Scene:**
1. `reveal` - Discovery of threat (ECU → medium → wide)
2. `action-sequence` - Chase begins (wide → medium → close-up → wide)
3. `establishing-to-intimate` - Hiding (wide → medium → ECU of fear)

**Example - Dramatic Conversation:**
1. `establishing-to-intimate` - Scene setup
2. `dialogue-coverage` - Main conversation
3. `reveal` - Surprising information revealed
