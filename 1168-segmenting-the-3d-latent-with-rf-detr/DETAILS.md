# RFD 1168 details: what already exists, and the two things that bound it

## The three pieces, and where each is

Nothing here is proposed from scratch. The proposal is a payload change
to a call that already runs.

    piece               where it is                          state

    the segmenter       rf-detr, SegmentationHead, and
                        `convert_segmentation_to_gguf.py`    in tree
    the lift            `voxhammer/extract_feature.py:96`,
                        `F.grid_sample(patchtokens, uv...)`  in tree
    the views           `sphere_hammersley_sequence` in
                        `trellis/utils/random_utils.py`      in tree
    the label set       `VALID_BODY_PARTS_V3`, 23 parts,
                        `common/live2d/scrap_model.py`       in tree

**`grid_sample` does not care what the channels mean.** Today it carries
1024 DINOv2 channels onto voxel centres. Carrying 23 class logits
instead is the same call with a different tensor, and the uv it samples
at is computed from the camera the renderer already used.

**The segmenter is the one model at rung 3.** RFD 1167 records rf-detr
as the only candidate the Dataflow Compiler has accepted -- 825 nodes,
22 operators, nothing outside `DEVICE_OPS`. A segmentation head is small
beside the backbone it sits on, so the device half already measured is
most of this.

## Why 3D is the right place, rather than a workaround

The layer names that matter are depth relations wearing appearance
names. `front hair` and `back hair` are not two textures, they are the
same material on either side of the head, and **a rendered view is
exactly where that distinction is destroyed** -- from the front, one
occludes the other and the pixels do not say which is which.

This is the same fact CLAUDE.md states from the other side when it says
a photograph has no ground-truth `front hair` / `back hair` split, and
why the blinded COCO holdout cannot validate this task. A 2D segmenter
is being asked for something its input does not contain.

Voxel centres carry it for free. Behind-the-head is a coordinate, not an
inference, so the split that is hardest in 2D is nearly free in 3D.
Multi-view voting over the Hammersley sequence then settles the parts
that are genuinely appearance rather than depth.

## Masking is corruption, and it is what makes the layers whole

Segmentation alone does not produce layers. It produces regions of a
surface, and a layer that stops where another one covered it is not a
layer -- it is a silhouette with a bite taken out. `back hair` has to
come out whole or it cannot be posed, restyled or painted on.

**So cut the occluder and call the hole corruption.** Remove `front
hair` and what is behind it is missing rather than wrong, which is the
shape of problem inpainting already solves. Neither candidate for that
job segments: rf-detr says where the boundary is, the mask makes the
hole, and the inpainter fills it.

## Two inpainters, and the choice is licence against accelerability

**LaMa is what See-Through used, and it is licence-clean.**
`annotators/lama_inpainter` loads `lama_large_512px.ckpt` from
`dreMaz/AnimeMangaInpainting`, which is **MIT**, over upstream LaMa code
which is **Apache-2.0**. Unlike every See-Through checkpoint RFD 1166
blocklists, this one carries a real grant -- so the useful part of that
project survives its licensing twice over, once as the taxonomy and once
as this.

It is also already the right domain. The checkpoint is fine-tuned for
anime and manga, which is the illustration domain the whole task sits
in, and it is a purpose-built inpainter rather than something adapted
into the role.

**And it will not compile for the accelerator.** LaMa is built on Fast
Fourier Convolutions: `ffc.py` calls `torch.fft.rfftn`, and no Fourier
operator appears anywhere in `DEVICE_OPS`. RFD 1131 names the refused
families and this is a new one -- not data-dependent indexing, simply
absent from the allowlist. LaMa runs on the host or it does not run.

**CycleGAN is the opposite trade.** It is a ResNet-9block generator,
plain convolution throughout, which is why RFD 1166 scores it 95 on
`shape` -- second only to rf-detr. It would compile. But it is an
unpaired translation model rather than an inpainter, so using it here
means training it for hole-filling, and the corruption pairs below are
exactly the supervision that would take.

    inpainter   licence            domain        compiles

    LaMa        MIT / Apache-2.0   anime, manga  no, rfftn is not
                                                 in DEVICE_OPS
    CycleGAN    BSD-3-Clause       untrained     yes, plain conv
                                   for this

So the recommendation is LaMa on the host for quality, and CycleGAN as
the option if this ever has to run on the device. That is a decision
about where the stage runs, not about which model is better, and it does
not need making until something forces it.

**The framing is worth more than the mechanism, because it supplies the
corpus.** The first bound below is that a segmenter has no labelled data
for this taxonomy. Corruption pairs do not have that problem:

    render an asset with every layer          -> the clean target
    render it again with one layer hidden     -> the corrupt input
    the difference                            -> that layer, whole

Both frames come from the same rig, the same seed and the same camera
sequence, so the pair is exact and the label is true by construction. No
annotator, no inference, and no generated data -- this is the
constructed synthetic CLAUDE.md admits as ordinary training data, with
`syn_data.py`'s Live2D renders as the reference case.

**It is also a negative control for free.** Hide a layer that is fully
occluded from a given view and the corrupt and clean frames are
identical; a model reporting a difference there is reporting noise. A
pipeline that cannot produce that case has not shown its difference
means anything.

## The first bound: the segmenter does not know these classes

RF-DETR-Seg is trained on COCO. It segments `person` and `object`, and
knows nothing of `topwear`, `earwear` or `back hair`. **The proposal
needs a retrain onto `VALID_BODY_PARTS_V3` and that needs labelled
data.**

That is the same wall RFD 1166 records for Kimodo, reached from a
different direction: the model is available and the corpus is not. What
is on hand:

- **Constructed synthetic is the honest candidate, and the corruption
  framing above is how it is generated.** Live2D drawables
  and ANNY rigs render deterministically with labels true by
  construction, and `VALID_BODY_PARTS_V3` came out of a Live2D scraper
  in the first place, so the vocabulary and the assets already agree.
  This is ordinary training data under CLAUDE.md, not generated data.
- **The blinded holdout cannot validate it**, for the reason above. Held
  out illustrations are needed and this workspace does not have a
  labelled set of them.
- **See-Through's own weights cannot supply labels.** They are
  blocklisted, and using a blocklisted model as a teacher would carry
  its licence into the student, which is the propagation the OpenRAIL-M
  row exists to stop.

## The second bound: the latent is coarser than the taxonomy

The sparse structure stage emits a voxel grid, and the taxonomy's finest
parts are far below it. `irides`, `eyewhite`, `eyelash` and `eyebrow`
are millimetres on a face -- about a credit card's thickness, 0.76 mm,
for a lash -- and no voxel in a structure latent is that small.

So the reachable label set is the coarse half: `front hair`,
`back hair`, `headwear`, `topwear`, `bottomwear`, `legwear`, `footwear`,
`tail`, `wings`. The eye and mouth parts are not reachable here at any
segmenter quality, and a result claiming them would be reporting the
segmenter's 2D confidence rather than anything the latent holds.

**This is worth stating before anyone measures it**, because a run that
scores well on nine coarse parts and badly on four fine ones will look
like a model problem and is a resolution problem.

## Laddering, and why the order is the decision

`The Embedder's Dilemma: LLMs Are Better, but at What Cost?` is the
framing offered for this, and it is applied here as a rule about
ordering rather than as a cited result -- nobody here has read it, and
the RFD should not lean on claims it has not checked. The rule it names
is the one RFD 1167 already runs on: **climb only as far as the answer
requires, and find out at each rung whether the next one is needed.**

Every choice in this document has that shape, and each ladder has a
cheap bottom that can refute the whole thing:

    question            bottom rung                    top rung

    does the lift work  a one-hot constant through     a retrained
                        `grid_sample`, no model        segmenter
    does the segmenter  stock COCO `person`, a         23-part
    reach the latent    checkpoint already held        `VALID_BODY_PARTS_V3`
    which parts are     the nine coarse ones           the eye and mouth
    reachable                                          parts
    where does the      LaMa on the host, MIT and      CycleGAN compiled,
    inpainter run       already domain-tuned           trained for this

**The inpainter row is the one where the dilemma bites.** LaMa is better
and does not compile; CycleGAN compiles and is not trained for the job.
The laddered answer is not to pick now: run LaMa on the host until
something measured says the stage must be on the device, and only then
pay for the training that CycleGAN would need. Choosing early costs
either quality or a corpus, and nothing yet demands either.

**The rungs below are ordered by what they cost, not by what they
prove.** That is deliberate: a step that costs an afternoon and can
refute the proposal outranks one that costs a corpus and can confirm it.

## What would settle it, in the order it should be tried

1. **Carry a constant through the lift.** Replace `patchtokens` with a
   one-hot tensor and confirm the voxels come back labelled. This tests
   the plumbing and needs no trained segmenter at all.
2. **Carry COCO `person` through it.** The stock RF-DETR-Seg checkpoint
   already emits this, so a whole-body mask lifting cleanly onto the
   latent is a real end-to-end result on an untrained taxonomy.
3. **Only then retrain**, on constructed synthetic, against the nine
   coarse parts rather than all 23.

Steps 1 and 2 cost no data and no training, and either can refute the
proposal on its own. Doing them before the retrain is the difference
between finding out in an afternoon and finding out after a corpus.

## What this does not claim

It does not claim either inpainter decomposes anything. rf-detr finds
the boundary; the inpainter only makes the remainder whole. Naming the
inpainter the decomposer would put the work in a component that cannot
do it.

**It does not claim the inpainting happens in the latent.** LaMa is a
2D image model, so on the obvious reading it completes rendered views
which are then lifted, and the layers are assembled from multi-view
agreement rather than repaired in three dimensions. Completing the
latent directly is a different and harder thing, and nothing here has
shown which one the task needs.

It does not claim parity with See-Through. See-Through decomposes an
illustration into raster layers a person can paint on; this labels a
sparse latent and fills what a mask removed. They answer different
questions and only one of them is available.
