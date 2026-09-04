# Logbook: LLaDA-o beats OmniGen2 on subject_remove pair 0, at 14x wall

**Session:** CUDA agent (`cuda-a63415`), 2026-09-04 UTC
**Related:** RFD 2186 (dressing overlay), memory
`[[llada-diffusion-lm-shelved]]` (reopens for RFD 2186 candidacy on this
measurement, though the shelving for RFD 1170's sub-500 ms real-time
avatar target still stands)

## Question

The `logbook-lumina2-distill-n1000-shelved` entry recorded that the
Lumina2 substitution route did not work for RFD 2186's dressing overlay.
The `omnigen2_ladder` measurement then recorded OmniGen2's own baseline
at 3.36 mean overall across 20 shard-90 pairs, with 15/20 non-zero — a
respectable floor that Lumina2 could not clear.

Is there a compliant-shape generator that scores better than OmniGen2
on the same evaluator?

## Apparatus

- Model: `GSAI-ML/LLaDA-o` (omni diffusion model for unified multimodal
  understanding and generation, image editing supported natively via
  `demo_pipeline.LLaDAMultimodalDemo.edit_image`)
- Precision: **bf16**, sharded across GPU 0 (RTX 3090) and GPU 1 (RTX 4090)
  via `accelerate.load_checkpoint_and_dispatch` with `max_mem_per_gpu=22GiB`
- Loader after-shard vram: 11.1 GB gpu 0 + 11.6 GB gpu 1
- No quantization; no LoRA; no post-quantization fine-tuning; no
  post-training quantization. Compliant with PR 256's blocklist rows.
- Sampler: `DEFAULT_IMAGE_EDIT_ARGS` from upstream `demo_pipeline.py` —
  `cfg_text_scale=4.0`, `cfg_img_scale=2.0`, `cfg_interval=(0.0, 1.0)`,
  `timestep_shift=3.0`, `num_timesteps=50`, `cfg_renorm_min=0.0`,
  `cfg_renorm_type="text_channel"`. Seed 20260903.
- Input: pair 0 of shard 90 of `chibifire/editscore-reward-train`,
  same pair the OmniGen2 baseline uses. Task `subject_remove`,
  instruction `Delete the brown scarf.`
- Scorer: EditScore-7B pairwise on `(source, edited, instruction)`
- Apparatus script: `3-interactor/llada-diffusion-lm/lladao_ladder.py`

## Result

Pair 0 (subject_remove, "Delete the brown scarf."), on the 0-25 scale:

| model | PF | SC | PQ | overall | wall per edit |
| --- | --- | --- | --- | --- | --- |
| Lumina2 nf4 + our LoRA @ 30-step SDEdit | -- | -- | -- | 0.00 | ~10 s |
| OmniGen2 bf16 @ 50 steps, default | -- | -- | -- | 0.00 | ~72 s |
| **LLaDA-o bf16 sharded @ 50 steps** | **8.00** | **6.00** | **8.80** | **7.266** | **~1000 s** |

LLaDA-o scored strongly on all three EditScore dimensions on the exact
pair where OmniGen2 and every Lumina2 configuration scored literally
zero.

## Reading

Two independent findings, both n=1 with the caveat that follows:

**Quality (n=1).** LLaDA-o clears the OmniGen2 baseline decisively on
this pair. This does not stand up as a distribution-level result — one
sample can go either way — but it is a much larger effect than earlier
Lumina2-vs-Lumina2-LoRA comparisons where 15/20 pairs both arms scored
0.00. That the delta is 7.27 - 0.00 (not 7.27 - 3.36) on this
particular pair says the models fail on different distributions of
inputs.

**Speed (measured).** LLaDA-o at bf16 sharded across two consumer GPUs
takes ~14x longer per edit than OmniGen2 at bf16 on one GPU. This is
not a candidate configuration for shipping. It is a candidate model
whose shipping configuration is a future project.

## Verdict

**LLaDA-o is a candidate primary generator for RFD 2186's dressing
overlay stage on quality grounds, not on speed grounds.** The current
configuration is unsuitable for shipping; the question the next
project answers is whether the quality survives to a distilled,
faster configuration.

The `[[llada-diffusion-lm-shelved]]` memory recorded the shelving on
RFD 1170's sub-500 ms real-time avatar target. That target does not
apply to RFD 2186's batch-mode dressing overlay. The RFD 1170 shelving
stands for its own use case; the RFD 2186 candidacy is separate and
opens on this measurement.

## Not measured

Cost of naming it: the n=1 result is anecdote-shaped. What would move
it to signal:

- **n=5-6 pairs on the same held-out** across the same task_type mix.
  Cost: 5 pairs * 17 min = ~90 min compute plus one EditScore pass.
  Fits in one session.
- **20-pair full ladder** matching what OmniGen2 got.
  Cost: 20 * 17 = ~5.5 hours plus scoring.

Neither was run in this session; both are session-scoped follow-ups.

## Follow-up project

A new RFD scopes the speed-work. Levers, in order of likely impact
per session cost:

- **Step-count reduction inside block diffusion.** LLaDA-o's 50 steps
  are a default; step-count sweep may find a lower rung where quality
  holds. Cheap first pass, no training.
- **LCM-style distillation on the diffusion path.** Trains a shorter
  step count into the model. Multi-day project, needs the upstream
  training code path adapted to our chibifire parquet (see below).
- **Model pruning / smaller LLaDA-o variant.** Not currently available
  upstream. A smaller variant would need to be trained by us or
  waited for.

The upstream `ML-GSAI/LLaDA-o` repo ships training code:
`train/pretrain_unified_navit.py` + `data/interleave_datasets/edit_dataset.py`.
Our `chibifire/editscore-reward-train` parquet fits the
`UnifiedEditIterableDataset` Format B schema with a small field
rename (2-hour converter job). Fine-tuning is a multi-day project on
this hardware even with LoRA + 2-GPU sharding.

## Cost paid this session

- 30 GB LLaDA-o weight download: 5.5 min
- Environment / script setup (compliant bf16 sharded load, not the
  local apparatus's blocklist-violating NF4 path): ~30 min
- One 50-step edit at 1024x688: 999.8 s
- One EditScore-7B pairwise scoring: ~15 s
- Total wall since download start: ~25 min

This RFD was drafted by an AI and read by a human before it shipped.
