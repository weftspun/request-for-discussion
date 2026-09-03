# Logbook: Flow-LCM + teacher LoRA at 4-step SDEdit distillation from Lumina2 nf4

**Session:** CUDA agent (`cuda-a63415`) on the RFD-2186 branch
**Date:** 2026-09-03
**Related:** RFD 2183 (layer-decomp pipeline), RFD 2186 (dressing overlay, parked)

## Question

Can a distilled 4-step SDEdit pass on Lumina2 nf4 stand in for OmniGen2
at RFD 2186's dressing-overlay stage, and at what cost to EditScore?

## Apparatus

- `3-interactor/omnigen2/artifacts/lumina2-distill/train_flow_lcm_i2i_probe.py`
- `3-interactor/omnigen2/artifacts/lumina2-distill/ladder_gate.py`
- `3-interactor/omnigen2/artifacts/lumina2-distill/held_out_ladder.py`
- Branch: RFD-2186
- Base: Lumina2, nf4 quantised
- Adapter: Flow-LCM + teacher LoRA, rank-64, targets `to_q/to_k/to_v/to_out.0`
- Training: 100 epochs, 706 s wall on a 3090; loss cap 5.3 to 0.036, con to 0.013 (99% reduction)
- Sampler: 4-step SDEdit, linear sigmas from strength to 0, Euler step v-parameterized
- Resolution 512, strength 0.5, seed 20260903
- Prompt: `Replace the therapist with a nurse.` Single-pair ladder, not aggregate.
- OmniGen2 baseline: same instruction, published-precision inference

## Train-set result at n=10

EditScore `overall` on a 0-25 scale, one source across the 2/4/6/8/10-step ladder:

- No-LoRA arm (Lumina2 + SDEdit, no adapter): 2.00 across every rung. The
  LoRA-less base does not follow the instruction at any step count.
- LoRA arm: 7.20 at steps 4, 8, 10 (identical across those three rungs).
- Ratio: 7.20 / 2.00 = 3.6x on the ladder.

Wall-clock: 1.5 s per edit at 4 steps with LoRA on the 3090; 12 min per
edit for OmniGen2 at the same instruction. 480x speed-up.

The one source used in the ladder was also in the n=10 training set,
so 7.20 is a train-set score, not a held-out one.

## Held-out follow-up at n=10

Five unseen pairs from shard 00 (`skip=10`, matching the n=10 training
offset; task mix `color_alter` x3, `ps_human`, `motion_change`),
4-step SDEdit, same LoRA. EditScore pairwise on `overall`:

| pair | task          | no_lora | with_lora | delta |
|-----:|---------------|--------:|----------:|------:|
|    0 | color_alter   |    0.00 |      0.00 | +0.00 |
|    1 | color_alter   |    1.55 |      1.55 | +0.00 |
|    2 | color_alter   |    0.00 |      0.00 | +0.00 |
|    3 | ps_human      |    0.00 |      0.00 | +0.00 |
|    4 | motion_change |    2.00 |      0.00 | -2.00 |

Means: no_lora 0.71, with_lora 0.31. Ratio 0.44x (LoRA worse by 2.3x).
LoRA wins 0 of 5; one pair (`motion_change`) regressed 2.00 to 0.00.
At n=10 the LoRA memorised its training pairs and does not generalise.
`motion_change` is a video-shaped edit that single-image SDEdit cannot
produce at any n, so a fair scale-up should stratify by `task_type` and
exclude `motion_change` alongside the already-parked `text_change`.

## Verdict

**n=10 result does not survive held-out.** The train-set 7.20 was
single-source memorisation, and on unseen pairs the LoRA scored 0/5
against the no-LoRA baseline. Method not vindicated at this n.

The 100-epoch x n=10 configuration is the memorisation story: each
pair was seen 100 times, inverting the "large-n, few-epoch" shape
LCM distillation is built for. The n=1000 scale-up runs 2 epochs, so
each pair is seen twice.

Next: n=1000 training on `chibifire/editscore-reward-train` (dataset
reupload landed today, shard 01 verified clean, full snapshot in
flight). Stratify by `task_type`; exclude `motion_change`. If n=1000
held-out also fails at the recipe's own shape, Lumina2 distillation
is not the primary generator for RFD 2186's dressing overlay.

This RFD was drafted by an AI and read by a human before it shipped.
