# RFD 2203: The first-subset row shape for the anny-soma keypoint corpus

**State:** discussion
**Feature:** the RFD 1173 keypoints stub, corpus render side
**Scope:** `6-datasource/anny-soma-corpus` (a new repository; creating it triggers a
`weftspun-keypoint` manifest PR on the 6-datasource side, owned by the GPU-grant holder)

## Decision

The first subset publishes a hybrid row: `image`, `camera`, `anny_posed_vertices` (19,158 × 3
float32, makehuman topology via `rig="soma"` + `remove_unattached_vertices=False`; a shard
whose vertex count differs is rejected by the manifest gate), `keypoints_2d` (133 × 3, baked
at the `wholebody133.pth` hash), `soma_pose` (77 rotvecs; anny prepends one root at call time), and a per-shard manifest carrying the
`wholebody133.pth` SHA-256, the observed SOMA joint count, the motion source, the sampler
configuration, and the render seed. Camera `sphere_hammersley_sequence` per CLAUDE.md.
Publish path RFD 2196 rule 5: LFS + `hf_transfer`, xet disabled, via `hf upload-large-folder`
for per-file resumable commits. Additive subsets and motion refinements each land as their
own commit set with the prior commit hash cited as retraction-in-place. Blinded holdout
untouched. `DETAILS.md` carries the tradeoff, the SOMA hook, the RFD 1122 lineage, and open
knobs.

## Problem

Task #67's living-dataset ANNY-SOMA corpus needs a schema pick before whoever holds the GPU
grant can render, and the pick closes the immutability-vs-agility tradeoff two single-shape
options force. Vertex-only rows are label-scheme-neutral but the RFD 2196 viewer cannot
overlay keypoints from vertices and the `.pth` version becomes an implicit training-time
dependency. Baked keypoints are viewer-friendly but freeze the current `.pth`; hybrid holds both.

## References

RFD 2196 (publish rules), RFD 1173 (multimodal pipeline), CLAUDE.md camera-sequence rule.

## Related

Rules originated in RFD 1122 (state abandoned), carried forward by RFDs 1121, 1123, 1126, 1128
and by CLAUDE.md. Consumer is task #65 (HERO's CUDA-only rescope). Anchor source is
`wholebody133.pth` at `weftspun/anny-keypoint-anchors` main. SOMA joint-count hook is task #76.

This RFD was drafted by an AI and read by a human before it shipped.
