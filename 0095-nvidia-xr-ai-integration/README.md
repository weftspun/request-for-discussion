# RFD 0095: A voice XR path, beside Task Manager, same backend

**State:** published
**Scope:** `/home/sifr/xr-ai`, `3DAIGC-API/mcp` (DGX-only)

## Problem

Task Manager already drives `3DAIGC-API` through REST, but a
headset user with hands full, or wanting a spoken "make a 3D model
of this," has no voice-and-camera path to the same inference
backend.

## Decision

Wire NVIDIA's `xr-ai` stack, running on the DGX Spark, to
`3DAIGC-API` through an HTTP MCP adapter, not a second inference
backend. Galaxy XR's camera and microphone reach the XR Media Hub
(port 8088, LiveKit for WebRTC on 7880-7882), which runs speech-to-text,
a vision-language model, then text-to-speech; a voice-agent sample
(`3daigc-vlm-example`) calls the same `3DAIGC-API` mesh jobs through
MCP tools (`upload_image`, `image_to_textured_mesh`,
`wait_for_job`). When a router blocks the headset from reaching the
DGX directly, `scripts/xr-spark-hub-proxy.mjs` on the Surface
forwards `:8443` to the DGX's own `:8088`.

See `DETAILS.md` for the full port table, the start and monitor
scripts, the MCP tool flow, and the troubleshooting table.

## Related

RFD 0086 gives the Surface/DGX topology this integration's proxy
step depends on. RFD 0100 gives the spatial-fabric publish path a
completed mesh job can still reach afterward, from either voice or
Task Manager.
