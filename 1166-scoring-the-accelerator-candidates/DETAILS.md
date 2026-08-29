# RFD 1166 details: the table, the runoff, and what each row rests on

## The STAR rank

STAR applied repeatedly: take the two highest sums, let the six
dimensions vote between them, seat the winner, remove it, repeat.
`runoff` reads wins-losses-ties against the runner-up it beat.
`loops` is which of RFD 1143 to RFD 1146 the model appears in.

     #  model                     fit shp ref clr val adp ask wnt  sum  runoff role
     1  rf-detr keypoint         100 100 100  80 100  95 100  85  760  7-0-1  fit
     2  cyclegan_style_transfer   95  95  60  50  70  95  80  60  605  4-4-0  style, both
     3  OmniGen2                  50  50  15  50  95  75 100  55  490  4-3-1  2D edit only
     4  EditScore, Qwen3-VL-8B    40  45  90  55  60  70 100  70  530  6-2-0  all three
     5  Kimodo                    95  40  10  55  40  85  30  80  435  5-3-0  -
     6  MoGe                      85  90  55  50  30  60  40  50  460  4-4-0  bootstrap only
     7  SkinTokens                95  15  10  45  35  80  30  85  395  4-3-1  -
     8  MuJoCo MJX                95  30   5  15  20  90  85  80  420  3-3-2  presence
     9  TRELLIS.2 / Pixal3D       60  35   5  25  75  30  35  90  355  4-3-1  3D backbone
    10  Mitsuba 3 shading         95  75   5  10  55  15  95  45  395  4-4-0  3D views
    11  VoxHammer                 30  50  55  15  60  10  30  80  330  last   3D ingest+edit

The sum is not the order. MoGe outscores EditScore by 20 and sits
below it, having lost the runoff that decided the seat.

**TRELLIS.2 and Pixal3D are one row.** They were never independent
candidates: Pixal3D's README says it is "heavily built upon Trellis.2
... the foundation of our codebase and model architecture", and its
install step begins by following TRELLIS.2's. Scoring them separately
counted one backbone twice and let the derived model rank below the
thing it is made of. The row takes the staged view RFD 1154 arrived
at -- the 1.3 B sparse structure stage rather than the 12.02 B whole
-- which is why `fit` is 60 rather than Pixal3D's old 30.

**Gemma 4 and `qwen35-defiant` are both struck from the ranking.**
Neither was a close call. Both are GGUF, so the format ends them
before memory or operators are reached, and no exporter can close that
gap because GGUF carries no graph at all. RFD 1155 abandoned Gemma 4
on the same ground.

Ranking a candidate with no path flatters the ranking rather than
informing it, and keeping one as a worked example only made the table
look like it had considered language models on their merits. It had
not: it had rediscovered the blocklist. BLOCKLIST.md is where that
argument lives.

**`unified-modal-embedder` and `residual-fsq-recommender` are struck
for a different reason: they are not what this product is.** One
embeds content for search and the other recommends a next item. Both
are infrastructure for finding things, and the two wants this ranking
serves are making and being present. Neither is in a chain, neither
has run here, and the embedder held the lowest `wanted` of any
surviving row at 20.

Nothing is wrong with either. A ranking of accelerator candidates is
not a list of the workspace's models, and the checkouts stay in the
manifest where they are placed.

**MoGe was struck and is restored, scoped to bootstrap.** It is not
an independent candidate: it sits in Pixal3D's core `requirements.txt`
and `app.py` calls it from `get_camera_params_wild_moge`, which takes
a photograph somebody else shot and estimates the camera that shot it,
producing exactly the `camera_params` dict `run()` demands.

The strike said the inverted chain deletes that input, and it does --
after the first turn. **It does not answer where the first asset comes
from.** ANNY originating a pose has no wild image and needs no camera
recovered. A photograph does, and image-to-3D is a catalog entry with
two models behind it, which is not what gets built if nobody brings
images.

So the strike was wrong twice over. The case survives at the
bootstrap, and more to the point, **a dependency that might be needed
is still code to write and QA on the device.** This ranking tracks
work the accelerator programme takes on, and work that turns out to be
unnecessary is discovered by doing it. Its `value` falls from 40 to 30
because it runs once at ingestion rather than every round, and that is
the whole of what the inversion changes.

## `wanted`, and what the product is for

The other seven dimensions all ask whether a model is tractable. None
asks whether the thing it does is wanted, and a model can be easy to
accelerate and serve nothing anybody needs.

What the product is for answers it, and the manifest says: a social
world with avatars people wear. `v-sekai` and `v-sekai-fabric` carry
the client and the fabric, ANNY is the body, and RFD 1122 is the chain
that puts a person into it. Two things follow and nothing else does.

**People make things and wear them.** A mesh someone made is worth
nothing until it is rigged, textured and in the world, so
`TRELLIS.2 / Pixal3D` takes 90 as the shortest path from an image to a
wearable asset and `SkinTokens` 85, because an unrigged mesh cannot be
worn at all. `VoxHammer` takes 60 for editing what exists.

**People are present to each other, and keypoints are how.** rf-detr
is markerless motion capture: a camera, a body, and the pose that
carries one person's movement onto another's avatar. That is
embodiment rather than a step toward it, so it takes 85, and `Kimodo`
80 for moving a body without a camera in front of it. `MuJoCo MJX`
takes 70, because a world that responds is the difference between a
room and a backdrop.

**EditScore takes 70, and an earlier revision had it at 10.** That
scored it as a thing nobody wears or sees, which is true and beside
the point: **it is a dependency of every making flow above it.** A
mesh generated, edited or restyled is a proposal, and something has to
say whether the proposal is good before it reaches a wardrobe. Without
a scorer the loops do not converge, so what people make is not made
well. It is invisible and load-bearing at once, and 10 recorded only
the first half.

## What each row is for, and what its score rests on

The table above ranks. This says what each row would actually do in a
chain and where its numbers came from, because a rank read without
either invites the reader to supply their own.

    model                    role in a chain                     basis

    rf-detr keypoint         live markerless pose, the           measured,
                             capture end of every making flow    40.85 M params
    cyclegan_style_transfer  style transfer, 2D and 3D views     read only
    OmniGen2                 text-guided 2D edit and corpus      measured,
                             restyle                             7.81 B params
    EditScore, Qwen3-VL-8B   the gate: scores a proposal         inferred from
                             before it is accepted               code, 6.75 GiB
    Kimodo                   pose without a camera               RFD 1026 estimate
    MoGe                     depth and intrinsics from one       read only, a
                             photograph, the ingest bootstrap    Pixal3D dependency
    SkinTokens               rigging and skinning, mesh to       RFD 1026 estimate
                             wearable asset
    MuJoCo MJX               body dynamics and collision,        runtime only,
                             the presence goal                   not a network
    Mitsuba 3 shading        forward shading, G-buffer and       measured, 14.1 ns
                             MToon per pixel                     a pixel
    TRELLIS.2 / Pixal3D      image to sparse 3D structure,       measured,
                             the 3D backbone                     24.04 GB weights
    VoxHammer                edit an existing asset in latent    read only, then
                             space                               its ViT measured

**Two rows are not networks and the basis column says so.** MuJoCo MJX
is a physics engine and Mitsuba 3 is a renderer. Both were measured at
runtime and neither has weights or a graph, so their `shape` and
`reference` scores answer a question the models were asked and these two
cannot be. RFD 1167 puts them off the ladder for the same reason.

**Mitsuba's 14.1 ns is the forward shading pass alone** -- fixed-dimension
per-pixel G-buffer and MToon arithmetic. Backward ray tracing and BVH
traversal are excluded, and that exclusion is the whole reason the row
scores 75 on `shape`: what remains is dense arithmetic at a fixed size,
and pointer-chasing traversal is not.

## The citations, and the eight this workspace had to correct

`references/` holds a `CITATION.cff` for each row. They exist because a
candidate table that names twelve projects and credits none of them is a
provenance failure of the kind the blocklist exists to catch.

A first draft of these files was supplied and **eight of the twelve
attributed work to the wrong party**, so every entry was checked against
the manifest's pinned parents and the LICENSE in each checkout rather
than accepted:

    row                  claimed                    actually
    rf-detr keypoint     Weftspun Team              Roboflow
    OmniGen2             VectorSpaceLab/OmniGen     .../OmniGen2
    EditScore            QwenLM/Qwen-VL             VectorSpaceLab/EditScore,
                                                    a LoRA over Qwen3-VL
    Kimodo               Weftspun Team              a weftspun wrapper only;
                                                    upstream unverified
    MoGe                 RuidaZhang/MoGe            microsoft/MoGe
    SkinTokens           Weftspun Team              a weftspun wrapper only
    See-Through          Weftspun Team              shitagaki-lab/see-through
    TRELLIS.2 / Pixal3D  microsoft/TRELLIS          microsoft/TRELLIS.2 and
                                                    TencentARC/Pixal3D, two
                                                    upstreams in one row
    VoxHammer            Weftspun Team              Nelipot-Lee/VoxHammer

Five of those credited someone else's model to this workspace, which is
the direction of error that matters. Licenses are read from the LICENSE
file in each checkout and not inferred: MIT for MoGe, TRELLIS.2, Pixal3D
and VoxHammer; Apache-2.0 for OmniGen2, EditScore, See-Through and
MuJoCo. Kimodo, SkinTokens and `rf-detr-cpp` carry no LICENSE file, so
none is claimed for them.

Where a row is a weftspun HTTP wrapper around a model held elsewhere,
the file says so and tells the reader not to cite it as the model.

## See-Through leaves the ranking and stays as a taxonomy

**Decision: Marigold is dropped and See-Through is kept as a reference
for layer taxonomy rather than as a model.** It is no longer an
acceleration candidate, so it is no longer a row, and the table above
holds eleven.

The reason is that nothing in its weight set can be used. The
repository is Apache-2.0 and that covers the code; every checkpoint the
inference scripts actually load is hosted separately and **states no
licence at all**, which is not permissive -- absent a grant the default
is all rights reserved:

    layerdifforg/seethroughv0.0.1_marigold     none stated (moved from 24yearsold/)
    24yearsold/l2d_sam_iter2                   none stated
    24yearsold/seethroughv0.0.2_layerdiff3d_nf4  none stated
    24yearsold/metricdepth3d_tmp               HTTP 401, unreadable

The depth checkpoint is additionally a fine-tune of
`prs-eth/marigold-depth-v1-1`, which is CreativeML Open RAIL++-M over
`stable-diffusion-2`. **A fine-tune does not reset that licence.** RAIL
requires its use restrictions to travel into derivatives, which is the
mechanism the OpenRAIL-M blocklist row already names, and nobody
downstream can relicense away restrictions they do not hold. Shipping
alongside Apache-2.0 code does not extend that licence to weights; a
project meaning to do so says so, as NVIDIA does for Kimodo.

Replacing the depth stage with MoGe was considered and is not a
substitution. MoGe is MIT and already in the manifest, but Marigold here
is a latent diffusion estimator -- VAE, UNet and CLIP, with
`cvt_marigold2d_to_3d.py` around it -- while MoGe is a feed-forward ViT
emitting point maps. That is a rewrite of the stage, and the fine-tune
exists because See-Through works on illustration where MoGe is trained
on photographs. Whether MoGe holds up there is unmeasured.

**What is kept costs nothing and is the useful part.** The layer
taxonomy is a vocabulary, and `common/live2d/scrap_model.py` carries
three revisions of it:

    V1  20 parts   hair, skin, beard, and single-part eyes
    V2  20 parts   drops skin and beard, adds objects
    V3  23 parts   front hair, back hair, headwear, face, irides,
                   eyebrow, eyewhite, eyelash, eyewear, ears, earwear,
                   nose, mouth, neck, neckwear, topwear, handwear,
                   bottomwear, legwear, footwear, tail, wings, objects

The V2-to-V3 change is the one worth having: hair splits into front and
back, and the eye splits into irides, eyewhite, eyelash and eyebrow.
That split is exactly what CLAUDE.md points at when it says a photograph
has no ground-truth `front hair` / `back hair`, and it is why the
blinded COCO holdout cannot validate this task whatever else it is good
for.

**Removing the row moved two others, and that is a property of the
method rather than a mistake.** With See-Through present, Mitsuba 3 took
seat 9 and TRELLIS.2 / Pixal3D seat 11; without it they swap to 9 and
10. STAR's runoff is not independent of irrelevant alternatives, so
dropping a candidate can reorder the ones that remain. The recorded
order is the one the eleven-row election produces, and
`check_rfd1166_rank.py` recomputes it against `starvote` rather than
trusting the arithmetic above.

## A row is not a model, and that is systemic

Every row here names a project. Not one of them is a single network, and
the composite is where both the licence and the accelerable part live.
Scoring and citing at row granularity hides both.

    row                  the part that would compile   the part that binds the licence

    rf-detr keypoint     a patch-12 DINOv2 backbone    Roboflow, Apache-2.0
    EditScore            Qwen3-VL's stock ViT          a LoRA over someone else's
                                                       base model
    MoGe                 DINOv2 ViT-B/14, four         microsoft/MoGe, MIT
                         intermediate layers
    VoxHammer            stock dinov2_vitl14_reg       Nelipot-Lee, MIT, over a
                         at 518 square                  TRELLIS backbone
    Kimodo               not examined                  code Apache-2.0, weights
                                                       NVIDIA Open Model, one
                                                       variant NVIDIA R&D
    See-Through          not examined                  code Apache-2.0, depth
                                                       OpenRAIL++-M, one checkpoint
                                                       unreadable
    TRELLIS.2 / Pixal3D  the SS stage alone            two upstreams, Microsoft
                                                       and TencentARC

**Four of the twelve rows compile because of DINOv2, and none of them
compile the same DINOv2.** rf-detr runs a custom patch-12 variant, MoGe a
ViT-B/14 taking intermediate layers, VoxHammer a stock ViT-L/14 with
registers at 518 square, EditScore the ViT inside Qwen3-VL. One HEF does
not serve them, and the tempting conclusion that it might is the reason
to write the sub-model down rather than the row.

**Kimodo's Apache-2.0 badge covers the code and not the weights.**
`Kimodo-SOMA-*` and `Kimodo-G1-*` are under the NVIDIA Open Model
Licence, which permits commercial use; `Kimodo-SMPLX-RP-v1` is under
NVIDIA's Internal Scientific Research and Development licence, which
does not. Reading the badge and stopping there answers for neither.

The restrictive variant turns out not to constrain this row, and the
reason is the rig rather than the licence. Motion travels SOMA-X to ANNY
to Godot Humanoid to VRM, so no SMPL-X checkpoint is on the route --
and SMPL-X is blocklisted besides. `Kimodo-SOMA-*` matches the rig and
is the shippable variant, which is the same conclusion
`logbook-rfd1016-model-repos.md` reached when it warned against swapping
checkpoints without re-checking RFD 1028.

**Retraining Kimodo to get an Apache-2.0 or MIT artifact was considered
and is not available, and the reason is the data rather than the model.**

The NVIDIA Open Model Licence does not force it. It permits commercial
use, permits derivative models, and states that the derivative is
owned by whoever made it -- it is not share-alike, so nothing propagates
the way OpenRAIL-M's restrictions do. What it does attach is
attribution, a guardrail-circumvention clause that terminates the
grant, a patent-litigation trigger, and NVIDIA's Trustworthy AI terms.
Those are conditions on use, not a bar to shipping, and
`logbook-rfd1016-model-repos.md` already recorded `Kimodo-SOMA` as the
shippable variant on that basis.

Retraining would buy an artifact with no third-party terms at all. It
cannot be done on Kimodo's own corpus. **BONES-SEED sits behind an
acceptance gate** -- 288 hours, 142,220 annotated animations, 522
performers, under a custom `bones-seed-license` whose terms are not
readable without accepting them first. That is the condition CLAUDE.md
names in as many words: a set behind a registration form is not
licence-clean, because terms that cannot be read cannot be gated on. It
is the same test that blocklists `24yearsold/metricdepth3d_tmp` two
sections above.

So the licence-clean motion pool is what remains after the blocklist
takes CMU on provenance, Mixamo on licensing and posemaniacs on
scraping: ANNY/SOMA's own pose library, constructed synthetic rendered
from assets held here, or a CC-BY-4.0 capture set with citation
metadata. A retrain is a data programme before it is a training run,
and pretending otherwise would put the effort in the wrong place.

**The recommendation is therefore to ship `Kimodo-SOMA-*` under its
licence and treat the retrain as a separate decision about corpus
independence, not about whether this row can be used.**

**See-Through is the sharpest case, and it reaches the blocklist.** The
repository is Apache-2.0 and pulls two checkpoints that are not:

- `prs-eth/marigold-depth-v1-1` is **CreativeML Open RAIL++-M**,
  fine-tuned from `stable-diffusion-2`. CLAUDE.md blocklists OpenRAIL-M
  as a generator because its use-restrictions propagate into anything
  trained on the output, and exempts passthrough use. Which of the two
  this is depends on whether See-Through's output enters a corpus --
  and `seethrough PSDs` is already a blocklist row for secondary
  generation. Those are the same fact reached from two directions.
- `24yearsold/metricdepth3d_tmp` returns **HTTP 401**. No readable
  licence, no model card, and a name ending `_tmp`. CLAUDE.md is
  explicit that terms which cannot be read without accepting them
  cannot be gated on, so this is not licence-clean.

Neither was visible from the row. Both were found by reading what the
code loads, which is the only method that works here.

**So the rule this section exists to state:** a candidate is cleared, or
scored, or cited, at the granularity of the checkpoints it loads. The
row is a name for a bundle, and a bundle has no licence and no operator
census of its own.

## What this ranking does not tell you

It ranks **units of work**, not deliverable capabilities, and two
things follow that a ladder would otherwise walk into.

**A chain delivers when every stage is placed, not when its best stage
is.** Accelerating one row leaves the others on the host, which is
often fine and sometimes the whole point -- rf-detr is worth doing
alone. But no row's rank is a claim that finishing it finishes
anything.

**Two rows interact, and the table shows them as separate jobs.**
`TRELLIS.2 / Pixal3D` sits at 11 and `VoxHammer` at 12 as though each
could be taken on alone. An earlier revision of this section said they
were mutually exclusive, on the reasoning that a compiled graph has no
Python forward for VoxHammer to replace. **That was asserted from a
general principle and the code does not support it.**

The patched attention blends a cached key against a live one:

    k = k * kv_mask + ss_kv[...].cuda() * (1 - kv_mask)

Mul, Sub, Mul, Add, all of them already inside `DEVICE_OPS`. The
arithmetic compiles. What is Python is the dict lookup, and a compiled
graph would take those cached tensors as inputs rather than fetching
them.

What actually bites is the interface, not the patching. The cache is
keyed by timestep, order, position, layer and type, so the tensors
crossing the boundary scale with all five, and the cache is state held
between the inversion pass and the edit pass. On a part that pays
2.18 ms a dispatch, marshalling that per timestep is the same
arithmetic that rules out a per-node ggml backend.

So the two rows are not a fork. They are one job that is larger than
either row suggests, and nothing here has measured how much larger.

## The critical path is a chain, not a set of loops

`value` was first scored per invocation, which treated the models as
independent candidates. They are stages of one shape:

    2D edit   CycleGAN  ->  OmniGen2                          ->  EditScore
    3D edit   CycleGAN  ->  VoxHammer over TRELLIS.2/Pixal3D  ->  EditScore
    fit       rf-detr   ->  ANNY fit                          ->  EditScore
                                                                  + soma_referee

OmniGen2 appears in one chain and not the other, which is a decision
rather than an omission. See below.

**The two are siblings here and the corpus already orders them.**
`pose-consensus/README.md` records the inversion: instead of
estimating poses from images, ANNY originates the pose, renders it,
and a diffusion model stylizes the render with the geometry pinned,
so the label is true by construction. That inversion ended the
consensus panel outright -- you do not convene three estimators to
adjudicate a pose you authored.

Run that way the chain is one, not two:

    originate 3D  ->  render views  ->  style views  ->  edit  ->  score

and 2D is an operation on views rather than a stage before 3D. Three
things follow.

**The camera question disappears.** OmniGen2's 0.04 obedience slope
only matters if the camera is asked for. Rendering from
`sphere_hammersley_sequence` gives it exactly, and the measurement
below stops being a problem to work around.

**The labels land on the right side of CLAUDE.md's synthetic rule.**
A render is constructed, deterministic from assets held here, with
labels true by construction. An image generated first and reconstructed
after is generated, and carries all five conditions.

**rf-detr changes job without changing score.** Estimating an unknown
pose and confirming an authored one survived a restyle are different
questions, and `test_pose_survives_restyle.py` asks the second. Its
`wanted` 85 covers the live case, a person in front of a camera, which
the inversion does not touch.

**The 3D chain does not go through the 2D one.** Pixal3D's `run()`
takes a single `Image.Image`, so reading it as an image flow suggests
2D must produce that image. It need not. `get_cond` one layer down
takes `list[Image.Image]`, and VoxHammer already drives that path:
`extract_feature.py` renders 150 views, runs DINOv2 over them,
projects voxel centres into each view and averages the patch tokens,
reproducing the encoder input for an asset that already exists.

So the views come from rendering an asset rather than generating an
image, which is also the cleaner side of CLAUDE.md's synthetic line:
constructed rather than generated. `sphere_hammersley_sequence` is the
mandated sequence and Mitsuba renders a view in 1.79 ms.

**Go through VoxHammer rather than calling the multi-view path
directly.** Both reach the same samplers, and only one of them is
already written, tested against a real asset and handling the
inversion the edit needs.

Three consequences, and each moved a row.

**EditScore terminates every chain.** Nothing reaches a wardrobe
without passing it, so a gain there lands three times. Its `wanted` is
70 for being the dependency of making it does not itself perform.

**CycleGAN styles both chains, and style is not 2D-only.** A 3D asset
is restyled through its views: render, restyle the views, ingest the
styled views. It is the same stage doing the same work in both chains
rather than a 2D step the 3D chain routes around, so `value` 70 and
`wanted` 60. It holds second on a runoff it drew four-all, seated by
score and the narrowest result in the table.

The hazard in that is already guarded. `test_pose_survives_restyle.py`
restyles and re-detects to measure joint drift, and
`verify_restyle.py` scores silhouette against the render's own alpha
with a shifted-reference control that must fail. A restyle that moves
the body is the failure both exist to catch, and styling views before
reconstruction is exactly where it would happen.

**Mitsuba is the 3D chain's view source, not a bystander**, which
takes `value` from 30 to 55 and `wanted` from 25 to 45.

## OmniGen2 is 2D only, and the measurement is why

The 3D chain could route through it and does not. Camera control is
what it would be for, and `write_omnigen2_jsonl.py` records what that
costs: asked for eight azimuths in plain language, the recovered
azimuth tracked the request with **a slope of 0.04**, where 1.00 is
obedience and 0.00 is a body that never turned. Six of eight views
came back between -1 and -11 degrees whatever was asked. The trained
adapter reached 0.099.

The 3D chain does not ask. It renders the view it wants from
`sphere_hammersley_sequence`, exactly, in 1.79 ms. Paying 133 s for a
slope of 0.04 when a camera transform is exact and free is the trade
this records, and it is why the 3D chain takes rendered views instead.

**What OmniGen2 keeps is the 2D chain, and nothing else here can do
it.** CycleGAN is style transfer, one learned mapping. OmniGen2 is
instructed editing: change this specific thing, in words. Those are
different capabilities and the second is what "moddable" means. It is
also `anny-camera-lora`'s base, so dropping it orphans RFD 1141's
published adapter, and it generates the corpus restyles.

Its `value` of 95 is the highest here because it is 133 s of a 163 s
round, so removing it takes out the largest cost in the loop. `value`
measures what accelerating a stage buys, not whether the stage should
exist, and on OmniGen2 those two point in opposite directions.

## VoxHammer has a device half, and it took three tries to see it

It holds no weights: no `nn.Module`, no `nn.Parameter` and no
checkpoint in `3-interactor/voxhammer-upstream`. An early revision
scored it n/a on that basis, which answered the wrong question --
weighing nothing does not put it outside a ranking of work.

**`shape` was then 0, on the reasoning that VoxHammer replaces
forwards at runtime and a compiled graph has none to replace. That was
wrong, and defended twice before anybody read the stage it describes.**

`extract_feature.py` loads `dinov2_vitl14_reg` and runs it at 518
square, `n_patch = 518 // 14`, under the same ImageNet constants
`compile_hef.py` folds into an input layer, **150 times per asset**. A
stock ViT at fixed resolution is the same family as rf-detr's device
half, which translated at 825 nodes with the allowlist holding.
`reference` is 55 for that precedent rather than 0.

What does not compile is separable and was never the whole model:
`F.grid_sample` projecting voxel centres into views, and the N x M
coordinate match with its `argmax` and scatter. Both are RFD 1131's
refused family and both sit either side of the encoder, which is the
cut rf-detr already uses. So `shape` is 50.

`fit` 30 and `clear` 15 are the model's own. `ask` 30 is not: upstream
runs, and the two weftspun wrappers raise `NotImplementedError`
outside stub mode, a wiring gap here. `value` 60 and `wanted` 80
follow from the chain, where it is two stages and the 3D route has no
other way in.

It still ranks last, now for an honest reason: four columns are low,
and one strong column does not carry a row through a runoff. RFD 1167
puts it on rung 0 with a rung-1 stage waiting -- the shortest export
left in the field.

## Five models the earlier revision omitted

`cyclegan_style_transfer` is the serious omission. It is **Loop 3**,
called at `localhost:8000` by `3-stylized-to-omnigen2.livemd` before
OmniGen2 runs, so the ranking claimed to cover the candidates while
skipping a model already inside the pipeline the accelerator serves.
It is also the accelerator's home ground: fixed-resolution
image-to-image convolution, no autoregression, no sparse indexing.

`MoGe` recovers point maps, depth, normals and camera FOV from one
image, and depth estimation is a category the Hailo zoo already ships
for HAILO10H, which is what its `reference` 55 records.

**MuJoCo MJX serves presence, and was twice mis-filed.** First as
tooling, then as interactability at the edge of the product. Physics
is embodiment: a body that collides, stands on ground and responds is
present, and one that floats and clips is not. Its `wanted` is 80,
with `rf-detr` and `Kimodo`.

 `mjx/mujoco/mjx`
is MuJoCo reimplemented in JAX: a differentiable physics graph, made
fixed-shape on purpose through fixed-size contact buffers, which is
why `adapt` is 90 -- gradients run through the simulator itself.

Its blocker is the interchange. JAX lowers to StableHLO through XLA
and the Dataflow Compiler consumes TensorFlow, TFLite and ONNX, so
there is no path today. That is a different failure from GGUF's: GGUF
carries no graph at all and nothing can convert it, while StableHLO is
a graph in the wrong dialect. Blocked on format, not structurally,
and `clear` 15 says which.

**Mitsuba 3 is scored as its shading pass, not as the renderer.** It
is a pixi dependency of `anny-render-corpus` at 3.9.1 rather than a
manifest project, and the row covers only the half that could go.

Ray tracing cannot: BVH traversal is pointer chasing with
data-dependent branch depth, which is what a dataflow part is least
able to express. Shading over a G-buffer is the opposite -- per-pixel
arithmetic at fixed dimensions -- and the corpus already separates
them, at 48.1 ns a pixel for the G-buffer against 14.1 for MToon
shading.

Two things hold it at 220 anyway. Dr.Jit compiles to LLVM IR and PTX,
which is machine code rather than a portable graph, so it is a level
below even MJX's wrong-dialect problem, and whether the Slang shading
path can be expressed as ONNX at all is unverified. And the ceiling is
small: the same measurements put intersection at 77 per cent of the
combined cost, so the whole prize is the other 23 of a pass already
made 1,272 times faster.

Not models, correctly absent: `tropes-removal-model` is `ste-enforcer`,
a prose linter under a misleading directory name; `mujoco-riscv64` is
an engine port; `anny` and `soma-x` are parametric bodies;
`pose-consensus` is a solver; `bumblebee` is a framework.

## What each row rests on

    row               basis
    rf-detr           MEASURED. 40.852 M parameters from the
                      checkpoint, 25.245 M in the device half.
                      Exported and translated.
    OmniGen2          MEASURED. 15.87 + 15.02 + 0.34 GB on disk at
                      fp32, so 7.81 B. Trained here: anny-camera-lora,
                      200 steps at 256 square in 22 minutes.
    Pixal3D           MEASURED. Repo safetensors total 24.04 GB
                      against RFD 1026's estimated 24.05.
    See-Through       RFD 1026 ESTIMATE, and the four components it
                      covers are not recorded. Only `layerdiff` is in
                      this table; `marigold-depth`, `vae` and
                      `partseg` are separate repos.
    TRELLIS.2         RFD 1026 estimate.
    SkinTokens        RFD 1026 estimate.
    Kimodo            RFD 1026 estimate.
    EditScore         INFERRED, and the inference was wrong once:
                      scoring assumed Qwen3-VL-4B and `weft_score.py`
                      loads the 8B.
    CycleGAN          UNEXAMINED. Scored from what it is, not from
                      anything run. `clear` 50 says so.

## The `adapt` column, and the one number that bounds it

It leans on RFD 1140: the desk trains an OmniGen2 LoRA at 256 square
in 22 minutes and does not finish one step in twelve at 512.
Pixal3D's 20 and Gemma 4's 15 come from that, and from GGUF carrying
no graph to train against.

**One kind of adaptation is out of reach entirely, at any size in this
table.** Quantization-aware fine-tuning exhausts the desk's 24 GiB on
rf-detr's own device half -- 25.245 M parameters, the smallest graph
here -- at the default batch and again at `batch_size=1, epochs=1`
over 64 frames, the directive verified in the loaded model script.
RFD 1165 carries the retraction that batch size was ever the lever.

So `adapt` scores ordinary training and LoRA, which the desk does. It
does not score QAT, which the desk does not do for anything, and a
column that scored both would rate every row zero and say nothing.
The distinction matters because RFD 1128's four-bit question wants
QAT: compression without fine-tuning is what optimization level 1
gives, and that is a different artifact rather than a slower one.
