# RFD 1158: See-Through is the largest model that fits at eight bits

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/seethrough-layerdiff`

## Problem

See-Through layer decomposition is 4.9 B parameters: 9.8 GB at
bf16, 4.9 GB at eight bits, 2.70 GB at four. Eight bits fits with
3 GB to spare, which no larger candidate manages.

That headroom is the interesting property. Every model above it is
either four-bit-only or sits with nothing left for activations, and
today's failure on a 25 M graph was activation memory rather than
weights.

It is four checked-out components, not one: layerdiff, marigold
depth, vae and partseg. The 4.9 B figure is RFD 1026's estimate for
the task, and which components it counts is not recorded.

Its output is layers, and no real photograph carries a ground-truth
front-hair and back-hair split. So the blinded holdout validates the
pose pipeline and not this one.

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and this scored 15 of 25 against RFD 1157's 18.

It ranked first among the abandoned candidates, on headroom.

**LICENSING NOW, NOT FIT.** RFD 1166 dropped See-Through entirely: no
checkpoint it loads carries a grant, so the headroom above measures a
model that cannot be used.

## Related

RFD 1030 records the components. RFD 1026 gives the memory.
RFD 1129 asks whether operators compile.
