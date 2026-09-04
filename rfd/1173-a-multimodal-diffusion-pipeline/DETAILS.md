# RFD 1173 details: a multimodal avatar pipeline

This RFD was drafted by an AI and read by a human before it shipped.

The target is Gemma-4-12B as the shared VLM. Two roles sit on the
same weights: the avatar's text+image reasoning core, and the reward
model that scores the model's own generations via the EditScore
fine-tune (RFD 1157). Audio is a separate stack per RFD 1170's
presence loop (Qwen3-ASR-1.7B for input, Qwen3-TTS-12Hz-1.7B-
CustomVoice for output). Shared weights are what close the MaskScore
loop.

## Gemma-4-12B (the shared VLM)

google/gemma-4-12B-it-qat-q4_0-gguf. Apache 2.0, open weights, dense
(not MoE), text and image input, text output. Ships as a true QAT
Q4_0 checkpoint (~7 GB) directly from Google, so QAFT is upstream
rather than something this workspace has to produce (RFD 1027's
QAFT-first rule; RFD 2139's survey established Gemma is the only
current-stack model with a true QAFT release). Fits 24 GiB with
plenty of activation headroom.

EditScore (RFD 1157) fine-tunes on top of Gemma, so the same base
weights serve the avatar's understanding path and the reward model
that scores its own generations. The share-backbone argument
survives the Qwen3-VL -> Gemma-4-12B swap because it turns on
share-backbone, not on which backbone: the reward model IS the base
VLM under a fine-tune, not a separate model.

The audio path is orthogonal and lives in RFD 1170: Qwen3-ASR-1.7B
on device for input, Qwen3-TTS-12Hz-1.7B-CustomVoice on host for
output. Neither passes through the VLM.

1. https://huggingface.co/google/gemma-4-12B-it-qat-q4_0-gguf
2. https://github.com/QwenLM/Qwen3-VL  (the retracted earlier choice)

## Wan-VACE (image and video generation)

**Gemma-4-12B does not generate images.** Its outputs are text; it
takes images as input but produces none. Wan-VACE fills the image
and video generation slot Gemma leaves open. ~14B params, ~28 GB
bf16, ~8.7 GB NF4.

Wan-VACE is the generator that produces the images the 3D stage consumes
and the images MaskScore's image-editing stubs edit and score.

## Pixal3D→VoxHammer (the 3D stage)

Wan-VACE generates and edits images and video; the 3D stage turns
those images into meshes. Pixal3D produces a coarse textured mesh
from an image, VoxHammer refines it. Gemma-4-12B Q4_0 (~7 GB) leaves
~17 GiB of the 3090's budget for the 3D stage; with Wan-VACE NF4
(~8.7 GiB) swapped in for generation and out for the 3D stage, total
peak occupancy is ~15.7 GiB.

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
recovers keypoints and SOMA bone poses (77 rotation vectors as Kimodo
emits them, plus root translation and a root identity anny prepends at
index 0 to reach the 78 pose parameters anny takes at call time — both
counts true at different levels of the stack, per
anny/test/test_soma.py:242-283 and task #76's back-port; the fitted
poses are directly consumable by any downstream that accepts Kimodo
output, without running Kimodo itself). MoGe-3 produces metric
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

| component                    |    bf16 | Q4/NF4  | co-resident? |
| ---------------------------- | ------: | ------: | :----------: |
| Gemma-4-12B (VLM)            | ~24 GB  |  ~7 GB  |    always    |
| Wan-VACE (image/video gen)   |  ~28 GB | ~8.7 GB |   swapped    |
| Pixal3D                      | 24.0 GB |    n/a  |   swapped    |
| VoxHammer                    |  0.0 GB |    n/a  |   swapped    |
| activation overhead          |     n/a | ~0.1 GB |     n/a      |

Gemma-4-12B Q4_0 (~7 GB) is Google's own QAT release. On the 3090's
24 GiB, Gemma-4-12B Q4_0 + Wan-VACE NF4 co-resident totals ~15.7
GiB -- comfortable, no workspace-side quantization required.

An earlier draft named Qwen3-VL-4B (fp16 ~8.9 GB) as the VLM; the
Qwen3-VL-8B fp16 fallback (~16 GB) was also on the shortlist. Both
retracted per RFD 2169. The reason is not tier -- Qwen3-VL fits --
it is that Gemma-4-12B has a true upstream QAFT release and Qwen
does not, and the workspace standardized on QAFT-first (RFD 1027).

## Why not LLaDA

LLaDA-o NF4 on the 3090 produced 64 tokens in 5.76 s at steps=128,
25x slower than the RFD 1170 presence-loop sub-500ms target. Block
diffusion iterates to convergence across the full block; an
autoregressive VLM streams from the first forward pass. The family
(LLaDA-o, iLLaDA, LLaDA-1.5) is blocklisted. The MaskScore technique transfers to Gemma-4-12B (or any VLM)
without change. Masking operates on latents, not on the model that
fills them.
