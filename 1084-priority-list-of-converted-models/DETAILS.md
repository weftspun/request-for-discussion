# RFD 1084 details: the conversion order and what it rests on

Every model in one table, from two sources that did not agree.

RFD 1010 inventories fifteen, drawn from `src/library/aiModelsCatalog.js` -- the
studio's catalog. `default.xml` records what is checked out, per goal. Neither is
a subset of the other, and an order built from one alone orders work that is
partly somewhere else.

    in RFD 1010 and on this goal's manifest          4
    in RFD 1010 but pinned to the mesh-latents goal  5
    in RFD 1010 and in no manifest here             6
    on a manifest and absent from RFD 1010          8
    in use with no repo and no catalog entry        2

## Ranked measured

`goal` is what `default.xml` says, which is what decides placement: `main` for
the keypoint goal, the `mesh-latents` tag for the other. A dash means the
catalog names it and no manifest here checks it out, so nobody can census it.

**TRELLIS2 is superseded by Pixal3D and is not in the table.** Both draw their
views from `sphere_hammersley_sequence` -- `render_view.py` names them together
-- so Pixal3D inherits the structured-latent lineage, and the mesh-painting
stage TRELLIS2 provided is derivable from it rather than lost. The three
`trellis2-*` repositories are still checked out on the mesh-latents tag and no
RFD records the supersession; this is the first place it is written down, which
means RFD 1026 and RFD 1027 package models nothing now plans to convert.

**Two models are in use with no repo of their own.** OmniGen2 and EditScore are
pip dependencies inside `6-datasource/anny-render-corpus`, declared as the
`omnigen2` and `editscore` pixi features, and neither appears in RFD 1010 nor as
a `<project>` anywhere. They are not missing by oversight -- they are used by the
corpus pipeline rather than served from the catalog, so nothing that enumerates
model IMAGES would ever find them. That is the third way a model can be absent
from a list of models, after "on the other goal" and "in no manifest at all".

| model id                        | goal         | status                            |
| ------------------------------- | ------------ | --------------------------------- |
| rfdetr keypoint                 | keypoint     | **rank 1, measured**              |
| omnigen2                        | keypoint     | in use, no repo, absent from 1010 |
| editscore                       | keypoint     | in use, no repo, absent from 1010 |
| qwen35_defiant                  | mesh-latents | uncensused, absent from 1010      |
| gemma4_composer                 | mesh-latents | uncensused, absent from 1010      |
| seethrough_layer_decomposition  | keypoint     | uncensused                        |
| skintokens_auto_rig             | keypoint     | uncensused                        |
| cyclegan_style_transfer         | keypoint     | uncensused, absent from 1010      |
| pose_consensus                  | keypoint     | uncensused, absent from 1010      |
| pixal3d_image_to_textured_mesh  | mesh-latents | uncensused                        |
| pixal3d_image_mesh_painting     | mesh-latents | derivable, no repo yet            |
| voxhammer_text_mesh_editing     | mesh-latents | uncensused                        |
| voxhammer_image_mesh_editing    | mesh-latents | uncensused                        |
| kimodo_text_to_motion           | keypoint     | uncensused                        |
| tropes_removal_model            | keypoint     | uncensused, absent from 1010      |
| multimodal_semantic_ids         | mesh-latents | uncensused, absent from 1010      |
| residual_fsq_recommender        | mesh-latents | uncensused, absent from 1010      |
| unified_modal_embedder          | mesh-latents | uncensused, absent from 1010      |
| weftspun_image_to_world         | -            | uncensused, no checkout           |
| lingbot_map_environment_scan    | -            | uncensused, no checkout           |
| worldmirror2_reconstruct        | -            | uncensused, no checkout           |
| triposplat_image_to_splat       | -            | uncensused, no checkout           |
| qwen_q4_k_m_image_edit          | -            | **blocklisted**                   |
| p3sam_mesh_segmentation         | mesh-latents | **blocklisted**                   |
| krea2_turbo_text_to_image       | -            | **blocklisted**                   |

The device half at 576 with `num_windows=1` is **825 nodes over 22 distinct
operators**, and every operator is inside `gate_onnx_device.py`'s allowlist. The
numeric check against PyTorch holds at 3.3e-6. Reproduce with
`scripts/gate_onnx_device.py --num-windows 1`.

**It does not yet compile, and that is why it stays first rather than a reason to
move it.** Parsing takes 36 s and optimization 1001 s, and then the allocator
refuses:

    slice1 failed on kernel validation: slice1 has 2 APUs but max allowed is 1
    BackendAllocatorException: No successful assignments: ne_activation_ew_sub_softmax4

That is a resource-placement failure on one layer, not a memory limit. The
weights are about 25 MB at int8 against a module carrying 4-8 GB of LPDDR4, so
capacity is not what stops it. Every allocator error carried
`NO_CONTEXT_ENABLED`, so multi-context compilation is the untried lever.

A second model would inherit this obstacle without adding information about it.

## The two with no repo

OmniGen2 generates the posed corpus in `gen_posed_from_reference.py`, and
BLOCKLIST.md names it as the replacement for Qwen-Image-Edit: 7.8B, Apache-2.0,
clean output on the same input that the blocked model corrupted. EditScore grades
those edits in `score_edits.py` -- a reward model rather than a generator, which
is why the measured refusal count there was zero of twelve and the search for an
uncensored base was unnecessary.

Neither is a conversion candidate today. Both run in the corpus pipeline on the
desk, not on the accelerator, and converting a 7.8B generator to a 24 GB-class
edge device is a different question from converting a detector. They are in the
table because a list of models that omits the two doing daily work is not a list
of models.

## The three that are excluded

Qwen-Image-Edit is 20.4B and runs here only quantised, and quantised it corrupts.
P3-SAM carries a territory-restricted licence excluding the EU, the UK and South
Korea. Krea 2 is revenue-gated and the restriction propagates.

The identifier `qwen_q4_k_m_image_edit` names the Q4_K_M build directly, which is
the quantised path the entry excludes -- the catalog identifier and the reason
for exclusion are the same fact. `BLOCKLIST.md` carries the argument for each.

Ranking them would send somebody to work the agreements have already closed.

## What ordering the rest requires

One number per model, and the tooling to produce it already exists:

1. Export to ONNX and census the operators, as `gate_onnx_device.py` does.
2. Run `check_device_ops.py`, which sorts every operator into observed and
   documented and reports which fall outside both.
3. Count how many operators need a secondary-path rewrite. 139 of the 178
   operators at opset 17 reduce to the 58 the device executes, so a model drawing
   only on those needs no new work; one reaching into the 39 refused operators
   may not be convertible at all.

The rank then follows from a measurement rather than a preference: fewest
operators outside the executable set goes first.

**The refused set is where a model becomes unconvertible rather than
inconvenient.** Four categories are permanent -- data-dependent output shape,
control flow, non-tensor types, and nondeterminism -- and no rewrite reaches
them. A model needing `NonZero`, or `TopK` with a data-dependent count, or `If`
does not get a lower rank; it gets a different deployment target.

## What this leaves for other RFDs

**RFD 1010 is missing eight models that are checked out**, three on this goal and
five on mesh-latents. Either its catalog is narrower than the workspace on
purpose, or it has drifted; this records the difference rather than deciding
which.

**Four catalog models have no checkout in either manifest here.** They cannot be
censused until somebody places them, and CLAUDE.md's Sides rule says an unplaced
project is the drift the six words exist to stop.

It does not decide whether a model that fails the census should be converted
partially, split across the accelerator and the backup runtime, or left on the
backup entirely. `nx_shuttle` already reports operators that run on one target
and not the other, so the split is measurable; whether to take it is a decision
nobody has made.
