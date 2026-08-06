# RFD 0115 details: forbidden changes, protected files, tests

Sourced from `vrm-animation-protected.mdc` (user-confirmed 2026-06-27)
and `weftspun3d-vrm-animation-playback.mdc`, near-duplicate rules
this RFD merges into one design.

## Retarget sampling

`withNeutralVrmSceneRootForRetarget` runs only while sampling a
retarget pose. It restores the scene root afterward. Loot FBX URLs
stay canonical (`2_Idle.fbx`, not `Idle.fbx`); the mixer will not
resolve a renamed or relocated file.

## Forbidden without an explicit user request

- Disabling the VRM0 quaternion or vector flip on a passthrough
  upload. This causes buckled knees.
- Skipping the shoulder tracks (`mixamorigLeftShoulder`,
  `mixamorigRightShoulder`) on passthrough. This causes twisted
  arms.
- Running the FBX reference mixer alongside the primary VRM mixer.
  This causes layered limbs.
- A passthrough-only animation shortcut in `loadMixamoAnimation.js`
  or `kimodoMotionLoader.js`, without approval.
- Reverting `resolveVrmBoneTrackName`, `_getActiveAnimationControls`,
  `_silenceOrphanFbxMixer`, `setAnimationFrameHook`, or
  `syncAnimationPrimaryTarget`, without a replacement in the same
  change.
- The studio bar loading anything but `LOOT_DEFAULT_ANIMATIONS`;
  `_studioDefaultsLoaded` blocks a trait-manifest overwrite.
- `normalizeLootAssetUrl` collapsing an `https://` prefix.

## Protected files

`animationManager.js`, `loadMixamoAnimation.js`,
`kimodoMotionLoader.js`, `viewportExpressionVrm.js`,
`vrmMixamoPlaybackGuard.js`, `studioAnimations.js`.

## Before merging an animation change

```bash
npm run test:run -- src/__tests__/loadMixamoAnimation.test.js \
  src/__tests__/animationManager.playback.test.js \
  src/__tests__/kimodoMotionLoader.test.js \
  src/__tests__/vrmMixamoPlaybackGuard.test.js
npm run test:anim-smoke   # optional; needs a LAN HTTPS dev URL, ?animSmoke=1
```

Re-test by hand too: upload a passthrough VRM, apply the Walking
preset, then apply a Kimodo motion.
