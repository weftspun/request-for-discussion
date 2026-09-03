# RFD 1161: Kimodo is the smallest catalog model, and it is a decoder

**State:** abandoned
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

## Problem

Kimodo text-to-motion is 0.3 B parameters: 0.6 GB at bf16 and 0.17
GB at four bits. It is the smallest model in the catalog and fits
the device many times over.

Size is not what decides it. Text-to-motion takes a variable-length
prompt and emits a variable-length motion sequence, and if it
generates that sequence autoregressively then it carries the same
obstacle as every language model here: a shape that grows per step
against a part that compiles fixed shapes.

If instead it emits a fixed-length latent that a decoder expands,
the generating graph is fixed and the model is a strong candidate.

Which of the two it is has not been read out of the code.

## Related

RFD 1126 names the control-flow obstacle. RFD 1026 gives the memory.
RFD 1004 catalogs the task.
