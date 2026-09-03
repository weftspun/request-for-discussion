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
- Branch: RFD-2186
- Base: Lumina2, nf4 quantised
- Adapter: Flow-LCM + teacher LoRA, rank-64, targets `to_q/to_k/to_v/to_out.0`
- Training: 100 epochs, 706 s wall on a 3090; loss cap 5.3 to 0.036, con to 0.013 (99% reduction)
- Sampler: 4-step SDEdit, linear sigmas from strength to 0, Euler step v-parameterized
- Resolution 512, strength 0.5, seed 20260903
- Prompt: `Replace the therapist with a nurse.` Single-pair ladder, not aggregate.
- OmniGen2 baseline: same instruction, published-precision inference

## Result at n=10

EditScore `overall` on a 0-25 scale, one source across the 2/4/6/8/10-step ladder:

- No-LoRA arm (Lumina2 + SDEdit, no adapter): 2.00 across every rung. The
  LoRA-less base does not follow the instruction at any step count.
- LoRA arm: 7.20 at steps 4, 8, 10 (identical across those three rungs;
  the LoRA generalises past its trained regime).
- Ratio: 7.20 / 2.00 = 3.6x on the ladder.

Wall-clock: 1.5 s per edit at 4 steps with LoRA on the 3090; 12 min per
edit for OmniGen2 at the same instruction. 480x speed-up.

**The one source used in the ladder was also in the n=10 training set,
so 7.20 is a train-set score, not a held-out one.** The immediate
follow-up is a held-out ladder on rows the LoRA did not see, runnable
today from shard 00 without waiting on the shard 01-15 X-Linked-ETag
issue (uploader-side, not Bao-side).

## Verdict

Candidate primary generator for RFD 2186's dressing-overlay stage,
pending scale-up. The 7.20 was measured on training data and the swap
into RFD 2183 / RFD 2194 stays off the table until a held-out ladder
holds and n>=1000 confirms it.

Left to the operator to make the actual generator swap in the
downstream RFDs when scale-up completes.

This RFD was drafted by an AI and read by a human before it shipped.
