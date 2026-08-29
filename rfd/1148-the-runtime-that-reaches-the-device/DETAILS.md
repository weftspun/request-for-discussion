# RFD 1148 details: what the wheel ships, and what refuses to build

## The accelerator is a binary, and the build settles it

`litert/runtime/accelerators/gpu/BUILD` declares
`macos_dylib(name = "build_ml_drift_webgpu_accelerator_dylib", …)` with
`minimum_os_version = "14.0"`, no `target_compatible_with` and no `nobuilder`
tag, unlike the Windows target beside it which carries both. Read alone, that
says macOS support withheld from the release.

Reading a BUILD file shows a target is declared. Whether its dependencies can be
fetched is a separate question, and bazel 7.7.1 against a fresh clone,
`--nobuild`, `--config=macos`, answers it:

    target                              failure
    ml_drift_webgpu_accelerator_dylib   @ml_drift: "At least one of url and urls
                                        must be provided"
    ml_drift_metal_accelerator_dylib    no such package 'tools/build_defs/swift'

`WORKSPACE:390` declares `http_archive(name = "ml_drift", strip_prefix =
"ml-drift-main", …)` carrying no `url` field, and no `workspace.bzl` supplies
one. `google-ai-edge/ml-drift`, `google/ml-drift` and `google-ai-edge/ml_drift`
all return 404. `ml_drift_delegate/` sits in the tree, and that is the delegate
glue rather than the compute core it binds to.

The Metal target fails earlier and for its own reason, on a Google-internal
`//tools/build_defs/swift` referenced from `ml_drift_delegate/delegate/BUILD:892`.

## What the three wheels ship

Read out of `ai-edge-litert` 2.2.0, listing the native libraries in each and the
backend strings inside them:

    platform        accelerator                            reaches the GPU via
    macOS arm64     libLiteRtMetalAccelerator.dylib 11 MB  Metal
    Windows amd64   libLiteRtWebGpuAccelerator.dll  23 MB  Tint -> HLSL -> D3D12
    Linux x86_64    libLiteRtWebGpuAccelerator.so   18 MB  Tint -> SPIR-V -> Vulkan

"WebGPU" here means Dawn rather than a browser: 1087 `dawn` and 2026 `tint`
strings in the Windows DLL, 718 and 1262 in the Linux `.so`, beside 134 `D3D12`
and 137 `hlsl` on Windows, 250 `Vulkan` and 164 `Spirv` on Linux.

Grepping the Linux accelerator for `cuda|cudnn|nvrtc` returns 0. The source tree
nevertheless carries `litert/vendors/nvidia/`, a TensorRT compiler plugin with
`.cu` kernels, so the shipped wheel and the tree disagree about NVIDIA and only
the wheel was measured.

The macOS wheel contains no file matching `webgpu`, `dawn` or `tint`, and
`libLiteRt.dylib` holds 16 `WebGpu` strings against 0 `Dawn` — the core knows the
enum while the plugin stays absent.

## The vendor ABI, for the Hailo work

    header                                      entry points   lines
    litert/vendors/c/litert_compiler_plugin.h   18             156
    litert/vendors/c/litert_dispatch.h          49             390

    reference                                          lines
    litert/vendors/examples/example_plugin.cc          416
    litert/vendors/examples/example_dispatch.cc        609
    litert/vendors/nvidia/compiler/compiler_plugin.cc  892

A vendor plugin is written once per device rather than once per model, which is
the axis ggml failed on: `trellis2.cpp` is 3420 lines of hand-written graph, 79
distinct `ggml_*` ops across 7 `ggml_build_forward_expand` sites, for one model.

## StableHLO sits upstream of the flatbuffer

`litert_torch/backend/lowerings/_basic.py` imports `stablehlo` from
`litert_converter.mlir.dialects` and emits `stablehlo.add` and
`stablehlo.multiply`; `_convolution.py` is headed "lowering for coreaten to
stablehlo"; `backend/export.py` returns an `MlirLowered` carrying `.module`.
`litert-torch` 0.9.4 requires `jax` outright and ships `backend/jax_bridge`, and
`backend/tf_integration.py:116` rewrites `arith.constant` to `stablehlo.constant`
"to run the module with TFXLA".

So the Cloud TPU route is a tap one stage above the flatbuffer rather than a
conversion. It stays deferred: no TPU is attached, and RunPod rents NVIDIA.

`jax-metal` does not serve as a Metal alternative — 0.1.1, released 2024-10-08,
pinning `jaxlib>=0.4.34` against a current 0.11.1, and it remains the only PJRT
Metal plugin in existence.

## What Metal reaches, measured

`scripts/litert_bench.py`, `ConvStack(width=64, depth=4, size=64)`, 460.1 M MACs, on an
Apple M2 Pro. The oracle is torch on CPU, which replaces the ONNX diff that retired with
the format. Rate counts a fused multiply-add as two operations, `gpu_tops.py`'s
convention, so these compose with RFD 1142's rows.

    backend      accel   best ms  spread   TFLOP/s   max|diff|
    cpu          True      12.24      0%      0.08   2.384e-07
    metal fp16   True       0.59      3%      1.56   1.687e-03
    metal f32    True       0.39     90%      2.33   2.682e-07
    coreml       -             -       -      6.97           -    RFD 1142, fp16

**Metal takes the whole graph** — `is_fully_accelerated()` answers true on every row, so
none of this is a partitioned graph with a fast fragment. It reaches **0.33x** the figure
Core ML's Metal path gave on the same part, and roughly thirty times CPU.

**The accelerator computes in fp16 unless told otherwise**, and the evidence is numeric
rather than a timing. The default carries `max|diff|` 1.687e-03 against torch; the same
model under `GpuOptions(enforce_f32=True)` carries 2.682e-07. Four orders of magnitude is
not a rounding difference, and it means the earlier reading of the default row as f32 was
wrong: the comparison against Core ML's fp16 figure is like for like.

**This harness declines to rank fp16 against f32, and the reason is an artefact worth
recording.** With
a fixed measurement order, whichever GPU configuration ran first won:

    order        fp16 best   f32 best   winner
    fp16 first      0.38        0.40     fp16
    f32 first       0.48        0.45     f32

The ranking followed the order rather than the arithmetic, so the gap between the two is
smaller than the artefact. A first version of this harness took one median of fifty
repetitions and reported 0.21x; the median moved 74% between rounds on identical input.
The harness now alternates the order every round, takes the fastest round rather than the
average because contention only subtracts, and prints the spread beside the rate.

## Hailo takes TFLite by its own direction

The Dataflow Compiler 5.3.0 guide names its inputs as "a Tensorflow checkpoint, a
Tensorflow frozen graph file, a TFLite file, or an ONNX file", mentions TFLite 57
times, and deprecates parsing TensorFlow 1.x and 2.x `.ckpt`/`.pb` "using all
parsing APIs" with guidelines for moving to TensorFlow Lite. Choosing LiteRT
lands on the input the vendor consolidates on.

Precision is integer: `fp16` occurs 0 times in the 83-page datasheet and 0 times
in the 187-page compiler guide. The modes are `a8_w4`, `a16_w8` and `a16_w16`,
set per layer through `quantization_param(layer, precision_mode=…)`.
