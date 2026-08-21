# RFD 1064 details: architecture, endpoints, environment mapping, and code

## Architecture

```
[this project]  World Library, GLB Export, Task Manager
       |  spatialFabricAdapter.js + useSpatialFabric hook
       v
[3DAIGC-API :7842]  /api/v1/spatial-fabric/*
       |  publish_glb_to_msf, OMB validation
       v
[MSF_Map_Svc on DGX]  Scene Assembler + fabric/*.msf
       v
[Open Metaverse Browser]  VR/AR spatial fabric (the OMB ecosystem)
```

## Client entry points

| UI            | Action                                                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Task Manager  | "Publish RP1" on a completed mesh job. "OMB" opens the Scene Assembler.                                                                         |
| GLB Export    | "Validate OMB tier". "Send To Metaverse Browser" (viewport GLB plus compression settings).                                                      |
| World Library | "Open Metaverse Browser", or a per-world RP1 (publishes mesh props from the manifest). "XR" loads the splat plus props in the main `/` session. |

## API endpoints (`3DAIGC-API`)

| Method | Path                                     | Purpose                                                     |
| ------ | ---------------------------------------- | ----------------------------------------------------------- |
| `GET`  | `/api/v1/spatial-fabric/config`          | Public MSF URLs plus the company id                         |
| `GET`  | `/api/v1/spatial-fabric/assets/{job_id}` | Mesh stats plus OMB tier, before publish                    |
| `POST` | `/api/v1/spatial-fabric/validate-glb`    | Upload a GLB for OMB tier analysis                          |
| `POST` | `/api/v1/spatial-fabric/publish`         | Copy a completed job's GLB into the MSF object library      |
| `POST` | `/api/v1/spatial-fabric/publish-glb`     | Upload a viewport or export GLB into the MSF object library |

## Environment mapping, DGX to Surface

| DGX (`3DAIGC-API`'s `.env`) | Surface (`.env`)          |
| --------------------------- | ------------------------- |
| `MSF_PUBLIC_BASE_URL`       | `VITE_MSF_PUBLIC_URL`     |
| `MSF_FABRIC_MSF_URL`        | `VITE_RP1_FABRIC_MSF_URL` |
| `RP1_COMPANY_ID`            | `VITE_RP1_COMPANY_ID`     |

On the DGX, `3DAIGC-API/scripts/sync-spatial-fabric-env.sh` copies
values from `~/.config/rp1-spatial-fabric/rp1.env` into the API's
own `.env`.

The API needs a restart after adding a spatial-fabric route or an
MSF env var; `start_services_detached.sh` sources `.env`, so
`MSF_PUBLIC_BASE_URL` reaches every worker. Verify with `curl
http://127.0.0.1:7842/api/v1/spatial-fabric/config`; it should
answer `"enabled": true`. When `VITE_API_ENDPOINT` is set, the
client prefers the live `/spatial-fabric/config` response over its
own static `VITE_*` values.

## OMB tier budgets

Client-side hints mirror the API's own limits
(`spatialFabricAdapter.js`'s `OMB_TIER_LIMITS`). "Validate OMB tier"
in GLB Export, or the "Publish RP1" preview in Task Manager, gives
the authoritative server-side analysis. See the OMB's own
spatial-fabric model guidelines for the budget rules themselves.

## Task Manager RP1 versus World Library RP1

| Entry point                 | Publishes                                               | Works when                                                                                                                                                    |
| --------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task Manager, "Publish RP1" | A completed mesh job's GLB, into the MSF object library | Any finished text-to-3D or image-to-3D job with an on-disk GLB                                                                                                |
| World Library, RP1          | The mesh props listed in `world.manifest.json`          | The world holds `props[]` with a `mesh_url` (TRELLIS props). A splat-only world (`prop_count` 0) cannot RP1-publish; an environment splat is not an MSF prop. |

Log markers distinguish the two: `[SpatialFabric] publish complete`
for a mesh job, `[SpatialFabric] world publish complete` for world
props.

## Code

| File                                  | Role                                                       |
| ------------------------------------- | ---------------------------------------------------------- |
| `src/library/spatialFabricAdapter.js` | The API client, URL resolution, OMB helpers                |
| `src/hooks/useSpatialFabric.js`       | The shared React hook for config, open, and publish        |
| `src/components/TaskManager.jsx`      | Publishes a completed mesh job                             |
| `src/components/GLBExport.jsx`        | Validates an export, opens the browser                     |
| `src/components/WorldLibrary.jsx`     | Loads worlds, XR, RP1 props publish, Scene Assembler links |

DGX: `/home/sifr/MSF_Map_Svc` runs the MSF Map Service and the Scene
Assembler.

`TaskManager.jsx` reads its API endpoint from `getApiEndpoint()`
only. It carries no second, duplicate `apiEndpoint` prop for the
same value. Product strings in this area say "Weftspun3DStudio";
"Character Studio" appears only as attribution, never as the
product name.
