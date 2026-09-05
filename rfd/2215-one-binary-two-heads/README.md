# RFD 2215: one Godot `platform=web` binary, two heads

**`platform=web` delivery surface:** retracted 2026-09-05 by
[RFD 2228](../2228-webgpu-native-drop-platform-web/) — operator
reversal (verbatim): *"drop webgpu platform=web. try webgpu
native"*. The **one-binary-two-heads architecture survives** —
the interactive head (Starforged VN game) and the headless
capture head (marketing video) still run from one source tree,
one CI workflow, one export template. What changes: it is one
**native** Godot binary per platform (macOS / Windows / Linux)
with the interactive head opening a native window and the
capture head invoked via `godot --headless --write-movie` per
[CineForm](../../../3-interactor/interactor-cineform/) doctrine.
The two-head shape is why this RFD is worth keeping; the
delivery surface name in the title is the pointer landing target
per retraction doctrine.

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** the shape that dissolves the RFD 2194 vs 2208 conflict
— one build serves both the marketing video (headless capture) and
the game (interactive session)
**Scope:** CI web-build workflow, headless render entrypoint,
game entrypoint

## Decision

One source tree, one CI workflow, one WASM binary, two invocation
flags:

- **Head A — game (formerly RFD 2208)**: interactive session in a
  browser tab. Loads Starforged fixture (`starforged.sqlite`,
  shipped from RFD 2208's earlier session — cross-session-lag
  applies), calls `taskweft.wasm`'s planner (RFD 2205,
  unchanged), surfaces the decision-point menu via a Godot
  Control-node VN layout, plays reactions on the VRM portrait
  via `MotionBricks` for motion + VRM expressions for face.
- **Head B — marketing video (formerly RFD 2194)**: headless
  render pass of the same runtime. `godot --headless --write-movie
  shot<NN>.mp4 ...` captures the runway scene per shot from a
  paired photo/anime asset library that RFD 2194's upstream
  generator pipeline still produces (the parked-on-sizing GPU work
  stays parked; this RFD does not un-park it). Video muxed via
  CineForm per RFD 1123 (ffmpeg is blocklisted; see memory
  `ffmpeg-blocklisted`).

Same `.tscn`/`.tres` assets, same WASM binary as the game head
(different invocation flag). The video is what the game looks like
when you run it deterministically with a script over the shot list.

## Why one binary

Six merge conflicts between RFD 2194 and RFD 2208 (render surface /
autonomy / identity pipeline / runtime footprint / parked-vs-live /
RFD-graph) all dissolve when one runtime serves both. Two binaries
is what created the conflicts in the first place.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3
  strategic bet.
- [RFD 2216](../2216-threejs-blocklist/) — the "one runtime, not
  two" argument that also drives the three.js blocklist.
- RFD 1123 (CineForm in Godot) — Head B's encoder.
- L1 execution recipe: TBD.

This RFD was drafted by an AI and read by a human before it shipped.
