# RFD 2183: MaskScore-driven layer decomposition on OmniGen2

**State:** discussion
**Feature:** SAM2/rf-detr-Seg mask + OmniGen2 reconstruction + MoGe-3 depth
**Scope:** layer decomposition rung of the gacha ladder

## Decision

Three license-clean, purpose-built steps:

- Mask: SAM2 or rf-detr-Seg (both Apache-2.0) from the composite.
- Reconstruction: new weights on OmniGen2 (Apache-2.0, Qwen-VL-2.5),
  MaskScore-driven (RFD 1173 edit-reward corpus), trained on
  multi-view renders of atelier-workshop-passed VRMs.
- Depth: MoGe-3 (MIT) per RFD 1102 (task catalog).

Replaces LayerDiff3D (See-Through's role) and RFD 1168's LaMa half;
rf-detr-Seg stays as segmentation. MaskScore's mask-reconstruct-score
loop fits natively: each layer IS a mask.

Corpus VRMs from the pipeline, `sphere_hammersley_sequence`
(CLAUDE.md); labels true by construction.

## Problem

See-Through's LayerDiff3D is closed both ways per BLOCKLIST.md.
`ask`: no grant on any weight; the new `seethroughv0.0.2_layerdiff3d`
labels apache-2.0 but a diffusion fine-tune does not cure SDXL's
CreativeML Open RAIL++-M. `adapt`: retraining on SDXL inherits it.

LaMa (RFD 1168's reconstruction substitute) is a patch inpainter and
cannot reconstruct hidden-layer content from surrounding pixels.

## Related

RFD 1168 (segmentation kept, LaMa superseded), RFD 1173 (edit-reward
corpus), RFD 1102 (task catalog), RFD 2136 (gacha ladder),
BLOCKLIST.md See-Through row.

This RFD was drafted by an AI and read by a human before it shipped.
