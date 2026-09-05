# RFD 2213: VRM 1.0 loading via `godot-sandbox` RISC-V ELF

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** how VRM 1.0 assets load in the atelier native binary
without adding new C++ or forking upstream
**Scope:** `3-interactor/entities-godot-sandbox/modules/sandbox`,
`V-Sekai/godot-vrm`

## Decision

Compile `V-Sekai/godot-vrm` (GDScript addon) to a RISC-V ELF via
`godot-sandbox`'s toolchain. Ship at
`res://addons/godot-vrm/godot-vrm.elf`. Load at runtime through
`modules/sandbox` (libriscv). Godot's `GLTFDocument` +
`GLTFDocumentExtension` API hands raw VRM bytes to the ELF; the
ELF returns node/skeleton/expression/spring-bone data.

## Rejected

- **New C++ `modules/vrm/`** subclassing `GLTFDocumentExtension` —
  duplicates work already done in godot-vrm's GDScript. Possible
  follow-up when sandbox overhead measurably hits latency.
- **Bundle godot-vrm as a plain GDScript addon** — parsing runs
  in the main GDScript VM; no isolation from a malicious VRM.

## Cascade

`modules/sandbox` (libriscv) is on the KEEP list because its
ELF-execution capability is what makes this work.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2211](../2211-base-tree-entities-godot-sandbox/) — the
  base-tree choice.
- [RFD 2230](../2230-ggml-adapters-in-godot-sandbox/) — parallel
  path for ggml adapters (GDScript-in-sandbox for orchestration,
  ELF-in-sandbox for third-party untrusted code).
- RFD 2206 (video-call VRM portrait) — uses this ELF path for
  the VRM LookAt + expression node.

This RFD was drafted by an AI and read by a human before it shipped.
