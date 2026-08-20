# RFD 0122: The wholebody gap, and the renderer that closes it

**State:** discussion
**Feature:** wholebody keypoint detection, and the corpus that trains it
**Scope:** `3-interactor/rf-detr-cpp`, `6-datasource/rf-detr-keypoint-data`,
`6-datasource/dataflow-coco-gemx`, `3-interactor/pose-consensus`,
`3-interactor/pixal3d-image-to-textured-mesh`, `4-entities/anny-pose-retarget-work`

## Problem

We need a model that finds 104 body points in a picture. We have one that finds 17.

Nobody sells a licence-clean upgrade, so we have to train it. Training needs example pictures
with the 104 points already marked. Those do not exist either.

Both problems have the same answer. A renderer makes pictures with the answers already on
them.

## Decision

Build the renderer. It serves two consumers and nothing else.

**1. Render the labels rather than annotate them.** Pose the ANNY body and take a picture of
it. The 104 joint positions come out of the camera arithmetic. The 52 face-expression numbers
are whatever we set. The part outlines come from the mesh. Nothing is guessed, so no licence
applies to any of it.

Face-expression data is normally expensive. It needs a head-mounted camera rig and per-person
calibration. Here we typed the number in, so we already have it.

**2. Mix domains without mixing labels.** Restyle one render four ways. Qwen-Image-Edit makes
it photographic. CycleGAN makes ukiyo-e and Monet. Corruption comes from ordinary code, not
from asking a model for a corrupted photo, so we can set the severity and repeat it exactly.

All four share one render, so all four share one set of answers. Scraping cannot give that.
You never find one person drawn four ways with the layers already separated.

**3. Train one head on heterogeneous annotation.** The head outputs 104 points. On a real COCO
photo only the 14 points COCO labelled score, and the other 90 are masked out. On our render
all 104 score. Real photographs teach appearance. Renders teach where the other 90 points go.

**4. Verify before training, not after.** Restyling moves things. A moved arm makes the label
a lie. Every frame is checked against the render it came from, and failed frames are discarded
rather than repaired. A wrong label teaches the model to be wrong.

**5. Evaluate where the labels are real.** Final scoring uses the held-out real photographs
only. Score the 14 shared points and the 90 render-only points separately, so drift towards
renders appears in the numbers rather than hiding in an average.

## What the corpus writes

Three outputs, each named against the consumer that asked for it.

| output | consumer |
| --- | --- |
| the image | both |
| keypoint positions | the keypoint detector |
| the 3D shape | Pixal3D |

Nothing else is written. Depth, the camera matrix and the part index are render intermediates.
No second annotator runs. A fourth output is drift unless a consumer asked for it.

## Only two pieces do not exist

Everything else is built and licence-cleared. The renderer does not exist, and the masked
training run does not exist. `DETAILS.md` gives the full inventory.

## Corrections this RFD carries

The design was written against three numbers that were wrong. They are corrected here rather
than replaced quietly.

**The mesh is 19,158 vertices, not 19,150.** **The unassigned block is 1,000 vertices in two
ranges, not 992 in one.** That is **125** joint cubes, not 124.

**And the original claim was true.** `body`, `HelperGeometry` and `JointCubes` partition the
mesh with no overlap and no gap. Coverage fails only through `hm08_config.json`'s twelve
ranges. RFD 0121 records the measurement and `2-contract/hm08-partition` proves it.

## One claim is marked unverified

The plan says only the `anny` topology carries UVs, all 52 facial actions and the hm08 group
ranges, which makes the choice over-determined. We could not re-derive the UV half.

`anny.Anny(topology=TopologyConfig(base_mesh="anny"))` raises `FileNotFoundError` for
`anny/data/topology/anny.obj`, and that file does not ship. This matters more than a missing
measurement. The topology the whole corpus depends on does not load here.

A silent skip reads exactly like a pass, so this is named and counted rather than omitted.

## The cheapest thing that could change the plan

All 810 licence-clean motion clips are walking, running, turning and standing still. Drawings
of characters are rarely mid-stride. They sit, lean and pose.

Checking costs an afternoon and needs no renderer and no GPU. Project the 104 joints with the
camera arithmetic, draw the stick figure, and look at twenty of them. If a character artist
would not draw those poses, we author poses by hand instead, which the rules already allow.

Run this before building the renderer, not after.

## Related

RFD 0121 covers the layer route and the tags ANNY does not model. RFD 0028 gives the licence
gate the checkpoint survey applies. RFD 0016 catalogs the models named here.
