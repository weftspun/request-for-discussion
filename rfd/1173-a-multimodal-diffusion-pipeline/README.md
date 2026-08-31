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

Recreate the Qwen3-Omni architecture with LLaDA-o as the thinker.
The talker needs an adapter (4096→3584 dim MLP) because the diffusion
thinker produces all positions at once and the talker expects a
sequential stream; the adapter feeds the final-pass hidden states
left-to-right. If the talker cannot be extracted standalone, halt.

    thinker     LLaDA-o (GSAI-ML)          Apache 2.0   diffusion text + image
    talker      Qwen3-Omni audio head      Apache 2.0   voice-cloning speech
    3D stage    Pixal3D → VoxHammer        Apache 2.0   image → mesh (swap)
    evaluation  EditReward-Bench           —             universal edit scoring

LLaDA-o is 31 GB bf16. CPU offload is blocklisted; NF4 (~9.3 GB) is
the desk path. QAFT is permitted for training. The talker co-resides
with the thinker; the 3D models swap in when needed.

## Related

RFD 66606.1.1.1172, RFD 66606.1.1.1166, RFD 66606.1.1.1170.
