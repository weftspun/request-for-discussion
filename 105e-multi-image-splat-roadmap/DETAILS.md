# RFD 105e details: current state, the three phases, and testing

## Current state

| Path                                            | Images    | Engine                                                                                           |
| ----------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------ |
| `image-to-splat`, one photo                     | 1         | TripoSplat                                                                                       |
| `image-to-splat`, two or more photos            | 2-8       | WorldMirror 2.0, into `gaussians.ply` (falls back to TripoSplat's primary view when unavailable) |
| `image-to-splat`, three or more, no WorldMirror | 3-8       | COLMAP sparse, into a PLY                                                                        |
| `image-to-world`                                | 1 or more | TripoSplat environment, plus optional TRELLIS props                                              |
| Avatar mesh, two or more photos                 | 2-8       | TRELLIS v1's `run_multi_image` (TRELLIS.2 delegates to it when multiview is on)                  |
| Avatar to splat preview                         | 1 or more | TripoSplat, or COLMAP when three or more references exist                                        |

## Phase 1: multi-image UX and the API contract, shipped

Goal: a user attaches several photos, and both the primary photo and
its references flow through the API and into job metadata.

API, optional on every splat, world, and mesh request:

| Field                      | Role                                                      |
| -------------------------- | --------------------------------------------------------- |
| `image_file_id`            | The primary view, required for inference                  |
| `reference_image_file_ids` | Up to seven extra uploaded `file_id`s, eight images total |

Client: multi-select on "Image to Splat," "Image to World," and
"Avatar from Image"; the user marks which thumbnail is primary; the
client uploads every file and sends `reference_image_file_ids` with
the job.

## Phase 2: multiview avatar mesh, shipped, splat turnaround partial

Goal: fuse multiple views for mesh quality, not only splat quality.

Backend, shipped: `mesh_generation` resolves every local path, and
sets `use_multiview_mesh: true` at two or more images.
`trellis_adapter` calls `pipeline.run_multi_image()` when multiview
is enabled. `trellis2_adapter` delegates to TRELLIS v1's own
multiview path when two or more views are present and
`use_multiview_mesh` is not explicitly false.

Client, shipped: a "Use all photos for mesh (TRELLIS multiview)"
checkbox appears once two or more photos are attached, on a
supported task. The avatar pipeline auto-selects
`trellis_image_to_textured_mesh` when references are present and
multiview is on.

Not yet shipped: a Blender turnaround render, producing a splat from
a mesh (8 or 12 views); Hunyuan3D 2.1 multiview wiring.

A real constraint: TRELLIS v1's own multiview path can fail on
GB200-class GPUs (an `xformers` issue). A single-photo avatar still
defaults to TRELLIS.2.

## Phase 3: WorldMirror 2.0 and COLMAP reconstruction, shipped

Goal: real photogrammetry splats from multiple photos.

Backend, shipped:

| Component                     | Status                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| `worldmirror2_reconstruct`    | The primary path: WorldMirror 2.0's feed-forward 3DGS (`thirdparty/HY-World-2.0`)  |
| `colmap_3dgs_reconstruct`     | The fallback, when WorldMirror is unavailable and three or more photos are present |
| The `splat_generation` router | Auto-selects WorldMirror at two or more images                                     |

Client, shipped: `worldmirror2_reconstruct` appears in the model
catalog; image-to-splat auto-routes, one photo to TripoSplat, two or
more to WorldMirror.

Host setup, DGX:

```bash
# Already cloned to thirdparty/HY-World-2.0
bash scripts/install_worldmirror2_deps.sh
# Weights download automatically on the first job, from tencent/HY-World-2.0
```

Optional COLMAP fallback: `sudo apt install colmap`.

Future work: full gsplat training and refinement from COLMAP's own
cameras, not only a sparse point PLY; a dedicated "Photos to Splat"
task type, with real progress stages.

## Related tracks

Arc2Avatar (a separate track): a single-image head-splat composite
on a rigged body. RFD 1054 gives the optional splat preview on
avatar-from-image. RFD 1053 gives the rig contract a mesh's own
bounds must still match, after the template-rig step.

## Testing

```bash
# API, on the DGX
./venv/bin/python -m pytest tests/test_multi_image_input.py -q

# Client, on the Surface
npm test -- src/__tests__/multiImageInput.test.js
```
