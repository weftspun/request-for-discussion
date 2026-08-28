# RFD 1153: Judging matte quality

**State:** published
**Feature:** matte evaluation

## Problem

Background removal produced three candidate mattes per image and no way to say
which was broken. The available proxy -- soft-alpha pixels per silhouette
perimeter -- ranks model families but cannot judge one matte.

Two attempts with EditScore failed. Whole images flattened onto grey scored
near-constant within each image and varied between images: the judge read the
photograph, not the cutout. A twin panel of cutout beside alpha was worse,
returning exactly 8.00 for all eighteen while dropping consistency by 2.6 points.

## Decision

Judging follows the field's standard benchmark. Rhemann et al., *A Perceptually
Motivated Online Benchmark for Image Matting* (CVPR 2009), derived error
functions from a 17-participant user study because SAD and MSE do not track human
judgement. Three of their decisions are adopted, each explaining one failure:

1. The judged artefact is a **composite onto a flat backing**, never raw alpha.
   Humans in the study were never shown alpha, which is why the twin panel did
   worse rather than better.
2. Crops of **100x100 pixels at native resolution**, where alpha is uncertain.
   Whole downscaled photographs resolved nothing: a few pixels of edge error are
   invisible at 448px.
3. Two categories scored separately: **connectivity** (detached fragments, holes)
   and **gradient** (oversmoothing, or false hard edges).

EditScore is built to rank: best-of-N reranking and RL reward are its stated
applications. Both were tested and both failed, so it is given absolute per-crop
scores and the weaker task it manages, locating faults. See `DETAILS.md`.

## Related

RFD 1152 selects the background remover this judges. RFD 1006 covers layer
decomposition.
