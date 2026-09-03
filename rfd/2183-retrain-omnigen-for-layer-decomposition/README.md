# RFD 2183: MaskScore-driven layer-decomposition model on OmniGen2

**State:** discussion
**Feature:** OmniGen2 (Apache-2.0) base + MaskScore reward = layer model
**Scope:** layer decomposition rung of the gacha ladder

## Decision

Train new model weights on OmniGen2 (Apache-2.0 unified image
generator, Qwen-VL-2.5 foundation, both Apache-2.0) as the base,
driven by MaskScore (RFD 1173 edit-reward corpus) as the training
signal, on multi-view renders of atelier-workshop-passed VRMs.
Replaces LayerDiff3D (See-Through's role) and the rf-detr-Seg +
LaMa substitute in RFD 1168.

Depth stays with MoGe-3 (MIT, feed-forward) per RFD 1102 (task
catalog). Corpus: VRMs shipped by the pipeline, rendered under
`sphere_hammersley_sequence` (per CLAUDE.md); labels true by
construction. Constructed synthetic.

MaskScore's edit-and-reconstruct loop (mask a layer, reconstruct
from the composite, score against ground truth) fits layer
decomposition natively: each layer IS a mask over the composite,
so training reward and evaluation reward are the same signal.

## Problem

See-Through's LayerDiff3D is closed both ways per BLOCKLIST.md.
`ask` closed: weights carry no grant, and the new
`seethroughv0.0.2_layerdiff3d` labels apache-2.0 but a diffusion
fine-tune does not cure its base's licence; SDXL's CreativeML
Open RAIL++-M propagates. `adapt` closed: retraining on SDXL
inherits the same restrictions.

LaMa (RFD 1168's substitute) is a patch inpainter; layer
decomposition needs semantic reconstruction of the hidden layer,
which LaMa cannot supply.

## Related

RFD 1168 (rf-detr-Seg substitute; superseded), RFD 1173
(edit-reward corpus), RFD 1102 (task catalog), RFD 2136 (gacha
ladder), RFD 2178 (QAFT across stack), BLOCKLIST.md See-Through row.

This RFD was drafted by an AI and read by a human before it shipped.
