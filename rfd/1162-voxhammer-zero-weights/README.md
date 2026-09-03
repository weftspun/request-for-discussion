# RFD 1162: VoxHammer holds no weights, so it inherits a placement

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/voxhammer-image-mesh-editing`,
`3-interactor/voxhammer-text-mesh-editing`

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and it was never scorable.

Do not rank VoxHammer as an acceleration candidate. Rank the
generator it edits, and let VoxHammer follow that placement.

Record the dependency rather than the size. An entry whose cost is
another entry's cost needs a named base, and RFD 1026's zero says
nothing about which. Name the generator, and VoxHammer's answer is
already written wherever that generator's answer is.

## Problem

Both VoxHammer entries carry 0 parameters in RFD 1026, and that is
published rather than unknown. They are editing methods over a base
generator, not models with weights of their own.

So the question this workspace has been asking of every other
candidate does not apply. There is no bf16 figure to compare, no
four-bit figure, and nothing to quantise. Asking whether VoxHammer
fits 8 GB has no answer, because the thing that occupies the memory
is whichever generator it edits.

`weftspun_image_to_world` is composite in the same way and inherits
the same reasoning.

## Related

RFD 1026 gives the zero. RFD 1016 lists both entries. RFD 1159 and
RFD 1154 hold the candidate generators.
