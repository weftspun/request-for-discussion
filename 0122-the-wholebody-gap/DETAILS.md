# RFD 0122 details: the checkpoint survey, the schema, and the inventory

## Why the head cannot be bought

| checkpoint | why it fails |
| --- | --- |
| Sapiens | CC-BY-NC, the exact class `filter_coco_licenses.py` drops |
| DWPose | Apache-2.0 weights, trained on UBody, distributed only behind a registration form |
| RTMW | the same UBody dependency, and not independent of DWPose, which distils from an RTMPose teacher |
| OpenPose | non-commercial academic licence, and CMU is blocklisted for provenance |
| AlphaPose | commercial use needs a separate licence |
| MediaPipe | Apache-2.0 and verified, but 33 plus 468 plus 42 landmarks, which is not a COCO-compatible wholebody head |

Five of the six fail on terms. The sixth answers a different question.

A permissive licence on the weights is not sufficient. A permissively licensed checkpoint
trained on a form-gated corpus re-exports terms nobody has read. DeepFashion is already
blocklisted for that pattern.

DWPose and RTMW are also not two opinions. RTMW supplies the teacher DWPose distils from, so
picking both gives one lineage wearing two names.

## The corpus schema

Essential Tuple Normal Form. Interned vocabularies, satellite relations rather than nullable
columns, no NULLs, no derivable columns.

Authored relations: `topologies`, `identities`, `bones`, `pose_rotations`, `rest_mesh`,
`constraints`. Emitted relations: `keypoints_2d`, `segmentation`, `depth_map`, `meshes`, each
reached by foreign key from `renders`.

Three attributes carry a decision rather than data.

**`rotation` is 3x2, not a quaternion and not 3x3.** A quaternion double-covers, so one
rotation has two tuples and the table would hold two rows for one fact. A 3x3 carries a third
column derivable as the cross product of the first two, which is a derivable column.

**`visibility` is int8, not bool.** Three separate reasons, and each alone is sufficient.

1. COCO has three states. Masked training must tell *not annotated* from *annotated as
   occluded*. A boolean cannot, so you skip the first and learn the second.
2. Multi-view labels are computed rather than annotated. Z-test each projected joint against
   the rendered depth. The answer is 2 for visible, 1 for projects inside the silhouette but
   fails the test, and 0 for outside the frame.
3. Real datasets guess at that middle state or omit it. A render knows it, and a boolean
   cannot carry the state that makes occlusion learnable.

**`topology_id` is a foreign key.** A `vertex_id` means nothing without it. The two ANNY
topologies share zero vertices, measured in both directions.

**Root translation is absent on purpose.** It follows from `constraints` and the chain, so
storing it would be a derivable column.

## Correspondence is 14 of 17, and it fails informatively

Shoulders, elbows, wrists, hips, knees, ankles and eyes map to ANNY bones. The nose and both
ears have no bone and need fixed mesh vertices. Those are topology-dependent, which is the
reason `topology_id` became a foreign key rather than a label.

Note the keypoint asset itself carries **23** points, not 17. `anny/data/keypoints/coco.pth`
is COCO-17 plus the six foot points. Each entry is a weight vector over the mesh that sums to
1, so a keypoint position is a weighted sum of posed vertices. The label is computed, never
detected.

The vectors are 19,158 wide, so the render must pin the topology that returns that count. The
default returns 13,718 and would fail to multiply.

## Layer extraction in 3D

Every piece is MIT and already packaged. They share one backbone, so the latent passes between
them without conversion.

| step | does | why it is that one |
| --- | --- | --- |
| Pixal3D | image in, SLAT out | it emits SLAT natively, so nothing is inverted. An ANNY-first order would pay a lossy `a_invert` on every use |
| fit ANNY | supplies the part semantics | Pixal3D gives geometry and not labels. A fitted ANNY carries hm08 groups, so masks come from the fit rather than from a segmentation model |
| mask by set operation | tokens, not meshes | `ANNY and Pixal3D` is body. `Pixal3D without ANNY` is garment or hair, because ANNY models anatomy and nothing else. No decode and no correspondence |
| VoxHammer | fills what was never seen | the 3D inpainter. It replaces LaMa rather than calling it |
| `a_splice` | preserves everything outside the mask | inversion is lossy, so without it every extracted layer perturbs the ones you did not touch |

**VoxHammer replaces LaMa because it is consistent across views.** A 2D inpaint answers for
one view. Fill behind the hair for a front view, then ask for a three-quarter view, and the
two disagree. A masked fill in the latent is one piece of geometry, so every view of it agrees.
See-Through's 2D path keeps LaMa, because there is no geometry to fill.

**The honest claim is smaller than it first sounds.** Where the image saw a surface and a
nearer layer covered it, 3D wins, because that content is rendered rather than invented. Where
nothing ever saw it, the back of a head being the obvious case, it is still invented. It is
invented earlier, by the reconstruction rather than by the inpainter.

Occlusion becomes rendering. Hallucination becomes verifiable. The second half is the real
gain. An inpainted patch cannot be checked against anything. A reconstructed surface can be
checked against a second view.

**Helmet hair removes the resolution problem.** Individual strands and one-pixel edges are the
cases a sparse latent cannot resolve, and they are out of scope by construction. What remains
is a front mass against a back mass, separated by the width of a head. That resolves, so there
is no densifying to 256 or 1024 and no retraining at a resolution the checkpoints never saw.
It is also what VRM and VR avatars already are.

**A hairline pixel holds two layers.** Split it fractionally so the alphas sum to one. That
leaves no seam and makes no choice. The soft rasteriser already computes this, because the
sigmoid of distance over temperature is fractional boundary coverage. Anti-aliased mattes come
free from the renderer built for the fit.

Bleeding is a separate and smaller thing. Dilate each layer's colour under its alpha, so
downstream resampling finds colour rather than background. One fills a layer's interior and
the other protects its edge. Both are called bleeding, which is how they get conflated.

**What this does not cover.** Multi-view refinement has to run before a 360 degree
decomposition is trustworthy. Until then the rear layers are confident fiction, and the greedy
version of that refinement is order-dependent by construction.

## What Pixal3D's toolkit demands

Read from `data_toolkit/README.md` rather than assumed.

| toolkit step | who does it | state |
| --- | --- | --- |
| download 3D assets | skipped, because ANNY is the asset | not applicable |
| process mesh, extract PBR | our renderer | build |
| render multi-view and cameras | our renderer | build |
| voxelize to O-Voxels | upstream | theirs |
| encode shape, PBR and sparse latents | upstream | theirs |

The last row is why decode-only still holds for us. Supplying geometry is not owning an
encoder.

**MakeHuman already has the material.** `node_trees/enhanced_skin.json` is a Principled skin
shader, a thin wrapper over a shader group. It drives Roughness with 3 references, Normal with
4 and Clearcoat with 2, and it sets Metallic nowhere, because skin is dielectric. `sss.png`
ships alongside it, with per-region maps for face, ears, lips, eyelids, fingernails and
toenails.

The toolkit wants a flat texture set and this is not one. So the job is a **bake**. Run the
node group once over the hm08 UV layout and write albedo, roughness and normal. Metallic is a
constant zero and needs no map. Bake once and reuse it in every render.

Do the bake in Blender. MPFB2 is a Blender addon, so the bake happens in the tool the material
was authored for rather than in a reimplementation of it.

The bake needs UVs, and they exist. `texture_coordinates` is (21334, 2) under
`topology="anny"`. An earlier version of this file called the bake blocked, which the section
below retracts.

## Retracted: the topology loads

An earlier version of this file marked the UV claim UNVERIFIED and reported that the topology
the corpus depends on does not load. Both were wrong. The retraction stays here beside what
replaces it.

`TopologyConfig(base_mesh=...)` and the `topology=` spec string take different vocabularies.
`AlternativeTopology` is `smplx`, `smpl`, `soma`, `anny_from_soma`, `notoes` and three collapse
variants. `"anny"` is not among them, so `base_mesh="anny"` falls through to
`data/topology/anny.obj`. That file was never meant to exist, and the resulting
`FileNotFoundError` names a missing asset rather than a bad argument. The failure mode invites
the wrong reading, and it got one.

The claim re-derives exactly through the spec string.

| call | vertices | `texture_coordinates` |
| --- | --- | --- |
| `topology="anny"` | 13,718 | (21334, 2) |
| `topology="soma"` | 18,056 | `None` |

The PBR bake is not blocked.

**The helper geometry was recovered too.** `Anny.faces` is the body submodel: 27,420 triangles
reaching vertex index 14741, and no higher under any of the eight combinations of
`eyes`, `tongue` and `nudity_edits`. Read as the whole mesh, it says `helper-hair`,
`helper-tights` and `helper-skirt` have no faces.

They do. `basemesh_face_to_vertex_table.json.gz` holds **18,486 quads** reaching **19,157**,
referencing all 19,158 vertices with none unreferenced. Every group has faces. A proxy surface
with no appearance is a different thing from absent geometry, and RFD 0121 means the first.

## OpenUSD is where the topology now lives

RFD 0053 makes OpenUSD the internal format. `export_hm08_usd.py` in
`2-contract/hm08-partition` is the body's entry point.

    /Hm08/Basemesh   19,158 points, 18,486 quads, all 12 groups, partition
    /Hm08/Body       13,718 points, 27,420 triangles, UVs (21334, 2)

The map between the two spaces is measured rather than assumed. `ref` is the ascending unique
index set of `Anny.faces`, the maximum positional difference between `basemesh[ref]` and the
body mesh is 0.0 exactly, so `body_index = searchsorted(ref, basemesh_index)`.

`UsdGeomSubset` carries a `partition` family type and USD validates it, so `three_groups_cover`
is enforced by the format rather than argued in a comment. `groups_by_range` is written as
`nonOverlapping` on purpose, because the Lean file proves it is not a partition.

Four negative controls ship with it. Two found real defects in the validator while being
written. A reused temporary filename handed each control the previous one's stage, because USD
caches stages by identifier, so three controls reported the second one's defect while all four
still printed FAIL. And `GetFamilyType` read the wrong prim, so relaxing the basemesh family
type to `unrestricted` was invisible and the layer validated while claiming no partition.

## Colour sketch: FastCUT, not CycleGAN and not CUT

The fourth appearance is a colour sketch. The tool is **FastCUT**, from
`taesungp/contrastive-unpaired-translation`. Three findings decided it, and one of them
disqualifies the obvious upgrade.

### Licence, read from the file

BSD-2-Clause, `Copyright (c) 2020, Taesung Park and Jun-Yan Zhu`, with CycleGAN's BSD text
concatenated below it. No non-commercial clause and no no-derivatives clause.

GitHub reports `NOASSERTION`, for exactly the reason the CycleGAN image already documents. Two
licence texts in one file defeat the detector. Read the file, not the badge.

### Full CUT is disqualified, and the reason is the feature

CUT drops cycle consistency and replaces it with a patchwise contrastive loss. That sounds
strictly better, and for our use it is not, because of what the authors themselves report:

> Our full method CUT has the flexibility to **enlarge the horses**, as a means of better
> matching of the training statistics than CycleGAN. FastCUT behaves more conservatively like
> CycleGAN.

Changing object size to match target statistics is the advertised advantage. It is also the one
behaviour a labelled corpus cannot tolerate. A stylizer that enlarges a body moves every joint,
and the keypoint label then describes a picture that no longer exists. The label becomes a lie
in the exact way step 4 exists to catch.

So the property that makes CUT better at translation makes it unusable here. Stated plainly
because the paper's headline result reads as a straightforward win.

### FastCUT against CycleGAN, on our criteria

| criterion | CycleGAN | FastCUT |
| --- | --- | --- |
| geometry | conservative | conservative, per the authors |
| licence | BSD, already cleared | BSD-2, read from the file |
| generator | ResNet-9block | the same, so the server and hash discipline carry over |
| training memory | baseline | about half |
| training time | baseline | about twice as fast |
| domain B | needs a corpus | **a single image suffices** |

The last row is the one that changes the plan. CUT supports single-image training, where each
domain is one image. A colour-sketch domain can therefore come from **one** licence-clean
sketch rather than from a sourced corpus.

That removes the blocker the previous version of this section spent most of its length on. The
cost was never the model. It was finding a licence-clean set of colour sketches, and a set of
one is a far easier thing to clear and to cite.

FastCUT is trained without the identity loss and with `lambda_NCE=10.0`. CUT uses the identity
preservation loss with `lambda_NCE=1`. The distinction is a training flag, `--CUT_mode FastCUT`,
so the wrong choice is one argument away and must be pinned rather than assumed.

### Was anything better available

Considered and not chosen, with the reason rather than a ranking.

**Exemplar transfer.** `AdaAttN` is Apache-2.0, verified by reading the LICENSE file, and takes
a style image at inference with no training at all. `CAST` is Apache-2.0 and `EFDM` is MIT.
Each removes the training run entirely. Each also adds a second code path and a second
checkpoint discipline for one style, and `AdaAttN`'s weights come from a personal drive link,
which is a pinning problem rather than a licence one. Worth revisiting if more styles are
wanted, because the marginal cost of style eleven is zero for an exemplar model and a training
run for FastCUT.

**A written filter.** Edge extraction, flat colour quantisation and a paper ground are
deterministic, so the output would be constructed rather than generated and would need no
licence at all. Rejected as the primary route for a stated reason. A filter looks like a
filter, so its domain shift is narrower than a drawn sketch, and a fourth domain that only
teaches the model about our own filter has not widened anything. It stays the fallback if
single-image FastCUT does not hold geometry.

**Diffusion restyling.** Rejected on common-mode grounds, which the CycleGAN image already
records. The photoreal branch is already Qwen-Image-Edit. Driving the stylised branch from the
same family would give every domain one set of texture statistics, hands and faces.

**`StyTR2`** stays excluded. It is the tool SDPose-OOD used for this exact job, and it carries
no licence.

### What must still be measured

FastCUT is conservative *relative to CUT*. That is a comparison, not a guarantee, and this
workspace does not accept a comparison as a bound. Run `pose-consensus`'s soft silhouette and
soft depth against the render each frame came from, and read the pose back with MediaPipe. A
style that moves a limb invalidated its own labels, whatever the authors report.

## What exists, and what does not## What exists, and what does not

| piece | note | state |
| --- | --- | --- |
| licence-clean mocap | 810 clips, CC-BY-4.0 and Apache or MIT, with `CITATION.cff` | exists |
| `extract_poses.py` | world-space joint positions, convention-free, avoiding the Euler trap | exists |
| `AnnyInverter` and LBFGS | solves pose, phenotype and local changes jointly | exists |
| **renderer** | image, keypoints, masks, camera parameters. Nothing turns a posed mesh into a labelled frame | **build** |
| appearance generators | Qwen-Image-Edit, CycleGAN monet and ukiyoe, algorithmic corruption, all licence-cleared | exists |
| **colour-sketch checkpoint** | FastCUT, single-image training. One licence-clean sketch needed | **build** |
| drift and hand verification | `silhouette.py`, `depth_term.py`, `soma_referee.py`, controls passing | exists |
| schema | `KEYPOINTS_2D`, `SEGMENTATION`, `RENDERS` defined. `visibility` int8 and `topology_id` pending | exists |
| COCO-format bridge | `gen_coco_dataset.py`, `gen_reference_keypoints.py`, `gen_reference_loss.py` | exists |
| **training loop** | upstream RF-DETR is Apache-2.0. The masked-loss run does not exist | **build** |
| GGUF conversion | `convert_keypoints_to_gguf.py` | exists |
| `rf-detr-cpp` inference | working port, head is COCO-17 | exists |

## What the chain is for

The head recovers a body from a picture. Each stage is blind to something another stage covers.

| step | recovers | blind to |
| --- | --- | --- |
| RF-DETR wholebody | 104 keypoints in 2D | depth, shape, anything unlabelled |
| `AnnyInverter` and LBFGS | the pose that puts those joints there | whether its correspondence is right |
| silhouette fit | the 11 phenotypes no keypoint constrains | depth, and the interior |
| depth fit and Marigold | interior surface, limb ordering | absolute scale |
| MediaPipe | 51 of 52 ARKit coefficients | the tongue, verified absent from the model |
| hm08 groups on the fit | body layers in 3D, depth-ordered, nothing inpainted | hair and garments, which ANNY does not model |

The estimator panel never had that property, because its members were all COCO-trained and
their errors correlated. Every fit here is descent through a forward we own. Where the forward
is differentiable there is no inverse model to license, train or trust.

The last row is what RFD 0121 answers.

## The corrected hm08 claim

The plan leaned on one sentence: the mesh already labels its own parts, so the layer masks have
no gaps. `2-contract/hm08-partition` states it in Lean 4 with Mathlib, 847 build jobs.

The first version of that file reported 992 unassigned vertices, 124 cubes and a 19,150-vertex
mesh. All three were wrong, and the file was wrong in the class of error it was written to
catch. It counted the ranges in one JSON field and took that count for the mesh.

| statement | result |
| --- | --- |
| `segs_disjoint` | holds. No vertex is in two groups |
| `not_a_partition` | the twelve-range claim fails. Vertex 13606 is in the mesh and in no group |
| `jointCubes_card` | the block is 1,000 vertices, which is 125 cubes of 8 |
| `covered_or_jointCubes` | the corrected claim, and it holds |
| `three_groups_cover` | `body` and `HelperGeometry` and `JointCubes` are the whole mesh |
| `three_groups_disjoint` | and no vertex is in two of them |

`JointCubes` is `[[13606, 14597], [19150, 19157]]`. The missing eight are `joint-ground`.
`HelperGeometry` excludes the cubes exactly, so `select_groups`' `HELPERS` entry never named
them.

The file uses interval sets rather than finite sets on purpose. A finite set over 19,158
vertices would tempt the checker into listing every one, and a single counterexample settles
it.

`check_hm08_claims.py` now re-derives every constant from the installed ANNY package, with six
negative controls that each must fail. RFD 0121 records the full measurement.

## The cheapest thing that could change the plan

All 810 clips are locomotion. Walking, running, turning and standing still. Character drawings
are rarely mid-stride, so walk cycles teach a keypoint detector little about sitting or
leaning.

The check needs no renderer, no GPU and no install. Project the 104 joints with the camera
arithmetic, draw the stick figure, and look at twenty. Ask whether a character artist would
draw that pose.

If the answer is no, author poses by hand. The pose-source rule already permits that, and a
hand-authored pose is constructed rather than generated.

Run this first. It is the one result that could redirect the work before any of it is built.
