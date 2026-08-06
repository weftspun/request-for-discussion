# RFD 0115: VRM animation playback, one mixer, normalized bones

**State:** committed
**Scope:** `animationManager.js`, `loadMixamoAnimation.js`,
`kimodoMotionLoader.js`, `vrmMixamoPlaybackGuard.js`,
`viewportExpressionVrm.js`, `studioAnimations.js`

## Problem

A Mixamo FBX preset and a Kimodo motion clip both drive the same
VRM, through retargeted humanoid bone tracks. Two failure modes kept
recurring: an orphan FBX mixer layering under the VRM mixer, and a
mixer track written against a raw skeleton bone name instead of a
normalized humanoid one. The second failure is silent: the mixer
time advances, the console logs a loaded clip, and the avatar stays
frozen, since `humanoid.update()` never sees a bone it does not
recognize.

## Decision

An `AnimationMixer` track targets a normalized humanoid bone name,
through `resolveVrmBoneTrackName`, never a raw skeleton bone name.
Every frame, after `mixer.update(delta)`, call `humanoid.update()`,
then `vrm.update(delta)`. The mixer root stays `vrm.scene`.

When `primaryAnimationVrm` is set, `_getActiveAnimationControls()`
returns VRM controls only. `_silenceOrphanFbxMixer()` stops any
leftover FBX mixer, on every preset swap and every Kimodo apply. A
preset swap sets `weightIn=1` and `weightOut=0` on the primary VRM,
never cross-fade-stacked. A VRM0 upload gets the standard axis flip
on every bone, legs, shoulders, and arms alike. Skipping the
shoulder tracks alone twists the arms.

See `DETAILS.md` for the forbidden-change list, the protected files,
and the pre-merge test commands.

## Related

RFD 0045 gives the Kimodo model feeding this retarget. RFD 0104
gives the upload-passthrough policy this path must not disturb.
