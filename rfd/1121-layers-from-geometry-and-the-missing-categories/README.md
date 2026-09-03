# RFD 1121: Layers come from geometry, and the missing categories come from a multiview rebuild

**State:** discussion
**Feature:** image-to-layers, corpus side
**Scope:** `2-contract/hm08-partition`, and under `3-interactor/`: `seethrough-torch`,
`pixal3d-image-to-textured-mesh`, `trellis2-image-to-textured-mesh`, `pose-consensus`,
`voxhammer-image-mesh-editing`, plus garment-retarget and ledger repositories

## Decision

Split the corpus into two halves, each with its own truth condition. **Half A is the modelled
half.** Render hm08 groups as depth-ordered layers. Nothing generates and no pixel is inpainted.
It needs a `body` sub-partition into head and neck tags, proved in Lean. Clothing belongs here
too: hm08 carries tights, skirt and hair as proxies, cloth-fit retargets an authored garment onto
them without intersections under MIT, and a dressed render differenced against an undressed one
gives the layer exactly. The five absent worn tags want a proxy each.

**Half B is the missing half.** Build the geometry first and render it second; the order is the
whole decision. Qwen-Image supplies appearance under its Apache-2.0 depth ControlNet, a 3D lift
turns the views into geometry, and VoxHammer adds one category at a time under a mask. Never
inpaint in 2D, because each 2D inpaint runs once per view and disagrees with the next. Half B is
generated synthetic, so all four conditions apply, and `pose-consensus` refits it to its pose.

See `DETAILS.md` for the `hm08-partition` correction, the ten absent tags, the frozen vertex
order and its hash gate, the garment route, and the ledger protocol.

## Problem

See-Through cuts one flat image into body-part layers, and a layer must show the whole part. An
occluder hides the surface behind it, so the model invents those pixels, and that invention is
the main source of error. Rendering each hm08 vertex group on its own and letting the depth
buffer order them removes it, because the hidden surface is real geometry.

That route covers only what ANNY models, and ANNY models a body: hm08 has 12 named groups, ten
tags have no geometry, and `body` is one 13,380-vertex block with no face, ears, nose or neck.

## Related

RFD 1006 places the See-Through stage, RFD 1030 lists its models, RFD 1048 the VoxHammer splice
guard, RFD 1110 the handoff shape, RFD 1122 the keypoints that carry a layer between poses.
