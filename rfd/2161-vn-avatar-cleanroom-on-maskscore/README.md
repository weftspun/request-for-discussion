# RFD 2161: Cleanroom Gemma-Avatar as a visual novel, on MaskScore

**State:** discussion
**Feature:** VN with location travel and prompt-driven talking-head
interactions, cleanroom-rebuilt on the RFD 1173 stack
**Scope:** taskweft, taskweft-godot-sandbox, weftspun-studio

## Decision

**Two-team cleanroom, role per model** (retracted from "one Qwen3-Omni
does everything"):

1. LLM + visual reward -> Qwen3-VL-4B MLX 4-bit + EditScore LoRA
2. TTS voice-clone -> ResembleAI/chatterbox
3. STT -> whisper-small (MLX); VAD -> silero
4. Viseme -> cleanroom small classifier
5. Renderer -> libgodot in BEAM (RFD 2154); Body -> ANNY + SOMA
6. Locations -> `6-datasource/{kenney,thebasemesh,quaternius}-stage`

Full retraction trail, stack table, Mac-mini smoke in `DETAILS.md`.

## Problem

Target uses Gemma + Cerebras + parakeet + Qwen3-TTS + MFCC-viseme +
Ready Player Me + Mixamo + three.js. Every piece has a substitute
here; Mixamo is CLAUDE.md-blocklisted.

## Compute

Reward-model role verified on Mac mini M2 Pro 32 GB, zero Vast (0.9s
load, 1.9s first token; 3.4 GB total). Operator moves to Windows 11
+ RTX 3090; 24 GB reopens QAFT-LoRA training on EditScore-Reward-Data
(97k rows, apache-2.0) and the Wan-VACE 14B slot without changing the
small-machine shipping path.

## Related

RFD 1173, RFD 2154, RFD 2160.

This RFD was drafted by an AI and read by a human before it shipped.
