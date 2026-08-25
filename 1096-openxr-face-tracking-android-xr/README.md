# RFD 1096: OpenXR face tracking, native and web, on Android XR

**State:** discussion
**Scope:** `src/library/xrExpressionTrackingDriver.js`, `openxrFaceParameterMap.js`, `native/android-xr-face-bridge/`

## Problem

Two separate paths can drive a VRM's face on Android XR: a browser's
own draft WebXR `expression-tracking` feature, and native OpenXR's
`XR_ANDROID_face_tracking`. Neither this project's code nor its
prior notes named the canonical API references, the exact payload
shape between the two, or which one wins when both are active.

## Decision

Prefer the Khronos online man pages over any bundled PDF; the PDFs
in this repository's own `OpenXR/` folder are raster, non-searchable
scans, useful for diagrams, not for exact API names, and may lag the
live registry version. `xrCreateFaceTrackerANDROID` and
`xrGetFaceStateANDROID` fill `XrFaceStateANDROID`'s 68-parameter
`XrFaceParameterIndicesANDROID` array; the web driver
(`xrExpressionTrackingDriver.js`) reads either the browser's own
`XRFrame.expressions`, or a native bridge's relayed weights,
whichever is fresher, with native weights overriding WebXR's own
values for that frame when both are present. `XR_ANDROID_face_tracking`
is Android-only by name; a Quest 3 or Vision Pro session runs the
`XRFrame.expressions` path alone, through the same driver, with no
native bridge involved. See `DETAILS.md` for every canonical
reference link, the payload contract in both its shapes, and the
mapping-fidelity caveats.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/OPENXR_FACE_TRACKING_ANDROID_XR.md` covers the
same topic, with real content differences; not yet reconciled. RFD
1082 gives the companion APK implementing the native side. RFD 1105
gives the WebXR-only fallback, and RFD 1119 the general hardware
requirement. The app's own `docs/FACE_EXPRESSION_TUNING_REFERENCE.md`
holds the numeric tuning baseline, not restated here, per RFD 1000.
