# RFD 2203 details: the row-shape tradeoff, the joint-count hook, and the RFD 1122 lineage

## The three row shapes and the axis they trade against

Three shapes considered; the axis is immutability versus label-scheme-agility.

**Vertex-only.** `image`, `camera`, `anny_posed_vertices (19158, 3)`. Training regresses labels
at batch time via `KeypointsRegressor.load_precomputed(wholebody133.pth)`. Label-scheme-
neutral: an anchor rework lands a new `.pth` without re-rendering. Two costs. The RFD 2196
viewer cannot render a keypoint overlay from vertex coordinates, so the dataset card carries
no visible label. And the `.pth` version becomes an implicit training-time dependency: which
labels did run X actually train against is not recorded anywhere the corpus can answer.

**Parquet-baked keypoints only.** `image`, `keypoints_2d (133, 3)`. Self-contained and
viewer-friendly; the dataset shows the labels. Freezes the current `wholebody133.pth`. Every
anchor rework forces a re-render, or at best a re-bake, and either is a new subset.

**Hybrid.** `image`, `camera`, `anny_posed_vertices`, `keypoints_2d` (baked at the `.pth`
hash), `soma_pose`, plus a per-shard manifest carrying the `wholebody133.pth` SHA-256. Cost is
one 133 × 3 float column per row (small next to a rendered image) and one manifest column.
Training can regress fresh from vertices when it wants the latest anchors or use the baked
column as the immutable comparison baseline; the viewer shows the baked column; an anchor
rework re-bakes as a new subset commit without touching images or vertices.

The hybrid dodges the tradeoff the two single-shape options force. Storage cost is real but
small; the alternative is either an unnavigable viewer or a re-render on every anchor rework.

## The SOMA pose column and its verification hook

The SOMA joint rotations that posed ANNY are the render input, so carrying them per row costs
nothing extra and lets the corpus feed RFD 1173's pose stub alongside the keypoints stub.
Column shape is `soma_pose (77, 3)` in axis-angle rotvecs as Kimodo emits them, verified at
the source: `anny/test/test_soma.py:242-283` shows Kimodo emits 77 joint rotations while
`anny.Anny(rig="soma", topology="soma")` takes 78 pose parameters, the 77 plus one root
identity prepended at index 0. RFDs 1102, 1173, and 2162's "78" and HERO's upstream "77" are
both true at different levels; task #76 back-ports the disambiguation.

The verification hook: the first subset render prints the observed count from the `.npz` and
records it in the manifest with an expected value of 77. A count mismatch surfaces there
rather than silently corrupting every subsequent frame's pose. The manifest column doubles as
the evidence source task #76 cites when it back-ports.

## The topology decision and the accuracy verification hook

`anny_posed_vertices` is `(19158, 3)` at the makehuman topology, built with `rig="soma"` +
`TopologyConfig(base_mesh="makehuman", remove_unattached_vertices=False)`. The `wholebody133.pth`
anchor weights index this topology; a shard whose vertex count differs is rejected by the
manifest gate, same shape as the SOMA joint-count hook.

Three vertex counts are shipped by anny's OBJs and are easy to confuse; the trap is named at
`anny-keypoint-anchors` README lines 63-67 for the first two, and this row adds the third:

| topology | source obj                     | vertex count |
| --- | --- | --- |
| makehuman | `legacy_default.obj`         | **19,158** |
| soma-wrap | `SOMA_wrap.obj`              | 18,056     |
| body      | `base_body.obj`              | 13,718     |

`topology="soma"` poses `SOMA_wrap.obj` at 18,056 vertices and `wholebody133.pth` cannot
index it. The SOMA rig reaches the makehuman mesh by barycentric projection onto `SOMA_wrap`
(`anny/src/anny/models/soma.py:84-125`). HERO re-verifies that projection's accuracy against
the direct `topology="soma"` path and records max/mean per-vertex displacement with household
anchors; if it lands worse than the direct path by more than a pencil (~7 mm), that becomes a
stated cost of choosing the makehuman topology for anchor compatibility. Under a pencil, the
projection is the row shape; the anchor compatibility justifies whatever the projection cost
is.

## The RFD 1122 lineage

RFD 1122 (`the-wholebody-gap`) originated the seven rules this corpus render follows, state
abandoned. The rules did not disappear; they are carried forward by their living carriers.

**Render the labels rather than annotate them.** Carried by this RFD: labels come out of the
camera arithmetic and the vertex positions rather than a human's clicks.

**Mix domains without mixing labels.** Carried by RFDs 1121 and 1126: domain (photograph,
sketch, ukiyo-e, corruption) rides on the image column, label rides on the vertex/keypoint
columns, the additive-subset labeling names the domain.

**Train one head on heterogeneous annotation.** Carried by RFD 1121: the head this corpus
feeds outputs 104 or 133 points; on a COCO photo only the 14 or 17 labeled ones score, on our
render all of them do.

**Verify before training, not after.** Carried by the verification hook above and by task
#76: a moved joint under a bad retarget is a label that lies, and the SOMA joint-count hook
catches it before any downstream frame is used.

**Evaluate where the labels are real.** Carried by CLAUDE.md's blinded-holdout rule: final
scoring uses `coco_person_commercial_val2017`, never any subset published under this RFD.

**Difference two renders rather than label one.** Carried by RFD 1123 for the pose-consensus
referee.

**The mesh is rung one, not the destination.** Carried by RFD 1121: garment layers come from
geometry rather than inference, and this corpus is the geometry-and-pose rung under them.

None of these should be cited as RFD 1122 itself; each has a living carrier that is not
abandoned. This RFD is one of those living carriers for the first rule.

## The publish path

RFD 2196 rule 5 as written: parquet shards under `data/`, row groups ≤ 300 MB, images
embedded as `struct<bytes:binary, path:string>`, no ETNF, LFS + `hf_transfer`, xet disabled
(`HF_HUB_DISABLE_XET=1 HF_HUB_ENABLE_HF_TRANSFER=1`), via `hf upload-large-folder` for the
per-file resumable commits the incremental-corpus doctrine requires.

HERO's `HF_XET_HIGH_PERFORMANCE` finding names a deprecation warning that is real but the
xet path itself is what RFD 2196 measured stalling at 6 KB/s on a 94 GB / 110 shard finalize;
deprecated is not removed. If the xet finalize behaviour improves and a later measurement
inverts the recipe, that is a revision to RFD 2196 rather than this one.

## What the first subset covers

To be settled with HERO in this RFD's review before the render begins: motion source (a walk
cycle set from the pose library), camera policy count (how many `sphere_hammersley_sequence`
views per pose), image resolution (256 × 256 is enough for the keypoints stub; higher costs
storage), split shape (train/val, no test — the test set is the blinded holdout, never
generated from). None of these change the row shape decision; they change what the first
subset's manifest records under motion source and sampler configuration.
