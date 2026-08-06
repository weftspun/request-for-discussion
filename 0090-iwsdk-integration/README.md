# RFD 0090: IWSDK, a separate `/xr` lab, Galaxy XR as the source of truth

**State:** published
**Scope:** `@iwsdk/*`, `src/pages/IwsdkImmersive.jsx`, `src/library/iwsdkWorld.js`

## Problem

Immersive Web SDK gives locomotion, grab, and spatial UI that this
project's own `SceneManager` does not build itself. Wiring it needed
a clear line between the existing authoring app and a new immersive
mode, and a rule for what counts as "verified": a PC emulator alone
is not proof a Galaxy XR session works.

## Decision

`/xr` is an IWSDK-only lab (`IwsdkImmersive.jsx`, bootstrapped by
`iwsdkWorld.js`'s `createIwsdkWorld`), separate from the main app's
own `/` (`SceneManager`, VRM authoring). `npm run dev` always serves
plain Vite on port 3000, HTTPS, so a headset hits the same URL as
daily development; a PC localhost emulator
(`npm run dev:iwsdk`) is an optional smoke test, never a substitute
for testing on the real headset. `@iwsdk/core`,
`@iwsdk/locomotor`, `@iwsdk/xr-input`, and `@iwsdk/glxf` are
installed as plain npm dependencies, imported from `@iwsdk/core`
directly, not copied into `src/`.

See `DETAILS.md` for the installed-package table, the AI dev-tooling
setup, the headset control map, and the recommended order of work.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/IWSDK_INTEGRATION.md` covers the same topic,
with real content differences. Neither version is authoritative;
that reconciliation is still open. RFD 0088 gives the HTTPS setup
WebXR needs on a device. RFD 0105 gives the webcam and native
face-relay path this lab's own face tracking does not wire in.
