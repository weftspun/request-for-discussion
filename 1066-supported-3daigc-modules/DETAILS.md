# RFD 1066 details: the task table, splat status, architecture, and further reading

## Task types, New Task panel

| Task | API feature | Example models (DGX, June 2026) |
| --- | --- | --- |
| Text to 3D | `text_to_textured_mesh` | TRELLIS |
| Image to 3D | `image_to_textured_mesh` | TRELLIS.2 (recommended), Pixal3D (PBR), Hunyuan3D-2.1 |
| Image to Raw Mesh | `image_to_raw_mesh` | Hunyuan3D-2.1, UltraShape |
| Mesh painting (text or image) | `text_mesh_painting` / `image_mesh_painting` | TRELLIS.2, Hunyuan |
| Mesh segmentation | `mesh_segmentation` | P3-SAM |
| Mesh retopology | `mesh_retopology` | AutoRemesher (default), Instant Meshes, Trimesh Decimate |
| Mesh UV unwrapping | `uv_unwrapping` | xatlas |
| Mesh editing (text or image) | `text_mesh_editing` / `image_mesh_editing` | VoxHammer |
| Auto rigging | `auto_rig` | SkinTokens (full GLB, recommended), UniRig (template VRM) |
| Text to Motion (Kimodo) | `text_to_motion` | Kimodo SOMA-RP-v1.1, into studio motion JSON, into VRM/rigged-GLB playback |
| Image to Gaussian Splat | `image_to_splat` | TripoSplat (1 photo), WorldMirror 2.0 (2+), COLMAP (3+) |
| Image to World | `image_to_world` | `weftspun_image_to_world` (a splat environment, plus optional TRELLIS.2 props) |
| Avatar from Image | a client pipeline | TRELLIS.2 mesh, into a UniRig template rig, into a GLB |
| Avatar From Photo | client only | AvatarSDK, not `3DAIGC-API` |

Also shipped, client plus API: multi-image input, a primary photo
plus up to seven references, on splat, world, and avatar tasks (RFD
0094); Publish RP1/OMB validate, sending a mesh job to the spatial
fabric through the MSF Map Service (RFD 1064); Kimodo
text-to-motion, an animation-bar prompt into a SOMA motion job into
viewport playback on a VRM or a rigged GLB
(`KimodoMotionPromptBar.jsx`, `kimodoMotionLoader.js`).

Not in the UI: "Part completion" (legacy upstream docs only).
License-blocked on a commercial tier: PartField, PartPacker,
FastMesh; see `3DAIGC-API`'s own `MODEL_LICENSES.md`.

## Gaussian splats (3DGS)

Splats live inside this app, the same `SceneManager` viewport as VRM
and mesh workflows, not a separate product. Generation runs on the
DGX, through `3DAIGC-API`; viewing uses Spark.js
(`sparkSplatManager.js`, `@sparkjsdev/spark`) in the main Three.js
scene.

### Shipped today

| Capability | Client | API (DGX) |
| --- | --- | --- |
| Splat preview in the viewport | A `SplatMesh`, alongside VRM and meshes | `POST /api/v1/splat-generation/image-to-splat` |
| One photo to a splat | Task Manager's multi-select, one primary photo | TripoSplat |
| Two or more photos to a splat | The same UI; mark the best front view as primary | WorldMirror 2.0 (COLMAP as the fallback, at three or more) |
| World package load | World Library, plus `worldSceneLoader.js` | `POST /api/v1/world-generation/image-to-world` (`weftspun_image_to_world`) |
| A walked, XR environment scan | Task Manager's "Environment Scan" | `POST /api/v1/world-generation/environment-scan` (LingBot-Map) |
| Env-scan Phase A, into Spark | Automatic, when `refine_to_3dgs` is set | Isotropic Gaussians, from a point cloud |
| Env-scan Phase B train | Separate, or `train_3dgs: true` | `POST /train-3dgs` / `env_scan_gsplat_train`, 7 or 10,000 steps |
| Avatar plus optional splat | "Avatar from Image," plus a "Gaussian splat preview" checkbox | TRELLIS.2 mesh, plus a UniRig template rig, plus an optional TripoSplat |
| Multi-image uploads | `multiImageInput.js`, on splat, world, and avatar tasks | `image_file_id` plus `reference_image_file_ids`, up to eight images total |

Task types in the New Task panel: "Image to Gaussian Splat," "Image
to World (splat + props)," "Environment Scan."

### Not done yet

Splat-only world RP1: World Library's own RP1 needs mesh props in
the manifest; a pure Gaussian environment needs a prop-generation
path before it can publish to OMB at all (RFD 1064 gives why).
Env-scan x402 SKUs: Phase A versus Phase B billing, plus a
frame-budget upsell, is roadmap work, not shipped.
Gaussian-VRM/RGBAvatar body pipelines: scan-based full-body avatars,
and the highest-fidelity head-attachment path, are separate from the
viewport's own TripoSplat preview, not the same code path as
`image-to-splat`.

### Where it lives, architecture

```
[DGX 3DAIGC-API]  TripoSplat, WorldMirror/COLMAP, image-to-world, LingBot env-scan A/B, avatar mesh/rig jobs
       |
[this project /]  SceneManager: one renderer, one WebXR session, VRM + tools
       |                  SparkRenderer + SplatMesh (LingBot: orientationMode none)
```

`/xr` stays an IWSDK lab for grab and locomotion regression (RFD
0090). The main app (`/`) runs IWSDK Option A on `SceneManager`:
distance and proximity grab (trigger), a grip that opens a context
menu or pans, and thumbstick locomotion, alongside loaded splat
worlds and a VRM, in the same session.

## Application feature summary

Rendering modes: Solid, Rendered, Wireframe, Skeleton, Part
Colorize. File formats: GLB, GLTF, OBJ, FBX, DAE, STL, VRM; images:
JPG, PNG, BMP, TGA, for image-to-3D workflows.

WebXR: VR with a floor-anchored, virtual-sky scene; AR with
pass-through transparency; Samsung Galaxy XR (Chrome WebXR) as the
primary on-device target; `bounded-floor`, `local-floor`, `local`,
and `viewer` reference spaces (RFD 106c gives the implementation);
WebXR expression tracking when the browser exposes it, a native face
relay through a companion APK when it does not (RFD 1060, RFD
0082).

Also shipped: WebGPU rendering with an automatic WebGL fallback;
SSAO, Bloom, and FXAA post-processing; positional (spatial) audio;
a Core3D integration for a model and materials library; a shared,
mode-detecting 3D viewer (`Universal3DViewer`).

Avatar and VRM: a trait-based VRM character system, with a soulbound
base body and equippable clothing, hair, and accessory layers;
drag-and-drop texture and model overrides; Mixamo integration and
Kimodo text-to-motion for animation; blend shapes, lip sync, eye
tracking, and automatic blinking; an optimized VRM export with
texture atlasing and mesh merging; batch VRM generation from a
manifest; one-click optimization down to a single draw call.

## Key components

Avatar and viewport: `Scene3D`, `TaskManager`, `FileUpload`,
`RenderModeSelector`, `APIStatus`, `SceneManager` (the WebGL-based
core), `Shared3DViewer`, `Universal3DViewer`, `Core3DViewer`,
`Core3DPanel`, `Core3DContext`, `Core3DService`.

Character and animation: `CharacterManager`, `AnimationManager`,
`BlinkManager`, `LookAtManager`, `EmotionManager`. State:
`taskStore`, `sceneStore`, `SceneContext`, `Core3DContext`.

This project began as Open3DStudio, a WebGL-only foundation with
basic 3D AIGC workflows, task management, and file import/export.
The Three.js WebGPU and WebXR migration guide documents the move
from that foundation to the current rendering stack.

## Further reading

RFD 105e (multi-image routing), RFD 105f (NVIDIA XR AI), RFD 1056
(dev machine topology), RFD 106b (world package format), RFD 1064
(spatial fabric/RP1), RFD 1054 (avatar pipeline, client side), RFD
0090 (IWSDK integration), RFD 1060 (OpenXR face tracking), RFD 1052
(the Android XR face-bridge APK), RFD 1069 (webcam/avatar control),
RFD 106c (XR floor anchoring and backgrounds), RFD 1058 (HTTPS
setup), RFD 1055 (the code map).

Not yet moved to a numbered RFD, still under weftspun-3d-studio's
own `thirdparty/m3/docs/` or `src/components/`: the Three.js
WebGPU/WebXR migration guide, VR positioning, the AR/Android XR
floor-anchoring fix notes, the Shared3DViewer and Core3D component
READMEs, the quickstart and avatar-creation guides, the
wallet-owned-assets approach, the model-format specification, the
Modder documentation, and the project history page.
