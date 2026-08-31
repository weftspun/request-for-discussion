# RFD 1173 details: a multimodal avatar pipeline

The target is the Qwen3-Omni architecture — text, image, audio, and video
in a single model — serving both MaskScore dataset construction and a
real-time avatar demo (Gemma Avatar architecture, sub-500ms first-packet
latency). The thinker-talker split is the key architectural feature: the
thinker reasons over all modalities, and the talker converts the thinker's
hidden states to speech with voice cloning.

## Qwen3-Omni (thinker + talker)

Qwen/Qwen3-Omni-30B-A3B-Instruct. Apache 2.0, open weights. 30B MoE with
3B active parameters. Text, image, audio, and video input; text and audio
output. 234ms first-packet latency, streaming.

The thinker handles all input modalities and produces text and hidden states.
The talker converts hidden states to speech tokens, decoded to audio via a
flow-matching vocoder. Voice cloning is the feature that distinguishes it
from standalone TTS.

If the talker cannot be extracted standalone, the audio head is deferred
rather than substituted with a standalone TTS model.

- https://github.com/QwenLM/Qwen3-Omni

## Pixal3D→VoxHammer (the 3D stage)

Qwen3-Omni generates and edits images; the 3D stage turns those images
into meshes. Pixal3D produces a coarse textured mesh from an image,
VoxHammer refines it. After QAFT, the thinker + talker occupy ~11.8 GiB,
leaving ~12 GiB for the 3D models to co-reside.

OmniGen2 was considered for this slot. It overlaps with Qwen3-Omni's
own image generation and editing, and RFD 1145 already places
it in the evaluation loop. The 3D stage fills a gap nothing else covers:
image→mesh is the step that produces geometry for rigging and animation.

## EditScore evaluation

EditScore/EditReward-Bench: 2,890 samples across 12 task types and 3
dimensions, each carrying an input image, an edit instruction, and
multiple scored output images. The benchmark evaluates image editing
quality — how well the edit follows the instruction while preserving
unmodified regions.

EditScore/EditScore-Reward-Data: 97,300 training samples for reward
models that score edit quality.

- https://huggingface.co/datasets/EditScore/EditReward-Bench
- https://huggingface.co/datasets/EditScore/EditScore-Reward-Data

## MaskScore self-supervised training

MaskScore extends EditScore to all modalities via latent masking. Mask a
region of a latent, reconstruct with the stage's denoiser, decode both
original and reconstruction, score the decoded output. The original is
the ground truth — no human annotation needed.

SpeakingFaces (CC-BY-4.0, 142 subjects, 13k+ instances) provides
cross-modal ground truth: synchronized visual (768×512), thermal
(464×348), and audio at nine camera angles. The ANNY canonical rig
fitted to video frames recovers keypoints and encodes the 3D latent,
giving (face image, thermal, keypoints, voxel grid, waveform) tuples
per synchronized frame.

The four-stage loop:

1. Mask→reconstruct (denoiser pretraining, reconstruction loss)
2. Score decoded outputs (LPIPS, Chamfer, UTMOS, BLEU — automated)
3. Train reward model on automated scores
4. RL fine-tune with reward model

## VRAM budget on the 3090

| component                          | bf16     | NF4 est. | co-resident? |
| ---                                | ---:     | ---:     | :---:        |
| Qwen3-Omni thinker (30B MoE, 3B active) | ~30 GB | ~9.3 GB | always      |
| Qwen3-Omni talker (if extractable) | ~10 GB   | ~2.5 GB  | always       |
| Pixal3D                            | TBD      | TBD      | yes (QAFT)   |
| VoxHammer                          | TBD      | TBD      | yes (QAFT)   |
| activation overhead                | —        | 0.09 GB  | —            |

Activation overhead measured at 0.09 GiB across context lengths 32–1024
tokens (2026-08-31, RTX 3090, measured on LLaDA-o NF4 as a proxy — the
MoE activation pattern will differ). The KV cache and attention
activations are negligible at text-generation lengths; the budget is
almost entirely weights.

QAFT NF4 thinker + talker NF4 + activations: ~11.9 GiB, leaving ~12.1 GiB
for the 3D stage to co-reside. QAFT makes the NF4 precision the published
one, so the budget is real rather than a post-hoc truncation.

NF4 is permitted here because condition 5 bars quantized weights from
corpus generation, not from evaluation or interaction. QAFT produces a
model whose published precision is the quantized one. This opens a path
to a 3090-native Qwen3-Omni that fits 24 GiB and is permitted for corpus
generation, if the quality measurement holds.

## Why not LLaDA

LLaDA-o NF4 on the 3090 produced 64 tokens in 5.76 s at steps=128 —
25x slower than the sub-500ms avatar target. Block diffusion iterates
to convergence across the full block; an autoregressive MoE streams from
the first forward pass. The family (LLaDA-o, iLLaDA, LLaDA-1.5) is
blocklisted. The MaskScore technique transfers to Qwen3-Omni without
change — masking operates on latents, not on the model that fills them.
