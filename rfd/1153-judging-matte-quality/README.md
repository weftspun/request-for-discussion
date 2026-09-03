# RFD 1153: Judging matte quality

**State:** published
**Feature:** matte evaluation

## Decision

Judging follows the field's standard benchmark. Rhemann et al., *A Perceptually
Motivated Online Benchmark for Image Matting* (CVPR 2009), derived error
functions from a 17-participant user study because SAD and MSE do not track human
judgement. Three of their decisions are adopted, each explaining one failure:

1. The judged artefact is a **composite onto a flat backing**, never raw alpha.
   Humans were never shown alpha, which is why the twin panel did worse.
2. Crops of **100x100 pixels at native resolution**, where alpha is uncertain.
   Whole downscaled photographs resolved nothing: edge error is invisible at
   448px.
3. Two categories scored separately: **connectivity** (detached fragments, holes)
   and **gradient** (oversmoothing, or false hard edges).

EditScore, configured as published, reproduces the ground-truth ordering of the
three backends; misconfigured it inverts it. It cannot pick between them on one
image, because it scores *edits* and three mattes of a photograph are
near-identical as edits. Use it where candidates differ semantically, and alpha
error where they differ by pixels of silhouette. `DETAILS.md` derives this.

## Problem

Background removal produced three candidate mattes per image and no way to say
which was broken. The available proxy -- soft-alpha pixels per silhouette
perimeter -- ranks model families but cannot judge one matte. Two attempts with
EditScore failed: whole images flattened onto grey scored near-constant within
each image, so the judge was reading the photograph rather than the cutout, and a
twin panel of cutout beside alpha returned exactly 8.00 for all eighteen.

## Related

RFD 1152 selects the background remover this judges. RFD 1006 covers layer
decomposition.
