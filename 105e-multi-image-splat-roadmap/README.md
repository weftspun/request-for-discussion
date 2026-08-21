# RFD 105e: Multiple photos, routed by count, not by user choice

**State:** committed
**Scope:** `image-to-splat`, `image-to-world`, avatar mesh generation

## Problem

A single photo gives a weak splat and a weak mesh. More photos help
both, but only if the API and client agree on how many photos mean
which engine, and whether an avatar's mesh generation actually fuses
multiple views instead of using only the first.

## Decision

Three shipped phases, one shared contract. Phase 1: every splat,
world, and mesh request accepts an optional primary
`image_file_id` plus up to seven `reference_image_file_ids` (eight
images total); the client lets a user multi-select and mark one
thumbnail primary. Phase 2: mesh generation sets
`use_multiview_mesh: true` at two or more images, and the TRELLIS
adapters fuse those views instead of using only the first; a
"Use all photos for mesh" checkbox surfaces this once two or more
photos are attached. Phase 3: `image-to-splat` auto-routes by
count, not by user choice: one photo runs TripoSplat, two or more
runs WorldMirror 2.0 feed-forward 3DGS, with a COLMAP sparse
reconstruction as the fallback when WorldMirror is unavailable and
three or more photos are present.

See `DETAILS.md` for the per-phase field and status tables, the DGX
host setup, and what remains unshipped.

## Related

RFD 1059 gives HY-World 2.0's own, separate full-world pipeline,
built on the same WorldMirror dependency this RFD's Phase 3 uses.
RFD 1053 gives the rig contract a multiview mesh must still pass.
