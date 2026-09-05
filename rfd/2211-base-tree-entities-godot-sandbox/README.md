# RFD 2211: base tree — `entities-godot-sandbox` for the atelier

**WebGPU-fork patch series:** retracted 2026-09-05 by
[RFD 2231](../2231-drop-webgpu-use-vulkan/) — Godot's shipping
Vulkan renderer is the answer, no fork patch needed. The
base-tree pick below stands unchanged (it survived three
reversals; that's the signal it was picked for the right reason).

**State:** discussion
**Flight level:** L2 (coordination)

## Decision

**`entities-godot-sandbox` is the atelier base tree.** It carries
local `modules/sandbox/` modifications libriscv needs for the ELF
loader path (RFD 2213 loads godot-vrm as a sandboxed ELF, RFD 2230
loads GDScript ggml adapters under Godot's script sandbox).

The `-main` sibling checkout was the same repo at revision `main`
rather than `feat/vsk-sandbox-4.7`; trimmed 2026-09-05 as
`weftspun-keypoint#101` per the interchangeable-parts consolidation
policy (RFD 2229).

Pin the exact commit in `.repo/manifests/default.xml`. Don't track
a moving branch.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2213](../2213-vrm-via-godot-sandbox-elf/) — why the local
  sandbox iteration matters here.
- [RFD 2229](../2229-interchangeable-parts-consolidation/) — the
  consolidation policy that trimmed `-main`.
- [RFD 2231](../2231-drop-webgpu-use-vulkan/) — the reversal that
  retracted the WebGPU-fork patch amendment.

This RFD was drafted by an AI and read by a human before it shipped.
