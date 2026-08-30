# In-betweens, phenotype clips, and what pass-through means

The blend-shape work grew in-betweens, phenotype clips, and a stated
pass-through rule today, and each one paid for itself by failing first
in a way a control caught.

## In-betweens bake through a piecewise-linear basis, and the corner control

USD in-betweens are intermediate targets at sub-unit weights. Each is
promoted to its own shape carrying its position, and the primary's
single weight evaluates through the basis (base at 0, in-betweens at
their positions, primary at 1) into per-member values and animation
keys. The trap is at the edges: a weight crossing a member position
BETWEEN two authored samples needs a key inserted at the crossing
time. The fixture plants exactly that: keys at 0 and 1 only, an
in-between at 0.5. A bake without crossing keys leaves the in-between
flat at zero rather than merely undershooting. A second control
catches the other wrong implementation: when the primary reads 0.999
the in-between must read near zero (measured 0.001), because an
in-between wrongly wearing the primary's own curve passes every
min/max check and fails only the phase.

## Phenotypes are clips, not sliders, and clips must be independent

A blendshape moves vertices and never joints, and ANNY's phenotypes
move both. Our own rules close the escape hatches, since a runtime
driver and a custom extension are both banned, but an animation clip
is pure data, and a clip can key the joint transforms default-rest to
phenotype-rest in sync with the shape weight. Scrubbing the clip is
the slider. The shape must then be the RESIDUAL against the
skeleton-only LBS deformation or the change is counted twice: for the
weight axis the residual moves 5,214 of 13,718 vertices where the
dense delta moved all of them.

The first authoring put eleven segments on one timeline, and that was
wrong twice: a 0-1-0 loop cannot hold a phenotype, and one timeline
cannot compose two. The shipped form is eleven INDEPENDENT
SkelAnimation prims, each 0 -> 1 and holding, with a variantSet as the
selector. That is the format's own idiom: multiple SkelAnimation
prims are USD's clip library, variants its documented switch, and
blending is deliberately absent from UsdSkel because it is a
baked-interchange model. The adapter grew the matching feature through
all five rings (converter, flat model, C ABI and sigs, builder, node):
every SkelAnimation imports as a named clip in a library.

Composition then belongs to the engine, and it measured clean through
an AnimationTree of Add2 nodes, one parameter per axis: weight=1 alone
probes the upperleg at 2.18 mm of an authored 2.18, about a penny and
a half; weight and muscle together at 3.49 mm; and both sliders
zeroed return to 0.00. Godot's additive blend subtracts the rest pose
itself, so clips pre-converted to deltas double-count: the same 2.18
mm authored travel probed 100.47 mm, which is the rest origin's own
length, before the clips went back to absolute values.

Two playback facts cost an hour each: the player loops by default and
starts during the async load, so any baseline captured at find-time is
mid-ramp, and closure is periodic, not terminal.

## Pass-through, stated as a systemic rule and applied in both directions

If an attribute is not authored, nothing downstream invents it; if it
is authored, nothing downstream changes it. Applying that rule cut
both ways today. The importer's inline face-normal fabrication and its
grouped-normal resmooth are gone. And the audit it forced found the
opposite defect: the export had been DROPPING authored data, namely
ANNY's 21,334 faceVarying texture coordinates and two whole shape
families.
The canonical fixture now carries everything the source authors: 11
phenotype axes, 52 facial actions, 254 local-change dials (317
shapes), the source's own UVs, and 9-influence skinning. Normals are
genuinely unauthored at the source (vn=0 in base.obj), so the
GENERATOR authors them: it is the asset's author, which is the line
between authorship and fabrication.

Correcting this entry's own inputs: the canonical ANNY has zero twist
bones. Its shipping twist fix is re-weighting, so the graded twist
rides in the skin weights and survives any export that carries them.

## The quaternion frame bug, measured to the digit

The importer rebases rest transforms and translations into Y-up but
passed animation rotations through in the stage's own frame, so a
Z-up stage played its joint animation 125.9 degrees off its own rest
pose at the canonical pelvis. Conjugating a rotation by the up-basis
maps its axis through the basis; predicted against the authored quat,
the sign-flipped twin matched component for component, and after the
fix the offset measured 0.0. The same session fixed a track-offset
accumulation that wrote a third animated attribute's keys past the
end of the vector.

## Sizes, and the container decision

At 317 shapes the fixture's text form reached 92 MB, and the local
dials are honestly dense: a torso scale moves 13,532 vertices at a
0.01 mm threshold, so sparsity thresholds cannot save it. It ships as
a stored usdz package, 23.6 MB, with the zip-ban exemption now written
into the working agreements: a usdz stores its entries uncompressed
and reads in place, so neither hazard the ban names can occur. The GLB
re-export was a static scene until the exporter materialised an
AnimationPlayer, because the adapter plays clips from inside its nodes
and GLTFDocument had nothing to read. Bone tracks then retargeted
through the joint map: full slashed USD joint paths cannot ride in a
:subname, and resolved naively only the slash-free root bone survived,
3 channels against 209 after (104 rotations, 104 translations, one
weights channel packing all 317 morph curves).

## The stress fixture goes back to its source

The committed morph stress usdc was a Blender conversion of Khronos's
MorphStressTest, and it had drifted from its origin: Key_8's authored
range in the canonical GLB is [0, 1], not the 0.1754 the derivative
carried and an earlier version of this record repeated. The fixture is
now generated straight from the GLB by a parser-and-author script, no
Blender in the chain. The test learned something too: a live frame
sweep cannot pin a one-sample-wide authored spike (it read 0.845 at
frame rate), so track fidelity is asserted by densely interpolating
the imported animation, exact to 0.01, and the live sweep only has
to prove playback drives the shape at all.

## Correspondence, checked per slider

Each phenotype axis at 1.0, plus the default body, round-trips
USD-import against an independently parsed GLB with bidirectional
vertex coverage above 99.9% at 0.1 mm -- an eighth of a credit card.
The control demands the heavy GLB fail against the default body, so a
green board is evidence the sliders differ.
