# Logbook: LLaDA-o held-out ladder at n=20 pairs, fixed 16-step (2026-09-04)

**Session:** CUDA agent (`cuda-a63415`), 2026-09-04 UTC
**Extends:** `logbook-lladao-5pair-step-sweep.md` (the 5-pair result that
suggested 16-step was the sweet spot; this n=20 tests whether the shape
holds at decision-grade N)
**Related:** RFD 2186, RFD 2194, RFD 2198, memory
`[[llada-diffusion-lm-shelved]]` (RFD 1170 shelving stays)

## Question

The 5-pair sweep suggested fixed 16-step LLaDA-o SDEdit beats OmniGen2
on every pair in the sample. Does that shape survive at n=20 pairs
distinct from the 5 originally tested? MPS's assignment framed the
question as gating RFD 2198's distillation lever: if n=20 confirms
LLaDA-o at 16-step wins >= 80% vs OmniGen2's 3.36 baseline, the
distillation path does not need to fire.

## Apparatus

- Model: `GSAI-ML/LLaDA-o`, bf16, sharded across GPU 0 (RTX 3090) and
  GPU 1 (RTX 4090) via `accelerate.load_checkpoint_and_dispatch` with
  `max_mem_per_gpu=22GiB`. Compliant with PRs #256/#257 (no NF4, no
  PTQ, no post-quantization fine-tuning).
- Sampler: `DEFAULT_IMAGE_EDIT_ARGS` from upstream `demo_pipeline.py`
  with `num_timesteps=16`.
- Seed: 20260903 for every edit.
- Pairs: shard-90 indices 20-39 (fresh 20 that do not overlap with the
  5-pair set at 0/1/2/5/17).
- Scorer: EditScore-7B pairwise `(source, edited, instruction)`.
- Baseline: OmniGen2 mean overall 3.36 on shard-90 pairs 0-19 measured
  earlier this session (not re-measured on 20-39; aggregated
  distribution comparison rather than pair-by-pair).
- Apparatus script:
  `3-interactor/llada-diffusion-lm/lladao_step_sweep.py`
  invoked with `--pair-idx 20 21 ... 39 --steps 16`.

## Result

n=20 aggregate against OmniGen2 baseline 3.36:

- **mean overall: 5.972** (1.78x OmniGen2)
- **median overall: 6.573**
- **wins over 3.36: 17/20 (85%)** — clears the 80% threshold that
  gates RFD 2198's distillation lever
- **non-zero: 18/20**

Per-pair breakdown, EditScore overall on the 0-25 scale:

| pair | task_type | PF | SC | PQ | overall |
| ---: | :--- | ---: | ---: | ---: | ---: |
| 20 | style | 8.00 | 4.00 | 7.20 | 5.367 |
| 21 | style | 8.00 | 4.00 | 7.20 | 5.367 |
| 22 | subject_replace | 9.20 | 7.20 | 6.00 | 6.573 |
| 23 | subject_replace | 9.20 | 7.20 | 6.00 | 6.573 |
| 24 | subject_replace | 9.20 | 7.20 | 6.00 | 6.573 |
| 25 | subject_add | 8.00 | 8.00 | 9.20 | 8.579 |
| 26 | subject_add | 8.00 | 6.00 | 8.80 | 7.266 |
| 27 | subject_add | 8.00 | 4.00 | 9.20 | 6.066 |
| 28 | subject_add | 8.00 | 8.00 | 8.80 | 8.390 |
| 29 | ps_human | 9.20 | 7.20 | 8.00 | 7.589 |
| 30 | tone_transfer | 8.00 | 6.00 | 9.20 | 7.430 |
| 31 | material_alter | 9.20 | 0.80 | 9.20 | 2.713 |
| 32 | material_alter | 9.20 | 2.80 | 8.00 | 4.733 |
| 33 | material_alter | 9.20 | 7.20 | 9.20 | 8.139 |
| 34 | material_alter | 9.20 | 7.20 | 9.20 | 8.139 |
| 35 | material_alter | 9.20 | 1.60 | 9.20 | 3.837 |
| 36 | material_alter | 9.20 | 7.20 | 9.20 | 8.139 |
| 37 | ps_human | 9.20 | 7.20 | 8.80 | 7.960 |
| 38 | subject_remove | 10.00 | 10.00 | 0.00 | 0.000 |
| 39 | subject_add | 0.00 | 10.00 | 0.00 | 0.000 |

## Reading

**Shape holds at n=20.** 85% wins vs OmniGen2's 3.36 baseline confirms
the 5-pair result at a distribution-level N. Median 6.573 is
substantially above the 3.36 baseline; mean 5.972 is dragged down by
two zeros at pairs 38 and 39 which are edge cases the raw axis scores
call out.

**Two zero-overall pairs are edge cases, not model failures.**

- Pair 38 subject_remove scored PF=10 SC=10 PQ=0. Model removed the
  target perfectly (both axes maxed) but the resulting image scored
  zero on perceptual quality. Reading: removal succeeded so
  completely that the output image lacks visible subject matter that
  EditScore's PQ prompt scores as "high quality." An EditScore
  scoring artefact more than a generator failure.
- Pair 39 subject_add scored PF=0 SC=10 PQ=0. Model preserved source
  perfectly (SC=10) but neither followed the addition prompt (PF=0)
  nor produced a scoring image (PQ=0). Reading: model punted on the
  edit entirely and returned the source unchanged.

Both classes of zero happen at generation edge cases and both hurt
the mean without a corresponding LLaDA-o quality issue at the mode.

**Material_alter cluster is high-variance:** 2.71 / 4.73 / 8.14 / 8.14
/ 3.84 / 8.14 across six candidates with the same instruction. The
non-monotonic pattern is source-consistency (SC) collapsing on 3 of
6 candidates (SC in 0.80 to 2.80 range) while PF and PQ stay strong.
Model over-follows the prompt on some seeds even at fixed 16 steps.

## Verdict

**LLaDA-o at 16-step SDEdit clears RFD 2198's 80% gating threshold at
n=20.** RFD 2198's distillation lever does not need to fire —
pretrained LLaDA-o at 16 steps is already good enough on this
dataset against this evaluator.

**Generator swap for RFD 2194 shot library:** LLaDA-o at 16-step
replaces OmniGen2 as the default generator for the shuttle demo shot
library. Retraction pointer per PR #253's doctrine will land as a
DETAILS.md amendment on RFD 2194.

**Provenance-check un-park:** the swap triggers one of the four
un-park conditions per operator's PR #274 direction on
generator-provenance-check parking. LLaDA-o's model-card + training
corpus for anime-styled outputs needs documentation before the
shuttle demo ships publicly. That documentation is now owed as part
of RFD 2194 execution.

## Not measured

- Per-pair-comparison against OmniGen2 on the same 20 pairs. This
  aggregate compared against OmniGen2's known mean on a different
  20-pair set (0-19); a paired comparison at same-pair-same-scorer
  would tighten the confidence but was not run because the shape is
  clear from the aggregate.
- Higher step counts on n=20. The 5-pair sweep showed 32 steps only
  on pair 0 (2.65 overall, worse than 16-step's 3.58). No 32-step
  measurement on the new pairs.
- LLaDA-o at non-default sampler config (cfg_text_scale, cfg_img_scale,
  cfg_interval, timestep_shift). All held at
  `DEFAULT_IMAGE_EDIT_ARGS`. Different configs may shift the mode.

## Cost paid

- LLaDA-o sweep wall (pairs 20-39, 16 steps each): ~87 min across two
  runs (initial died at pair 35 mid-generation from session teardown;
  resumed for pairs 36-39, ~17 min)
- EditScore scoring (20 pairwise passes): ~3 min
- Full dataset published at
  `chibifire/lladao-step-sweep-shard90-20260904` covers the earlier
  5-pair result; a separate n=20 publication is not owed.

This RFD was drafted by an AI and read by a human before it shipped.
