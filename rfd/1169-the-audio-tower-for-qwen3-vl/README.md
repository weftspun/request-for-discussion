# RFD 1169: The audio tower for Qwen3-VL, and which half compiles

**State:** ideation
**Feature:** sound, without returning to Gemma 4
**Scope:** `3-interactor/llama-cpp-npu-vision-upstream`

## Decision

**The tower is a plausible device half.** A Whisper-shaped encoder is
Conv, MatMul, Softmax, LayerNormalization and gelu's Erf, all inside
`DEVICE_OPS`, and `PROJECTOR_TYPE_QWEN3A`'s `conv2d` front end shows
the log-mel is a single-channel image — escaping the input-rank
refusal that stopped Pixal3D.

**The blocker is our own fork.** `clip_init_hailo` hardcodes
`CLIP_MODALITY_VISION`; the `mtmd` around it already carries
`CLIP_MODALITY_AUDIO` and `PROJECTOR_TYPE_QWEN3A`.

**No projector transfers, and the AuT source is old.** Qwen3-Omni is
1280 wide over a 2048 decoder, has no standalone checkpoint, and
predates Qwen3-VL-8B. Qwen3.5-Omni has no official release. **Take
`Qwen3-ASR-1.7B`** instead — Apache-2.0, ungated, 128-bin, newer than
our base, 2.04 GB at eight bits.

**A voice is available; it is the acceleration that is not.**
`Qwen3-TTS-12Hz-1.7B-CustomVoice` is Apache-2.0 and clones. Its
autoregressive stage is RFD 1126's obstacle and runs on the host — at
12 Hz, 120 steps for ten seconds of speech. `DETAILS.md` has the
widths, the dates and the fixed window.

## Problem

RFD 1155 abandoned Gemma 4 and left one thing open: what Qwen3-VL does
not carry is sound. An AuT encoder with an MLP projector, taking
128-bin log-mel into the decoder's 4096 space, closes that — the
pattern RFD 1157 established for vision.

## Related

RFD 1155 left this open. RFD 1157 holds the vision tower.
