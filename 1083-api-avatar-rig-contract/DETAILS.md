# RFD 1083 details: coordinate system, requirements, failure codes, and the Blender path

## Coordinate system (glTF / three.js)

| Axis | Role                                        |
| ---- | ------------------------------------------- |
| Y    | Up                                          |
| -Z   | Character forward, faces the default camera |
| X    | Right                                       |

Blender scripts run in Z-up internally; glTF import and export
convert to and from this contract.

## Export requirements

1. A skinned mesh, at least one skin, 40 or more joints for a humanoid template rig.
2. Applied transforms: armature and mesh transforms baked (`export_apply=True`).
3. One coordinate space for mesh vertices and joint rest positions.
4. Upright: spine above hips (client check), head above feet (API glTF check).
5. Forward: character forward aligns with -Z.
6. Vertical co-location: mesh and bone centers within roughly 35% of mesh height.
7. Hips at torso: hips near 52% ± 15% of mesh height (client), or 25-70% from the feet (API).
8. Feet on floor: foot bones and mesh feet share the same ground plane (client check).

## Failure codes

| Code                          | Blocks API export    | Client                                             |
| ----------------------------- | -------------------- | -------------------------------------------------- |
| `character_upside_down`       | yes                  | fails                                              |
| `character_facing_backwards`  | yes                  | fails                                              |
| `missing_skinned_mesh`        | yes                  | fails                                              |
| `insufficient_joints`         | yes, under 40 joints | —                                                  |
| `mesh_bone_vertical_mismatch` | no, advisory         | fails                                              |
| `hips_not_at_mesh_torso`      | no, advisory         | fails                                              |
| `api_validation_failed`       | —                    | fails, when `rig_info.validation.passed === false` |

Client-only structural codes: `no_model_root`, `empty_mesh_bounds`,
`empty_bone_bounds`, `missing_hips_bone`, `no_bones_in_glb`,
`mesh_bone_feet_mismatch`.

Severity split: the API fails a job only on a critical code
(`character_upside_down`, `character_facing_backwards`,
`missing_skinned_mesh`, `insufficient_joints`). Advisory codes still
appear in `rig_info.validation.codes` and
`metrics.advisoryCodes`. The client logs FAIL whenever any row above
fires in the viewport, a stricter second check after download.

## Design split, VRM versus AIGC

| Path     | Source                                        | Client behavior                                                                                                                                                                                |
| -------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VRM load | A `.vrm` file, loot assets, and so on         | `vrmLoader.normalizeVRM` only; no contract flags, no `preserveExportedOrientation`. RFD 1104 gives the full pipeline.                                                                          |
| AIGC GLB | Avatar-from-image or template rig, on the DGX | Validates against this contract. Targeted skinned-mesh repair runs when `needsSkinnedMeshRigRepair` fires (a contract FAIL, a feet/XZ mismatch, or a template-rig export). Feet anchor to y=0. |

The DGX template rig should export a GLB in the same coordinate
frame as `template.vrm`
(`humanoid_template_id: "template"` maps to
`assets/example_autorig/template.vrm`). A contract violation means
the Blender export step drifted from that reference; fix it on the
DGX, never by reusing VRM loader flags on VRM files.

## Implementation

| Side                    | File                                                                                                                                   |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Client validate and log | `src/library/aigcRigContract.js`                                                                                                       |
| Client rig repair       | `src/library/rigBoneUtils.js`: `needsSkinnedMeshRigRepair`, `normalizeRiggedModelTransforms`; feet anchor via `anchorModelFeetToFloor` |
| API export gate         | `3DAIGC-API/core/utils/aigc_rig_contract.py`: `validate_aigc_rigged_glb()`                                                             |
| Blender template rig    | `3DAIGC-API/scripts/blender/apply_humanoid_template_rig.py`                                                                            |
| Job payload             | `rig_info.validation = { passed, codes, metrics }`, on template rig completion                                                         |

### The template-rig Blender path

`3DAIGC-API/scripts/blender/apply_humanoid_template_rig.py`:

1. Uniform-scale from the armature's bone span to the target mesh height (Blender Z-up, after the glTF import).
2. Yaw or flip the armature to face glTF -Z, before parenting; this step must not rotate the skinned mesh.
3. Move the foot bones to the mesh floor (the minimum Z, in Blender).
4. Center on Blender's XY ground plane.
5. Envelope the skin, then export the GLB with `export_apply=True`.

Do not align on Blender's Y axis for height; that caused the
inverted rigs found in June 2026. Do not yaw the armature after
parenting; that rotates the mesh away from the upload, also found
in June 2026.

## Validation timing, client side

1. Pre-process: the raw GLB, right after load, before `processModel`'s scale and ground step.
2. Post-viewport-layout: after that scale and ground step.

Grep the remote log for `[API-Contract]`.

## Retest

1. Hard-reload this project.
2. Run "Avatar from Image" as a new job.
3. Grep the remote log for `[API-Contract] PASS`.
4. Confirm an upright mesh and skeleton, in both Solid and Skeleton view modes.
