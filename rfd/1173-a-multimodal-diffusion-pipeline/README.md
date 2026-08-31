# RFD 1173: A multimodal diffusion pipeline

**State:** discussion
**Feature:** an omni-modal model with a diffusion backbone
**Scope:** `3-interactor/llada-diffusion-lm`, EditScore evaluation

## Problem

Qwen3-Omni is text + image + audio in one model, but its thinker is
autoregressive. LLaDA-o is text + image with a diffusion backbone.
The question is whether the omni-modal architecture can use a diffusion
thinker — keeping the audio head while gaining parallel generation.

EditScore is functionally complete in the NAND-gate sense: every
generation task reduces to an edit. One reward covers every modality.

## Decision

Recreate the Qwen3-Omni architecture with LLaDA-o as the thinker.

    thinker     LLaDA-o (GSAI-ML)          Apache 2.0   diffusion text + image
    talker      Qwen3-Omni audio head      Apache 2.0   voice-cloning speech
    evaluation  EditReward-Bench           —             universal edit scoring

LLaDA-o is 31 GB bf16. CPU offload is blocklisted; NF4 (~8 GB) is the
desk path. QAFT is permitted for training. The talker sizes like
Gemma 4 12B — it must fit one consumer card alongside the thinker.
If the Qwen3-Omni talker cannot be extracted standalone, the audio
head is deferred rather than substituted.

## What this does not decide

Whether the talker accepts hidden states from a different thinker
without retraining. The diffusion thinker produces all positions at
once; the talker expects a sequential stream. `DETAILS.md` carries
the two adaptation paths.

## Related

RFD 1172 (dLLM throughput), RFD 1166 (TTS), RFD 1170 (presence loop).
