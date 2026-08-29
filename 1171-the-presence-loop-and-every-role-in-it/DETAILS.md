# RFD 1171 details: every role, what fills it, and the five that are empty

## The taxonomy is the spine, and it already splits correctly

`common/live2d/scrap_model.py` in See-Through's tree carries
`VALID_BODY_PARTS_V3`. RFD 1166 kept it as the one part of that project
whose licence permits reuse, and it turns out to be the vocabulary this
whole loop needs:

    worn, and therefore swappable    the body, and therefore given

    headwear                          front hair
    eyewear                           back hair
    earwear                           face
    neckwear                          irides, eyewhite, eyelash, eyebrow
    topwear                           ears
    handwear                          nose
    bottomwear                        mouth
    legwear                           neck
    footwear                          tail, wings
                                      objects

**Nine worn slots, thirteen body parts, one catch-all.** The split was
drawn by somebody decomposing illustrations into layers, not by anybody
thinking about garments, and it lands exactly where a try-on needs it.
That is worth noticing rather than assuming: a taxonomy that survives
being used for a second purpose is usually describing something real.

Two of the body rows are load-bearing for the rest. `front hair` and
`back hair` are a depth relation, which is why RFD 1168 argues the
decomposition belongs in 3D, and it is the same reason a hat has to know
which hair it sits under.

## Movement one: make a persona

Language and an image become a character, and a character with a manner
and a voice is a persona rather than a model sheet.

    role                       filled by            state

    understand the ask         Qwen3-VL-8B          runs, host
    generate and edit in 2D    OmniGen2             measured, never
                                                    exported
    style, 2D and 3D           cyclegan_style_...   no model in the
                                                    workspace
    photo to depth and         MoGe                 rung 2, MIT
    intrinsics
    image to 3D structure      TRELLIS.2 / Pixal3D  rung 2, refused at
                                                    rung 3
    accept or reject a         EditScore            runs, host
    proposal
    a manner                   Qwen3-VL, prompt     unwritten
                               or LoRA
    a voice identity           Qwen3-TTS            Apache-2.0, ready
                               CustomVoice

**The gate is the stage most worth questioning.** EditScore is a LoRA
over Qwen3-VL-8B at 6.75 GiB, which is most of an 8 GB device, and RFD
1166 records the open question from arXiv:2608.12875: if that gate is
classification, an embedding model ties an LLM at a fraction of the
cost. Nobody has established which it is.

## Movement two: dress it

The character's worn layers are swapped.

    role                       filled by            state

    name the slots             VALID_BODY_PARTS_V3  in tree, licence
                                                    clean
    the body boundary          ANNY mesh through    silhouette.py
                               silhouette.py        exists
    the person boundary        MoGe depth           rung 2, MIT
    the camera both need       MoGe intrinsics      returned by infer
    either, as a fixed ring    contour.py           WRITTEN, tested
    carry it into the latent   VoxHammer's          the call exists,
                               grid_sample          payload untested
    fill what the mask         LaMa,                MIT, does NOT
    removed                    AnimeMangaInpaint    compile, rfftn
    edit the asset in latent   VoxHammer            rung 0, wrapper
    space                                           unwired
    rig a mesh into a          SkinTokens           wrapper only, MIT
    wearable                                        upstream
    cloth against body         MuJoCo MJX           not a network

**A try-on is the masking operation from RFD 1168, run for a different
reason.** Decomposition removes a layer to see it; a try-on removes a
layer to replace it. The hole is the same hole and LaMa fills it either
way, which is why one mechanism serves both and neither needs its own.

**`objects` is where this gets hard and the taxonomy stops helping.** A
bag, a prop or a held item is not a slot on a body, and
`VALID_BODY_PARTS_V3` puts all of them in one bucket. Anything beyond
the nine slots is unmodelled here.

## Movement three: be it

A person wears the character, live, and supplies its motion.

    role                       filled by            state

    track a body every frame   rf-detr keypoints    RUNG 3, alone
    keypoints to a rig         SOMA-X, anny_from_   topology exists,
                               soma                 gap is RFD 1122
    lip-sync from the wearer   TalkingHead, MIT     unstudied
    render, live               Godot                four checkouts
    render, reference          Mitsuba 3            the oracle
    body dynamics              MuJoCo MJX           not a network

## Movement four: make a friend

Nobody wears it. It has presence to someone, and supplies its own motion
and its own voice.

    role                       filled by            state

    hear                       Qwen3-ASR-1.7B       Apache-2.0, ready
    think                      Qwen3-VL-8B          runs, host
    speak, in its own voice    Qwen3-TTS 12Hz       Apache-2.0, ready
                               CustomVoice
    move with no camera        Kimodo-SOMA + LoRA   wrapper unwired
    lip-sync from its own      TalkingHead, MIT     unstudied
    speech
    render                     Godot                four checkouts

**These two movements are the same avatar and opposite directions, and
that is why the loop needs both motion sources.** RFD 1170 called the
split presence against authoring without noticing it is also first
person against second. `be it` has a person in the room supplying
everything; `make a friend` has nobody, so every input the person was
providing has to come from a model instead.

    supplied by a person       supplied by a model

    body motion, a webcam      Kimodo
    what is in the room, the   nothing -- the friend sees only what it
    same webcam                is shown
    speech, a microphone       Qwen3-VL and Qwen3-TTS
    intent                     the persona's manner

## The webcam is not only a motion source, and each head is its own compile

rf-detr covers three camera tasks -- **keypoints, segmentation and
object detection** -- so the camera is an input to every movement and
not just to `be it`.

**AN EARLIER REVISION SAID ONE HEF SERVES ALL THREE. THAT WAS WRONG.**
It reasoned from `gate_onnx_device.py` compiling "the backbone and
projector" and from `rf-detr-cpp/scripts/` holding separate GGUF
converters per head, and concluded one graph carried three tasks. The
checkpoints say otherwise:

    checkpoint                patch   resolution   windows

    keypoint-preview-xlarge     12       576          1
    seg-nano                    12       312          1
    seg-small                   12       384          2
    large, detection            16       704          2

**Different resolutions and different patch sizes are different
graphs.** A HEF is compiled for one fixed input shape, which is the
whole premise of the device, so a 576-square keypoint HEF does not
serve a 312-square segmenter. Each checkpoint is its own translate,
its own calibration set and its own quantisation.

That matters because rung 4 is the expensive step. RFD 1165 measures
QAFT at 32.5 GiB, which the desk's 24 GiB cannot reach at any batch
size, so every additional compiled model is another rented card rather
than another afternoon.

## So the camera feeds all four movements, not just `be it`## So the camera feeds all four movements, not just `be it`

    movement        what the camera gives          through

    make            a photograph of a person or    detection, then
                    a garment becomes the source   segmentation
    dress           show a real garment to the     segmentation, into
                    camera and try it on           the slot it belongs
    be it           a body tracked every frame     keypoints
    make a friend   the friend sees what it is     detection
                    shown

**The `dress` row is the one worth noticing.** RFD 1168 established that
a try-on needs a boundary and a hole to fill. A webcam plus the
segmentation head is a boundary from the real world, so a garment can
enter the loop by being held up rather than by being modelled. Nothing
in this workspace does that yet and the parts are all present.

**And `objects` stops being only a taxonomy problem.** The detection
head names things the nine worn slots do not cover, which is the bucket
flagged above as unmodelled. Detection does not say what to do with a
held prop, but it does say one is there, which is more than the
taxonomy manages.

## Everything is a contour, and one of them is a projection not an inference

A SOMA-X or ANNY body is vertices. What every stage above actually wants
is an **outline**, and an outline is one representation:

    task            as a contour

    pose            landmarks, a sparse contour
    segmentation    a closed ordered ring
    detection       that ring's extent
    the body        the posed mesh, projected

**The last row is not a model.** Once a pose is fitted, the body outline
is a render of geometry already held -- deterministic, exact, no
checkpoint, no calibration set and no rung to climb. Everything above it
is an inference and that one is arithmetic.

**And it already exists.** `pose-consensus/python/silhouette.py` is a
differentiable soft silhouette, written under a docstring calling it
"the route from pose to SHAPE" because keypoints give pose and not
build: ANNY carries 11 phenotype parameters and 256 local changes, and
no keypoint constrains any of them. CLAUDE.md already reports
"photographic silhouette agreement" as a measured quantity, 0.776
against 0.825 in the precision table, so a silhouette is already this
workspace's currency for asking whether a body matches a pose.

**The garment is then the difference, and that is the useful part.** The
mesh silhouette is the body. What lies outside it and still belongs to
the person is worn. A skirt, a coat and a hat all extend past the body
outline, and that overhang is the garment boundary -- derived from
geometry rather than learned from labels, which is the corpus problem
RFD 1168 could not solve any other way.

That inverts the `dress` movement. It does not need a segmenter that
knows `topwear`; it needs a body it already has and the difference
between that body and the picture.

## MoGe supplies both halves, and the second is the one nobody asked for

The body contour comes from the mesh. The person's outer edge has to
come from the image, and **MoGe answers that without a segmenter and
without a taxonomy** -- a depth step separates a person from the wall
behind them, and no labelled corpus is involved. That is the blocker
RFD 1168 could not get past, sidestepped rather than solved.

**And it also hands over the camera.** `silhouette.py` projects through
a pinhole `Camera(width, height, fx, fy, cx, cy)`, and those numbers
have to come from somewhere. MoGe v2's `infer` returns `intrinsics` as
a 3x3 alongside the point map, recovered from the picture by
`recover_focal_shift`.

    what the loop needs        where it comes from

    body outline               ANNY mesh, posed, through silhouette.py
    person outline             MoGe depth, thresholded
    the camera both project    MoGe intrinsics
    through

**Without that third row the first is guesswork.** A projected
silhouette is only as good as the camera it is projected through, and a
wrong focal length yields a body outline of the wrong size in the right
place -- which subtracts into a garment boundary that is wrong
everywhere and looks plausible. One model closing both gaps is worth
more than the depth alone.

**The domain risk that applied elsewhere does not apply here.** RFD
1166 records MoGe as unproven on illustration, which is why it was not
a drop-in for See-Through's depth stage. A webcam pointed at a person is
photographs, which is exactly what MoGe was trained on. Same model,
different use, and the caveat does not travel.

MoGe is MIT and already at rung 2 here: 885 nodes, 26 operators, with
`Mod x4` outside `DEVICE_OPS` and unexplained. Nothing in this section
needs it compiled -- it runs on the host beside the fit.

## `contour.py`, which is the first piece of this actually built

`pose-consensus/python/contour.py` turns a mask into a fixed count of
ordered points and back. Trace with Moore neighbours, keep the largest
component, resample by arc length to N.

    shape    round trip IoU at 128 points

    disc     0.966
    square   0.969
    L        0.959

**The round trip is the test.** Fill the contour back in and compare
against the mask it came from; a contour that cannot rebuild its own
mask is not describing it. The bound is 0.95.

Two negative controls, and the second is the useful one:

- shuffling the point order must break the round trip, or nothing has
  tested that the ordering means anything.
- **two separate blobs must FAIL.** One ring cannot hold two regions,
  which this document states as a limit rather than a defect, so the
  test asserts the limit still holds. If somebody later makes
  multi-region contours work, that test fails and sends them here to
  update the claim.

numpy only, and nothing about it needs the accelerator. It is the
smallest piece of the plan and it is done.

## Multi-view is preferred, and the input decides whether it exists

**A webcam is multi-view by construction.** Frames over time are views
of one scene from a moving relationship, so the presence loop gets
multi-view for free and should use it: "a person is scenery if they do
not move" is a temporal statement, and a single frame cannot make it.

**An illustration has one view and there is no second one to take.** A
drawing is not a scene anybody can walk around. For that input,
multi-view has to be *generated* -- which is TRELLIS.2 or Pixal3D --
and then verified back against what conditioned it, exactly the control
rule CLAUDE.md states for poses.

    input          views available     what supplies geometry

    webcam         many, over time     multi-view over frames
    photograph     one, or a few       depends how many were taken
    illustration   exactly one         generated views, then verified

**That is the real split in this pipeline**, and it is not depth
against mapping. It is whether a second view exists.

## LingBot-Map is the one that is licence-clean, and it was never checked

RFD 1050 abandoned it on scope and left two blockers open rather than
answered: the parameter count, and **"License | RFD 1028 gates the
ship"**. Nobody had looked. Looking resolves it in the good direction.

    Robbyant/lingbot-map      Apache-2.0, code
    robbyant/lingbot-map      Apache-2.0, WEIGHTS, stated on the card
    Robbyant/lingbot-depth    Apache-2.0
    Robbyant/lingbot-world    Apache-2.0

That is the pattern from Kimodo and See-Through inverted. There the code
was permissive and the weights were not; here the card says the weights
are Apache-2.0 in as many words.

**And it is the right shape.** Streaming feed-forward reconstruction
from video or an image sequence, emitting camera poses, metric scale and
dense point clouds -- roughly 20 fps at 518 by 378, over sequences past
ten thousand frames.

    what the loop needs        MoGe            LingBot-Map

    person against scene       depth step      the static map itself
    camera                     intrinsics      full poses
    scale                      affine          METRIC
    views                      one             many, which is preferred

It answers the mapping role better than MoGe and better than Metric3D,
which needed the camera it was supposed to supply. MoGe stays useful
for the single-image case, where no sequence exists.

## The walk video can be rendered, which makes the error measurable

A walk video is a camera path, and this workspace already renders camera
paths deterministically. **Mitsuba 3 can produce the input LingBot-Map
consumes**, from geometry already held.

That is worth more than convenience, because it turns an unmeasurable
stage into a measured one:

    render a walk of KNOWN geometry, with a KNOWN camera path
    reconstruct it with LingBot-Map
    the difference is the reconstruction error, exactly

Ground truth is not estimated here, it is the input. RFD 1170 already
makes Mitsuba the reference renderer against Godot; this is the same
instrument pointed at a different consumer, and CLAUDE.md already fixes
the camera sequence, so `sphere_hammersley_sequence` is the path unless
somebody argues otherwise.

**It is also constructed synthetic by CLAUDE.md's definition** --
rendered deterministically from assets held here, labels true by
construction, the same seed reproducing the corpus. Not generated data,
so none of the four conditions apply.

**The domain gap is the honest caveat.** LingBot-Map is trained on real
rooms walked through by real cameras. A Mitsuba walk around one
character is neither, and a model measured only on renders has been
measured on renders. Use it to bound the error and to catch regressions,
not to claim the number transfers to a webcam in a room.

## Mapping models were reconsidered, and the field is licence-hostile

RFDs 1051 and 1052 abandoned WorldMirror 2.0 and TripoSplat when RFD
1064 turned toward character concepts and away from scene
reconstruction. **That reason has inverted** -- the presence loop makes
scene reconstruction a character tool, because the static scene is what
a moving person is separated from. So the abandonment was revisited.

The models are not available:

    tencent/HunyuanWorld-Mirror   tencent-hunyuanworld-mirror-community,
                                  the same family as Hunyuan3D-Part,
                                  blocklisted for excluding the EU, UK
                                  and South Korea
    facebook/VGGT-1B              CC-BY-NC-4.0, non-commercial
    naver/dust3r                  CC-BY-NC-SA, non-commercial AND
                                  share-alike, blocked twice over

**Every learned multi-view reconstructor reachable from here is
non-commercial or territory-restricted.** That is worth recording as a
property of the field rather than as three separate disappointments,
and it is probably why RFD 1064's pivot cost less than it looked like
it would.

**What is licence-clean is classical.** OpenCV is Apache-2.0 and COLMAP
is new BSD, with the caveat COLMAP states itself: its dependencies are
separately licensed and building against them can affect the result.
For a fixed webcam the classical route is also the simpler one --
accumulating a static scene over frames is arithmetic, not a model, and
it needs no checkpoint, no corpus and no licence at all.

## Metric3D v2 was assessed as a fallback, and it is not one

Proposed as a substitute for MoGe. It is not a substitute, and the
reason is the half that was not being thought about.

    MoGe                          Metric3D v2

    affine-invariant depth        METRIC depth, which is better
    RECOVERS intrinsics           CONSUMES intrinsics
    MIT, weights and code         code BSD-2, weights unstated
    exported here, 885 nodes      ONNX published, CC0 claimed

**It needs the camera it was meant to replace.** `hubconf.py` takes
`intrinsic = [fx, fy, cx, cy]` and line 197 computes
`canonical_to_real_scale = intrinsic[0] / 1000.0`, dividing by the
canonical camera's focal length. The depth is only metric because the
focal length was supplied. Swap MoGe out for it and the loop loses the
camera `silhouette.py` projects the body mesh through, which is the gap
MoGe was closing that nobody had asked it to.

**So they chain rather than compete.** MoGe recovers the intrinsics,
Metric3D turns them into metric depth. That is a better arrangement
than either alone and it is two models rather than one, which is a cost
to weigh rather than a free upgrade.

**The licence needs care, and in an unusual direction.** The code is BSD
2-Clause, which is clean. The weights on `JUGGHM/Metric3D` state no
licence at all. The ONNX re-exports at `onnx-community/metric3d-vit-*`
declare **CC0-1.0** -- a third party dedicating to the public domain
weights whose author granted nothing. That is the See-Through problem
inverted: there a downstream party could not relicense restrictions
away, and here a downstream party cannot grant rights it was never
given. A CC0 label over unlicensed weights is not a licence.

**What is genuinely attractive is the export.** `onnx/model.onnx` and
`model_fp16.onnx` are published for three sizes, so rung 1 costs a
download rather than a script. If the licence were resolved this would
be the cheapest operator census in the field.

## The hazard in doing this, which is not small

**Spending the silhouette as an output spends it as a check.**
`silhouette.py` is valuable precisely because it has NO correspondence:
its own docstring says a vertex mislabelled as its neighbour does not
move the outline, so it fails differently from the LBFGS vertex fit and
catches the candy-wrapper failure that fit cannot see.

If the projected contour becomes the segmentation, that independence is
gone. The outline stops being a second opinion about whether the pose is
right and becomes an assumption that it is. **A wrong pose then produces
a confidently wrong garment boundary with nothing left to notice**, and
the failure looks like a clothing bug rather than a fitting one.

So the two uses have to stay separated: fit the pose, check it against
the image silhouette, and only then use the mesh contour as geometry.
Using one silhouette for both is the thing to avoid.

## What the mesh contour does not give

**Hair is not body.** `front hair` and `back hair` are two of the
taxonomy's 23 parts and neither is in a body mesh, so the outline
excludes exactly the parts RFD 1168 spends its argument on.

**A single ring cannot hold a hole or a split**, which is the bound
already stated for contour segmentation and applies here unchanged.

**Scene objects are not in the mesh.** The taxonomy's `objects` bucket
is outside this entirely, and detection-as-contour would be answering
about things no rig knows about.

## Decided: keep keypoints and segmentation, drop detection

Two compiles, not three. The reason is not that keypoints can kludge a
box, though they can.

**RF-DETR-Seg is a DETR, and a DETR's queries carry a class and a box
alongside the mask.** Instance segmentation is not a mask floating free
-- each query emits `pred_logits`, `pred_boxes` and its mask together,
because that is how the architecture separates instances at all. So the
segmentation checkpoint already answers "what is there and where",
which is the whole of what a detection checkpoint would add.

    task            served by                    costs

    pose            keypoint-preview-xlarge      its own HEF
    segmentation    a seg checkpoint             its own HEF
    detection       the seg checkpoint's boxes   nothing

**Dropping detection therefore costs nothing rather than costing
accuracy**, which is a better position than the kludge argument
reached. The kludge -- deriving a coarse box from joints -- stays
available for the case where only the keypoint model is compiled, and
it is a fallback rather than the plan.

**Keypoints cannot be dropped and segmentation should not be.**
Keypoints are `be it`, they are the only model at rung 3, and nothing
else tracks a body every frame. Segmentation is `dress`: RFD 1168 needs
a boundary before it needs anything else, and a garment held up to a
webcam is a boundary from the real world.

**The order is settled by what is already measured.** The keypoint
model is at rung 3 and a seg checkpoint has never been exported here,
so the second compile waits on the first reaching rung 5 -- and on a
card that can run QAFT.

## Express the surviving two as keypoints, because keypoints are fixed-shape

Having dropped detection, the remaining question is what shape the
segmentation output takes. **A keypoint head has a fixed-shape output
by construction, and fixed shape is the single thing the compiler
demands.**

    task            as its own head              as keypoints

    detection       boxes, a variable-length     N centre points, fixed
                    list, then NMS
    segmentation    a mask, then a per-pixel     M contour points in
                    argmax or run-length          order, fixed
    pose            joints                       joints

**The head-shaped versions reach for operators RFD 1131 refuses.** A
detection head wants `TopK` for query selection and
`NonMaxSuppression`, both in `KNOWN_BLOCKERS`, and the second is there
specifically for a data-dependent output shape. A mask head wants
`NonZero` or a scatter. A head that regresses a fixed count of
coordinates wants none of them.

That is the argument. Not that one head is tidier than three, but that
two of the three are shaped like the thing the accelerator cannot do,
and the third is shaped like the thing it can.

**The technique is established rather than invented here.** Detection
as centre points and segmentation as an ordered contour are both
published families, and this workspace would be choosing them for a
reason the papers were not written for.

**It also suits the deployment rule.** A contour is coordinates, which
is data, and CLAUDE.md's glTF constraint is that an export carries pure
data. A mask is pixels and needs somewhere to live.

## What the unification costs, which is not nothing

**A fixed contour cannot express a hole or a split.** A garment
occluded into two pieces by an arm is two regions, and an ordered ring
of M points is one. That is a real loss and it lands on exactly the
case a try-on produces most often.

**Fine boundaries get worse.** M points around a silhouette is a
polygon, and hair, lace or a fringe is not a polygon at any M this
would use. RFD 1168 already bounds the fine parts out on latent
resolution; this bounds them out again for a different reason, and two
independent bounds agreeing is worth more than either alone.

**A kludge is available before any of this.** If only the keypoint head
is compiled, a coarse box follows from the joints and a coarse region
per limb follows from the box. It would place `topwear` roughly where a
torso is. That is enough for RFD 1168's step 1, which only tests the
plumbing, and nowhere near enough to cut a garment out of a photograph.
Take it to close the loop early, not as the answer.

**Only one row differs in hardware terms**, and it is the important
one: `be it` needs rf-detr running every frame on the accelerator,
and `make a friend` does not need the camera at all. The friend is the
cheaper loop to build and the one that runs without the device.

**The division was not chosen.** rf-detr is the only model the Dataflow
Compiler has accepted, and it is the one that must run every frame with
low latency. Everything with a voice in it is autoregressive and cannot
compile. So the device took the body and the host took the speech
because that is what the graphs allow, and it happens to be the right
split — continuous tracking on the accelerator, bursty turn-taking on
the host, which tolerates delay.

## The five stages with no model

Naming these is most of the value of reorganising the document.

1. **Keypoints to a SOMA pose.** rf-detr emits keypoints; ANNY needs a
   pose. `anny_from_soma` exists as a topology, and RFD 1122's
   wholebody gap is the distance between them. Nothing fills it.
2. **A segmenter that knows these classes.** rf-detr-seg is
   COCO-classed and knows `person`, not `topwear`. RFD 1168 records
   that corrupt-clean render pairs would generate the corpus.
3. **Audio to visemes.** RFD 1170 found the Space ships this as two
   minified vendor modules and a `.bin` with no stated licence, so it
   is the part to replace rather than reuse — and whether ANNY even
   carries viseme morph targets is unchecked.
4. **A garment representation.** Every row above treats a garment as
   pixels or voxels. Nothing here says what a `topwear` *is* as a
   shippable asset, and glTF's pure-data rule constrains the answer.
5. **A persona.** `make a friend` needs the character to have a manner
   -- what it knows, how it speaks, what it will not say -- and nothing
   in this workspace holds one. A system prompt is the cheap version
   and a LoRA over Qwen3-VL is the durable one, which is EditScore's
   arrangement pointed at personality instead of judgement.

## What is measured against what

Three oracles, and they are the reason to believe any of it:

    fast thing            reference             the check

    rf-detr C++           PyTorch, gen_reference  .bin diff per tensor
    Godot                 Mitsuba 3               per pixel, per view,
                                                  on sphere_hammersley
    a compiled HEF        the same graph at       to be established
                          full precision

**The third row is empty and that is the gap that matters most.**
Nothing yet compares a HEF's output against the model it came from, so
`compare_precision.py` in `rf-detr-cpp` is the closest thing and it
compares precisions rather than devices. A quantised graph that runs is
not a graph that is right.
