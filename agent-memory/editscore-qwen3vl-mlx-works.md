---
name: editscore-qwen3vl-mlx-works
description: "EditScore reward-model role runs on Mac mini via MLX at 3.4 GB, no training needed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T02:52:52.830Z
---

The visual-LLM reward-model role for RFD 1173's MaskScore loop
reduces to two apache-2.0 artifacts already published on HF, both
fitting easily on any 16+ GB machine:

    mlx-community/Qwen3-VL-4B-Instruct-4bit    3.1 GB   MLX 4-bit base
    EditScore/EditScore-Qwen3-VL-4B-Instruct   270 MB   peft LoRA (r=32)
                                                        base_model=Qwen/Qwen3-VL-4B-Instruct

Verified 2026-09-01 on Mac mini M2 Pro 32 GB:
- `scripts/smoke_editscore_mlx.py` in `3-interactor/editscore-lora-qwen3vl-4b/`
- Cold load: 0.9 s
- First token: 1.9 s
- Dummy 224x224 image + text -> single-token score

**Nothing needs training** for the reward-model role. The Track A
"QAFT-LoRA on Gemma-4-E4B for EditScore" project is unnecessary
because EditScore already published the LoRA over the same base
architecture. Skip re-doing that.

v0.1 uses the plain MLX base and reads its reward as an instruction-
follow answer. v0.2 merges the peft LoRA into an fp16 copy of the
base and re-quantizes to MLX; the merge is a one-shot job.

EditScore also published larger reward variants for when compute
allows: `EditScore/EditScore-Qwen3-VL-8B-Instruct` (400 MB LoRA),
`EditScore/EditScore-Qwen3-VL-32B-Instruct`, `EditScore/EditScore-7B`
(over Qwen2.5-VL-7B), `EditScore/EditScore-32B`, `EditScore/EditScore-72B`.
Same peft pattern, same apache-2.0 (except `-7B` which declares
license=None — reject).

Related: [[hardware-pivot-2026-09-01]], [[rfd-2156-retraction-trail]].
