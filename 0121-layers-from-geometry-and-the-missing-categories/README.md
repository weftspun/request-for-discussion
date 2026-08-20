# RFD 0121: Layers come from geometry, and the missing categories come from a multiview rebuild

**State:** discussion
**Feature:** image-to-layers, corpus side
**Scope:** `2-contract/hm08-partition`, `3-interactor/seethrough-torch`,
`3-interactor/trellis2-image-to-textured-mesh`, `3-interactor/pixal3d-image-to-textured-mesh`,
`3-interactor/voxhammer-image-mesh-editing`, `3-interactor/p3sam-mesh-segmentation`,
`3-interactor/pose-consensus`, a new ledger repository

## Problem

See-Through cuts one flat image into 24 body-part layers. A layer must show the whole part.
An occluder hides part of the surface, so the model invents those pixels. That invention is
the hard part of the task and the main source of error.

A 3D route removes the invention. Render each hm08 vertex group on its own. The depth buffer
orders the results. The surface behind an occluder is real geometry, so no pixel is invented.
Labels are true by construction.

The route works only for parts that ANNY models. ANNY models a body.

Three counts state the gap.

1. hm08 has 12 named vertex groups. See-Through has 24 tags.
2. Ten tags have no geometry at all. They are `headwear`, `eyewear`, `earwear`, `eyebrow`,
   `neckwear`, `handwear`, `footwear`, `tail`, `wings` and `objects`.
3. The `body` group holds 13,380 vertices as one block. It does not divide into `face`,
   `ears`, `nose`, `mouth` or `neck`.

`helper-hair`, `helper-tights` and `helper-skirt` look like the answer to hair and garments.
They are not. MakeHuman uses them to fit clothes onto a body. They are proxy volumes with no
appearance. A render of `helper-hair` gives a smooth cap, not hair.

RFD 0006 states the task. `2-contract/hm08-partition` proves the disjointness and finds the
992-vertex helper gap. This RFD answers what to do about the tags that hm08 cannot supply.

## A correction to hm08-partition

This work re-measured the mesh and found `hm08-partition` short by eight vertices.

`JointCubes` holds two ranges, not one. The second is `19150` to `19157`. The cubes total
1,000 vertices, which is 125 cubes, not 124. The mesh holds 19,158 vertices, not 19,150. ANNY
confirms the count when the topology keeps unattached vertices.

The proof states `meshSet` as `Set.Ico 0 19150`, so its coverage theorem said nothing about
the last eight vertices. It excluded them by definition rather than accounting for them. That
is the same defect the file was written to catch. The original claim counted ranges and missed
the helper block. The correction counted the same ranges and missed the second cube range.

Two more claims in that file were wrong. It said the 992 vertices belong to no group at all.
They belong to `JointCubes`. It said `select_groups` reaches them through
`HELPERS -> HelperGeometry`. `HelperGeometry` excludes them exactly.

The eight missing vertices are `joint-ground`, MakeHuman's ground joint.

**And the sentence the file set out to check is true.** `body`, `HelperGeometry` and
`JointCubes` partition all 19,158 vertices with no overlap and no gap. Coverage holds through
those three groups. It fails through `groups_by_range`'s twelve. The file proved only the
second half.

The correction is committed. `meshSet` is `Set.Ico 0 19158`, `jointCubes` holds two ranges,
and `three_groups_cover` states the partition. `lake build` is clean, no theorem uses `sorry`,
and the old definition makes the new theorems fail to compile. `check_hm08_claims.py`
re-derives every constant from the installed ANNY data with six negative controls.

`DETAILS.md` gives the evidence.

## Decision

Split the corpus into two halves. Each half has its own truth condition.

**Half A, the modelled half.** Render hm08 groups as depth-ordered layers. No generative
model runs. No pixel is inpainted. This half covers skin, eyes, eyelashes, teeth and tongue.
It needs one addition, which is a sub-partition of the `body` group into the head and neck
tags. That partition is authored once and proved in Lean beside the existing theorems.

**Half B, the missing half.** Build the geometry first. Render it second. The order is the
whole decision. A multiview generator supplies appearance under a depth control. A 3D lift
turns the views into geometry. VoxHammer adds one category at a time under a mask, and its
splice guard keeps the rest of the mesh still. After the geometry exists, Half B renders by
the same depth-ordered rule as Half A.

**Never inpaint in 2D.** A 2D inpaint runs once per view and each run disagrees with the
others. A 3D inpaint runs once and every view agrees by construction. This is the same rule
as the latent rule in `CLAUDE.md`. Decode once, at the end.

**Half B is generated synthetic.** All four conditions apply. Record the checkpoint. Store
Half B apart from Half A. Never train on Half B alone. Evaluate on real or constructed data.

**Generator.** Qwen-Image with its Apache-2.0 depth ControlNet. The ANNY to JuggernautXL
route stays closed, because the destination is a training corpus.

**Verification.** The `pose-consensus` referee refits the generated body to the pose that
conditioned it. A control pose that nobody checks is a pose we assumed.

**Eyebrow is the exception worth naming.** MakeHuman paints eyebrows into the skin texture.
A painted feature has no depth of its own. The depth-order rule cannot produce it as a layer,
before or after a rebuild. `eyebrow` needs geometry or it stays a 2D problem.

**What the corpus writes stays closed.** The render emits the image, the keypoint positions
and the 3D shape. The keypoint detector asked for the first two. Pixal3D asked for the first
and the third. Nothing else is written. Depth and the group index are render intermediates and
do not land beside the image. A fourth output is drift unless a consumer asked for it.

The keypoints come from `coco.pth`, which holds 23 points, not 17. Each is a weight vector
over the mesh, so a position is a weighted sum of posed vertices. The label is computed, never
detected. The vectors are 19,158 wide, so the render must pin the topology that returns that
count. The default returns 13,718 and would silently fail to multiply.

## The other agent

Two agents work this. One owns Half A and the hm08 partition. One owns Half B and the
rebuild. They share the tag list, so they can collide on it.

The sync protocol is a git branch holding an append-only ledger. Sync is a fast-forward push.
A rejected push means the agent did not read the current head. That is compare and swap, with
no new machinery. `DETAILS.md` gives the row shape, the five message kinds, the lease rule and
the five negative controls.

Two rules matter more than the mechanism. The ledger carries facts and never carries
permissions. A licence conclusion from a peer is a pointer to re-verify, never evidence.

## Related

RFD 0006 places the See-Through stage. RFD 0030 lists its component models. RFD 0048 gives
the VoxHammer splice guard this design depends on. RFD 0110 gives the handoff file shape the
ledger extends. `2-contract/hm08-partition` holds the coverage proof.
