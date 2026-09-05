# RFD 2211: base tree — `entities-godot-sandbox` for the atelier

**State:** discussion
**Flight level:** L2 (coordination)

## Decision

`entities-godot-sandbox` is the atelier base tree. It carries local
`modules/sandbox/` modifications libriscv needs for the ELF loader
path (RFD 2213 loads godot-vrm as a sandboxed ELF, RFD 2230 loads
GDScript ggml adapters under Godot's script sandbox). Pin the exact
commit in `.repo/manifests/default.xml`.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2213](../2213-vrm-via-godot-sandbox-elf/) — sandbox ELF loader.
- [RFD 2229](../2229-interchangeable-parts-consolidation/) —
  consolidation policy.

This RFD was drafted by an AI and read by a human before it shipped.
