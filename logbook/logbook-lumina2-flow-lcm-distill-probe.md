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
- Adapter: Flow-LCM + teacher LoRA
- Sampler: 4-step SDEdit
- Comparison target: OmniGen2 baseline at published-precision inference

## Result at n=10

- **EditScore:** 3.6× vs OmniGen2 baseline (higher is better on the
  ladder gate)
- **Wall-clock:** 480× faster than OmniGen2 at equal input size

n=10 is a probe. The number that would drive a swap is n≥1000 on
unseen edits; that measurement is blocked on the chibifire/editscore-
reward-train shards 01-15 X-Linked-ETag issue (uploader-side, not
Bao-side).

## Verdict

**Candidate primary generator for RFD 2186's dressing-overlay stage,
pending scale-up.** Not landed as the primary in RFD 2183 / RFD 2194
yet — n=10 is a probe, not a corpus-level result, and the 480× speedup
is decision-grade only after the n≥1000 result holds on unseen edits.

Left to the operator to make the actual generator swap in the
downstream RFDs when scale-up completes.

This RFD was drafted by an AI and read by a human before it shipped.
