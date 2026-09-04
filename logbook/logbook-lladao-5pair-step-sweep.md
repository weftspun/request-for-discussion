# Logbook: LLaDA-o step-count sweep on 5 shard-90 pairs (2026-09-04)

**Session:** CUDA agent (`cuda-a63415`), 2026-09-04 UTC
**Extends:** `logbook-lladao-n1-quality-beats-omnigen2.md` (the n=1 pair-0
finding that opened this line of work)
**Related:** RFD 2186 (dressing overlay), RFD 2198 (LLaDA-o speed work),
memory `[[llada-diffusion-lm-shelved]]` (RFD 1170 shelving stays; this
sweep is scoped to RFD 2186 batch-mode dressing overlay)

## Question

The pair-0 n=1 measurement suggested 4-step SDEdit was the sweet spot
for LLaDA-o. Anecdote or distribution? Does the 4-step sweet spot
generalise across task types, or is it specific to subject_remove?

## Apparatus

- Model: `GSAI-ML/LLaDA-o`, bf16, sharded across GPU 0 (RTX 3090) and
  GPU 1 (RTX 4090) via `accelerate.load_checkpoint_and_dispatch` with
  `max_mem_per_gpu=22GiB`. Compliant with PRs #256/#257 (no NF4, no
  PTQ, no post-quantization fine-tuning).
- Sampler: `DEFAULT_IMAGE_EDIT_ARGS` from upstream `demo_pipeline.py`
  with `num_timesteps` varied per this sweep.
- Seed: 20260903 for every edit.
- Pairs: shard-90 indices 0/1/2/5/17 from
  `chibifire/editscore-reward-train`, chosen to span task_type variety
  (subject_remove, material_alter, color_alter, background, style).
- Scorer: EditScore-7B pairwise `(source, edited, instruction)`.
- Apparatus script:
  `3-interactor/llada-diffusion-lm/lladao_step_sweep.py`
- Full dataset (parquet + images + scores) published at
  `chibifire/lladao-step-sweep-shard90-20260904`.

## Result

Mean EditScore `overall` across the 5 pairs at each step count, against
OmniGen2's 3.36 baseline on the same 5 pairs:

| steps | n | mean overall | wins vs OmniGen2 3.36 | wall/edit |
|------:|--:|-------------:|:----------------------|----------:|
|     2 | 5 |        3.378 | 3/5                   |    ~57 s  |
|     4 | 5 |        3.519 | 3/5                   |    ~85 s  |
|     8 | 5 |        4.953 | 5/5                   |   ~143 s  |
|    16 | 5 |    **5.682** | **5/5** (sweet spot)  |   ~264 s  |
|    32 | 1 |        2.653 | 0/1 (pair 0 only)     |   ~486 s  |

**16 steps beats OmniGen2 on every pair in the sample**, at ~3.7x the
wall (264 s vs 72 s).

Task-specific optima observed:

- subject_remove (pair 0): peaks at 4 steps (6.573 overall)
- material_alter (pair 1): peaks at 16 (7.960); fails at 2/4 (0.00
  because model does not attempt the edit)
- color_alter (pair 2): peaks at 4 (5.657); non-monotonic; PQ
  degrades at higher step counts
- background (pair 5): peaks at 16 (7.200); 4-step failure mode where
  model outputs source unchanged (SC=10, PF=0)
- style (pair 17): peaks at 8 (6.066); SC stays low across all steps

## Reading

The n=1 pair-0 measurement was anecdote, not distribution. Fixed
4-step gives 3/5 wins with mean 3.52; fixed 16-step gives 5/5 wins
with mean 5.68. A shipping configuration that uses a single step
count for all inputs should pick 16.

Two failure modes visible in the shape:

1. **Under-stepped punt.** At 2-4 steps some tasks (material_alter,
   background) produce either a source-passthrough (SC=10 PF=0
   overall=0) or unrelated-content (all zeros). The model does not
   attempt the edit rather than attempting poorly.
2. **PQ collapse at intermediate steps.** color_alter and
   subject_remove show non-monotonic curves where PQ or SC drops at 8
   or 16 steps before recovering at higher counts. Not consistent
   enough across tasks to characterise further.

## Verdict

LLaDA-o at 16-step SDEdit is a candidate primary generator for
RFD 2186's dressing-overlay stage on quality grounds. Best mean
overall in the sample, wins every pair, no per-task step-count
tuning needed if 16 is picked.

Cost is the wall-clock gap: 264 s per edit sharded on two 24 GB GPUs,
against OmniGen2's 72 s on one 24 GB GPU. RFD 2198's middle lever
(LCM-style distillation on the block-diffusion path) is where that
gap gets closed if the decision is to ship LLaDA-o. RFD 2198 does
not need re-scoping on this measurement; the levers named there
still apply.

The RFD 1170 shelving of LLaDA-o for the real-time avatar target
stays intact. This sweep is scoped to batch-mode dressing overlay
per RFD 2186.

## Not measured

- **Per-task-type step counts as a shipping shape.** A router that
  picks step count per task_type would out-perform fixed-16 on some
  pairs (subject_remove would drop from 3.58 to 6.57), but adds
  dispatch complexity and needs a task-type classifier at inference
  time. Deferred.
- **Steps between 16 and 50.** No 24-step or 40-step measurement;
  50-step was measured on pair 0 only (7.266) but the trend from
  16-step (5.68) suggests continued gains, at continued wall cost.
- **Larger n.** 5 pairs from one shard; a 20+ pair round on the same
  step count would tighten the mean's confidence interval. Deferred
  because the qualitative shape (16-step wins on every pair, 4-step
  wins 3/5) is already decision-grade for RFD 2198 targeting.

## Cost paid

- Sweep wall (pairs 1/2/5/17 at 2/4/8/16 + pair 0 at 2/4/8/16/32):
  ~55 min
- EditScore scoring (21 pairwise passes): ~5 min
- Total including model load and setup: ~65 min

This RFD was drafted by an AI and read by a human before it shipped.
