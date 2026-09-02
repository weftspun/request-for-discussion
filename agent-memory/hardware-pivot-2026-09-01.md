---
name: hardware-pivot-2026-09-01
description: "Operator moved from Mac mini M2 Pro (only, no local GPU, no rentals) to Windows 11 + RTX 3090"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T02:45:53.042Z
---

Session 2026-09-01 ran the whole RFD 2156 conversation on a Mac mini
M2 Pro 32 GB with zero Vast rental and no other hardware. Next
session runs on Windows 11 with an RTX 3090 (24 GB).

What that unlocks and what it does not:

- **QAFT-LoRA training on Qwen3-VL-4B** returns to the table. Base is
  8.9 GB fp16, LoRA rank 32 optim state fits 24 GB VRAM. Training
  data is `EditScore/EditScore-Reward-Data` (97,300 rows, 161.8 GB,
  apache-2.0). Scaffold at `3-interactor/editscore-lora-gemma4-e4b/`
  (name is stale — will retarget from Gemma-4-E4B to Qwen3-VL-4B).
- **Wan-VACE 14B NF4** (~8.7 GB) fits alongside the reward model on
  the 3090 with swap. RFD 1173's image-gen slot returns.
- **bitsandbytes** was pinned linux-64 in the pixi.toml; needs
  `win-64` added when the Windows pipeline is real.
- **Hailo track stays parked** — 3090 does not fill the Linux/DFC
  gap, and there is still no Hailo hardware.

The Mac-mini shipping path stays as the small-machine reference:
Qwen3-VL-4B MLX 4-bit + EditScore LoRA verified running in 1.9s per
first token, 3.4 GB total. That path does not need the 3090.

Related: [[editscore-qwen3vl-mlx-works]], [[vast-api-notes]],
[[rfd-2156-retraction-trail]].
