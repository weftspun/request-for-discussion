# RFD 2217: ggml WebGL2 backend evaluation

**ggml WebGL2 backend evaluation:** retracted 2026-09-05,
superseded by [RFD 2218](../2218-ggml-webgpu-backend/) — operator
reversal (verbatim): *"blocklist webgl2 ggml. allowlist webgpu
ggml"*. WebGL2 has no compute shaders (fragment-shader-only
compute is a fit for TFJS's op library but a poor fit for ggml's
graph shape); WebGPU has native compute shaders and llama.cpp
already goes there. The scoping question this RFD asked (build /
adopt / defer) still applies — RFD 2218 re-asks it against
WebGPU.

**State:** abandoned
**Flight level:** L2 (coordination — spans ggml + motion-bricks-cpp
+ atelier web surface)
**Feature:** whether to write (or adopt) a WebGL2 backend for ggml so
that browser-side motion-bricks inference clears the "usable
latency" bar without relying on CPU-only WASM
**Scope:** `2-contract/ggml`, `3-interactor/motion-bricks-cpp`,
[RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) (model
bundle path), [RFD 2210](../2210-atelier-godot-web-shipping-surface/)
(L3 anchor)

## Question

WebGPU is blocklisted (standing 2026-09-05 operator directive).
Vulkan is not available in the browser. That leaves **CPU-in-WASM**
as the ggml browser path today, which is 10–100× slower than
GPU-accelerated inference on matmul-heavy workloads. Motion-bricks's
transformer graph (attention `mul_mat` + softmax + norm + leaky-relu)
is exactly the matmul-heavy shape the CPU path handles worst.

**WebGL2 is the third option** — universally available (since
2017–2018 baseline), no WebGPU dependency, precedents exist for
tensor-ops-as-fragment-shaders. This RFD scopes whether the
workspace writes one, adopts one, or defers.

## Precedents (all Apache-2.0 or MIT)

- **`tfjs-backend-webgl`** — TensorFlow.js runs tensor ops as WebGL2
  fragment shaders since 2018. ~200 shaders across the op library.
  Handles int8/f16/f32 dtypes, dequant, matmul.
- **ONNX Runtime Web** — carries a WebGL execution provider
  alongside WASM + WebGPU EPs.
- **MediaPipe Solutions** — on-device inference in browser,
  WebGL-backed.

`llama.cpp` went WebGPU; there is **no upstream ggml WebGL2 backend
today**.

## Approach options

### A) Write a motion-bricks-shaped ggml WebGL2 backend (weeks)

Motion-bricks-cpp uses a subset of ggml ops (per Explore 2026-09-05
survey of `src/root.cpp` + `src/pose.cpp`): `mul_mat`, `soft_max`,
`permute`, `view_2d`, `leaky_relu`, `norm`, `add`, `mul`. ~8–12
ops × 2–3 dtypes (Q4, F16, F32) = ~30 shaders — manageable.

ggml's backend interface (`ggml-backend.h`) already accepts new
backends the same way it accepts Metal, Vulkan, CUDA. The workspace
ggml (`2-contract/ggml/`, RFD 2188) is the right home for the new
backend.

- **Effort**: 4–8 weeks single-engineer for motion-bricks parity.
- **Risk**: Q4 dequant fidelity in fragment shaders (fp16 texture
  precision + `EXT_color_buffer_float` extension gating).
- **Reversibility**: high — the backend is a discrete file, can be
  removed if WebGPU un-blocks or motion-bricks migrates.

### B) Adopt tfjs's WebGL kernels as reference (compressed weeks)

Port tfjs's per-op GLSL to ggml's backend interface. Faster than A
because the shaders exist and are battle-tested. Attribution +
license bookkeeping is real (tfjs is Apache-2.0). Requires a shim
translating tfjs's tensor-descriptor conventions to ggml's.

- **Effort**: 2–4 weeks.
- **Risk**: the tfjs shaders assume tfjs's memory manager; some
  will need rewrite when the memory manager is ggml's.
- **License**: Apache-2.0 permits use with attribution; verify
  before shipping.

### C) Convert motion-bricks-cpp's graph to ONNX, run via ORT-Web WebGL EP

Sidesteps the "write a backend" question by changing the runtime.
Motion-bricks-cpp's hand-written ggml graph in `src/root.cpp` exports
to ONNX; browser loads the ONNX file and dispatches to ORT-Web's
WebGL EP.

- **Effort**: 1–2 weeks conversion + ORT-Web wiring.
- **Risk**: hand-written ggml graph → ONNX conversion is not
  automatic; each custom op needs an ONNX equivalent or a custom
  op registered with ORT.
- **Reversibility**: low — motion-bricks-cpp becomes two runtimes,
  ggml (native) and ORT (browser). The atelier's "one runtime"
  ethos suffers.

### D) Ship CPU-only WASM, defer acceleration until measured

The default from RFD 2214. Motion-bricks plan latency in
CPU-only-WASM is untested. If a `walk(60 frames)` plan clears
under 500 ms on a mid-range laptop, the browser experience is
acceptable and this RFD parks. If it doesn't, options A/B/C
un-park.

- **Effort**: 0 additional (already scoped).
- **Risk**: user experience under CPU-only is unknown; deferring
  means committing to it in v1.

## Recommended

**D as gate, A as unblock**. Ship CPU-only WASM per RFD 2214 as v1.
Land a measurement pass under RFD 2214's Verification section: cold
`walk(60)` on a stock browser + mid-range laptop. If plan latency
exceeds a defined threshold (proposal: >500 ms — same threshold
RFD 1170's presence loop uses), un-park option A. If under
threshold, park this RFD; note the measurement.

WebGL2 backend work costs weeks of engineer time; do it when we
know CPU-in-WASM isn't enough, not before.

## Related

- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) — the
  model bundle sizing that assumes CPU-in-WASM as the default. This
  RFD is the "what if that's not enough" companion.
- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- RFD 2188 (one ggml across workspace) — the WebGL backend, if
  written, lives in `2-contract/ggml/` per this consolidation.
- RFD 1170 (cleanroom presence loop) — the sub-500 ms latency
  threshold this RFD borrows.

## Operator context 2026-09-05

Operator asked (verbatim): *"review webgl2 code didn't they get
tensorflow lite working for tensors so can't we write a webgl2
backend for ggml for some acceleration"*. Answer: yes; TensorFlow.js
(not TFLite specifically) proves it; this RFD scopes cost + gate.

This RFD was drafted by an AI and read by a human before it shipped.
