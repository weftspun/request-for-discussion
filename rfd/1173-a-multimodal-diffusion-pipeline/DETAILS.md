# RFD 1173 details: a multimodal avatar pipeline

The target is Qwen3-VL as the shared VLM: the avatar's text+image
reasoning core, and — via the EditScore LoRA that RFD 1157 records —
the reward model that scores its own generations. Audio is a separate
stack per RFD 1170's presence loop (Qwen3-ASR-1.7B for input,
Qwen3-TTS-12Hz-1.7B-CustomVoice for output). The shared-backbone
argument is what closes the MaskScore loop: reward and generator sit
on the same weights.

## Qwen3-VL (the shared VLM)

Qwen/Qwen3-VL-4B-Instruct. Apache 2.0, open weights, dense (not MoE),
text and image input, text output. 8.9 GB fp16 measured on the 3090
per RFD 2161; fits 24 GiB comfortably at fp16 without quantization.

EditScore (RFD 1157) is a LoRA over Qwen3-VL, so the same base weights
serve the avatar's understanding path and the reward model that scores
its own generations. The share-backbone argument is what Qwen3-VL
carries into RFD 1173 unchanged: the reward model IS the base VLM
under a LoRA adapter, not a separate model.

The audio path is orthogonal and lives in RFD 1170: Qwen3-ASR-1.7B on
device for input, Qwen3-TTS-12Hz-1.7B-CustomVoice on host for output.
Neither passes through Qwen3-VL.

1. https://github.com/QwenLM/Qwen3-VL
2. https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct

## Wan-VACE (image and video generation)

**Qwen3-VL does not generate images.** Its outputs are text; it
understands images as input but produces none. Wan-VACE fills the
image and video generation slot Qwen3-VL leaves open. ~14B params,
~28 GB bf16, ~8.7 GB NF4.

Wan-VACE is the generator that produces the images the 3D stage consumes
and the images MaskScore's image-editing stubs edit and score.

## Pixal3D→VoxHammer (the 3D stage)

Wan-VACE generates and edits images and video; the 3D stage turns those
images into meshes. Pixal3D produces a coarse textured mesh from an
image, VoxHammer refines it. Qwen3-VL-4B fp16 (~8.9 GiB) leaves ~15 GiB
of the 3090's budget for the 3D stage; with Wan-VACE NF4 (~8.7 GiB)
swapped in for generation and out for the 3D stage, total peak
occupancy is ~17.6 GiB and no QAFT is required.

## EditScore evaluation

EditScore/EditReward-Bench: 2,890 samples across 12 task types and 3
dimensions, each carrying an input image, an edit instruction, and
multiple scored output images. The benchmark evaluates image editing
quality: how well the edit follows the instruction while preserving
unmodified regions.

EditScore/EditScore-Reward-Data: 97,300 training samples for reward
models that score edit quality.

1. https://huggingface.co/datasets/EditScore/EditReward-Bench
1. https://huggingface.co/datasets/EditScore/EditScore-Reward-Data

## MaskScore self-supervised training

MaskScore extends EditScore to all modalities via latent masking. Mask a
region of a latent, reconstruct with the stage's denoiser, decode both
original and reconstruction, score the decoded output. The original is
the ground truth. No human annotation needed.

SpeakingFaces (CC-BY-4.0, 142 subjects, 13k+ instances) provides
cross-modal ground truth: synchronized visual (768×512) and audio at
nine camera angles. The ANNY canonical rig fitted to video frames
recovers keypoints and SOMA bone poses (78 bones, rotation vectors
plus root translation, the same format Kimodo-SOMA produces, so the
fitted poses are directly consumable by any downstream that accepts
Kimodo output, without running Kimodo itself). MoGe-3 produces metric
depth maps from the visual frames; Pixal3D encodes images to voxel
grid latents via the sparse structure VAE.

This gives (face image, depth, keypoints, pose, waveform) tuples per
synchronized frame, with voxel grids produced downstream by Pixal3D
from the image rather than from the ANNY fit.

The four-stage loop:

1. Mask→reconstruct (denoiser pretraining, reconstruction loss)
2. Score decoded outputs (LPIPS, Chamfer, UTMOS, BLEU; all automated)
3. Train reward model on automated scores
4. RL fine-tune with reward model

## VRAM budget on the 3090

| component                    |    fp16 |     NF4 | co-resident? |
| ---------------------------- | ------: | ------: | :----------: |
| Qwen3-VL-4B (dense)          | ~8.9 GB | ~2.9 GB |    always    |
| Wan-VACE (image/video gen)   |  ~28 GB | ~8.7 GB |   swapped    |
| Pixal3D                      |     TBD |     TBD |    swapped   |
| VoxHammer                    |     TBD |     TBD |    swapped   |
| activation overhead          |     n/a | ~0.1 GB |     n/a      |

Qwen3-VL-4B fp16 (~8.9 GB) is the RFD 2161 Mac mini measurement and
matches the model card's published size. On the 3090's 24 GiB,
Qwen3-VL-4B fp16 + Wan-VACE NF4 co-resident totals ~17.6 GiB —
comfortable, no QAFT required. The condition 5 quantization argument
that earlier drafts needed for a 30B MoE does not apply here.

Qwen3-VL-8B is the reserved fallback if 4B's reasoning falls short:
~16 GB fp16, ~6.75 GiB NF4 measured (RFD 1163). Either variant leaves
budget for a co-resident 3D stage in NF4.

## Why not LLaDA

LLaDA-o NF4 on the 3090 produced 64 tokens in 5.76 s at steps=128,
25x slower than the RFD 1170 presence-loop sub-500ms target. Block
diffusion iterates to convergence across the full block; an
autoregressive VLM streams from the first forward pass. The family
(LLaDA-o, iLLaDA, LLaDA-1.5) is blocklisted. The MaskScore technique
transfers to Qwen3-VL without change. Masking operates on latents,
not on the model that fills them.
