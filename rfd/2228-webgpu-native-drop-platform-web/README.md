# RFD 2228: native binary, drop `platform=web`

**WebGPU compute/render API:** retracted 2026-09-05 by
[RFD 2231](../2231-drop-webgpu-use-vulkan/) — the compute/render
API is **Vulkan** (MoltenVK on macOS), not WebGPU. The title's
"WebGPU" phrase is the pointer landing target per retraction
doctrine.

**State:** discussion
**Flight level:** L3 (strategy — dropped the `platform=web`
delivery premise that RFDs 2210/2211/2218/2227 stood on)

## The surviving decision

The atelier ships as a **native binary per platform** (`.exe` /
`.app` / `.AppImage`) built from `entities-godot-sandbox`. No
Emscripten toolchain, no browser bundle, no HTTP-Range SQLite
fetch, no browser memory ceiling as sizing constraint. Model
files live on local disk (`sqlite3_open()` per RFD 2214), Godot's
renderer is Vulkan (per RFD 2231), ggml links Vulkan too (per
RFD 2218 rescope in RFD 2231).

The one-binary-two-heads architecture (RFD 2215) survives — one
source tree, one CI workflow, one native binary per platform,
invoked as an interactive window or via `godot --headless
--write-movie` for the capture head.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3
  anchor; retracted its own `platform=web` half by this RFD.
- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — base
  tree pick (unchanged).
- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) —
  model bundle format (SQLite + ZSTD on local disk after this
  RFD's reversal).
- [RFD 2215](../2215-one-binary-two-heads/) — the two-heads shape.
- [RFD 2218](../2218-ggml-webgpu-backend/) — abandoned by
  RFD 2231; superseded compute-API pick.
- [RFD 2231](../2231-drop-webgpu-use-vulkan/) — the follow-up
  that flipped compute/render from WebGPU to Vulkan.

This RFD was drafted by an AI and read by a human before it shipped.
