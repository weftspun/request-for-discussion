# RFD 1148: The runtime that reaches the device

**State:** discussion
**Feature:** one inference runtime for the Mac GPU and the Hailo part
**Scope:** `pixi.toml`, `3-interactor/litert-upstream`

## Decision

**LiteRT, and the argument is reach rather than speed.**

    candidate               why it is out
    ANE                     2 GiB weight ceiling at 2^31 bytes
    tinygrad NVIDIA eGPU    one device init per power cycle
    Core ML native          per-model porting cost
    ORT CoreML EP           7.01 TFLOP/s, the same Metal path
    ORT WebGPU EP           1.90 TFLOP/s, 0.27x of the same GPU
    IREE                    a compiler, not an execution provider
    ONNX                    superseded by TFLite as the interchange
    ggml                    reaches neither Hailo nor Cloud TPU

ggml is quick here and that never was the question. The Dataflow
Compiler parses TFLite, TensorFlow and ONNX; GGUF appears on none of
those, and a format that cannot reach the hardware cannot be the format.

**The accelerators are binaries we receive.** No LiteRT GPU accelerator
builds from the public tree, so the wheel decides the menu: Metal on
macOS, Dawn elsewhere. The cost is ggml's single static executable for
three platforms, which nothing restores.

## Problem

RFD 1142 chose Metal as the Mac's engine, RFD 1129 asks whether the
operators compile, and nothing asked which runtime reaches **both** this
GPU and the edge device. Candidates were excluded one at a time, so the
elimination existed only as a scatter of rows.

## Related

RFD 1129 asks whether the operators compile, RFD 1142 which engine the
Mac uses, and RFD 1122 is the goal. `DETAILS.md` has the apparatus.
