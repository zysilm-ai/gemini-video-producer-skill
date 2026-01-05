# Troubleshooting Guide

Common issues and solutions for AI video production.

## Image Generation Issues

### Issue: Subject doesn't match description
**Symptoms**: Generated character looks different from description or reference
**Causes**:
- Prompt too vague
- Conflicting descriptions
- Reference image not properly weighted

**Solutions**:
1. Be more specific in physical descriptions
2. Remove ambiguous terms
3. Use multiple reference images for consistency
4. Break complex subjects into separate generation passes

### Issue: Style inconsistency between images
**Symptoms**: Different scenes look like different movies
**Causes**:
- Style section varies between prompts
- Different lighting descriptions
- Inconsistent color references

**Solutions**:
1. Create a style template and copy exactly
2. Use the `--style-ref` flag consistently
3. Include explicit color palette in every prompt
4. Reference a "style anchor" image

### Issue: Composition doesn't allow for motion
**Symptoms**: Video looks cramped or subject exits frame
**Causes**:
- Subject too centered with no movement space
- Background too busy
- No clear motion path

**Solutions**:
1. Plan composition with motion in mind
2. Leave "lead room" in direction of motion
3. Use rule of thirds with subject off-center
4. Simplify background in motion path

## Video Generation Issues

### Issue: Subject distortion during rotation
**Symptoms**: Face becomes distorted when character turns
**Causes**:
- Veo doesn't have information about unseen angles
- Rotation angle too extreme

**Solutions**:
1. Provide reference images showing all needed angles
2. Split rotation into multiple segments (<90° each)
3. Add intermediate keyframe showing the hidden angle
4. Keep subject facing consistent direction

### Issue: Unnatural motion
**Symptoms**: Movement looks robotic or physics-defying
**Causes**:
- Motion description too vague
- Conflicting motion cues
- Duration too short for action

**Solutions**:
1. Add specific motion quality descriptors
2. Describe the weight and momentum
3. Increase duration if action is complex
4. Reference real-world motion ("like a dancer", "like falling leaves")

### Issue: Style drift from keyframes
**Symptoms**: Video doesn't match the style of keyframe images
**Causes**:
- Style not reinforced in video prompt
- Conflicting style cues
- Technical settings override style

**Solutions**:
1. Include full style description in video prompt
2. Use `--style-ref` to load consistent settings
3. Avoid conflicting terms (e.g., "realistic" with "cartoon")

### Issue: Wrong action interpolation
**Symptoms**: Dual-frame generates unexpected action between frames
**Causes**:
- Ambiguous motion path
- Multiple valid interpretations
- Frames too different

**Solutions**:
1. Add explicit motion description
2. Describe the path, not just endpoints
3. Add intermediate keyframe if transition is complex
4. Simplify the change between frames

### Issue: Audio doesn't match video
**Symptoms**: Generated audio is wrong mood or out of sync
**Causes**:
- Veo's audio generation is best-effort
- No audio cues in prompt

**Solutions**:
1. Add audio descriptions: "dramatic orchestral swell"
2. Describe sound effects: "footsteps on gravel, wind howling"
3. Use `--no-audio` and add audio separately
4. Generate multiple takes and select best audio

## API and Technical Issues

### Issue: GOOGLE_API_KEY not found
**Symptoms**: Script fails with "API key not set" error
**Solution**:
```bash
export GOOGLE_API_KEY="your-api-key-here"
# Or add to ~/.bashrc for persistence
```

### Issue: Rate limiting
**Symptoms**: "Quota exceeded" or "Too many requests" errors
**Causes**:
- Too many concurrent requests
- Daily quota exceeded

**Solutions**:
1. Wait and retry (usually 1-5 minutes)
2. Check quota in Google Cloud Console
3. Upgrade API plan if needed
4. Implement request spacing

### Issue: Generation timeout
**Symptoms**: Status remains "processing" beyond max wait time
**Causes**:
- Complex generation taking longer
- API backend issues

**Solutions**:
1. Increase `--max-wait` parameter
2. Check operation status manually later
3. Simplify the generation request
4. Try again during off-peak hours

### Issue: Video file corrupted or won't play
**Symptoms**: Downloaded video doesn't open
**Causes**:
- Download interrupted
- Format incompatibility

**Solutions**:
1. Re-download the video
2. Check file size (should be several MB)
3. Try different video player (VLC recommended)
4. Regenerate if issue persists

## Workflow Issues

### Issue: Can't maintain character consistency
**Symptoms**: Same character looks different in each scene
**Solutions**:
1. Create detailed character reference sheet
2. Use the same reference image for all generations
3. Include character description in every prompt
4. Generate character turnaround (front, side, back views)
5. Consider using character in consistent pose for references

### Issue: Scenes don't cut together well
**Symptoms**: Jarring transitions, mismatched lighting/color
**Solutions**:
1. Plan transitions during Scene Breakdown phase
2. Ensure consistent lighting direction across scenes
3. Use matching color grades in style configuration
4. Consider transition shots (fade, match cut planning)
5. Review all keyframes together before generating videos

### Issue: Total video too short/long
**Symptoms**: Assembled video doesn't match target duration
**Solutions**:
1. Plan scene durations during breakdown
2. Remember: each segment max 8 seconds
3. Build in flexibility with ambient/transition scenes
4. Some scenes can be extended with speed adjustments in editing

## Quality Improvement Tips

### Increasing Visual Quality
1. Use 1080p resolution (`--resolution 1080p`)
2. Ensure keyframe images are high quality
3. Add technical quality terms: "sharp focus", "high detail"
4. Avoid asking for too much action in one segment

### Improving Motion Quality
1. Study real reference videos for the motion type
2. Add specific physics descriptors (weight, momentum)
3. Use appropriate duration for the action
4. Reference known motion styles ("like parkour", "like ballet")

### Achieving Consistency
1. Create comprehensive Production Philosophy first
2. Use style.json for all generations
3. Generate all keyframes before any videos
4. Review all keyframes together for consistency
5. Make style adjustments globally, not per-scene

## When to Start Over

Consider regenerating from scratch if:
- Style has drifted too far from vision
- Character consistency is broken
- Technical issues have corrupted files
- Client/vision has fundamentally changed

It's often faster to regenerate with lessons learned than to fix multiple broken pieces.
