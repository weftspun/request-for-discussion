# RFD 1076: XR embody, view toggle, and Move stay input, not menu state

**State:** committed
**Scope:** `sceneManagerXr*.js`

## Problem

Inside the main app's XR session (not the `/xr` IWSDK lab), the
headset controls three things: whether the camera rides the avatar
(embody) or floats free (third-person), whether Move drives the
avatar or the free viewpoint, and an in-headset menu. Left X and the
stick click must toggle view and Move at any time, menu open or
closed; a regression kept gating both behind an open menu instead.

## Decision

On XR spawn, `alignXrLocomotionRigToViewport` runs on the first
frame, from the current desktop view and the live headset pose. On
XR exit, `captureXrViewAsDesktop` carries the last XR view back into
desktop OrbitControls. Left X always toggles view; the stick click
always toggles Move; neither reads menu state. Embodying the avatar
aligns the rig's XZ position and yaw only, never Y. Disembodying
places the avatar at the exit spot, facing the headset, with the
viewer one meter behind, and switches Move to Viewpoint. Yaw math
stays parent-local, `theta = atan2(fx, fz)`, where yaw zero faces
+Z in this scene tree.

The in-headset menu keeps a 25% opacity background, right-side tabs
in one uniform column, Close at the bottom, and View, Move, and
Measure paired together. The menu panel's bottom edge sits on the
controller grip; it does not float roughly 0.5 m ahead of it.

`bash scripts/verify_xr_avatar_view_locomotion.sh` runs before a
merge touching this file. See `DETAILS.md` for the changes this RFD
forbids without an explicit user request.

## Related

RFD 100a gives the WebXR session modes this locomotion runs inside.
RFD 106c gives the floor-anchor placement this embody step assumes.
