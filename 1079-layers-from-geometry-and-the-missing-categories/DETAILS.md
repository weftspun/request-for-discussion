# RFD 1079 details: the coverage table, the rebuild pipeline, and the ledger protocol

## What hm08 actually covers

Ranges come from `anny/data/mpfb2/mesh_metadata/hm08_config.json` and
`basemesh_vertex_groups.json`. Counts are inclusive at both ends. The 13 rows sum to 19,150.

**That is not the whole mesh. The mesh has 19,158 vertices.** See the correction below.

| group                  | range          | vertices | verdict                         |
| ---------------------- | -------------- | -------- | ------------------------------- |
| `body`                 | 0 to 13379     | 13,380   | one block, no sub-parts         |
| `helper-tongue`        | 13380 to 13605 | 226      | renderable                      |
| (unnamed helper block) | 13606 to 14597 | 992      | 124 joint cubes, not renderable |
| `helper-l-eye`         | 14598 to 14669 | 72       | renderable                      |
| `helper-r-eye`         | 14670 to 14741 | 72       | renderable                      |
| `helper-l-eyelashes`   | 14742 to 14866 | 125      | renderable                      |
| `helper-r-eyelashes`   | 14867 to 14991 | 125      | renderable                      |
| `helper-lower-teeth`   | 14992 to 15059 | 68       | renderable                      |
| `helper-upper-teeth`   | 15060 to 15127 | 68       | renderable                      |
| `helper-genital`       | 15128 to 15327 | 200      | renderable                      |
| `helper-tights`        | 15328 to 18001 | 2,674    | proxy volume                    |
| `helper-skirt`         | 18002 to 18721 | 720      | proxy volume                    |
| `helper-hair`          | 18722 to 19149 | 428      | proxy volume                    |

`select_groups` names the 992-vertex block `HELPERS`. `groups_by_range` gives it no range.
A caller who counts ranges misses it. `hm08-partition` proves this and names the block.

## The correction: the mesh is 19,158 vertices, and the joint cubes come in two ranges

`hm08-partition` states the mesh as 19,150 vertices and the unnamed block as one range,
`13606` to `14597`, which is 992 vertices and reads as 124 joint helper cubes of 8.

Both numbers are short by one cube. `basemesh_vertex_groups.json` gives `JointCubes` **two**
ranges, not one.

    "JointCubes": [[13606, 14597], [19150, 19157]]

That totals 1,000 vertices, which is **125** cubes. The highest index in any of the 144
groups is `19157`, so the mesh holds 19,158 vertices.

The measurement confirms it. `anny.Anny(topology=TopologyConfig(base_mesh="makehuman",
remove_unattached_vertices=False))` returns 19,158 vertices. The default returns 13,718,
because the default drops every unattached vertex, and all of the helper geometry is
unattached.

This repeats the exact error `hm08-partition` was written to catch, one level up. The original
claim counted the ranges in `groups_by_range` and missed the helper block. The correction
counted the same 12 ranges, stopped at `19149`, and missed the second `JointCubes` range. The
tidy arithmetic is what sold it. `992 = 124 * 8` divides evenly, so nobody asked whether 992
was all of them.

The consequence is the one the original file named. Eight vertices at `19150` to `19157` fall
through every mask **built from `groups_by_range`**. They either vanish from the corpus or
appear as one small floating box inside whichever layer catches the remainder.

Those eight have a name. They are `joint-ground`, which is MakeHuman's ground joint and a
group of its own. It sits at the end of the mesh instead of in the contiguous block, which is
how one read of one range lost it.

## Two more corrections, and the claim that was true all along

**The cubes are not unnamed.** `hm08-partition` said 992 vertices belong to no group at all.
They belong to `JointCubes`. The true claim is narrower. They belong to no group in
`groups_by_range`.

**`HELPERS` does not name them.** The file said `select_groups` reaches them through
`HELPERS -> HelperGeometry`. `HelperGeometry` is `[[13380, 13605], [14598, 19149]]`, which
excludes the joint cubes exactly. `select_groups` never mentions `JointCubes`.

**And the original sentence is true.** Three top-level groups in `basemesh_vertex_groups.json`
partition the mesh with nothing left over.

| group            | vertices |
| ---------------- | -------- |
| `body`           | 13,380   |
| `HelperGeometry` | 4,778    |
| `JointCubes`     | 1,000    |
| total            | 19,158   |

No overlap and no gap. So "hm08 partitions the mesh, so layer masks have no gaps by
construction" holds through these three. It fails through `groups_by_range`'s twelve. A mask
built from the twelve has gaps. A mask built from the three does not.

The count of 125 is also read from the data rather than divided out. The file holds 125 groups
named `joint-*`. Each one is 8 vertices. Their union is `JointCubes` exactly.

## The state of that repository

`2-contract/hm08-partition` now carries the correction. `meshSet` is `Set.Ico 0 19158`.
`helperBlock` is renamed `jointCubes` and holds two ranges. Two new theorems state the
partition, `three_groups_cover` and `three_groups_disjoint`. Both retractions stay in the
docstring beside what replaces them.

`lake build` is clean and no theorem uses `sorry`. Reverting `jointCubes` to the single old
range makes `three_groups_cover` and `covered_or_jointCubes` fail to compile, so both gates
have teeth. `check_hm08_claims.py` re-derives every constant from the installed ANNY package
and ships six negative controls that each must fail.

The repository is now a git repository with two commits, and `default.xml` places it on the
contract side. The remote does not exist yet, so `repo sync` fails on that entry until it is
created.

## The 24 tags, against those groups

The 24 tags are the 13 body tags plus the 11 head tags. `head` expands into the head tags.
Both lists live in `common/utils/inference_utils.py`.

| tag                                    | source                                     | verdict                                 |
| -------------------------------------- | ------------------------------------------ | --------------------------------------- |
| `head`, `neck`, `face`, `ears`, `nose` | inside `body`                              | geometry exists, no split               |
| `mouth`                                | `body` lips, plus teeth and tongue helpers | partial, needs a split                  |
| `eyes`                                 | `helper-l-eye`, `helper-r-eye`             | separated                               |
| `irides`, `eyewhite`                   | inside the eye helpers                     | not separated                           |
| `eyelash`                              | eyelash helpers                            | separated                               |
| `front hair`, `back hair`              | `helper-hair`                              | proxy only, and no front and back split |
| `topwear`, `bottomwear`, `legwear`     | `helper-tights`, `helper-skirt`            | proxy only                              |
| `eyebrow`                              | none, painted into the skin texture        | absent, attached like a garment         |
| `headwear`, `eyewear`, `earwear`       | none                                       | absent                                  |
| `neckwear`, `handwear`, `footwear`     | none                                       | absent                                  |
| `tail`, `wings`, `objects`             | none                                       | absent                                  |

Ten tags are absent. Five have a proxy volume and no appearance. Nine need a partition of
geometry that already exists.

`eyebrow` is not a special case. It joins the absent list, which makes **ten**, not nine.

MakeHuman paints it into the skin texture, so it shares the skin's depth and the depth-order
rule gives it no layer of its own. The fix is the same as for every other absent tag. It
becomes a separate attached mesh, handled like a garment or an object, with its own geometry
and therefore its own depth.

The ten absent tags are `eyebrow`, `headwear`, `eyewear`, `earwear`, `neckwear`, `handwear`,
`footwear`, `tail`, `wings` and `objects`. One route serves all of them.

An earlier draft carved `eyebrow` out and proposed authoring it against the basemesh. That was
wrong twice. It invented a special case where the ordinary one works, and it pointed at the
one mesh that must not be edited.

## The basemesh vertex order is frozen

This is the hard constraint, and it is about **order**, not count.

Two things read the basemesh by index, and both break silently under a permutation.

**`coco.pth` weights are per-index.** Each keypoint is a weight vector 19,158 wide. The
weights for `nose` are non-zero at indices 161, 162, 163, 164, 184, 197 and others. Reorder
the mesh and the vector still has 19,158 entries, still multiplies, and puts the nose
somewhere else.

**Every hm08 group is a range.** `body` is `[[0, 13379]]`. `helper-hair` is `[[18722, 19149]]`.
A range is an order claim. Reordering invalidates every group, so it invalidates every mask.

So no part may be merged into the basemesh, and no operation may renumber it. Attached parts
carry their own vertex arrays. This is what makes "treat it like a garment" the safe answer
rather than merely the tidy one.

### The count gate was decoration

The earlier gate asserted 19,158 vertices. A permutation keeps that count exactly, so the gate
passes on the broken input it exists to catch.

The order-sensitive form hashes the face index array, because face indices reference vertex
indices and therefore encode the order:

    faces        (27420, 3)
    sha256       6b98503de9657efce24300113b90bdc5a4e06a87e2f7d7f7067400a563185da4

Permuting the vertices leaves the count at 19,158 and changes that hash to
`616c75243f...`. That is the negative control, and it is the reason the hash replaces the
count rather than joining it.

**State the coverage honestly.** The face array references vertex indices up to 14741 only, so
the hash pins the order of that span and says nothing about 14742 to 19157. The group-range
assertions in `check_hm08_claims.py` cover the remainder. Neither check alone is sufficient,
and reporting the hash as though it pinned the whole mesh would be the same error one level
down.

## Why the depth order needs no inpainting

Render one group with the full scene in the depth buffer. Write colour only where the group
owns the fragment. Then render the same group alone. The second render shows the occluded
surface, because that surface is real. The difference between the two renders is the amodal
region, which See-Through must otherwise invent.

This holds for Half A because the geometry is there. It fails for Half B until the rebuild
runs, and that is the entire reason for the rebuild.

One cost is real. A garment shell sits above the skin. Set that offset too small and the two
surfaces fight in the depth buffer. Set it too large and the garment floats. The working
figure is about 2 mm at body scale, which is a little over two stacked credit cards. Measure
the offset per garment. Do not assume it.

## The rebuild, stage by stage

Bugs live at interfaces. Each stage names its interface and the check that guards it.

1. **Pose and render.** ANNY originates the pose. Render N views with colour, depth and the
   hm08 group index per pixel. Interface: camera convention. Parse the up axis, the rotation
   order and the units. Do not assume them.

   Depth and the group index are intermediates. Depth feeds the control at stage 2. The group
   index feeds the cross-check at stage 5. Neither one lands beside the image in the corpus.
   The section below states what the corpus render writes, and that list is shorter.

2. **Stylize under depth control.** Qwen-Image plus its Apache-2.0 depth ControlNet turns each
   view into an illustration with hair and garments. Interface: the depth image. Check that
   the control reached the model, because a dropped control looks like a bad seed.
3. **Referee the result.** `pose-consensus` refits the stylized body to the conditioning pose.
   Report the residual as a percentage of stature. The finger chain gate runs, because
   `handwear` is one of the 24 tags. A gate that did not run is a failure, not a waiver.
4. **Lift to geometry.** TRELLIS.2 or Pixal3D takes the N stylized views and returns a mesh.
   Interface: view count and camera agreement. Single view is not enough here.
5. **Segment the new geometry.** P3-SAM cuts the lifted mesh into parts. Interface: part to
   tag mapping. This mapping is inferred, not true by construction, so it is checked against
   the hm08 group index that stage 1 rendered.
6. **Edit one category under a mask.** VoxHammer adds or replaces one tag. Its splice step
   runs before the decode, so geometry outside the mask does not move. RFD 1030 states this
   guard.
7. **Render the layers.** Repeat stage 1 on the rebuilt mesh. Now every tag has geometry, so
   the depth order gives the layers, and nothing is inpainted.

Stages 2 and 6 are the only generative steps. Everything they produce is Half B and carries
the four conditions.

## What the corpus render writes

The rebuild above is pipeline. The corpus render is the thing two models train on, and its
output list is short and closed.

| output             | consumer              | why it cannot be recomputed                                           |
| ------------------ | --------------------- | --------------------------------------------------------------------- |
| the image          | both                  | it is the input                                                       |
| keypoint positions | the keypoint detector | the pose is authored, so the position is not inferable from the image |
| the 3D shape       | Pixal3D               | the same, in three dimensions                                         |

Nothing else is written. Depth, the hm08 group index, the camera matrix and the material
identifier are intermediates of the render. No second annotator runs. No derived column is
stored, because a derived column can be recomputed and a stored one can disagree with its
source.

A new output is drift unless one of the two consumers asked for it. Name the consumer or drop
the output.

### The keypoints are true by construction

`anny/data/keypoints/coco.pth` holds **23** named keypoints, which is COCO-17 plus the six
foot points. It is not COCO-17 alone.

Each entry is a weight vector over the mesh vertices. The vectors sum to 1 and the first one
has 317 non-zero entries. A keypoint position is therefore a weighted sum of posed vertices.
The renderer computes it from the mesh it just posed. No detector runs, and no label is
inferred.

### The topology must be pinned, or the keypoints land on the wrong body

The weight vectors are 19,158 wide. That is the makehuman basemesh with unattached vertices
kept.

    TopologyConfig(base_mesh="makehuman", remove_unattached_vertices=False)

The default configuration returns 13,718 vertices. A weight vector of width 19,158 cannot
multiply it. This resolves the open question in `logbook/todo.md`, which asks which topology
`coco.pth` targets and suggests the topology may not be exposed. It is exposed. It needs the
two arguments above.

`remove_unattached_vertices` is the only argument that moves the count. A sweep over
`nudity_edits`, `eyes` and `tongue`, all eight combinations, returns 19,158 every time. Those
three flags change faces and not vertices. So one argument decides whether the keypoints can
be computed at all, and the other three cannot break it by accident.

Pin the topology in the render configuration and assert the vertex count before the first
frame. A silent shape mismatch here would produce keypoints for a different body.

## Gates, each with a negative control

A check that passes on known-broken input certifies the defect. Each gate ships with an input
that must fail.

| gate               | passes on                                              | must fail on                       |
| ------------------ | ------------------------------------------------------ | ---------------------------------- |
| coverage           | every mesh vertex in a group or the named helper block | a mesh with one unnamed vertex     |
| depth order        | layers composite back to the source render             | a layer pair swapped in z          |
| pose fidelity      | referee residual under the stature bar                 | the impossible pose control        |
| finger chain       | flat residual from MCP to DIP                          | the compounding chain control      |
| control reached    | depth control present in the call record               | a run with the control dropped     |
| provenance         | checkpoint and prompt recorded per Half B row          | a row with the checkpoint missing  |
| vertex count       | the posed mesh has 19,158 vertices                     | a run on the 13,718 default        |
| vertex order       | the face-index hash matches                            | the mesh permuted, count unchanged |
| basemesh untouched | every added part is its own mesh                       | any part merged into the basemesh  |
| output set         | the corpus row holds image, keypoints and shape        | a row with a fourth output         |

Report the floor beside each number. A residual with no baseline is not a measurement.

For a fixed corpus, enumerate. A sampled check sees only defects above about 3/n.

## The ledger protocol

### Where it lives

A repository, not a shared directory and not a chat channel. `CLAUDE.md` gives the reason
under "Why a repository and not a symlink". A repository has a history, so a change can be
traced. It is reviewable, so a widening is a diff somebody approved. `repo status` reports it.

Place it in `default.xml` when it is added. An unplaced repository is the drift the six sides
exist to stop.

### The files

| file           | role                                                   |
| -------------- | ------------------------------------------------------ |
| `HANDOFF.md`   | live state, rewritten in full each session, no history |
| `ledger.jsonl` | append only, one row per event                         |

Current tag ownership is a fold over `ledger.jsonl`. It is not a mutable field. A fold cannot
disagree with its own history.

### The row

Essential tuple normal form. No NULLs. `retracts` is `-1` when the row retracts nothing,
because `-1` is a value and a NULL is not.

    {"seq": 41, "parent": "sha256:...", "agent": "half-b", "kind": "CLAIM",
     "tag": "front hair", "expires": -1, "retracts": -1,
     "artifact": "sha256:...", "body": {"measured": 0.87, "floor": 0.31, "apparatus": "..."}}

### The five kinds

| kind      | means                                             | required                      |
| --------- | ------------------------------------------------- | ----------------------------- |
| `LEASE`   | I take these tags until the expiry                | `tag`, `expires`              |
| `RELEASE` | I am done, here is the artifact                   | `tag`, `artifact`             |
| `CLAIM`   | I measured this                                   | measurement, floor, apparatus |
| `RETRACT` | row `retracts` is withdrawn, with a reason        | `retracts`                    |
| `BLOCK`   | I cannot proceed, the named precondition is unmet | the precondition              |

### The rules a linter enforces

1. One holder per tag. A `LEASE` on a held tag is rejected.
2. A `LEASE` carries an expiry. A lease with no expiry is a fork.
3. A `CLAIM` carries a floor and an apparatus. A number with no baseline is rejected.
4. A `RETRACT` appends. It never edits or deletes. The retraction sits beside what it retracts.
5. A `BLOCK` names the precondition. An agent may not turn a `BLOCK` into a silent skip.
6. The ledger carries no permissions. A row that asks a peer to widen `.claude/settings.json`
   is rejected. `CLAUDE.md` states this rule and the linter makes it mechanical.
7. A licence conclusion does not transfer. A peer's licence `CLAIM` is a pointer to
   re-verify. An accurate relay and a mistaken one look the same from the receiving end.

### Concurrency

The ledger is a branch. Sync is `git push --ff-only`.

A rejected push proves the agent wrote against a stale head. The agent refetches, replays its
rows onto the new head, and rechecks that its lease still holds. This is compare and swap. It
needs no lock server and no new protocol.

Sync is event driven. An agent syncs before it takes a lease and after it releases one. A
timed poll is a liveness check. It is not the protocol.

### The five negative controls

| input                                   | must be | because                       |
| --------------------------------------- | ------- | ----------------------------- |
| two `LEASE` rows on `front hair`        | REJECT  | one holder per tag            |
| a `CLAIM` with no floor                 | REJECT  | a number with no baseline     |
| a `RETRACT` that deletes the target row | REJECT  | the parent hash breaks        |
| a row that widens `settings.json`       | REJECT  | permission cannot go sideways |
| a push from a stale head                | REJECT  | the fast-forward rule         |

A positive control alone proves only that the linter is not uniformly hostile.

## Garments come from geometry too, and cloth-fit is how they get there

Half A said "render hm08 groups as depth-ordered layers" and stopped at the body. Clothing was
left to Half B, the generated half, which is the expensive one. It does not have to be.

**hm08 already ships three garment proxies.** `helper-tights` is 2,674 vertices, `helper-skirt`
is 720 and `helper-hair` is 428, all in the base mesh and all posed by the same rig as the body.
They carry no appearance, which is why the coverage table above marks `topwear`, `bottomwear`,
`legwear`, `front hair` and `back hair` as "proxy only". A proxy with no appearance is still a
volume with a correct silhouette and a correct depth, and those are the two things a layer needs.

**cloth-fit puts a real garment on that volume.** `Huangzizhou/cloth-fit` implements
*Intersection-free Garment Retargeting*, Huang, Araújo, Kunz, Zorin, Panozzo and Zordan,
SIGGRAPH Conference Papers 2025. It is **MIT**, which clears the licence bar outright, and it is
CPU-only over PolyFEM, so it needs no GPU and no quantisation and therefore raises none of the
generated-synthetic conditions. It is not a generator: it deforms a garment somebody authored
onto a body somebody authored, which is constructed rather than sampled.

**CORRECTION, BECAUSE THE PREMISE FOR READING IT WAS WRONG.** It was reached for on the
understanding that it fits garments to *volumes*. Its README says the opposite in one line: "For
avatars and garments, only `.obj` triangular mesh is supported." The inputs are four surfaces --
target avatar, source garment, source skeleton and target skeleton, the last two as edge meshes
-- plus an optional skinning-weight matrix of skeleton nodes by vertices, and vertices project to
the nearest bone by distance when it is absent. Whether PolyFEM tetrahedralises internally is
unverified here: the paper PDF exceeds the fetch limit and was not read, so this records what the
interface takes and makes no claim about the solver.

The correction does not cost the plan anything, and it is worth saying why rather than leaving it
to be re-derived. What the method needs is an avatar surface, a skeleton and skinning weights.
ANNY supplies all three from one call. The hm08 proxies remain the right target because they are
already the garment-shaped surface at the garment's place on the body; they are simply surfaces
rather than solids, which is what the tool wanted anyway.

**Adding proxies is the extension point.** Five of the ten absent tags are garments or worn
objects -- `headwear`, `eyewear`, `earwear`, `neckwear`, `footwear` -- and each one wants the
same treatment `helper-tights` already has: a proxy group in the mesh, posed by the rig, then a
retarget onto it. That is an edit to the partition rather than to the basemesh, so the frozen
vertex order above is not disturbed and its hash gate still holds.

**And the layer falls out of a subtraction.** Render the body without the garment, render it
with, and difference the two. The garment layer's alpha is where they differ and its depth order
is the depth buffer's, both exact, neither inferred. That is the same construction the keypoints
use and it inherits the same property: there is no annotator and no model in the label. It also
supplies the negative control this section would otherwise lack -- a retarget that intersects the
body produces a garment layer with body pixels inside it, so the subtraction detects the failure
the tool's own guarantee is supposed to prevent.

Two limits, stated rather than discovered.

**A 2D garment layer composites only in the pose it was drawn in.** The kimono art that prompted
this is A-pose, and it lands on an A-pose body and nowhere else. Carrying it to another pose
needs a dense correspondence over the body, which is what RFD 107a's 104 points are for. The two
RFDs meet here rather than merely citing each other.

**Reproducibility has a floor on the GPU.** `cuda_ad_rgb` is byte-identical at 16 samples per
pixel and stops being so above it, with the disagreement growing as samples rise -- 5.8e-11 mean
at 64, 1.9e-08 at 1024, worst case 3.6e-07 against one 8-bit level at 3.9e-03, so roughly one
eleven-thousandth of one level. Far below anything visible, and fatal to a hash. A render whose
evidence is a digest is produced on `llvm_ad_rgb`, which held byte-identical at every count
tested and did so without being pinned to one thread.

### The tag count in this document does not match the code

Stated as a defect rather than fixed silently, because the fix is a decision about which list is
authoritative and that has not been taken.

This document says "the 24 tags are the 13 body tags plus the 11 head tags" and sources both to
`common/utils/inference_utils.py`. That file holds one list, `VALID_BODY_PARTS_V2`, with **19**
entries. The current vocabulary is a third file the document does not name,
`common/assets/bodytags_v3.json`, with **23** keys: it splits `hair` into front and back and
`eyes` into `irides`, `eyewhite` and `eyelash`, and carries the danbooru synonyms for each.

So 24 matches neither artefact. The coverage table above is still right about which tags have
geometry, which is what it is for; the count in the prose is not.

### The quads exist, and they are discarded at ANNY's Python boundary

The basemesh is not quad-dominant, it is **pure quad**: `mpfb2/3dobjs/base.obj` has 18,486 faces
and every one of them is a quad, over 19,158 vertices. `Anny(...).faces` returns 36,108
triangles, which is exactly twice 18,054, so the pairing is thrown away at the API rather than
absent from the data.

That matters because the two consumers want different things. cloth-fit takes `.obj` triangles
and nothing else, by its own README. Catmull-Clark subdivision wants quads and degrades on
triangles. OpenUSD stores either, since `faceVertexCounts` is per-face, so the corpus can hold
the quads and hand triangles only to the solver.

**Triangulation adds faces and never vertices**, which is why this is safe here. The frozen
vertex order above is untouched by it and its hash gate still holds, and a deterministic split
restores the quads exactly.

One trap, of the same kind the `Hips`-to-`root` mapping already produced. `base.obj` carries
19,158 vertices and ANNY reports 18,056, because the joint cubes are pruned. The quad table
indexes the un-pruned mesh, so the index mapping is recorded with it or the restore writes onto
the wrong vertices, silently and plausibly.

### PolyFEM does not export to ONNX, and the corpus path does not want it to

Asked and answered rather than assumed. PolyFEM is C++ under MIT with no PyTorch, TensorFlow or
ONNX component anywhere in it. ONNX encodes a static tensor dataflow graph; a barrier-method
Newton solve has an active contact set that changes each iteration, with dynamic sparsity, a line
search and collision queries. There is no fixed graph to export, so this is a shape mismatch and
not a missing feature.

It also buys nothing. The fit is an offline authoring step: one garment against one body is
solved once and the result is baked geometry, and nothing in the inference path calls the solver.

What is exportable is a surrogate trained on the solver's outputs, and its classification is
worth stating before somebody assumes the cautious answer. A deterministic FEM solve over assets
we hold is **constructed** synthetic, not generated -- the same inputs reproduce it and the
labels are true by construction -- so the four generated-synthetic conditions do not apply to it.

**A gate before adoption, from the project's own README.** It says the code is MIT and then warns
to "be mindful of third-party libraries which are used by PolyFEM and may be available under a
different license". MIT on the code is not MIT on the build, and the dependency licences are read
before this becomes a `<project>` in a manifest, not after.

### A proxy is a form, and a form is free

**RETRACTED: proxies do not inherit a garment's licence, and the first version of this section
said they did.** It read that a proxy derived from an encumbered garment is a derivative of it
because "shape is usually the protected part". That is wrong about the thing it was most
confident about. A garment is a useful article, so its cut and shape are largely outside
copyright and only separable pictorial elements -- a print, an applique, a logo -- carry it. That
is what *Star Athletica v. Varsity Brands* turned on. A weapon form is functional shape for the
same reason. People are free to make body forms and weapon forms, and the retracted paragraph
would have blocked a legitimate route on a misreading.

The line that actually holds is narrower. **Copying the file is the problem; re-expressing the
form is not.** An authored mesh is somebody's creative work and a silhouette is not, so
decimating their mesh into a proxy copies the asset, while authoring a proxy to the same form
does not. Looking at the garment is not what makes the difference, and the earlier framing put
the boundary there.

So a proxy is a good way to distribute the shape of clothing that cannot itself be shared. It
travels as a placement spec -- this class of garment sits here on this body, at this ease -- and
the recipient supplies their own asset for cloth-fit to retarget onto it. That is also the honest
statement of what a proxy is worth: a stand-in that is worse than the real garment wherever the
real garment exists, and better than nothing everywhere else.
