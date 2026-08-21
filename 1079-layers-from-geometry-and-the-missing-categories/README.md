# RFD 1079: Layers come from geometry, and the missing categories come from a multiview rebuild

**State:** discussion
**Feature:** image-to-layers, corpus side
**Scope:** `2-contract/hm08-partition`, and under `3-interactor/`: `seethrough-torch`,
`pixal3d-image-to-textured-mesh`, `trellis2-image-to-textured-mesh`, `pose-consensus`,
`voxhammer-image-mesh-editing`, `p3sam-mesh-segmentation`, plus a new ledger repository

## Problem

See-Through cuts one flat image into 24 body-part layers, and a layer must show the whole part.
An occluder hides the surface behind it, so the model invents those pixels, and that invention
is the main source of error. Rendering each hm08 vertex group on its own and letting the depth
buffer order them removes the invention, because the hidden surface is real geometry.

That route covers only what ANNY models, and ANNY models a body. hm08 has 12 named groups against
24 tags, ten have no geometry at all, and `body` is one 13,380-vertex block that does not divide
into face, ears, nose, mouth or neck.

## Decision

Split the corpus into two halves, each with its own truth condition. **Half A is the modelled
half.** Render hm08 groups as depth-ordered layers. Nothing generates and no pixel is inpainted.
It needs a `body` sub-partition into head and neck tags, proved in Lean.

**Half B is the missing half.** Build the geometry first and render it second. The order is the
whole decision. Qwen-Image supplies appearance under its Apache-2.0 depth ControlNet, a 3D lift
turns the views into geometry, and VoxHammer adds one category at a time under a mask. Never
inpaint in 2D, because each 2D inpaint runs once per view and disagrees with the next. Half B is
generated synthetic, so all four conditions apply, and `pose-consensus` refits the result to the
pose that conditioned it.

See `DETAILS.md` for the `hm08-partition` correction, the ten absent tags, the frozen vertex order
and its hash gate, and the ledger the two agents sync through.

## Related

RFD 1006 places the See-Through stage. RFD 101e lists its component models. RFD 1030 gives the
VoxHammer splice guard. RFD 106e gives the handoff file shape the ledger extends.
