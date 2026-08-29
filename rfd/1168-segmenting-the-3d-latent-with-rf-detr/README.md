# RFD 1168: Segment the 3D latent with rf-detr, and treat masking as corruption

**State:** ideation
**Feature:** layer decomposition without See-Through
**Scope:** `3-interactor/rf-detr-cpp`, `3-interactor/voxhammer-upstream`

## Problem

RFD 1166 dropped See-Through, so layer decomposition has no model. The
obvious 3D replacement is gone too: P3-SAM / Hunyuan3D-Part is
blocklisted on a territory-restricted licence.

## Decision

Segment in 3D, from parts already held. RF-DETR-Seg has a
`SegmentationHead` that `convert_segmentation_to_gguf.py` converts, so
the segmenter is the one model at rung 3. VoxHammer's
`extract_feature.py:96` projects per-view tensors onto voxel centres
with `F.grid_sample`, over the `sphere_hammersley_sequence` views
CLAUDE.md mandates. **The lift is that call with a different payload:**
class logits where DINOv2 patch tokens go now.

3D is the right place: `front hair` against `back hair` is a depth
relation, and a rendered view is where it is destroyed.

**Masking is corruption.** A layer is only a layer if it is whole, so
emitting `back hair` means restoring what `front hair` hid.

**LaMa fills the hole, and is the licence-clean half of See-Through** —
`dreMaz/AnimeMangaInpainting`, MIT over Apache-2.0, tuned for this
domain. It will not compile: its Fourier convolutions call `rfftn`, and
no Fourier operator is in `DEVICE_OPS`. CycleGAN is the opposite trade.

**Unbuilt.** `DETAILS.md` bounds the COCO classes and the resolution,
supplies the corpus from corrupt-clean render pairs, and gives two
tests costing no training.

## Related

RFD 1166 drops See-Through. RFD 1167 places rf-detr at rung 3.
