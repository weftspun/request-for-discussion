# RFD 1054 details: the quick path, the task table, and the key files

## Quick path

1. Connect to `3DAIGC-API` (DGX).
2. Task: "Avatar from Image" (mesh plus template VRM).
3. Upload a photo, wait for the mesh and the template rig.
4. The viewport loads the rigged GLB.
5. Optional: "Download VRM after pipeline" saves `*.vrm` through the browser.

## What "VRM export from rigged GLB" means

The API returns a rigged GLB. This project's own `VRMExporter` (the
Save panel, or a post-pipeline hook) builds a `.vrm` blob and
triggers a browser download. Nothing uploads unless the user mints
or saves it elsewhere.

```
Photo -> API (TRELLIS) -> GLB
      -> API (template rig) -> rigged GLB
      -> load in viewport
      -> exportAvatarPipelineVrm() -> user downloads avatar.vrm
```

Template expression names can embed in VRM metadata directly. Mesh
morphs need a wrap step instead (see the API's own
`MESH_WRAP_ROADMAP.md`).

## Task types

| Task                             | API                                    | Viewport                          |
| -------------------------------- | -------------------------------------- | --------------------------------- |
| Image to 3D                      | mesh-generation                        | GLB mesh                          |
| Auto rigging, template VRM       | auto-rigging, `rig_mode: template`     | Rigged GLB                        |
| Avatar from image                | mesh plus template rig chain           | Rigged GLB, optional VRM download |
| Image to Gaussian splat          | splat-generation                       | Spark `SplatMesh`                 |
| Avatar from image, splat checked | the above, plus TripoSplat in parallel | Body GLB plus splat preview       |

## Rig alignment and the contract

The API's export validates against RFD 1053's contract. After a new
avatar-from-image job, grep the remote log for `[API-Contract]
PASS`.

A backward rig, or one floating at the hips, means re-running after
pulling the latest API, not a client-side fix. The Blender script
aligns on Z-up (Blender's own vertical axis after a glTF import),
not glTF's Y-up. Feet align to the mesh ground, the skeleton is no
longer inverted (head up, feet down), and this project skips its own
auto-180°-reorient and rig-repair heuristics for `fromAigc` loads.
The client validates pre-process and post-viewport-layout only, no
client-side rig hack.

## Blend shape sources

| Source              | Expressions                                                   |
| ------------------- | ------------------------------------------------------------- |
| `template.vrm`      | 124+ morphs, ARKit/Vive-style, on the template's own topology |
| A rigged AIGC mesh  | Skeleton only, until a wrap step runs                         |
| Arc2Avatar (future) | FLAME, on head splats                                         |
| TripoSplat          | Preview only, not a rigged VRM                                |

XR face tracking needs a wrap or a head-stitch step, tracked in the
API's own docs.

## Uploaded VRM, a separate path

A user-uploaded `.vrm` file takes a separate path from a rigged GLB
this pipeline produces. RFD 1068 gives that path (scene-root
transforms, multi-skin rebind, skeleton visualization, the
export round-trip).

## VRM drag-drop metadata

`CombinedImport` plus `vrmTemplateMetadata.js`: dragging a `.vrm`
parses its extensions (`VRM` or `VRMC_vrm`), stores presets in
`sessionStorage`, and optionally pairs it with a splat preview URL
(`attachSplatPreviewMetadata`).

## Key files

| File                                   | Role                                                |
| -------------------------------------- | --------------------------------------------------- |
| `src/library/avatarPipelineCatalog.js` | Template id, rig modes                              |
| `src/library/taskManager.js`           | `executeAvatarFromImage`, the template rig API call |
| `src/library/avatarPipelineExport.js`  | The post-pipeline VRM download                      |
| `src/library/vrmTemplateMetadata.js`   | VRM file parsing, splat pairing                     |
| `src/library/sparkSplatManager.js`     | Spark.js splats                                     |
| `src/components/TaskManager.jsx`       | The UI tasks, the export checkbox                   |

## Tests

```bash
node node_modules/vitest/vitest.mjs run src/__tests__/avatarPipelineCatalog.test.js src/__tests__/taskManagerTemplateRig.test.js
```
