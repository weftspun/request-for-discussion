# RFD 2210: atelier shipping surface — Godot native binary + ggml module

**Platform=web delivery surface:** retracted 2026-09-05,
superseded by [RFD 2228](../2228-webgpu-native-drop-platform-web/)
+ [RFD 2231](../2231-drop-webgpu-use-vulkan/) — the delivery surface
is one **native Godot binary per platform** (macOS / Windows /
Linux) with the Vulkan renderer (MoltenVK on macOS), not an
Emscripten browser export. The title's `platform=web` phrase is
the pointer landing target per retraction doctrine.

**State:** discussion
**Flight level:** L3 (strategy, portfolio bet — see RFD 2177)
**Feature:** one native Godot binary from `entities-godot-sandbox`
serves both the shuttle marketing video (headless capture head) and
the Starforged VN game (interactive head); ggml as one shared
module (RFD 2230) with per-model GDScript adapters; three.js goes
on the blocklist
**Scope:** `3-interactor/entities-godot-sandbox`,
`2-contract/ggml`, RFDs 2211/2214/2215/2216 (L2 fanout) + RFDs
2228/2229/2230/2231 (reversal + consolidation policy)

## Decision

One runtime, one binary per platform, two heads. Godot from
`entities-godot-sandbox` (RFD 2211 base-tree pick, RFD 2228 native
delivery, RFD 2231 Vulkan renderer) exports as a native binary.
Interactive head opens a native window; headless head is invoked
via `godot --headless --write-movie` (RFD 2215) and muxes video
through CineForm (ffmpeg blocklisted, see memory
`ffmpeg-blocklisted`). ggml consumers ride on one shared
`modules/ggml/` (RFD 2230) with per-model GDScript adapters.
Three.js is blocklisted (RFD 2216).

## Related

- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — L2 base
  tree pick.
- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) — L2
  model bundle format (SQLite + ZSTD on local disk).
- [RFD 2215](../2215-one-binary-two-heads/) — L2 two-heads shape.
- [RFD 2216](../2216-threejs-blocklist/) — L2 three.js blocklist.
- [RFD 2228](../2228-webgpu-native-drop-platform-web/) — L3
  reversal to native delivery.
- [RFD 2229](../2229-interchangeable-parts-consolidation/) — L3
  consolidation policy (this RFD is one of its live cases).
- [RFD 2230](../2230-ggml-adapters-in-godot-sandbox/) — L2 ggml
  as one shared module + GDScript adapters.
- [RFD 2231](../2231-drop-webgpu-use-vulkan/) — L3 Vulkan renderer
  pick.
- RFD 2205 (Taskweft in Bao), RFD 2206 (video-call VRM portrait),
  RFD 2207 (Nord palette), RFD 2188 (one ggml across workspace).
- RFD 1123 (CineForm in Godot) — the encoder for the headless
  head's video output.
- RFD 1170 (cleanroom presence loop) — the earlier RFD that names
  Godot over three.js for the presence workload; this RFD extends
  the choice to the atelier workload.

This RFD was drafted by an AI and read by a human before it shipped.
