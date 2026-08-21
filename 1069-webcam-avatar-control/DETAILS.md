# RFD 1069 details: features, usage, the Android XR path, and remote logging

## Stack and features

MediaPipe Holistic reads face landmarks, Kalidokit's `Face.solve()`
turns them into weights, and those weights drive the VRM's
`expressionManager` and humanoid bones. Features: blink (optionally
per eye), mouth shapes (Ah, Ee, Oh, Ou), and smoothed neck/head
rotation from the same landmarks.

`src/library/webcamAvatarDriver.js` is created, started, and stopped
from `SceneContext`; the UI toggle lives in `BottomDisplayMenu`. It
acts on the same VRM files the rest of the app uses (character
manager avatars, or the current scene VRM), and never touches WebXR
session state directly.

## Usage

1. Load a VRM model.
2. Click "Cam" in the bottom control bar to start webcam avatar control.
3. Allow camera access when prompted; the avatar's face follows the user's face.
4. Click the same button ("Cam on") to stop.

## Galaxy XR and WebXR expression tracking

When a browser does not grant the `expression-tracking` feature, a
WebView-wrapped Android XR app relays OpenXR's own
`XR_ANDROID_face_tracking` weights into the page through
`nativeFaceBridge.js`. See RFD 1060 for that native path, and
`native/android-xr-face-bridge/README.md`.

On a supported user agent (Chrome on Android XR, for instance),
immersive VR and AR sessions request the optional
`expression-tracking` feature descriptor. When granted, each
`XRFrame` may expose `frame.expressions`, a draft WebXR Expression
Tracking map of roughly FACS-like weight keys; the runtime maps
headset sensors to `XR_ANDROID_face_tracking` semantics underneath.

Implemented: `src/library/xrExpressionTrackingDriver.js` reads
`XRFrame.expressions` and maps weights heuristically to VRM presets
(`Blink`, `Ah`, `Ee`, `Oh`, `Ou`), with light per-VRM smoothing.
`SceneManager` adds `expression-tracking` to `optionalFeatures` for
both AR (`ARButton`) and manual VR
(`requestSession('immersive-vr')`), logs once when
`session.enabledFeatures` includes it, and applies the mapping every
XR render frame. `SceneContext` registers the same VRM-list resolver
webcam control uses.

Debugging: append `?xrExpressionProbe=1` to log one `XRFrame`
introspection (`maybeProbeXRFrame`).

### Why a second permission prompt may not appear

On Android XR, Chrome can fold several sensitive capabilities,
including tracked face, eye, and hand data, into the initial WebXR
or spatial-mapping consent, rather than a separate dialog per
sensor, per Android's own "Develop for the web on Android XR" page.
No extra prompt after entering AR or VR is the expected case.

Separately, `expression-tracking` is optional: if a Chrome build
does not implement the draft `XRFrame.expressions` API yet,
`session.enabledFeatures` may not list it, and the avatar's face
stays neutral in XR with no error.

Galaxy XR development workaround: install the "Weftspun XR Face"
APK, run `npm run dev` on a PC, open Chrome's menu, "Open in Chrome
for WebXR (+ face)" (`?nativeFaceRelay=1`), and keep the APK visible
or in picture-in-picture so Jetpack or OpenXR PBuffer face tracking
can relay to the dev server during Chrome's Full Space AR. See RFD
0096 and the Android Studio AI brief (weftspun-3d-studio-designs'
own numbering) for the fuller setup.

First-frame diagnostics log as `[XR][expression] First-frame
diagnostics`, with `enabledFeatures`, `expressionTrackingGranted`,
and `expressionsNonNull`. Forward that line from a headset with
`?remoteLog=1`.

## Remote logging from a headset

1. Start the dev server (`npm run dev`; HTTPS on port 3000 by
   default when certs exist).
2. On the headset, open `https://<PC-LAN-IP>:3000/?remoteLog=1`
   (add `&xrExpressionProbe=1` for the extra probe).
   `https://localhost:3000` on the headset targets the headset
   itself, not the PC; use the PC's LAN address.
3. Logs POST to `/__remote_log` on the same origin. Vite prints
   them and appends `logs/remote-log.txt`.
4. A working client logs `[RemoteLog] Forwarding console to
   /__remote_log` in the browser console.

## Current behavior, summarized

Webcam avatar control stays off during WebXR. XR expression tracking
applies only inside an immersive session, and only when the user
agent exposes `expressions`; otherwise the avatar's face stays
unchanged from whichever non-XR driver last ran.
