# RFD 106c: Floor-anchor in both AR and VR, opaque sky only in VR

**State:** committed
**Scope:** `src/library/sceneManager.js`, `enableVR()`, `initialize()`

## Problem

AR needs a transparent renderer so the camera feed shows through;
VR needs an opaque sky. Both need the same model bottom-aligned to
the physical or virtual floor, at the same wrapper position. A
texture loader re-applying a stored sky to `scene.background` during
AR, or a runtime reporting `floorAlignmentY: 1` instead of near
zero, are the two regressions this area kept reintroducing.

## Decision

One unified `renderer.xr.setSession` override in `enableVR()`
handles both session types. Reference spaces request in this order:
`bounded-floor` (Galaxy XR's own boundary-calibrated floor level),
`local-floor`, `local`, `viewer`; `bounded-floor` needs no manual
floor-height code, since WebXR itself gives a floor-aligned origin.
On entering either mode, an XR wrapper group holding only model
content gets `x=0`, `z=-0.5`, and `y` set to the negative of the
model's own bounding-box bottom, aligning that bottom to Y=0.
AR keeps `scene.background = null` and a zero clear alpha, never
letting a sky texture loader re-apply itself; VR keeps an opaque
clear alpha and a mesh-based sky, since some runtimes handle
`scene.background` alone unreliably. A background snapshot, captured
before any session starts, restores exactly on AR exit.

See `DETAILS.md` for the exact wrapper math, the snapshot fields,
wrapper re-centering (including the long-press software recenter
gesture), and the troubleshooting checklist.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/XR_MODE_FLOOR_ANCHORING_AND_BACKGROUNDS.md`
covers the same topic, with real differences; neither is
authoritative. RFD 105a gives the IWSDK lab this file's own XR path runs beside.
