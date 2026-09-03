# Logbook: n=1000 Flow-LCM + teacher LoRA on Lumina2 nf4 — shelved

**Session:** CUDA agent (`cuda-a63415`), 2026-09-03
**Retracts:** the "candidate primary generator" hedge in the n=10 probe
entry `logbook-lumina2-flow-lcm-distill-probe.md`
**Related:** RFD 2186 (dressing overlay), RFD 2183 (layer-decomp pipeline)

## Question

Did the n=10 probe's memorisation failure hide a working method? If we
train with the shape LCM distillation actually calls for — large n, few
epochs — does the LoRA generalise?

## Apparatus

- `3-interactor/omnigen2/artifacts/lumina2-distill/train_flow_lcm_scale.py`
- `3-interactor/omnigen2/artifacts/lumina2-distill/held_out_ladder_parquet.py`
- Dataset: `chibifire/editscore-reward-train` (98 parquet shards, 109 GB
  local, downloaded 2026-09-03 after MPS Dataset's reupload)
- Training: 1800 pairs (200 per task-type across 9 non-parked types),
  2 epochs, 3600 steps, 2431 s wall on 3090
- LoRA: rank 64 on `to_q/to_k/to_v/to_out.0`, nf4 quantised base
- Excluded: `text_change` (already parked) and `motion_change` (video-shaped,
  single-image SDEdit cannot produce it at any n)
- Held-out ladder: 20 pairs from shard 90's parquet (provably outside
  training's coverage; training scanned shards 0-~20 to fill quotas)
- Sampler: 4-step SDEdit, strength 0.5, seed 20260903

## Result

Training converged cleanly:

- Loss `cap` 5.30 → 0.08 (99% reduction)
- Loss `con` → 0.02

Held-out ladder, 20 pairs, EditScore `overall` on the 0-25 scale:

- No-LoRA arm mean: **0.716**
- With-LoRA arm mean: **0.655**
- Ratio: **0.92×** (LoRA marginally worse, statistically indistinguishable
  at n=20)
- LoRA wins: **3/20** pairs (13 ties, 4 losses)

Per-task-type shape:

- 14/20 pairs both arms score 0.00. Background, tone_transfer, most
  color_alter — 4-step Lumina2 SDEdit does not produce EditScore-scoring
  edits and LoRA cannot rescue what the base cannot do.
- 3 pairs LoRA wins by exactly +2.68 (subject_remove ×2, color_alter ×1).
- 3 style pairs LoRA loses uniformly, 2.83 → 0.00. The LoRA is actively
  suppressing style edits, not just failing to add them.

## Reading

Not the memorisation failure of the n=10 probe — a genuine null. The
training recipe converged and matched LCM's large-n low-epoch shape; each
pair was seen exactly twice, not the 100 times that caused the earlier
overfit. What the LoRA learned nevertheless does not translate to
EditScore gains on unseen edits.

The mechanism failed: teacher-endpoint LoRA distillation fits the
consistency-plus-capability objective (loss dropped as expected), but the
objective does not map to EditScore movement at 4-step SDEdit inference.
The 480× wall-clock speedup vs OmniGen2 is still real, but only matters
if quality clears the no-LoRA baseline, and it does not.

## Verdict

**Lumina2 distillation via Flow-LCM + teacher-endpoint LoRA is not a
candidate primary generator for RFD 2186's dressing-overlay stage.**

Shelving the recipe. The "candidate primary generator, pending scale-up"
line in the n=10 probe entry is retracted by this measurement. The base
model (Lumina2) is not shelved — only this training recipe for it.

Left in place at
`3-interactor/omnigen2/artifacts/lumina2-distill/flow_lcm_scale_lora_r64/`
as a null-result artifact so a future attempt can inspect what a
2-epoch × n=1800 Flow-LCM run does converge to.

## Not tried (any is a new experiment, not a rescue of this one)

- Longer SDEdit sampling (`--steps 10` or `20`) — would erase the 480×
  speedup that motivated the exercise
- Higher SDEdit strength (0.5 → 0.7 or 0.9) — larger noise perturbation
- v-prediction target rather than x0 reconstruction
- Direct EditScore-in-the-loop objective
- Larger LoRA rank (128, 256) or additional target modules (MLP)

## Cost paid

- 45 min: full-dataset snapshot download (98 shards, 109 GB)
- 40 min: training wall (2431 s)
- ~25 min: held-out ladder (two model loads × 20 SDEdits + 40 EditScore
  passes)

This RFD was drafted by an AI and read by a human before it shipped.
