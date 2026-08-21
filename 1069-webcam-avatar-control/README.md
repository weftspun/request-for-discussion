# RFD 1069: Webcam avatar control, off during WebXR

**State:** published
**Scope:** `src/library/webcamAvatarDriver.js`, `xrExpressionTrackingDriver.js`

## Problem

A webcam can drive the current VRM's face and head, using Kalidokit
plus MediaPipe Holistic, the same approach XR Animator and Kalidoface
use. That driver must never fight a headset's own tracking once a
WebXR session presents.

## Decision

The webcam driver does not run while WebXR is presenting. Entering
VR or AR stops it by itself: it frees the camera, ends the detection
loop, and returns the avatar to neutral, with nothing left to
conflict with headset tracking or Galaxy XR. A separate driver,
`xrExpressionTrackingDriver.js`, takes over inside an immersive
session, reading the draft WebXR `XRFrame.expressions` feature when
a user agent grants it. Neither driver touches `enableVR()`,
`enableAR()`, or reference spaces.

See `DETAILS.md` for the feature list, the Android XR native-bridge
path, and remote-logging setup for headset debugging.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/WEBCAM_AVATAR_CONTROL.md` covers the same topic,
with real content differences. Neither version is authoritative;
that reconciliation is still open. RFD 1060 gives the Android XR
native face-tracking path this RFD's XR driver falls back to.
