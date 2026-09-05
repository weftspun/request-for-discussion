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

This RFD was drafted by an AI and read by a human before it shipped.
