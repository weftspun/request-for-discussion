# RFD 0090 details: packages, tooling, controls, and the work order

## Development strategy, Galaxy XR first

| Target | Command or URL | Role |
| --- | --- | --- |
| Samsung Galaxy XR (the truth) | `npm run dev`, then `https://<PC-LAN-IP>:3000/xr` | Real WebXR input and rendering; validate here |
| PC localhost emulator | `npm run dev:iwsdk`, or Vite's `iwsdkDev` on localhost only | An optional Quest-like smoke test, not a substitute for the headset |
| Automation | `npm run iwsdk:xr-smoke`, Playwright | CI or agent checks, PC only |

A full page reload on `/xr` is needed before "Enter VR"; hot module
reload can kill the session. Headset logs forward to
`logs/remote-log.txt` in development. Main VRM authoring stays on
`/` (`SceneManager`); `/xr` is the IWSDK-only lab.

## Install location

Run every `npm install` from the project root, the directory
holding `package.json`:

```
Weftspun3DStudio\
├─ package.json
└─ node_modules\
   └─ @iwsdk\...
```

IWSDK is a plain npm dependency, never copied into `src/`; code
imports directly from `@iwsdk/core` once wired up.

## Currently installed, runtime

| Package | Approximate version | Role |
| --- | --- | --- |
| `@iwsdk/core` | 0.4.1 | The main WebXR ECS runtime (`World`, systems, session) |
| `@iwsdk/locomotor` | a dependency of core | Locomotion: teleport, slide, turn |
| `@iwsdk/xr-input` | a dependency of core | Controllers, hands, rays, pointers |
| `@iwsdk/glxf` | a dependency of core | The GLXF scene loader |

Installed with `npm install @iwsdk/core`. `three` is already a
dependency of this project; do not pin a second, conflicting
Three.js version unless IWSDK's own docs require a specific range.

A related note: legacy `@thirdweb-dev/react` and
`@thirdweb-dev/sdk` (v4, `ethers@^5` only) were removed to fix an
`ERESOLVE` conflict. Blockchain code now uses the unified `thirdweb`
v5 package (`ethers@^5 || ^6`). `.npmrc` may still carry
`legacy-peer-deps=true` as a safety net for other peer warnings.

## AI dev tooling, installed

| Package | Role |
| --- | --- |
| `@iwsdk/vite-plugin-dev` | Quest emulation, a headless Playwright agent browser, an MCP WebSocket |
| `@iwsdk/cli` | `iwsdk dev up`, `iwsdk xr …`, `iwsdk browser screenshot`, `iwsdk mcp stdio` |
| `@iwsdk/reference` | A semantic IWSDK API-search MCP server (`iwsdk-reference`) |

MCP config lives at `.cursor/mcp.json`, naming the `iwsdk-runtime`
and `iwsdk-reference` servers; regenerate it with `npm run
iwsdk:adapter-sync`.

### First-time setup

```bash
npm install
npm run playwright:install    # Chromium for the agent browser, once
npm run iwsdk:adapter-sync    # refresh .cursor/mcp.json
npm run iwsdk:reference-warmup   # optional: a local API corpus for iwsdk-reference
```

### Running development with the autonomous agent browser

```bash
npm run dev              # vite --host on port 3000; headset + daily dev; emulator only, no Playwright
IWSDK_AI=1 npm run dev   # also launches the IWSDK Playwright agent browser (MCP / screenshots)
npm run dev:iwsdk        # iwsdk dev up + the agent browser (may fail on Windows if port 3010 is busy)
npm run dev:runtime      # the same as npm run dev
```

PowerShell: `$env:IWSDK_AI='1'; npm run dev`.

If `npm run dev` fails with "port already in use," stop the old
server (`Ctrl+C` in its own terminal), or run `npx iwsdk dev down`,
then retry.

Without `IWSDK_AI=1`, Vite never auto-launches Chromium, avoiding
`net::ERR_CONNECTION_CLOSED` noise on Windows HTTPS. With it
enabled, the Playwright tab sets `window.__IWER_MCP_MANAGED`, and
the app auto-redirects to `/xr` in development.

### Autonomous XR tests, no headset

With `npm run dev:runtime` running:

```bash
npm run iwsdk:xr-smoke          # quick: reload /xr, enter VR, screenshot
npm run iwsdk:xr-deep-test      # full: grab, hand-only, exit panel, scene inspect
```

Screenshots and a `report.json` land in `logs/iwsdk-deep-test/`.

Headset note: the remote log on `/xr` (auto-enabled in development)
shows a crash if a visual adapter gets hijacked; keep the
pointer-only patch. Distance grab is a ray plus trigger; proximity
grab is walking up plus a grip squeeze.

### Useful CLI commands

```bash
npx iwsdk dev status
npx iwsdk browser screenshot
npx iwsdk xr enter
npx iwsdk xr set-transform --hand right --x 0.3 --y 1.2 --z -0.5
npx iwsdk mcp inspect
```

### Add later, for product features

| Package | Purpose | Install when |
| --- | --- | --- |
| `@iwsdk/vite-plugin-uikitml` | Compiles UIKitML into JSON, for spatial in-headset UI | Building XR-native panels, not flat React overlays |
| `@iwsdk/vite-plugin-gltf-optimizer` | Optimizes GLTF/GLB at build time | Large world or prop assets, slow headset loads |
| `@iwsdk/vite-plugin-metaspatial` | Meta Spatial Editor to GLXF, plus component discovery | Using the Meta Spatial Editor in the pipeline |

### Do not install for this repository

`@iwsdk/create` scaffolds a brand-new app; this project already
exists, so it is never needed here.

## The immersive route

| Path | Component | Notes |
| --- | --- | --- |
| `/xr` | `src/pages/IwsdkImmersive.jsx` | IWSDK's own `World` only, no `SceneManager` |
| `/` | `src/App.jsx` | This project's existing authoring app |

Bootstrap: `src/library/iwsdkWorld.js` (`createIwsdkWorld`,
`disposeIwsdkWorld`). Open locally at `https://localhost:3000/xr`;
HTTPS is required for on-device WebXR (RFD 0088).

### Headset controls, Galaxy XR or Quest

| Action | Control |
| --- | --- |
| Move | The left thumbstick |
| Turn | The right thumbstick, horizontal |
| Teleport | Push the right thumbstick forward to aim, release to land |
| Distance grab | Point at the target (a white dot appears), then trigger or pinch |
| Proximity grab | Walk within roughly arm's reach, then a grip squeeze on the slightly larger hit volume |
| Hand-only (controllers set down) | Hands take primary input; rays stay active; a red Exit panel follows the head |
| Exit XR | The controller's Menu or B button; ray-select the head-locked red Exit panel; or an Exit XR button, or Escape, on phone or PC |

`src/library/iwsdkXrEnhancements.js` runs the headset input
pipeline: controllers stay primary for locomotion, hands stay
tracked when docked, both ray and grab pointers are active, the
floor is walkable, and `inputsourceschange` session hooks apply. The
demo cube uses both `DistanceGrabbable` and a `OneHandGrabbable`
proximity volume; `layers: false` avoids a Galaxy XR black-frame
issue.

## Recommended order of work

1. Wire `@iwsdk/core` into code: done (`/xr` route plus `iwsdkWorld.js`).
2. Add dev tooling: done (`vite-plugin-dev`, `cli`, `reference`, MCP sync).
3. Test WebXR on Galaxy XR's own Chrome, on device (HTTPS required; RFD 0088).
4. Later: UIKitML, a GLTF optimizer, Meta Spatial, and optional Gaussian-splat worlds.

Face tracking in Chrome XR stays a separate concern (a relay, or a
future native `expression-tracking`), not wired into `/xr`. For VRM
plus APK face relay, use the main app instead, at
`https://<PC-LAN-IP>:3000/?nativeFaceRelay=1` (RFD 0105).

## Architecture intent, in short

```
This project (React + SceneManager)  ->  authoring, tasks, VRM tools
IWSDK immersive mode                 ->  presence: locomotion, grab, spatial UI, worlds
Galaxy XR Chrome WebXR               ->  the target runtime for immersive mode
```

## Quick verification

```bash
npm ls @iwsdk/core @iwsdk/locomotor @iwsdk/xr-input @iwsdk/glxf --depth=1
```
