# RFD 1027 details: the tier table, staging, quantization, what to do

## Tier per model

A tier must hold the weights and the activations together. Format is
QAFT 4-bit where upstream ships one; bf16 otherwise. Peak is the
resident weight set, which is smaller than total for staged models.

| Model                                | Format | Weights |    Peak | Tier  |
| ------------------------------------ | :----: | ------: | ------: | ----- |
| Gemma-4-12B (reasoning core)         |  Q4_0  |  6.6 GB |  6.6 GB | 24 GB |
| Qwen3-TTS-12Hz-1.7B-Base             |  bf16  |  3.4 GB |  3.4 GB | 24 GB |
| pixal3d_image_to_textured_mesh       |  bf16  | 24.0 GB |  6.5 GB | 24 GB |
| trellis2_image_to_textured_mesh      |  bf16  |  8.0 GB |  8.0 GB | 24 GB |
| voxhammer_image_mesh_editing         |  n/a   |  0.0 GB |  0.0 GB | 24 GB |
| skintokens_auto_rig                  |  bf16  |  1.0 GB |  1.0 GB | 24 GB |
| kimodo_text_to_motion                |  bf16  |  0.6 GB |  0.6 GB | 24 GB |
| ASR panel (Voxtral, Whisper, ...)    |  bf16  |  ~3 GB  |  ~3 GB  | 24 GB |

Removed rows relative to the earlier draft: `qwen_q4_k_m_image_edit`
(Qwen-Image-Edit blocklisted); `krea2_turbo_text_to_image` (Krea 2
blocklisted); `seethrough_layer_decomposition` (See-Through checkpoints
blocklisted); `worldmirror2_reconstruct` + `triposplat_image_to_splat`
(RFDs 1051/1052 abandoned); `p3sam_mesh_segmentation` (P3-SAM
blocklisted, replaced by rf-detr-Seg per RFD 1168). VoxHammer's 0.0 GB
row is per RFD 1162 -- it holds no weights and inherits placement.

Every surviving model reaches a 24 GB card. That is the finding, and
it is the opposite of what this RFD first recorded.

## QAFT-first is the rule

QAFT 4-bit (quantization-aware fine-tuning) is preferred where
upstream ships one. Only Gemma ships true QAFT for the current stack;
Wan-VACE, Pixal3D, VoxHammer, MoGe-3 do not, per RFD 2139's 2026-09-01
survey. Those run at published precision (bf16) with staged loading.

CLAUDE.md's 2026-09-02 retraction of Condition 5 lifts the earlier
ban on quantised weights producing corpus data; PTQ (AWQ, GPTQ, NF4)
is now permitted where a QAFT release is not available, subject to
the four surviving conditions on generated synthetic.

## Staging is what makes the tier

Pixal3D holds 24.05 GB and peaks at 6.50 GB. Three stages run in
order, and each frees before the next loads. Without that staging it
would need an 80 GB card.

See-Through holds 9.82 GB and peaks at 5.13 GB, for the same reason.
RFD 1044 makes the load and the unload real actions, thus the peak is
a planning result.

A model image that loads every stage at once pays for a larger card every
second it runs.

## Quantization is standardized, not a cost choice

An earlier draft framed quantization as a per-request cost knob
against Replicate pricing. Retracted: the workspace uses the local
desktop GPU only (CLAUDE.md; Replicate is not a host here), so there
is no per-second price signal to trade against quality. The
standardization is QAFT 4-bit where upstream publishes one, bf16
otherwise. See the QAFT-first rule above.

## What to do

- Size each model alone. A set total means nothing here.
- Stage the loads, and report the peak and not the sum.
- Prefer bf16 over fp16 where a checkpoint offers both. The memory is
  the same, and bf16 carries the wider exponent range.
- Add the activation peak for the resolution and the batch size of
  each job. The tiers above count weights only.
