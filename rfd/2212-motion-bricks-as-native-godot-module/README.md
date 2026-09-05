# RFD 2212: motion-bricks-cpp as a native Godot module

**State:** discussion
**Flight level:** L2 (coordination)
**Feature:** how the G1 whole-body motion planner reaches GDScript
**Scope:** `3-interactor/entities-godot-sandbox/modules/motionbricks/`
(new), `3-interactor/motion-bricks-cpp`

## Decision

New C++ Godot module `modules/motionbricks/` in
`entities-godot-sandbox` statically linking
`motion-bricks-cpp`'s `libmotionbricks.a`. Maps the 54 `MB_API` C
exports (`MB_ABI_VERSION=1`, opaque handles, fixed-width scalars)
to GDScript classes 1:1. Motion output copies row-major float32
buffers into `PackedVector3Array` + `PackedByteArray` via `memcpy`
(zero-copy is a follow-up).

## Rejected

- **GDExtension calling motion-bricks-cpp as a shared lib** —
  GDExtension's per-call marshalling cost the plan-per-frame loop
  cannot swallow.
- **Out-of-process motion-bricks server the game HTTPs to** —
  breaks the "one binary, two heads" invariant from RFD 2215.

## Depends on

- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) — the
  model bundle needs the `mb_model_load_from_memory` C API this
  module calls through.
- RFD 2188 — `motion-bricks-cpp` ggml migration to
  `2-contract/ggml/`.
- Q4 QAT loop (HERO in-flight) — the 180 MB Q4 model is the
  browser page-load enabling gate; the F32 730 MB bundle is
  untenable.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- L1 execution recipe: TBD (planned RFD in the 22xx range).

This RFD was drafted by an AI and read by a human before it shipped.
