# RFD 66606.1.1.1173 details: recreating an omni-modal model with a diffusion backbone

The target is the Qwen3-Omni architecture — text, image, and audio
in a single model — with the autoregressive thinker replaced by
LLaDA-o's diffusion backbone. The thinker-talker split is the key
architectural feature: the thinker reasons over all modalities, and the
talker converts the thinker's hidden states to speech. Replacing the
thinker with a diffusion model changes the generation pattern from
sequential to parallel while keeping the talker interface.

## LLaDA-o (the thinker)

GSAI-ML/LLaDA-o. Apache 2.0, open weights, ungated. Text + image
understanding, text generation (block diffusion), image generation and
editing (VAE latent diffusion). The LLM backbone is 8B-class with MoE
generation layers; the full checkpoint (LLM + SigLIP ViT + VAE +
connector) is 31 GB at bf16 across 10 sharded safetensors.

The text generation path uses `chat_block()`: block-diffusion with a
KV cache, iterative unmasking with confidence-based token transfer,
EOS-terminated. The image editing path uses the VAE through an
`InterleaveInferencer`. Both paths share the LLM backbone.

Upstream pins torch 2.5.1 and transformers 4.49.0. The model code is
vendored (not loaded via `trust_remote_code`), so compatibility with
our torch 2.11 / transformers 5.16 depends on which internal APIs
changed. The known risk areas are `Cache`, `DynamicCache`,
`AttentionMaskConverter`, and `_prepare_4d_attention_mask`.

- https://huggingface.co/GSAI-ML/LLaDA-o
- https://github.com/ML-GSAI/LLaDA-o

## Qwen3-Omni talker (the audio head)

Qwen/Qwen3-Omni-30B-A3B-Instruct. Apache 2.0. The "talker" component
generates speech tokens from the thinker's hidden states, decoded to
audio via a flow-matching vocoder. Disabling the talker saves ~10 GB,
so the talker alone is roughly that size. Voice cloning is the feature
that distinguishes it from standalone TTS.

The architecture question: the talker expects a causal stream of hidden
states from the thinker — one state per step, left to right. A
diffusion thinker produces all positions at once. Two adaptation paths:

1. **Adapter projection.** Train a small MLP that maps LLaDA-o's
   hidden states (produced all at once, 4096-dim) to the talker's
   expected format (sequential, likely 3584-dim for the 30B thinker's
   A3B hidden size). The diffusion model's final-pass hidden states
   are ordered by position, so they can be fed left-to-right to the
   talker even though they were produced in parallel.

If the talker cannot be extracted standalone, the audio head is
deferred rather than substituted with a standalone TTS model.

- https://github.com/QwenLM/Qwen3-Omni

## Pixal3D→VoxHammer (the 3D stage)

LLaDA-o generates and edits images; the 3D stage turns those images
into meshes. Pixal3D produces a coarse textured mesh from an image,
VoxHammer refines it. The two are sequential, not concurrent, so they
swap in and out of VRAM rather than co-residing with the thinker.

OmniGen2 was considered for this slot. It overlaps with LLaDA-o's
own image generation and editing, and RFD 66606.1.1.1145 already
places it in the evaluation loop. The 3D stage fills a gap nothing
else covers: image→mesh is the step that produces geometry for
rigging and animation.

## EditScore evaluation

EditScore/EditReward-Bench: 2,890 samples across 12 task types and 3
dimensions, each carrying an input image, an edit instruction, and
multiple scored output images. The benchmark evaluates image editing
quality — how well the edit follows the instruction while preserving
unmodified regions.

EditScore/EditScore-Reward-Data: 97,300 training samples for reward
models that score edit quality. Not used for LLaDA-o evaluation
directly, but available if we train a reward model to automate scoring.

- https://huggingface.co/datasets/EditScore/EditReward-Bench
- https://huggingface.co/datasets/EditScore/EditScore-Reward-Data

## VRAM budget on the 3090

| component                  | bf16     | NF4 est.  | co-resident? |
| ---                        | ---:     | ---:      | :---:        |
| LLaDA-o full               | 31.0 GB  | ~9.3 GB   | always       |
| Qwen3-Omni talker (if extractable) | ~10 GB | ~2.5 GB | always |
| Pixal3D                    | TBD      | TBD       | swap         |
| VoxHammer                  | TBD      | TBD       | swap         |
| peak activation             | varies   | varies    | —            |

LLaDA-o NF4 + Qwen3-Omni talker NF4: ~11.8 GB, fits if the talker
can be extracted. The 3D models swap into the remaining ~12 GiB
when needed. LLaDA-o bf16 + anything: does not
fit 24 GiB. CPU offload is blocklisted (the CPU as a model execution
target), so NF4 is the desk path and bf16 requires a rented 40+ GiB
card.

NF4 is permitted here because condition 5 bars quantized weights from
corpus generation, not from evaluation or interaction. The text sweep measured NF4 text quality across step counts
(2026-08-31, RTX 3090, VRAM 9.4 GiB peak):

| steps | valid tokens | wall s | tok/s | coherent | relevant |
| ---:  | ---:         | ---:   | ---:  | :---:    | :---:    |
| 128   | 64           | 5.76   | 11.1  | Y        | Y        |
| 64    | 64           | 23.52  | 2.7   | Y        | Y        |
| 32    | 64           | 6.30   | 10.2  | Y        | Y        |
| 16    | 48           | 7.23   | 6.6   | Y        | Y        |
| 8     | 64           | 9.95   | 6.4   | Y        | Y        |

All five passed. The negative control at steps=16 also passed, so
the quality gate is too loose — the coherence and relevance checks
accept degenerate output. The gate needs tightening before these
numbers carry weight. steps=64 is an outlier at 23.52s wall time;
the cause is not yet identified.

QAFT (quantization-aware fine-tuning) is permitted for training. A
QAFT model is trained with quantization in the loop, so the weights
are adapted to the lower precision rather than post-hoc truncated.
Condition 5 bars post-hoc quantized inference for corpus generation;
QAFT produces a model whose published precision is the quantized one.
This opens a path to a 3090-native LLaDA-o that fits 24 GiB and is
permitted for corpus generation, if the quality measurement holds.
