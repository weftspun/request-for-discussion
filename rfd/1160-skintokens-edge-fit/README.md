# RFD 1160: SkinTokens fits at every precision

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/skintokens-auto-rig`

## Problem

SkinTokens auto-rig is 0.5 B parameters: 1.0 GB at bf16, 0.5 GB at
eight bits, 0.28 GB at four. Every precision fits inside 8 GB with
room to spare, so memory decides nothing here and the operator
question decides everything.

Its input is not an image. Auto-rig consumes a mesh and emits skin
weights, and a mesh has no fixed shape: vertex count varies per
asset, and the catalog caps it at 210,000.

A dataflow part compiles fixed shapes. A graph whose first dimension
is the vertex count of whatever arrives is the wrong shape for this
device, whatever its parameter count says.

## Decision

Abandoned on 2026-08-28. The accelerator work is scoped to
rf-detr keypoint and RFD 1157, and this scored 12 of 25 against RFD 1157's 18.

Rank SkinTokens low despite the comfortable fit, and say why in the
rank: it is variable-topology work, not fixed-resolution work.

Before dismissing it, check one thing. If the model tokenizes the
mesh to a fixed token budget, the graph after that point is fixed
and the variable part is host-side preprocessing. That would make it
a device half in the same shape as rf-detr's.

## Related

RFD 1033 separates the geometric algorithms, which scale with the
vertex budget rather than a parameter count. RFD 1131 cuts the
graph. RFD 1026 gives the memory.
