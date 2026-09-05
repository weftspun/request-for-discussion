# RFD 2217: ggml WebGL2 backend evaluation

**ggml WebGL2 backend evaluation:** retracted 2026-09-05,
superseded by [RFD 2218](../2218-ggml-webgpu-backend/) — operator
reversal (verbatim): *"blocklist webgl2 ggml. allowlist webgpu
ggml"*. WebGL2 has no compute shaders; WebGPU does, and llama.cpp
already ships a WebGPU backend. RFD 2218 carries the surviving
question (build / adopt / defer) re-asked against WebGPU.

**State:** abandoned

This RFD was drafted by an AI and read by a human before it shipped.
