# Blend-shape animation through the flow adapter, and TokenRig's first light

Two stages of the character pipeline gained running code today: the
rig stage ran its upstream forward pass for the first time, and the
USD-to-Godot bake stage learned to play blend-shape animations.

## TokenRig runs on this desk, without bpy and without flash-attn

`skintokens-auto-rig` was a stub with two `NotImplementedError`s and
sat alone on the demo's critical path. The upstream checkpoint is
confirmed as HF `VAST-AI/SkinTokens` (MIT): TokenRig 1.1 GB, skin VAE
465 MB, a Qwen3-0.6B config. `probe_forward.py` drives it through the
npz loader: trimesh reads the mesh, so upstream's bpy I/O layer is
never imported, which keeps the Blender row of the blocklist
untouched. flash-attn does not build on this desk; a scoped
`flash_attn_interface` stand-in computes through sdpa and is deleted
from `sys.modules` before transformers probes for it, and the Qwen
backbone is forced to `attn_implementation="sdpa"`.

The giraffe example returned 51 joints and a (14807, 51) skin, mean
2.20 joints per vertex above 1%. Row sums came back 0.045 to 2.573
because the voxel post-process is not applied yet; that is the next
step, not a defect. The environment is pixi with torch-gpu cu12, so
the build is declared rather than remembered.

## The bake stage plays blend shapes, and the port fixed a bug the original had

The flow adapter is `v-sekai-fabric/datasource-flow` now. The
`idtx-flow` fork holds two unmerged branches with the blend-shape
animation work, and the restructure moved every file they touch. So
the change was re-derived rather than cherry-picked: TRACK_BLEND_WEIGHT
in the core AnimationConverter, scalar keys in the FlatTree model,
`idtx_anim_track_get_key_float` across the C ABI including
`idtx_core.sigs`, native TYPE_BLEND_SHAPE tracks in the Godot builder,
and playback in UsdSkeletonNode3D resolving shape names onto child
mesh instances.

The original branch sampled blend weights at the joint-transform
timecodes, on the reasoning that both live on the same
UsdSkelAnimation prim. A key that exists only in `blendShapeWeights`,
such as a mid-clip peak, is invisible to that sampling, and the fixture was built with exactly one: weights keyed
0 -> 1 -> 0 at timecodes 0/24/48 against joint samples at 0/48. First
run returned 2 keys instead of 3, both zero. Sampling at
`GetBlendShapeWeightTimeSamples` returns the three. Had the fixture's
peak lined up with a joint keyframe, the spec would have passed on the
broken sampling; the fixture is only as good as the disagreement it
plants.

The spec (`flow/core/spec/test_blend_shape_animation.py`) drives the
built DLL over ctypes with no engine, and carries three controls.
Static weights yield only rest keys, with the population asserted
first so that an empty scan is a FAIL rather than a vacuous pass. A
shapeless rig yields no tracks. The comparator is shown to reject a
planted wrong key.

## The canonical ANNY through the importer, nine ways, checked to 0.1 mm

Three phenotypes (default, heavy, tall_muscular) times three poses
(identity, elbow at 90 degrees, wrist roll at 60 degrees dispersed
across the forearm), built from `anny_rig.build_corpus_model` so the
twist fix rides along, 13,718 vertices each, written as Z-up metre
stages by `mesh_to_usda.py`.

The first run of the checker read 0% coverage on all nine, and the
importer was right: it converts Z-up to Y-up, so every position moves
by (x, y, z) -> (x, z, -y), and it splits vertices per face corner,
13,718 becoming 82,260. A checker that assumes no convention reads a
correct import as total failure. With the stage's declared mapping
applied, all nine variants round-trip with bidirectional position
coverage above 99.9% at 0.1 mm, about an eighth of a credit card's
thickness. Two controls prove the checker can fail: the bent pose is
not covered by the identity source, nor the heavy phenotype by the
default.

## Godot plays it

`datasource-flow-project` turned out to already carry the Godot-side
harness and fixtures, plus the vsekai_godot_mcp addon. Its committed
animation fixture has a valueless `blendShapeWeights`, which is the
content-side half of "blend-shape animations are not done". A new
fixture keys one shape 0 -> 1 -> 0 over two seconds;
`test_blendshape_animation.gd` samples `get_blend_shape_value` while
the stage plays. Animated: 218 samples spanning 0.116 to 0.999.
Static control on the committed fixture: 219 samples, flat at 0.000.

Found and reported rather than fixed: the project's pre-existing
`test_blendshapes.gd` expects `smile` at weight 0.75 from a fixture
that carries `thin`/`angle` with no weight values. It was red against
its own fixture before this work and is red after; the expectations
belong with whoever swapped the fixture.

## Where this leaves the demo

The gacha's critical path was one red stage. It is now a stage with a
proven forward pass and a bake seam that carries the full deformation
budget: LBS, twist bones (the canonical ANNY already has them), and
corrective blend shapes animated in clips. Owed next: the voxel
post-process and skin normalization, a Pixal3D mesh through TokenRig,
skeleton-conditioned skin mode against the canonical ANNY, and the
UsdSkel writer with the VRM joint-map metadata.
