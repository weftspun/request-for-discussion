# RFD 1122: The wholebody gap, and the renderer that closes it

**State:** abandoned
**Feature:** wholebody keypoint detection, and the corpus that trains it
**Scope:** `3-interactor/rf-detr-cpp`, `6-datasource/rf-detr-keypoint-data`,
`6-datasource/dataflow-coco-gemx`, `3-interactor/pose-consensus`,
`3-interactor/pixal3d-image-to-textured-mesh`, `4-entities/anny-pose-retarget-work`

## Problem

We need a model that finds 104 body points in a picture. We have one that finds 17. Nobody sells
a licence-clean upgrade, so we train it, and training needs pictures with the 104 points already
marked. Those do not exist either. A renderer makes pictures with the answers already on them.

> TL;DR: I'm using AI tools to turn regular 2D pictures into 3D digital models or full-body pose skeletons, then training the system to make smart edits using a scoring system.

## Decision

The pose-library check has run and redirected the plan. All twenty sampled clips are upright
locomotion, so crouches and getups come from the gap corpus, which already sits in ANNY's SOMA
space — bone lengths agree to a stacked penny. The renderer is now first, under seven rules.

1. **Render the labels rather than annotate them.** Pose the ANNY body and photograph it. The 104
   joints come out of the camera arithmetic and the outlines from the mesh, so nothing is guessed.
2. **Mix domains without mixing labels.** OmniGen2 gives photographic and colour sketch, CycleGAN
   gives ukiyo-e and Monet, corruption comes from code. Two of the four share one model.
3. **Train one head on heterogeneous annotation.** The head outputs 104 points. On a real COCO
   photo only the 14 COCO labelled score, on our render all 104 do. Renders teach the other 90.
4. **Verify before training, not after.** Restyling moves things and a moved arm makes the label a
   lie. Each frame is checked against its render, and a failure is discarded rather than fixed.
5. **Evaluate where the labels are real.** Final scoring uses the held-out real photographs only,
   scoring the 14 shared points apart from the 90 render-only ones.
6. **Difference two renders rather than label one.** A body posed from the skeleton and one posed
   by an estimate differ in pose alone, so the difference is ground truth and AD gives its gradient.
7. **The mesh is rung one, not the destination.** The ladder ends at a clothed character, and
   garment layers come from geometry rather than inference. See `DETAILS.md` and RFD 1121.

## Related

RFD 1121 gives the layer route, RFD 1028 the licence gate, RFD 1016 the model catalog.
