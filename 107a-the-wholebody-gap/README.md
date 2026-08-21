# RFD 107a: The wholebody gap, and the renderer that closes it

**State:** discussion
**Feature:** wholebody keypoint detection, and the corpus that trains it
**Scope:** `3-interactor/rf-detr-cpp`, `6-datasource/rf-detr-keypoint-data`,
`6-datasource/dataflow-coco-gemx`, `3-interactor/pose-consensus`,
`3-interactor/pixal3d-image-to-textured-mesh`, `4-entities/anny-pose-retarget-work`

## Problem

We need a model that finds 104 body points in a picture. We have one that finds 17. Nobody
sells a licence-clean upgrade, so we have to train it, and training needs example pictures with
the 104 points already marked. Those do not exist either. Both problems have the same answer.
A renderer makes pictures with the answers already on them.

## Decision

Build the renderer. It serves two consumers and nothing else, under five rules.

1. **Render the labels rather than annotate them.** Pose the ANNY body and photograph it. The
   104 joints come out of the camera arithmetic, the 52 expression numbers are whatever we set,
   the part outlines come from the mesh. Nothing is guessed, so no licence applies to any of it.
2. **Mix domains without mixing labels.** Restyle one render four ways. Qwen-Image-Edit gives
   photographic and colour sketch, CycleGAN gives ukiyo-e and Monet, corruption comes from code.
   Two costs: two appearances share one model, and that path has no depth control.
3. **Train one head on heterogeneous annotation.** The head outputs 104 points. On a real COCO
   photo only the 14 COCO labelled score, on our render all 104 do. Renders teach the other 90.
4. **Verify before training, not after.** Restyling moves things and a moved arm makes the label
   a lie. Each frame is checked against its render, and a failure is discarded rather than fixed.
5. **Evaluate where the labels are real.** Final scoring uses the held-out real photographs only,
   scoring the 14 shared points apart from the 90 render-only ones.

See `DETAILS.md` for the corpus schema, the two costs, the checkpoint hash the packaged server
still owes, the corrected hm08 counts, the topology retraction, and the one check to run first.

## Related

RFD 1079 covers the layer route and the tags ANNY does not model. RFD 101c gives the licence
gate the checkpoint survey applies. RFD 1010 catalogs the models named here.
