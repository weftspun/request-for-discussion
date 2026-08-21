# RFD 1052: A companion APK relays face weights past Chrome's own gap

**State:** discussion
**Scope:** `native/android-xr-face-bridge/`, `com.weftspun.xrfacebridge`

## Problem

Chrome on Android XR does not grant WebXR's `expression-tracking`
feature, so `XRFrame.expressions` never reaches the web app inside
an immersive session, and a VRM avatar's face cannot follow the
user's own face in AR or VR through Chrome alone. This gap is
specific to Android XR's own Chrome build; a headset whose browser
grants `expression-tracking` needs no bridge at all.

## Decision

A companion APK, `com.weftspun.xrfacebridge`, runs native face
tracking (Jetpack XR, with OpenXR's `XR_ANDROID_face_tracking` as a
parallel path per RFD 1060), then POSTs face JSON to the dev PC over
LAN while the user is inside Chrome WebXR. Chrome loads this
project's own URL with `?nativeFaceRelay=1`, and applies the
relayed weights through the same code path native WebView injection
already uses. This is a development-time workflow; production would
need real WebXR expressions, a hosted relay, or a native immersive
host instead.

See `DETAILS.md` for the end-to-end data flow, the implementation
status table, the platform constraints, and the test steps.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/ANDROID_STUDIO_AI_BRIEF.md` covers the same
topic, with real content differences. Neither version is
authoritative; that reconciliation is still open. RFD 1060 gives the
OpenXR spec this bridge's native path implements. RFD 1069 gives the
webcam-driven fallback this bridge complements. RFD 1077 gives the
general hardware requirement this Android-only bridge is one
enhancement on top of, not a dependency.
