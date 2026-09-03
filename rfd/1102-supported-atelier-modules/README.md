# RFD 1102: The supported task catalog, one live source

**State:** committed
**Scope:** RFDs 1036 (packaging), 1173 (pipeline), 2136 (gacha ladder)

## Decision

The task catalog is now the set of Docker images this workspace ships
per RFD 1036 (plain HTTP, `/health` + `/predict`, weights at build
time, one model per image), running on the local desktop GPU per
CLAUDE.md, feeding the two pipelines the workspace actually operates:

- **MaskScore corpus construction** (RFD 1173): eight stubs across
  mesh/depth/pose/keypoints/multimodal/speech/text/video. Five shipped
  on HF (RFD 2164 speech + Rung 1 walking skeleton).
- **The gacha critical path** (RFD 2136): ten-rung ladder from a
  language prompt to a public roll-button-dispensed VRM.

`DETAILS.md` carries the current per-task table, the pipeline
diagrams, and the retraction record for the browser-client + DGX
catalog this RFD used to describe.

## Problem

The earlier draft named a browser New Task panel, `3DAIGC-API` on
the DGX at port 7842, and a JS `aiModelsCatalog.js` as three sources
of truth. Every premise was walked back: RFD 2169 abandoned the
strangler-fig studio core the browser client fed; RFD 2175 abandoned
rented compute; CLAUDE.md's hard constraint is the local desktop GPU
only. Six of the fourteen catalog rows referenced blocklisted or
abandoned models (P3-SAM, TripoSplat, WorldMirror 2.0,
weftspun_image_to_world, LingBot-Map, Hunyuan3D-2.1).

## Related

RFD 1036 (Docker packaging), RFD 1053 (OpenUSD internal + glTF/VRM at
edge), RFD 1027 (GPU tier), RFD 1173 (multimodal pipeline), RFD 2136
(gacha ladder), RFD 2164 (Speech stub shipped), RFD 2169 (studio-core
abandonment), RFD 2175 (rented compute abandoned).
