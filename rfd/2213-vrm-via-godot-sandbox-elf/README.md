# RFD 2213: VRM 1.0 loading via `godot-sandbox` RISC-V ELF

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** how VRM 1.0 assets load in the atelier `platform=web`
export without adding new C++ or forking upstream
**Scope:** `3-interactor/entities-godot-sandbox/modules/sandbox`,
`V-Sekai/godot-vrm`

## Decision

Compile `V-Sekai/godot-vrm` (GDScript addon) to a RISC-V ELF via
`godot-sandbox`'s toolchain. Ship at
`res://addons/godot-vrm/godot-vrm.elf`. Load at runtime through
`modules/sandbox` (libriscv). Godot's `GLTFDocument` +
`GLTFDocumentExtension` API hands raw VRM bytes to the ELF; the
ELF returns node/skeleton/expression/spring-bone data.

Operator directive 2026-09-05: *"if you use godot-sandbox you can
compile godot-vrm to a sandbox elf and use it as a native module."*

## Rejected

- **New C++ `modules/vrm/`** subclassing `GLTFDocumentExtension` —
  duplicates work already done in godot-vrm's GDScript. Possible
  follow-up L2 RFD when sandbox overhead measurably hits latency.
- **Bundle godot-vrm as a plain GDScript addon** — parsing runs in
  the main GDScript VM; no isolation from a malicious VRM.

## Cascade

`modules/sandbox` (libriscv) moves from the disable list to the
KEEP list in the slim custom.py. Its ELF-execution capability is
what makes this work; the size cost is paid by removing the need
for C++ VRM parsing.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — the
  base-tree choice, driven partly by this RFD.
- RFD 2206 (video-call VRM portrait) — amended to swap
  `@pixiv/three-vrm` for the ELF path here.

This RFD was drafted by an AI and read by a human before it shipped.
