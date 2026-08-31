# RFD 66606.1.1.1173: A multimodal diffusion pipeline

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

Two roles, two architectures. LLaDA-o's block diffusion measured
5.76s for 64 tokens; Qwen3-Omni streams from 234ms. A real-time
avatar demo (Gemma Avatar powers 9k+ robots) needs sub-500ms.
Diffusion does not stream.

**MaskScore corpus factory** (offline, batch): LLaDA-o as the
thinker. Masking IS its training objective. Constructs the
MaskScore training set and reward model data across all modalities.

**Avatar deployment** (real-time, streaming): Qwen3-Omni thinker-
talker architecture (or the Gemma Avatar pipeline: LLM + Qwen3-TTS).
RL fine-tuned with the MaskScore reward model.

    corpus      LLaDA-o (GSAI-ML)          Apache 2.0   MaskScore construction
    deploy      Qwen3-Omni architecture    Apache 2.0   real-time streaming
    3D stage    Pixal3D → VoxHammer        Apache 2.0   image → mesh
    scoring     MaskScore + EditScore      —             self-supervised reward

LLaDA-o NF4 (~9.3 GiB) is the desk path for corpus construction.
After QAFT, thinker + talker occupy ~11.8 GiB, leaving ~12 GiB
for the 3D stage to co-reside on one 24 GiB card.

## Related

RFD 66606.1.1.1172, RFD 66606.1.1.1166, RFD 66606.1.1.1170.
