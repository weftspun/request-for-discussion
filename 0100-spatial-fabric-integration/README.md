# RFD 0100: Publishing to the Open Metaverse Browser's spatial fabric

**State:** abandoned
**Scope:** `spatialFabricAdapter.js`, `useSpatialFabric.js`, `3DAIGC-API`'s `/api/v1/spatial-fabric/*`

## Problem

A finished mesh job, or a viewport export, has no path into the
Open Metaverse Browser's shared spatial fabric (RP1/OMB), a
separate system from this project's own in-app world packages (RFD
0107) and the `/xr` IWSDK lab.

## Decision

Route every publish through `3DAIGC-API` on the DGX, not directly
from the client to the fabric. Task Manager's "Publish RP1" sends a
completed mesh job's GLB; GLB Export's "Send To Metaverse Browser"
sends a viewport export, after "Validate OMB tier" checks it; World
Library's own RP1 publishes a world's mesh props from its manifest,
not its environment splats, which are not MSF props at all. Five API
endpoints carry this (`config`, `assets/{job_id}`, `validate-glb`,
`publish`, `publish-glb`), and the API restarts after any
spatial-fabric env change.

See `DETAILS.md` for the architecture diagram, the endpoint table,
the DGX/Surface environment-variable mapping, and the Task
Manager/World Library publish distinction.

## Related

RFD 0107 gives the separate in-app world-package system this
integration does not touch. RFD 0011 (weftspun-3d-studio's own
`decisions/`) gives the client-side publish flow this RFD's API
backs.
