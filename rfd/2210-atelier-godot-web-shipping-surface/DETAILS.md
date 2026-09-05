# RFD 2210: details (L3 — strategy)

Strategy-level doctrine only. Architecture lives in
[RFD 2211](../2211-atelier-web-architecture/). Execution lives in
[RFD 2212](../2212-atelier-web-execution/).

## The reversal being made

`2-contract/manuals-vsk/decisions/20260425-deck-log.md:34` dropped
Godot `platform=web` in April 2026 in favour of "Godot native PCVR +
three.js WebGPU (browser observer + WebXR)". This RFD reverses that
decision for one workload (the atelier's marketing video + Starforged
VN game), keeps it in place for the other (browser observer + XR).

The scope carve is: the atelier surface is a per-turn re-render VN
plus a headless capture pass, not a real-time XR observer. The April
argument (unmeasured, framed against XR performance) does not
apply to this workload. If the argument does apply and hits the same
wall, this L3 bet's collateral says so.

## What this RFD retracts

- **RFD 2194** (atelier-shuttle-portfolio-widget) — retracted
  2026-09-05, superseded by RFD 2210 + 2211 + 2212.
- **RFD 2208** (decision-point-control-surface) — retracted
  2026-09-05, superseded by RFD 2210 + 2211 + 2212.

Six merge conflicts between 2194 and 2208 (render surface / autonomy /
identity pipeline / runtime footprint / parked-vs-live / RFD-graph)
all dissolve when one runtime serves both heads. That runtime is
Godot 4.7-beta from `entities-godot-sandbox` compiled via `scons
platform=web`.

## What this RFD amends

- **RFD 2206** (video-call VRM portrait) — stays live but drops
  `@pixiv/three-vrm` in favour of `V-Sekai/godot-vrm` compiled to a
  RISC-V ELF loaded by `modules/sandbox`. Amendment paragraph in
  RFD 2206 DETAILS, not a retraction.

## Blocklists this RFD introduces

**Three.js as an in-browser 3D runtime.** Not licence (MIT); runtime
story. The workspace ships every other 3D surface via Godot; a
three.js path forks the scene-graph, material pipeline, animation
graph, and lighting model. The `platform=web` export from
`entities-godot-sandbox` covers the same role using the same source
tree that produces every other Godot surface — one runtime, not two.

Row lands in `CLAUDE.md` and section in `BLOCKLIST.md`; carve-outs
name vendored upstream demos and third-party viewers-we-do-not-ship
as exempt. Full row text + section body: **RFD 2212 §Three.js
blocklist landing**.

## Companion RFDs at other flight levels

L2 (coordination — one per component decision):

- **[RFD 2211](../2211-base-tree-entities-godot-sandbox/)** — base
  tree is `entities-godot-sandbox`.
- **[RFD 2212](../2212-motion-bricks-as-native-godot-module/)** —
  motion-bricks-cpp as a native Godot module (not GDExtension, not
  out-of-process).
- **[RFD 2213](../2213-vrm-via-godot-sandbox-elf/)** — VRM 1.0
  loading via `V-Sekai/godot-vrm` compiled to a `godot-sandbox`
  RISC-V ELF.
- **[RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/)** —
  model bundle as ZSTD-compressed SQLite range-fetched from the
  browser.
- **[RFD 2215](../2215-one-binary-two-heads/)** — one binary serves
  both marketing-video (headless) and game (interactive) heads.
- **[RFD 2216](../2216-threejs-blocklist/)** — three.js blocklist
  row + BLOCKLIST.md section.

L1 (operations — execution recipes; TBD, one per critical file):

- Custom.py slim disable list
- motion-bricks-cpp `if(EMSCRIPTEN)` CMake branch
- `mb_model_load_from_memory` C API addition
- `modules/motionbricks/` SCsub + register_types
- GGUF → ZSTD SQLite converter (Elixir per language-preference
  doctrine)
- godot-vrm → RISC-V ELF build recipe
- CI web workflow amendment for slim custom.py
- Retirement PRs for each three.js consumer named in RFD 2216

## Cross-references

- RFD 1170 (cleanroom presence loop) — already picks Godot over
  three.js for the presence workload; this RFD extends the choice
  to the atelier workload.
- RFD 2177 (flight-levels taxonomy) — defines L1/L2/L3.
- RFD 2188 (one ggml across workspace) — motion-bricks-cpp becomes
  a consumer via RFD 2212.
- RFD 2205 (Taskweft in Bao) — unchanged; the game head's planner
  brain.
- RFD 2207 (Nord palette) — unchanged; applies to Godot themes
  the same way it applies to CSS.

This RFD was drafted by an AI and read by a human before it shipped.
