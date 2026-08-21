# RFD 1077: Target hardware stays generic

**State:** discussion
**Scope:** the backend GPU host, the XR headset target

## Problem

Several RFDs name one specific machine, the DGX Spark, and one
specific headset line, Android XR (Galaxy XR), as if the project
needed that exact hardware. Neither dependency is real. The backend
needs a CUDA GPU with enough VRAM for the loaded models. The client
needs a WebXR-capable browser. A reader who owns a 4090 desktop, a
Quest 3, or an Apple Vision Pro should not read those RFDs as
requirements they fail to meet.

## Decision

The backend (`3DAIGC-API`) runs on any machine with a CUDA GPU. The
DGX Spark is this project's own reference machine, not a
requirement; RFD 101b's memory budget, not a DGX-specific spec,
decides whether a GPU fits the loaded models.

The client runs in any WebXR-capable browser, on any headset that
supports it. Quest 3 and Apple Vision Pro reach the dev URL the same
way Galaxy XR does, through `enableVR()` or `enableAR()`, per RFD 100a. Android XR's own native face-tracking bridge (RFD 1052, RFD 1060) stays Android-specific, since it calls an Android-only OpenXR
extension. That path is a Galaxy-XR enhancement, not a requirement
for XR elsewhere. A headset without it still gets VR, AR, floor
anchoring, and the WebXR-native `expression-tracking` feature where
the browser grants it.

See `DETAILS.md` for the affected RFDs.

## Related

RFD 101b gives the GPU memory budget that replaces "runs on a DGX
Spark" as the real constraint. RFD 100a gives the WebXR session
modes every supported headset shares. RFD 1052 and RFD 1060 give the
Android-specific enhancement this decision does not remove.
