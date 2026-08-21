# RFD 106b details: layout, manifest, XR mapping, and the API calls

## Layout

```
worlds/
  my-world-v1/
    world.manifest.json
    reference.jpg
    environment.ply
    props/
      lamp.glb
```

## Manifest (`world.manifest.json`)

```json
{
  "id": "my-world-v1",
  "version": 1,
  "name": "My World",
  "spawn": { "position": [0, 0, 0], "rotation_y": 0, "player_height": 1.6 },
  "environment": {
    "type": "gaussian_splat",
    "url": "environment.ply",
    "format": "ply",
    "renderer": "spark"
  },
  "props": [
    {
      "id": "lamp",
      "role": "interactable",
      "mesh_url": "props/lamp.glb",
      "transform": { "position": [1, 0, -1], "rotation_y": 0, "scale": 1 },
      "interaction": { "type": "grabbable", "collider": "auto_bbox" }
    }
  ]
}
```

## Scene layers

| Layer | Root | Contents |
| --- | --- | --- |
| Player | `playerRoot` | The rigged avatar (VRM or GLB) |
| World | `worldRoot` | The environment splat |
| Props | `propsRoot` | Interactable mesh props |

An avatar load never replaces the world or its props; a world load
never replaces the avatar.

## XR interaction, Galaxy XR

Mesh props are grabbable in the main app (`/`), through
`SceneManager`'s IWSDK Option A: distance and proximity grab,
thumbstick locomotion, and a grip that opens a context menu on a hit
or pans on a miss.

| Input (Galaxy XR) | Main `/` session |
| --- | --- |
| Trigger (select) | Grab, distance and proximity |
| Grip (squeeze) | A ray hit opens a right-click/model menu; a miss pans |
| Right stick | Locomotion, or teleport aim |

The `/xr` IWSDK lab stays for regression testing
(`iwsdkWorldPackage.js`):

| Input | IWSDK component | Galaxy XR action |
| --- | --- | --- |
| Far grab | `DistanceGrabbable` | Aim, then trigger |
| Near grab | `OneHandGrabbable` | Walk up, then grip squeeze |

Environment splats are visual only, through Spark.js. An optional
`environment.collider_url` supplies a walk mesh for locomotion,
since a splat alone has none.

Open a world directly on a headset:

```
https://<PC-IP>:3000/?worldManifest=/worlds/my-world/world.manifest.json
```

Or from World Library's own "XR" button. Implementation:
`worldSceneLoader.js` for the main `/` session,
`iwsdkWorldPackage.js` for the `/xr` lab.

## API jobs and the Redis TTL

`POST /api/v1/world-generation/image-to-world` registers the job in
Redis, with roughly a 24-hour TTL; the on-disk outputs stay under
`3DAIGC-API/outputs/worlds/{job_id}/` regardless of that TTL.

A walked, Galaxy-XR physical-replica scan uses `POST
/api/v1/world-generation/environment-scan` (LingBot-Map). Passing
`metric_calibration` makes `environment.transform.scale` read in
real meters, one to one; the manifest's own metadata then carries
`metric_calibration.one_to_one` and `coordinate_units: "meters"`.

Phase A and Phase B: `refine_to_3dgs: true` gives isotropic Spark
Gaussians (Phase A). `train_3dgs: true` (or a later `POST
/train-3dgs` call) runs a photometric gsplat train, at 7 or 10,000
steps, densify off. The door metric uses `mode: reference_length`,
`axis: horizontal`, `true_meters: 0.762` (30 inches), measured
against `recon_length`. Gravity alignment uses floor RANSAC by
default (`prefer_floor`); a wall-heavy close-up falls back to
camera-up instead. The client loads LingBot Gaussians with
`orientationMode: 'none'`. See `3DAIGC-API/docs/LINGBOT_MAP_ENVIRONMENT_SCAN.md`
for the full scan pipeline.

`worldSceneLoader.js` routes by source type, not by pipeline name.
An `environment.type` of `gaussian_splat` or `spark`, or any
Gaussian source, loads through the Spark loader only; routing it
through the point-cloud loader instead scatters the Gaussian PLY.
`point_cloud` or `points` loads through the XYZRGB point loader
instead. A gravity-aligned LingBot Gaussian world skips
`anchorObjectBottomToFloor`; running it hoists the whole room, since
the scan is already floor-aligned. LingBot Gaussians also skip
TripoSplat's own 180-degree X flip.

## Floor-Y computation, world layers only

`computeXrFloorAlignmentY` reads bounds from `playerRoot`,
`worldRoot`, and `propsRoot` only, never every child of the XR
scene wrapper; including `viewportGridHelper` or
`viewportAxesHelper` in that bounds pass reintroduces a roughly 1 m
lift. `shouldSkipXrFloorWrap()` excludes the grid, the axes, the
skybox, and other helpers from XR wrapping for the same reason. A
rigged or VRM avatar's own floor bounds come from
`getViewportFloorAnchorBounds(..., { meshFeetOnly: true })`, not a
full-scene `setFromObject`; a multi-skin VRM0 passthrough upload
needs its mesh-feet bounds specifically, since an armature-only or
hips-only bounds box misplaces the feet. A correct computation logs
`[XR][floor]` with `boundsMinY` near zero and the wrapped source
names; a `boundsMinY` near 1, or a wrapped-object count that
includes a helper, is the regression signal.

If the API answers 404 for a job whose files still exist on the
DGX, rehydrate Redis there directly:

```bash
/home/sifr/3DAIGC-API/venv/bin/python \
  /home/sifr/Weftspun3DStudio/scripts/dgx-rehydrate-world-job.py <job_id>
```

The client (`worldPackage.js`) builds manifest URL candidates itself
and surfaces a clearer 404 hint when a rehydrate may help.

## API summary

`POST /api/v1/world-generation/image-to-world`: a DGX-local
pipeline, TripoSplat plus optional TRELLIS props.

`POST /api/v1/world-generation/environment-scan`: a walk video, or
three or more frames, into a LingBot-Map world package, with an
optional Phase A/B 3DGS pass and `metric_calibration` for real,
one-to-one meters.

`POST /api/v1/world-generation/train-3dgs`: a Phase B gsplat train,
against an existing environment-scan world's own `gs_dataset/`.
