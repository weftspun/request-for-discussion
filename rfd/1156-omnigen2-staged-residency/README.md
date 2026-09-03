# RFD 1156: OmniGen2 fits as stages, not as a pipeline

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/omnigen2`, `5-repository/omnigen2-base-df5dca8a`

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and this scored 13 of 25 against RFD 1157's 18.

Treat OmniGen2 as three placement questions, not one. Ask whether
the device can hold one stage and swap, and measure the transfer
that costs before choosing a precision.

Take the vae first. At 0.085 B it is the cheapest graph here, it is
a plain encoder-decoder, and it answers the operator question for
this family without committing to the 4 B transformer.

## Problem

OmniGen2 is three components on disk, measured rather than
estimated: a 15.87 GB transformer, a 15.02 GB mllm and a 0.34 GB
vae, stored at float32. That is 7.81 B parameters.

Resident together at eight bits they are 7.81 GB against 8 GB. The
arithmetic fits and the device does not, because nothing is left for
activations. At four bits they are 4.30 GB and the pressure lifts.

The components run in sequence. If they need not be resident at
once, the binding number is the largest single stage at 3.97 B,
which is comfortable at eight bits. Whether this part can stage
residency is unknown, and on a USB accelerator swapping a 4 GB stage
per invocation is the streaming case RFD 1130 exists to measure.

## Related

RFD 1130 separates resident from streaming. RFD 1026 gives the
catalog memory. RFD 1128 decides four bits.
