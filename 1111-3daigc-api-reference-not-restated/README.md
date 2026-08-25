# RFD 1111: The 3DAIGC-API reference, not restated here

**State:** committed
**Scope:** `3DAIGC-API` (DGX, port 7842), `weftspun-3d-studio`'s own
`thirdparty/m3/api/api.md`

## Problem

`thirdparty/m3/api/api.md` held an 1,872-line endpoint reference for
`3DAIGC-API`: health checks, file upload, mesh generation,
segmentation, auto-rigging, splat generation, mesh editing,
retopology, UV unwrapping, workflow examples, error codes, and the
spatial-fabric publish path. RFD 1000's DRY policy forbids a copy of
source documentation in this repository, since a copy drifts and the
source stays correct. RFD 1085 already made this same call for the
browser client's own API surface.

## Decision

`3DAIGC-API`'s own repository, not this one, holds the current
endpoint reference. `3DAIGC-API` itself ships interactive docs at
`/docs` (Swagger UI) and `/redoc` on its own host and port, and those
stay the source of truth for exact request and response shapes. RFD
1102 already gives this project's own task-to-model catalog, at the
level a client developer needs. See `DETAILS.md` for the endpoint
group names this reference held, kept as a map, not a copy.

## Related

RFD 1085 gives the same DRY call for the browser client's own
module map. RFD 1102 gives the task catalog a client developer needs
day to day. RFD 1100 gives the spatial-fabric publish path this
reference's own RP1/OMB section covered.
