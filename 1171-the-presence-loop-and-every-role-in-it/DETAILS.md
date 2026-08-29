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
    find the boundary          rf-detr-seg          converter written,
                                                    COCO-classed
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

## The webcam is not only a motion source, and one HEF covers all of it

The table above says "body motion, a webcam" and that undersells it.
rf-detr carries three heads -- **keypoints, segmentation and object
detection** -- and they sit on one backbone.

**That backbone is the device half.** `gate_onnx_device.py` builds it
from `model.model.model.backbone[0]` under a docstring reading *"The
backbone and projector, which is exactly what would be compiled"*, and
`rf-detr-cpp/scripts/` holds separate GGUF converters for the decoder,
the keypoint head and the segmentation head. So the arrangement is one
compiled graph and three small heads on the host:

    on the device     the backbone and projector, 825 nodes, rung 3

    on the host       keypoint head    -> a pose
                      segmentation head -> a mask per part
                      decoder          -> boxes

**One HEF therefore serves every camera task in the loop**, and the
825-node translation already measured is most of the work for all three
rather than for pose alone. That is a better position than RFD 1166
described, where rf-detr was scored as though it did one thing.

## So the camera feeds all four movements, not just `be it`

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

## Express everything as keypoints, because keypoints are fixed-shape

The three heads can be collapsed into one, and the reason is not
economy. **A keypoint head has a fixed-shape output by construction,
and fixed shape is the single thing the compiler demands.**

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
