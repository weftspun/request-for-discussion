---
rfd: 1172
title: "RFD 1172: A diffusion LM does not land on the NPU"
state: "discussion"
feature: "where diffusion text generation runs on this desk"
scope: "the XDNA1 NPU in the 7840U laptop, and the dLLM candidates of 2026"
---

The strongest diffusion language model whose weights we could hold is
LLaDA2.1-flash, a 100B mixture of experts with 6.1B active parameters,
Apache 2.0 and ungated, with the best benchmark table any dLLM has
published. It does not run on the laptop's XDNA1 NPU, and neither does
anything in its class. The vendor's LLM flows require the 50 TOPS
XDNA2 generation; the one prototype flow that reaches Phoenix measured
2.3 tokens per second on the NPU against 7.8 on the CPU beside it; and
the single published NPU deployment of a dLLM anywhere needed a 45
TOPS phone accelerator plus an algorithm rewrite. The XDNA blocklist
row stands. If diffusion text generation earns a place here, it runs
on the 3090 or a rented GPU, with DiffusionGemma 26B-A4B and
LLaDA2.1-mini as the desk-card sizes.
