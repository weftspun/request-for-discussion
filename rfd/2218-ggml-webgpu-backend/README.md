# RFD 2218: ggml WebGPU backend

**ggml WebGPU backend:** retracted 2026-09-05, superseded by
[RFD 2231](../2231-drop-webgpu-use-vulkan/) — operator directive
(verbatim): *"if we're native we can blocklist webgpu and only
use vulkan which has more quality assurance hours in production"*.
Native delivery (RFD 2228) removed the browser-shipping constraint
that put WebGPU in the stack; Vulkan has ~10 years of production
QA vs WebGPU's ~2, is Godot 4's primary renderer, and skips a
translation layer on Linux/Windows. This RFD's approach-A (adopt
llama.cpp's backend as reference) still applies against
llama.cpp's **Vulkan** backend rather than its WebGPU one — same
`ggml_backend_*` interface, older codepath, more field-tested.

**State:** abandoned
**Flight level:** L2 (coordination — spans ggml + motion-bricks-cpp
+ atelier web surface)
**Feature:** WebGPU is the browser acceleration path for ggml (and
therefore motion-bricks-cpp in the atelier `platform=web` export)
**Scope:** `2-contract/ggml`, `3-interactor/motion-bricks-cpp`,
[RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) (model
bundle path), [RFD 2210](../2210-atelier-godot-web-shipping-surface/)
(L3 anchor), [RFD 2217](../2217-ggml-webgl2-backend-evaluation/)
(retracted precursor that asked the same question against WebGL2)

## The reversal

Operator directive 2026-09-05, verbatim: *"blocklist webgl2 ggml.
allowlist webgpu ggml"*.

This inverts the two earlier standing positions:

- **WebGPU is no longer blocklisted for ggml.** The earlier
  2026-09-05 "WebGPU is blocklisted" directive stands as a general
  default (browser 3D runtimes, non-ggml consumers) but carves out
  an explicit allowlist exception for ggml. Any non-ggml consumer
  reaching for WebGPU still needs its own RFD.
- **WebGL2 is now blocklisted for ggml.** The RFD 2217 evaluation
  path (build a WebGL2 backend borrowing TFJS shaders) is closed.

## Why the reversal is technically coherent

WebGL2 has no compute shaders. Tensor ops in WebGL2 are fragment-
shader compute (write to a framebuffer texture that represents the
tensor). Works for TFJS's op library because TFJS ships hundreds of
per-op shaders and battle-tested memory management around them.
Poor fit for ggml because:

1. ggml's execution model wants explicit compute dispatch, not
   fragment-pass-per-op. Every op wraps in a render-target bind /
   viewport / draw-triangles ceremony, and the pipeline stalls on
   framebuffer readback.
2. Q4 dequant → matmul (motion-bricks's hot path) benefits from
   workgroup-shared memory. Fragment shaders in WebGL2 have no
   shared memory; every dequant is per-fragment.
3. Precision is optional — `EXT_color_buffer_float` is not
   guaranteed on every device; some Android GPUs ship WebGL2
   without full float32 render targets.

WebGPU addresses all three: native compute pipeline, workgroup
storage (`var<workgroup>`), guaranteed f32 storage buffers.
`llama.cpp` already went WebGPU as its browser backend; that's
proof-of-concept for ggml-graph-in-WebGPU.

## Approach options

### A) Adopt llama.cpp's WebGPU backend structure

`llama.cpp` (which shares ggml with everything else in the family)
has an in-tree WebGPU browser build. The kernels port to a
motion-bricks-shaped subset because both projects use the same
`ggml_backend_*` interface. Cost: weeks, not months — kernels
exist, adaptation is the work.

### B) Write a fresh WebGPU backend against upstream ggml

Same shape as adding a Vulkan backend to ggml: `ggml-backend-webgpu.
c` + WGSL compute-shader library. Motion-bricks-cpp uses ~8-12 ops
(per Explore 2026-09-05); ~30 WGSL kernels (op × dtype) covers
motion-bricks. Larger than A but produces an upstream-clean patch.

### C) Route via ONNX Runtime Web's WebGPU EP

Convert motion-bricks-cpp's ggml graph to ONNX, load in browser
via ORT-Web's WebGPU EP. Sidesteps ggml WebGPU altogether. Same
runtime-fork objection as RFD 2217 §C (motion-bricks-cpp becomes
two runtimes).

## Recommended

**A** — adopt llama.cpp's WebGPU backend as reference, adapt to the
motion-bricks op subset. Land in `2-contract/ggml/` per RFD 2188.
Motion-bricks-cpp's `if(EMSCRIPTEN)` CMake branch (see RFD 2214's
follow-up L1 recipe) gains a `GGML_WEBGPU=ON` toggle that swaps
the CPU compute path for the WebGPU one when the browser's
`navigator.gpu` is available; falls back to CPU-in-WASM otherwise
(same graceful-degrade the plugin's blast-radius section calls out
in RFD 2205).

## Browser support (2026-09-05 as of writing)

- Chrome, Edge: shipped.
- Firefox: enabled by default in nightly, targeting stable by Q4.
- Safari 26: preview.
- Mobile: Android Chrome shipped; iOS 18 Safari has it behind a
  flag.

CPU-in-WASM fallback stays required for older browsers or feature-
detection-fail cases. `navigator.gpu?.requestAdapter()` → success →
WebGPU path; failure → CPU path.

## Godot-side WebGPU already patched in

Operator refinement 2026-09-05, verbatim: *"use the existing webgpu
godot fork. add it as a patch to our godot-entities"*. Per RFD 2211,
the WebGPU-capable Godot fork lands as a **patch series** on top of
`entities-godot-sandbox`, not as a base-tree replacement. Practical
implication for this RFD: Godot's `RenderingDevice` acquires the
WebGPU `GPUDevice` at scene-start; the ggml WebGPU backend piggybacks
on that same device rather than requesting its own adapter. One
browser, one WebGPU adapter, two subsystems (Godot renderer +
ggml compute) sharing it. The atelier's `platform=web` binary
therefore ships with a single WebGPU init path, not two.

Follow-up L1 execution RFD (planned in the 22xx range): the
concrete recipe for the ggml-backend-webgpu `GPUDevice` handshake
with Godot's `RenderingDevice` — who allocates, who owns the
error-scope, how buffer transfers avoid a round-trip through
JavaScript.

## Related

- [RFD 2210](../2210-atelier-godot-web-shipping-surface/) — L3.
- [RFD 2214](../2214-model-bundle-sqlite-range-fetch-zstd/) — the
  model bundle path; loader hands buffers to the WebGPU backend
  the same way it hands them to CPU today.
- [RFD 2216](../2216-threejs-blocklist/) — three.js blocklist that
  currently mentions WebGPU as blocklisted; needs an amendment
  paragraph noting the ggml allowlist carve-out.
- [RFD 2217](../2217-ggml-webgl2-backend-evaluation/) — retracted
  precursor (WebGL2 evaluation, superseded by this RFD's WebGPU
  answer).
- RFD 2188 (one ggml across workspace) — the WebGPU backend lands
  in `2-contract/ggml/` per this consolidation.
- Upstream: `llama.cpp`'s WebGPU browser backend, the reference
  implementation to port from.

## Operator context 2026-09-05

Reversal directive (verbatim, this session): *"blocklist webgl2
ggml. allowlist webgpu ggml"*.

This RFD was drafted by an AI and read by a human before it shipped.
