# RFD 2216: Three.js blocklist

**State:** discussion
**Flight level:** L2 (coordination — closes a runtime fork)
**Feature:** three.js goes on the CLAUDE.md / BLOCKLIST.md
blocklist as an in-browser 3D runtime
**Scope:** `CLAUDE.md`, `BLOCKLIST.md`, cascade of retirements
in consumer files

## Decision

Blocklist three.js as an in-browser 3D runtime. Substitute is
**Godot as a native binary per platform** built from
`entities-godot-sandbox` with the Vulkan renderer (MoltenVK on
macOS) per [RFD 2231](../2231-drop-webgpu-use-vulkan/). Three.js
itself is MIT-licensed — the objection is not licence, it is
runtime story: the workspace ships every 3D surface via Godot,
and a three.js path forks the scene-graph, material pipeline,
animation graph, and lighting model.

Live rows: `CLAUDE.md` blocklist table + `BLOCKLIST.md` full
section (the section body carries the argument in current form).

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3
  strategic bet.
- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — base
  tree pick.
- [RFD 2215](../2215-one-binary-two-heads/) — the "one runtime,
  not two" argument that also drives this blocklist.
- [RFD 2228](../2228-webgpu-native-drop-platform-web/) — native
  delivery.
- [RFD 2231](../2231-drop-webgpu-use-vulkan/) — Vulkan renderer.
- RFD 1170 (cleanroom presence loop) — earlier RFD picking Godot
  over three.js for a different workload.

This RFD was drafted by an AI and read by a human before it shipped.
