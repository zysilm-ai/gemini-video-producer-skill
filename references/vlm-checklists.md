# VLM Review Checklists (v4.0)

> **When to Read**: Phases 4-6 (Execution) - before reviewing generated assets, keyframes, and videos.

Use these checklists when using vision capabilities to review generated content.

---

## For Character Assets (Model Sheet / Turnaround)

After generating a character model sheet, verify:

- [ ] **Multiple views present**: Front, 3/4, side profile, and back views all visible
- [ ] **Consistent scale**: All views same size/proportion across the sheet
- [ ] **Neutral pose**: T-pose or A-pose (arms slightly away from body)
- [ ] **Neutral expression**: No emotion, relaxed face suitable for reference
- [ ] **Appearance matches description**: Hair, eyes, clothing, distinguishing features correct
- [ ] **Style matches production philosophy**: Art style consistent with genre preset
- [ ] **Clean background**: White or neutral gray, no distracting elements
- [ ] **Full body visible**: Head to feet in frame for all views
- [ ] **No artifacts**: No distortions, extra limbs, or generation errors

### Character Asset Regeneration Criteria

Regenerate if:
- Missing views (e.g., only front view, no turnaround)
- Views at inconsistent scales
- Action pose instead of neutral T-pose/A-pose
- Emotional expression instead of neutral
- Identity features don't match (wrong hair color, eye color, etc.)
- Distortions or artifacts present
- Style inconsistent with project
- Busy or distracting background

---

## For Object Assets (Prop Reference Sheet)

After generating a prop reference sheet, verify:

- [ ] **Multiple views present**: Front, side, and 3/4 perspective views visible
- [ ] **Scale reference included**: Human silhouette or measurement indicator present
- [ ] **Detail callouts**: Important features shown in close-up (if applicable)
- [ ] **Consistent lighting**: Same light direction across all views
- [ ] **Appearance matches description**: Materials, colors, details correct
- [ ] **Clean background**: White or neutral, no distracting elements
- [ ] **No artifacts**: No distortions or generation errors

### Object Asset Regeneration Criteria

Regenerate if:
- Missing views (single angle only)
- No scale reference
- Important details not visible
- Inconsistent lighting across views
- Object design doesn't match description
- Artifacts or distortions present

---

## For Keyframes (with Shot Type Verification)

After generating a scene keyframe, verify:

- [ ] **Shot type matches specification** (wide actually shows full environment, close-up fills frame appropriately)
- [ ] **Composition follows notes** (rule of thirds, headroom, lead room as specified)
- [ ] **Screen direction is correct** (subject facing/moving in specified direction)
- [ ] **Spatial setup is viable** (180-degree axis can be maintained from this position)
- [ ] Characters match their asset references (identity preserved)
- [ ] Character positions match prompt descriptions
- [ ] Background/environment matches philosophy
- [ ] Lighting is consistent with style.json and genre preset
- [ ] No text or watermarks in frame

### Shot Type Verification

| Shot Type | Check For |
|-----------|-----------|
| wide | Full environment visible, subject small in frame |
| medium | Waist-up framing, balanced subject/environment |
| close-up | Face/shoulders fill frame, minimal background |
| ECU | Single feature fills frame completely |
| POV | First-person perspective, hands at edges optional |
| OTS | Foreground shoulder visible, subject in 2/3 |
| two-shot | Both subjects visible, balanced composition |
| insert | Object fills frame, clean background |

### Keyframe Regeneration Criteria

Regenerate if:
- Shot type clearly wrong (e.g., "wide" but only showing head)
- Screen direction incorrect
- Character identity not preserved
- Composition prevents planned continuity

---

## For Videos (with Shot Type and Continuity Verification)

After generating a video segment, verify:

- [ ] **Shot type maintained throughout** (framing does not drift from specified type)
- [ ] **Camera movement matches specification** (push-in actually pushes in, pan direction correct)
- [ ] **Screen direction preserved** (subject does not flip orientation mid-segment)
- [ ] **Spatial relationships maintained** (characters do not teleport between frames)
- [ ] Motion matches prompt description
- [ ] Characters remain consistent throughout (no identity drift)
- [ ] No sudden jumps, flickers, or artifacts
- [ ] Environmental interactions look natural

### Camera Movement Verification

| Movement | Check For |
|----------|-----------|
| static | Camera holds steady, no drift |
| push-in | Camera moves toward subject |
| pull-out | Camera moves away from subject |
| pan-left/right | Camera rotates in specified direction |
| track-left/right | Camera moves bodily in direction |
| crane-up/down | Camera rises or descends |
| handheld | Organic movement feel |
| steadicam | Smooth floating movement |

### Video Regeneration Criteria

Regenerate if:
- Shot type drifts significantly during video
- Camera movement is wrong direction
- Screen direction flips mid-video
- Major artifacts or character inconsistency
- Motion doesn't match prompt

---

## For Scene Continuity (Cross-Scene Review)

Before concatenating scenes, review all keyframes and first frames together:

- [ ] **Screen direction consistent** between scenes (unless intentional change)
- [ ] **180-degree rule maintained** within dialogue/interaction scenes
- [ ] **Lighting direction consistent** across segments in same scene
- [ ] **Character positions logical** (no unexplained teleportation)
- [ ] **Props/objects maintain position** between segments
- [ ] **Transition type appropriate** for narrative beat

### Cross-Scene Review Process

1. Open all keyframes side by side
2. Verify screen direction matches continuity map
3. Check lighting direction consistency
4. Verify character positions are logical
5. Confirm transition types are appropriate

---

## Review Workflow

### Phase 4: Asset Review
```
For each asset:
1. Generate asset
2. Apply Character Asset checklist
3. If issues → regenerate
4. If good → mark completed, continue
```

### Phase 5: Keyframe Review
```
For each keyframe:
1. Generate keyframe
2. Apply Keyframe checklist
3. Verify shot type
4. If issues → regenerate
5. If good → mark completed, continue
```

### Phase 6: Video Review
```
For each video:
1. Generate video
2. Apply Video checklist
3. Verify camera movement
4. If issues → regenerate
5. If good → mark completed, continue
```

### Final: Continuity Review
```
Before concatenation:
1. Apply Cross-Scene checklist
2. Review all keyframes together
3. Address any continuity issues
4. Proceed to concatenation
```

---

## Informing User of Issues

When issues are found, report:
1. Which checklist item failed
2. What was expected vs. what was generated
3. Recommendation (regenerate, accept, or adjust prompt)

Example:
```
Issue: Shot type mismatch
- Expected: wide (full environment visible)
- Actual: medium (only showing upper body)
- Recommendation: Regenerate with stronger modifier
  "wide establishing shot, full environment, subject small in frame"
```
