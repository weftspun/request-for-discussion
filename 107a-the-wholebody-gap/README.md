# RFD 107a: The wholebody gap, and the renderer that closes it

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
it photographic and also makes a colour sketch. CycleGAN makes ukiyo-e and Monet. Corruption
comes from
ordinary code, not from asking a model for a corrupted photo, so we can set the severity and
repeat it exactly.

Colour sketch also uses Qwen-Image-Edit. It is Apache-2.0, already in the catalog, and needs
no training run and no new domain corpus.

Two costs come with that, and both are accepted rather than absent.

**Two of the four appearances now share one model**, so their errors correlate. Qwen's idea of
a hand appears in two domains rather than one, and the spread narrows to nearer three. Report
the two Qwen-derived domains together when scoring, because an average over four columns where
two share a model overstates the spread.

**This path has no depth control.** The interface takes an instruction and a strength, so
geometry preservation rests on `strength` alone. A low strength keeps the pose and barely
changes the picture. A high strength gives a real sketch and is free to move a limb. The
usable window is empirical and it may be empty. The default of 0.8 is high for this purpose
and should not be inherited.

`DETAILS.md` also records a change the packaged server needs. It returns no checkpoint hash, so
condition 1 is not satisfied on this path until it does.

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

| output             | consumer              |
| ------------------ | --------------------- |
| the image          | both                  |
| keypoint positions | the keypoint detector |
| the 3D shape       | Pixal3D               |

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
ranges. RFD 1079 records the measurement and `2-contract/hm08-partition` proves it.

## Retracted: the topology loads, and there was no blocker

An earlier version of this RFD marked the UV claim UNVERIFIED and said the topology the corpus
depends on does not load. **Both statements were wrong, and the error was mine.**

`TopologyConfig(base_mesh=...)` and the `topology=` spec string take different vocabularies.
`AlternativeTopology` is `smplx`, `smpl`, `soma`, `anny_from_soma`, `notoes` and three collapse
variants. `"anny"` is not in it. Passing `base_mesh="anny"` falls through to
`data/topology/anny.obj`, a file that was never meant to exist, so the error named a missing
asset rather than a bad argument. I read a packaging fault into an invalid argument.

The spec string works, and the claim re-derives exactly.

| call              | vertices | `texture_coordinates` |
| ----------------- | -------- | --------------------- |
| `topology="anny"` | 13,718   | (21334, 2)            |
| `topology="soma"` | 18,056   | `None`                |

The PBR bake is not blocked. Nothing in the package is missing.

**And the helper geometry was recovered.** `Anny.faces` is the body submodel, 27,420 triangles
reaching index 14741. `basemesh_face_to_vertex_table.json.gz` holds 18,486 quads reaching
19,157 and references all 19,158 vertices with none left over. Every group has faces, the hair,
tights and skirt helpers included.

## OpenUSD carries the topology, so the question cannot recur

RFD 1035 makes OpenUSD the internal format. The body now enters it at one point.
`2-contract/hm08-partition/export_hm08_usd.py` writes a layer with two prims.

    /Hm08/Basemesh   19,158 points, 18,486 quads, all 12 groups, partition
    /Hm08/Body       13,718 points, 27,420 triangles, UVs

Downstream stages compose against that layer rather than importing `anny`. A layer has one way
to be opened, so no stage has to know which loader path ships in which release.

`UsdGeomSubset` carries a `partition` family type and USD validates it. The property
`three_groups_cover` proves is now enforced by the data format. `groups_by_range` is written
as `nonOverlapping` on purpose, because the Lean file proves it is not a partition.

## The cheapest thing that could change the plan

All 810 licence-clean motion clips are walking, running, turning and standing still. Drawings
of characters are rarely mid-stride. They sit, lean and pose.

Checking costs an afternoon and needs no renderer and no GPU. Project the 104 joints with the
camera arithmetic, draw the stick figure, and look at twenty of them. If a character artist
would not draw those poses, we author poses by hand instead, which the rules already allow.

Run this before building the renderer, not after.

## Related

RFD 1079 covers the layer route and the tags ANNY does not model. RFD 101c gives the licence
gate the checkpoint survey applies. RFD 1010 catalogs the models named here.
