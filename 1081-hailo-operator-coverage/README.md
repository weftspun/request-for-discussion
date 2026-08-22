# RFD 1081: Which operators the Hailo-10H will not take

**State:** discussion
**Feature:** operator coverage for edge deployment
**Scope:** `3-interactor/rf-detr-cpp`

## Problem

A model reaches the ASUS UGen300 through the Dataflow Compiler, which
takes a graph and rejects operators it cannot map. Two stages of the
mesh pipeline are built from operators with no portable form at all.

Sparse submanifold convolution runs on `flex_gemm` and `o_voxel`, CUDA
kernels over sparse voxel grids, and ONNX has no operator for it.
Neighborhood attention runs on natten, whose fused CUTLASS kernels are
compiled per NVIDIA architecture. Neither is a quantisation question.
Both ask whether the graph exists outside CUDA at all.

## Decision

Answer by compiling, not by reading documentation. The compiler is the
authority on what the compiler accepts.

`gate_dfc_parse.py` and the `DEVICE_OPS` allowlist exist already, for
the keypoint detector. Point the same gate at an ONNX export of each
stage and read the rejections. A disagreement between allowlist and
compiler is the finding rather than an error.

Export the smallest graph that carries the question: one DiT block,
and NAF's attention layer, rather than the whole cascade. A rejection
names an operator at any size, and a small graph fails in seconds.

The keypoint detector still ships; this asks what else could.

See `DETAILS.md` for the two stages. `SKILL.md` gives the procedure.

## Related

RFD 1080 asks whether four bits survive. RFD 1082 asks about
throughput and needs this first. RFD 1028 packages the model.
