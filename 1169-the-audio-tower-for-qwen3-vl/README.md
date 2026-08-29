# RFD 1169: The audio tower for Qwen3-VL, and what it cannot carry

**State:** ideation
**Feature:** sound, without returning to Gemma 4
**Scope:** `3-interactor/llama-cpp-npu-vision-upstream`

## Problem

RFD 1155 abandoned Gemma 4 and left one thing open: what Qwen3-VL does
not carry is sound, and no Hailo audio reference was known here.

A 300M AuT encoder with an MLP projector, taking 128-bin log-mel
spectrograms into the same 4096 sequence space, closes that. RFD 1157
established the pattern: a compiled tower replaces the projector and
decode stays on the host.

## Decision

**The tower is a plausible device half and the operators say so.** A
Whisper-shaped encoder is Conv, MatMul, Softmax, LayerNormalization and
gelu's Erf — every one inside `DEVICE_OPS`. A log-mel is 128 bins by a
fixed frame count, so it presents as a single-channel image and does
not meet the input-rank refusal that stopped Pixal3D four times.

**The blocker is our own fork, not the hardware.** `clip_init_hailo`
hardcodes `CLIP_MODALITY_VISION` and takes only image-shaped
parameters, while upstream `mtmd` already carries
`CLIP_MODALITY_AUDIO`, `clip_graph_whisper_enc` and `n_mel_bins`.

**ASR is in reach, voice cloning is not, and the split is the finding.**
Understanding audio is an encoder, which compiles. Producing audio is
autoregressive decode into a vocoder, which is RFD 1126's obstacle
unchanged. This buys ears, not a voice.

`DETAILS.md` carries the fixed-window question and what to measure.

## Related

RFD 1155 left this open. RFD 1157 holds the vision tower.
RFD 1126 names the decode obstacle.
