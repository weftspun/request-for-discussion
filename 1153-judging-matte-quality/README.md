# RFD 1153: Judging matte quality

**State:** published
**Feature:** matte evaluation

## Problem

Background removal produced three candidate mattes per image and no way to say
which was broken. The available proxy -- soft-alpha pixels per unit of silhouette
perimeter -- ranks model families but cannot judge an individual matte, and it
conflates genuine transparency with an unsure model.

Two attempts to judge with EditScore failed. Whole images flattened onto grey
gave scores that were near-constant within each image and varied between images:
the judge was reading the photograph, not the cutout. A twin panel showing the
cutout beside its alpha was worse, returning exactly 8.00 for all eighteen
cutouts while dropping consistency by 2.6 points uniformly.

## Decision

Judging follows the method of the field's standard benchmark rather than a format
chosen by us. Rhemann et al., *A Perceptually Motivated Online Benchmark for
Image Matting* (CVPR 2009), derived error functions from a 17-participant user
study, precisely because SAD and MSE do not track human judgement. Four of their
design decisions are adopted, and each explains one of our failures:

1. The judged artefact is a **composite onto a flat backing**, never a raw alpha
   channel. Humans in the study were never shown alpha. This is why the twin
   panel scored worse rather than better.
2. Crops of about **100x100 pixels at native resolution**, chosen where alpha is
   uncertain. This is why whole downscaled photographs could not resolve
   anything: a few pixels of edge error are invisible at 448px.
3. Two artefact categories, scored separately: **connectivity** (detached
   fragments, holes) and **gradient** (oversmoothing, or false hard edges).
4. Absolute per-crop scores for identification. The study's relative ranking is
   better for ordering, but ordering is not the task.

EditScore's role is to **identify, not to rank and not to repair**. It reports
which crops of which cutouts contain an artefact, so they can be looked at.

## Related

RFD 1152 selects the background remover whose output this judges. RFD 1006
covers layer decomposition.
