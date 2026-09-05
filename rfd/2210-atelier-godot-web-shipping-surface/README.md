# RFD 2210: atelier shipping surface — Godot `platform=web` + motion-bricks module

**Platform=web delivery surface:** retracted 2026-09-05, superseded
by [RFD 2228](../2228-webgpu-native-drop-platform-web/) — operator
reversal (verbatim): *"drop webgpu platform=web. try webgpu
native"*. The L3 bet on Godot + `entities-godot-sandbox` + motion-
bricks + Three.js blocklist all stand; the delivery surface flips
from `scons platform=web` (Emscripten) to native binaries with
Godot's WebGPU renderer (Dawn / wgpu-native). The "one binary two
heads" architecture (interactive + headless capture) survives — see
RFD 2228 for what changes and what stays.

**State:** discussion
**Flight level:** L3 (strategy, portfolio bet — see RFD 2177)
**Feature:** one Godot `platform=web` binary from `entities-godot-sandbox`
serves both the shuttle marketing video (headless capture pass) and the
Starforged VN game (interactive session); `motion-bricks-cpp` inference
lands as a native `modules/motionbricks/` module; three.js goes on the
blocklist
**Scope:** `3-interactor/entities-godot-sandbox`, `3-interactor/motion-bricks-cpp`,
`2-contract/ggml`, RFDs 2194 (retracted) + 2208 (retracted) + 2206
(amended) + 2205 (unchanged), CLAUDE.md + BLOCKLIST.md blocklist tables

## Decision

Combine RFD 2194 (atelier shuttle portfolio widget) and RFD 2208
(decision-point control surface) under one runtime: **Godot 4.7-beta
from `entities-godot-sandbox` compiled via `scons platform=web`** to
an Emscripten-built browser artefact. Both heads — the paired
photo/anime marketing video (2194) and the FaceTime-like VN game
(2208) — ship from that binary. The video is a headless capture pass
of the same runtime that serves the game interactively. Three.js is
blocklisted; every current three.js consumer moves to `platform=web`
or retires.

A new C++ Godot module `modules/motionbricks/` links
`motion-bricks-cpp`'s C ABI (54 `MB_API` exports at
`MB_ABI_VERSION=1`) and exposes on-device G1 whole-body motion planning
to GDScript. `motion-bricks-cpp` migrates its ggml source to
`2-contract/ggml/` per RFD 2188 and gains an `if(EMSCRIPTEN)` branch
in its CMake for the browser build (Vulkan/Metal/BLAS off,
`GGML_WASM_SINGLE_FILE=ON`).

VRM 1.0 support lands via **godot-sandbox**: `V-Sekai/godot-vrm`
compiles to a RISC-V ELF loaded by `modules/sandbox` (libriscv).
`modules/sandbox` moves from the disable list to the keep list for
this reason.

## Problem

Two live RFDs cover pieces of the atelier's shipping surface but
disagree on runtime:

- **RFD 2194** ships a paired photo/anime marketing video. Says
  "Live Godot render acceptable"; execution parked 2026-09-04 on
  ~158 h GPU sizing (LLaDA-o 16-step at K=4 × 3 rounds × 12 shots).
- **RFD 2208** ships the Starforged VN game. Reference impl at
  `7-service/service-sqlar-cas/docs/` uses **three.js + three-vrm**.

Six merge conflicts between them (render surface / autonomy / identity
pipeline / runtime footprint / parked-vs-live / RFD-graph). All six
dissolve when one runtime serves both heads — and Godot is the
runtime the workspace already ships every other 3D surface through
(`entities-godot-main`, `entities-godot-sandbox`, `datasource-flow/
flow/adapters/godot`, `turboquant-godot`). Three.js is a second
scene-graph the avatar has to be re-authored into; the workspace has
no interest in maintaining two 3D runtimes.

## Terminology

**`platform=web`** means `scons platform=web target=template_release`
— the Godot engine compiled via Emscripten to a `godot.web.*.wasm` +
`godot.web.*.js` template loaded by an exported project. This is
Godot's standard web export, in tree since 4.0, built by
`entities-godot-sandbox/.github/workflows/web_builds.yml`.

**`godot-wasm`** (specifically the `ashtonmeuser/godot-wasm` project)
is a Godot extension for running WebAssembly modules INSIDE a native
Godot build. **Opposite direction. Out of this RFD's scope.**

**`godot-sandbox`** is `modules/sandbox` (libriscv-based RISC-V VM
inside Godot), an existing custom module in `entities-godot-sandbox`.
Used here to load `V-Sekai/godot-vrm` as a sandboxed ELF.

## The April 2026 pendulum

`2-contract/manuals-vsk/decisions/20260425-deck-log.md:34` records
the operator's earlier decision: *"Client strategy: Godot wasm32/
wasm64 web export **dropped**. Two clients replace it — Godot native
PCVR and Three.js WebGPU (browser observer + WebXR)."* That decision
lived April 2026 → September 2026.

This RFD is the reversal. Reconciliation: April's argument was
scoped to browser-observer + WebXR performance under the presence
loop (RFD 1170). The atelier shipping surface (this RFD) is a
different workload — a decision-point VN with per-turn re-renders
and a headless capture pass, not a real-time XR observer. Both can
be right: `platform=web` for the atelier surface here; the April
"Godot dropped for browser observer + WebXR" is scoped-out to that
XR observer case which this RFD does not touch. If the same wall
that dropped Godot-web in April (unmeasured; the deck log names it
without measuring) turns out to hit the atelier surface too, this
RFD's L3 status is that bet's collateral.

## Non-goals

- Not un-parking RFD 2194's upstream generator pipeline; the parked-
  on-sizing GPU work stays parked. RFD 2210 only redirects where its
  output flows (the paired asset library becomes Godot resources).
- Not touching `platform=android`, `platform=ios`, `platform=macos`,
  `platform=linuxbsd`, `platform=windows` builds. This RFD's slim
  `custom.py` applies to web only; desktop/mobile inherit the stock
  module set from the same source tree.
- Not blocklisting WebGL2 or WebGPU as such. `platform=web` uses
  WebGL2 under the hood via Godot's renderer. **WebGPU stays on the
  blocklist per the standing 2026-09-05 operator directive** — even
  when browser support is available, no consumer in this RFD reaches
  for it.
- Not the `ashtonmeuser/godot-wasm` project. Separate concern.

## Related

- RFD 2194 (atelier-shuttle-portfolio-widget) — **retracted 2026-09-05**.
- RFD 2208 (decision-point-control-surface) — **retracted 2026-09-05**.
- RFD 2206 (video-call VRM portrait) — **amended** to swap
  `@pixiv/three-vrm` for `godot-vrm` as a sandbox ELF.
- RFD 2207 (Nord palette for demos) — unchanged; applies to Godot
  themes as directly as CSS.
- RFD 2205 (Taskweft in Bao) — unchanged; `taskweft.wasm` planner
  stays the game-loop's brain.
- RFD 2188 (one ggml across workspace) — `motion-bricks-cpp` becomes
  a consumer via this RFD.
- RFD 1077 (H2O edge-CDN) — the pattern for streaming the Q4 GGUF
  bundle at runtime rather than shipping in the WASM binary.
- RFD 1123 (CineForm in Godot) — the encoder for the video head's
  MP4 output ([[ffmpeg-blocklisted]]).
- RFD 1170 (cleanroom presence loop) — earlier RFD that names Godot
  over three.js for the presence workload; this RFD extends the
  choice to the atelier workload.

This RFD was drafted by an AI and read by a human before it shipped.
