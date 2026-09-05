# RFD 2210: atelier shipping surface

**State:** discussion
**Flight level:** L3 (strategy, portfolio bet — see RFD 2177)
**Feature:** the atelier ships as one native Godot binary per platform;
one runtime, two heads (interactive + headless capture)
**Scope:** `3-interactor/entities-godot-sandbox`, `2-contract/ggml`,
L2 fanout at RFDs 2211/2214/2215/2216, adapter shape at RFD 2230

## Decision

One runtime, one binary per platform (macOS / Windows / Linux) from
`3-interactor/entities-godot-sandbox`. Vulkan renderer (MoltenVK on
macOS). Two heads: interactive window for the Starforged VN game,
headless `godot --headless --write-movie` for the marketing video.
Same `.tscn` / `.tres` assets, same binary, different invocation
flag. ggml consumers ride on one shared `modules/ggml/` module
(RFD 2230) with per-model GDScript adapters. Three.js is
blocklisted (RFD 2216). SQLite + ZSTD is the model bundle format
on local disk (RFD 2214). Video muxed through CineForm per
RFD 1123.

## Related

- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — base tree.
- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) — model
  bundle format.
- [RFD 2215](../2215-one-binary-two-heads/) — two-heads shape.
- [RFD 2216](../2216-threejs-blocklist/) — three.js blocklist.
- [RFD 2229](../2229-interchangeable-parts-consolidation/) —
  consolidation policy.
- [RFD 2230](../2230-ggml-adapters-in-godot-sandbox/) — ggml as
  one shared module + GDScript adapters.
- RFD 2205 (Taskweft in Bao), RFD 2206 (video-call VRM portrait),
  RFD 2207 (Nord palette), RFD 2188 (one ggml across workspace),
  RFD 1123 (CineForm in Godot), RFD 1170 (presence loop).

This RFD was drafted by an AI and read by a human before it shipped.
