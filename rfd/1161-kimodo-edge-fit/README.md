# RFD 1161: Kimodo is the smallest catalog model, and it is a decoder

**State:** discussion
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/kimodo-text-to-motion`

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and this scored 14 of 25 against RFD 1157's 18.

Read the sampling loop before ranking. One question settles this
model: does it emit its sequence in one pass or one step at a time.
If one pass, rank it high. It is small, its input is text rather
than a mesh, and it would be the cheapest whole model this workspace
could put on the device.

**Un-abandoned 2026-09-04.** RFD 2199 parked, zoo-DETR revive
rejected, vision-Hailo culled. Kimodo is the sole latency-critical
Hailo-10H track that fits. `nv-tlabs/kimodo` is "kinematic motion
diffusion": N sampling steps × per-step forward, not autoregressive
per-frame. Feasible slice at 20 steps × 5 ms on INT4. Rescore +
un-park scope in DETAILS.md.

## Problem

Kimodo text-to-motion is 0.3 B parameters: 0.6 GB at bf16 and 0.17
GB at four bits. It is the smallest model in the catalog and fits
the device many times over.

Size is not what decides it. Autoregressive per-step generation
carries the shape-grows-per-step obstacle every language model here
has against a compiler that emits fixed shapes. A fixed-length
latent expanded by a decoder is a fixed graph and a strong candidate.

## Related

RFD 1126 obstacle. RFD 1026 memory. RFD 2199 parked. RFD 1170 budget.

This RFD was drafted by an AI and read by a human before it shipped.
