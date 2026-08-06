# RFD 0089 details: stages, schema, prerequisites, rollout, and risk

## Today versus the target

| | Today (`weftspun_image_to_world`) | Target (`hyworld2_image_to_world`) |
| --- | --- | --- |
| Input | One reference photo | One photo, or text, to a panorama |
| Environment | A TripoSplat single-view `.ply` | A trained 3DGS world, multi-view consistent |
| Scale | A room-sized splat blob | A navigable scene with a real trajectory |
| Props | Optional TRELLIS.2 bounding-box crops | WorldStereo keyframes plus composition |
| Client | `world.manifest.json` plus Spark plus IWSDK | The same manifest contract, extended |
| DGX cost | Roughly 20 GB VRAM, minutes | Multi-stage, hours, 17-billion-plus-parameter models |

WorldMirror 2.0 reconstruction (`worldmirror2_reconstruct`) already
shipped; this RFD covers only the full navigable-world path, a
separate scope.

## The HY-World pipeline, five stages plus panorama

From `thirdparty/HY-World-2.0/hyworld2/worldgen/README.md`:

| Stage | Script | GPU | External dependency |
| --- | --- | --- | --- |
| 0. Panorama | `hyworld2/panogen` (HY-Pano-2) | 1 or more | Hugging Face `HY-Pano-2.0` (roughly 80B, or a 425M Qwen LoRA) |
| 1. Trajectory | `traj_generate.py` | 1 | vLLM plus Qwen3-VL-8B |
| 2. Trajectory render | `traj_render.py` | multi (8 tested) | vLLM |
| 3. World expansion | `video_gen.py` | multi, plus FSDP | WorldStereo-2 (roughly 17B) |
| 4. Gaussian-splat data prep | `gen_gs_data.py` | CPU or GPU | WorldMirror depth and normals |
| 5. 3DGS train | `world_gs_trainer.py` | 1 or more | `gsplat_maskgaussian` |

Output: an optimized Gaussian-splat world plus cameras, exported as
a `.ply` for Spark.js.

## Proposed API shape

New model entry, alongside the existing fast path:

```yaml
# config/models.yaml
image_to_world:
  weftspun_image_to_world:  # existing, the fast path
    enabled: true
  hyworld2_image_to_world:   # new, the quality path
    enabled: false             # flip once the staged pipeline is verified
    vram_requirement: 81920    # the peak across every stage
    max_workers: 1
```

Job input:

```json
{
  "image_file_id": "...",
  "model_preference": "hyworld2_image_to_world",
  "model_parameters": {
    "pano_model": "hy-pano-2-qwen",
    "worldstereo_checkpoint": "auto",
    "llm_addr": "127.0.0.1",
    "llm_port": 8000,
    "llm_name": "Qwen/Qwen3-VL-8B-Instruct",
    "target_path_subdir": "job_{job_id}",
    "skip_stages": []
  }
}
```

Job output, extending the world manifest to version 2:

```json
{
  "version": 2,
  "generator": "hyworld2_image_to_world",
  "environment": {
    "type": "gaussian_splat",
    "url": "environment.ply",
    "scale": 1.0,
    "origin": "floor_center"
  },
  "props": [],
  "collider": null,
  "metadata": {
    "stages_completed": ["pano", "traj", "expand", "gs_train"],
    "hyworld_scene_dir": "outputs/worlds/{job_id}/"
  }
}
```

The client needs no new task type; the same "Image to World" task
gains a model picker naming `hyworld2_image_to_world`.

## Adapter architecture, `3DAIGC-API` side

`adapters/hyworld2_image_to_world_adapter.py`, an orchestrator, not
a monolithic inference call:

```
_process_request():
  1. Stage images into outputs/worlds/{job_id}/
  2. If no panorama exists, run the panogen CLI / HunyuanPanoPipeline
  3. Subprocess: traj_generate.py (needs vLLM)
  4. Subprocess: torchrun traj_render.py
  5. Subprocess: torchrun video_gen.py
  6. Subprocess: gen_gs_data.py
  7. Subprocess: world_gs_trainer.py
  8. Copy the final .ply to its manifest path
  9. Emit world.manifest.json, reusing the existing image_to_world_adapter helpers
```

Progress callbacks write `job_progress.json` per stage, for client
polling. Failure policy: a stage timeout, plus a log tail; the
manifest never partially publishes unless stage 5 completes.

## Infrastructure prerequisites, DGX

| Requirement | Notes |
| --- | --- |
| The HY-World repository | `thirdparty/HY-World-2.0`, already cloned |
| WorldMirror | Already shipped, for splat reconstruction |
| `worldgen` dependencies | `requirements_git.txt`, its submodules, `gsplat_maskgaussian`, a navmesh |
| A vLLM server | A separate process; Qwen3-VL-8B for trajectory stages 1 and 2 |
| Hugging Face weights | HY-Pano-2, WorldStereo-2, WorldMirror (partially already present) |
| Disk | 50 to 100 GB per world job, for intermediates |
| GPU policy | Serialize against other 23GB-plus jobs; a dedicated queue is recommended |

Not available on a single Spark GPU today: the full 8-GPU torchrun
paths. A phased rollout should support a reduced GPU count, or stage
skipping, for a smoke test.

## Phased rollout

Phase A, panorama only (smoke test): the adapter runs HY-Pano-2-Qwen
on the input photo, producing a 360-degree panorama PNG; the client
previews it in an IWSDK skybox or a world-layer placeholder. This
validates the panogen install, Hugging Face auth, and VRAM.

Phase B, trajectory plus render, no WorldStereo: a vLLM sidecar runs
from `scripts/start_vllm_worldgen.sh`; only stages 1 and 2 run,
exporting a camera-path JSON onto the manifest. This validates the
LLM integration and the navmesh submodule.

Phase C, WorldStereo expansion: stage 3's `video_gen.py` runs on one
or two GPUs, a reduced configuration. This validates the 17-billion
parameter model load, and FSDP on GB200.

Phase D, full 3DGS train plus manifest: stages 4 and 5 produce the
`.ply`, loaded through the existing Spark/IWSDK world loader; the
`hyworld2_image_to_world.enabled` flag flips to true, and an A/B
comparison runs against TripoSplat on the same photos.

Phase E, text-to-world: an optional prompt drives HY-Pano's text
mode instead of a photo, through the same pipeline.

## Client changes

| Area | Change |
| --- | --- |
| `aiModelsCatalog.js` | A new `hyworld2_image_to_world` entry |
| `TaskManager.jsx` | A model picker for image-to-world; a multi-stage progress UI |
| `taskManager.js` | Polls `job_progress`/a stage field, once the API adds it |
| `worldPackage.js` | Reads the manifest's version-2 `generator` field; the same splat-load path otherwise |
| `iwsdkWorldPackage.js` | No change needed, if the `.ply` and manifest shape stay the same |

## Risks

| Risk | Mitigation |
| --- | --- |
| Upstream assumes 8 GPUs | Patch torchrun's `--nproc_per_node=1` for a single Spark; document the resulting quality tradeoff |
| vLLM operational burden | Optional: skip the VLM trajectory step, use a fixed camera orbit for a minimum viable version |
| Job runtime measured in hours | `max_workers: 1`, queue priority, a user-facing ETA |
| Licensing | Tencent's own HY-World license, added to `docs/MODEL_LICENSES.md` |

## Testing plan

```bash
# API unit test
pytest tests/test_hyworld2_available.py

# Stage A smoke test, after the panogen install
python -m hyworld2.panogen... --image assets/open3dstudio_demo.jpg

# End-to-end, Phase D
curl -X POST .../world-generation/image-to-world \
  -d '{"model_preference":"hyworld2_image_to_world", ...}'
```
