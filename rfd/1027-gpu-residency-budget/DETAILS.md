# RFD 1027 details: the tier table, staging, quantization, what to do

## Tier per model

A tier must hold the weights and the activations together. Format is
QAFT 4-bit where upstream ships one; bf16 otherwise. Peak is the
resident weight set, smaller than total for staged models.

### Reasoning + generation

| Model                            | Format | Weights |    Peak | Tier  |
| -------------------------------- | :----: | ------: | ------: | ----- |
| Gemma-4-12B (reasoning core)     |  Q4_0  |   ~7 GB |   ~7 GB | 24 GB |
| Qwen3-VL-4B (EditScore base)     |  bf16  |  ~9 GB  |  ~9 GB  | 24 GB |
| Wan-VACE 14B (image + video gen) |  bf16  |  ~28 GB |  ~8 GB  | 24 GB* |
| OmniGen2                         |  bf16  |   ~4 GB |   ~4 GB | 24 GB |

*Wan-VACE at bf16 exceeds 24 GB total; runs staged (encoder/UNet/decoder freed in turn) with peak ~8 GB. No QAFT release upstream (RFD 2139 survey).

### 3D + rigging

| Model                            | Format | Weights |    Peak | Tier  |
| -------------------------------- | :----: | ------: | ------: | ----- |
| Pixal3D (image -> textured mesh) |  bf16  | 24.0 GB |  6.5 GB | 24 GB |
| TRELLIS.2                        |  bf16  |  8.0 GB |  8.0 GB | 24 GB |
| VoxHammer (image -> mesh edit)   |  n/a   |  0.0 GB |  0.0 GB | 24 GB |
| MoGe-3 (metric depth)            |  bf16  |   ~1 GB |   ~1 GB | 24 GB |
| SkinTokens (auto rig)            |  bf16  |  1.0 GB |  1.0 GB | 24 GB |
| Kimodo (text -> motion)          |  bf16  |  0.6 GB |  0.6 GB | 24 GB |

VoxHammer's 0.0 GB row is per RFD 1162 -- it holds no weights and
inherits placement.

### Vision heads

| Model                          | Format | Weights | Peak    | Tier  |
| ------------------------------ | :----: | ------: | ------: | ----- |
| rf-detr / rf-detr-Seg          |  bf16  |  ~0.2 GB| ~0.2 GB | 24 GB |
| LaMa (AnimeMangaInpainting)    |  bf16  |  ~0.2 GB| ~0.2 GB | 24 GB |

### Voice (TTS)

| Model                          | Format | Weights | Peak    | Tier  |
| ------------------------------ | :----: | ------: | ------: | ----- |
| Qwen3-TTS-12Hz-1.7B-Base       |  bf16  |  ~3.4 GB| ~3.4 GB | 24 GB |

### ASR panel (12 tracks per RFD 2164)

| Model                          | Format | Weights | Peak    | Tier  |
| ------------------------------ | :----: | ------: | ------: | ----- |
| Voxtral Mini 3B (2507)         |  bf16  |  ~6.0 GB| ~6.0 GB | 24 GB |
| Whisper large-v3               |  bf16  |  ~3.0 GB| ~3.0 GB | 24 GB |
| Parakeet TDT 0.6B v3           |  bf16  |  ~1.2 GB| ~1.2 GB | 24 GB |
| wav2vec2-large-960h-lv60-self  |  bf16  |  ~1.3 GB| ~1.3 GB | 24 GB |
| ipa-whisper-small              |  bf16  |  ~0.5 GB| ~0.5 GB | 24 GB |
| ipa-whisper-base               |  bf16  |  ~0.2 GB| ~0.2 GB | 24 GB |
| WavLM Base+ SV                 |  bf16  |  ~0.1 GB| ~0.1 GB | 24 GB |
| allosaurus (uni/eng/rus)       |  bf16  |  ~0.1 GB| ~0.1 GB | 24 GB |

Panel runs in one container that loads/frees each track in turn per
RFD 1036's staging rule; peak is the largest single track (~6 GB).

Removed rows relative to the earlier draft: `qwen_q4_k_m_image_edit`
(Qwen-Image-Edit blocklisted); `krea2_turbo_text_to_image` (Krea 2
blocklisted); `seethrough_layer_decomposition` (See-Through checkpoints
blocklisted); `worldmirror2_reconstruct` + `triposplat_image_to_splat`
(RFDs 1051/1052 abandoned); `p3sam_mesh_segmentation` (P3-SAM
blocklisted, replaced by rf-detr-Seg per RFD 1168).

Every surviving model reaches a 24 GB card. Wan-VACE reaches it
staged; every other model reaches it flat.

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
