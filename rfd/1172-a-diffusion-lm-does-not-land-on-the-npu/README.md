# RFD 1172: A diffusion LM does not land on the NPU

**State:** discussion
**Feature:** where diffusion text generation runs on this desk
**Scope:** the XDNA1 NPU in the 7840U laptop, and the dLLM candidates of 2026

## Problem

Diffusion language models generate text by unmasking a full sequence over
repeated denoising passes instead of decoding one token at a time. The
strongest one whose weights we could hold is LLaDA2.1-flash: a 100B mixture
of experts with 6.1B active parameters, Apache 2.0, ungated, with the best
benchmark table any dLLM has published (MMLU-Pro 76.6, HumanEval+ 89.6).
The question was whether it, or any dLLM, could run on the laptop's NPU.

## Decision

It cannot, and the XDNA blocklist row stands unchanged.

Three facts settle it, each sourced in DETAILS.md. The vendor's LLM flows
exclude this NPU generation: every supported path requires the newer 50 TOPS
part, and the one prototype flow that reaches ours measured 2.3 tokens per
second on the NPU against 7.8 on the CPU beside it. The inference pattern is
heavier than autoregressive decoding: bidirectional attention over the full
sequence, dozens of passes, no KV cache in the standard formulation. The one
published NPU deployment of a dLLM anywhere runs an 8B model on a phone
accelerator in the 45 TOPS class, and it rewrote the algorithm to get there.
Ours peaks at 10.

If diffusion text generation earns a place in this workspace, it runs on the
3090 or a rented GPU. DiffusionGemma 26B-A4B and LLaDA2.1-mini, both Apache
2.0, are the sizes that fit a desk card.

## References

- Candidate table, sources, and the throughput numbers: `DETAILS.md`
- The XDNA row in `BLOCKLIST.md` carries the standing toolchain argument.
