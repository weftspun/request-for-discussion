# RFD 1102: The supported 3DAIGC task catalog, one live source

**State:** published
**Scope:** `TaskManager.jsx`, `src/library/aiModelsCatalog.js`

## Problem

The New Task panel's own task list, `3DAIGC-API`'s live model list,
and this project's catalog file can drift from each other, and a
reader had no single table naming which model backs which task
today, or which task is client-only (no DGX call at all).

## Decision

`GET /api/v1/system/models` on `3DAIGC-API` (DGX, port 7842) is the
live source; `src/library/aiModelsCatalog.js` mirrors it for the
client. Fourteen task types are named in one table (text-to-3D
through Avatar From Photo), each with its API feature key and a
recommended model. Two tasks run with no `3DAIGC-API` call at all:
"Avatar From Photo" (AvatarSDK, client-only) and the client-side
avatar pipeline's own rig step. Three models are license-blocked on
a commercial tier (PartField, PartPacker, FastMesh); "Part
completion" exists only in legacy upstream docs, not in this UI.

See `DETAILS.md` for the full task table, the Gaussian-splat
capability matrix (shipped versus not yet done), the architecture
diagram, and the full further-reading index this catalog page
carried.

## Related

RFD 1004 (weftspun-3d-studio's own `decisions/`) gives the AIGC task
catalog's own original design. RFD 1094 gives the multi-image
routing this catalog's splat and avatar tasks both use. RFD 1100
gives the spatial-fabric publish path a completed mesh task reaches.
