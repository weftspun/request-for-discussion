# RFD 1154: Pixal3D fits only at four bits

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/pixal3d-image-to-textured-mesh`

## Problem

Pixal3D is 12.02 B parameters, the largest candidate that fits the
UGen300 at all. At bf16 it is 24.05 GB and at eight bits 12.02 GB,
against 8 GB of device memory. At four bits it is 6.61 GB and fits.

One precision reaches it and no other does. That makes RFD 1128 a
precondition rather than a refinement: if four bits do not hold for
this cascade, the model has no place on this device.

Nothing has compiled it. The operator question is unasked, and
Pixal3D is 480 times the size of the one graph this workspace has
put through the Dataflow Compiler.

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and this scored 10 of 25 against RFD 1157's 18.

Rank Pixal3D behind RFD 1128. Ask no operator question until four
bits have an answer, because a compile that succeeds at eight bits
answers nothing about the only configuration that fits.

If it is revived, take it up RFD 1129's ladder in order and stop at
translate. The 4-bit figure is derived from RFD 1026 at the 0.55
bytes per parameter its own Q4_K_M column implies, not measured, and
no Pixal3D artifact has been built.

## Related

RFD 1128 decides four bits. RFD 1129 asks whether operators compile.
RFD 1130 measures the device. RFD 1026 gives the memory.
