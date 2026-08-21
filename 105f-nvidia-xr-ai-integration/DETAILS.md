# RFD 105f details: architecture, ports, start scripts, and troubleshooting

## Architecture

```
[Galaxy XR Chrome]  camera + mic
        |  HTTPS (often through a Surface proxy, see below)
        v
[xr-ai XR Media Hub :8088]  web client + LiveKit (7880-7882)
        |  speech-to-text -> vision-language model (local or NVIDIA NIM) -> text-to-speech
        v
[3daigc-vlm-example worker]  voice agent + scene vision
        |  HTTP MCP tools (upload_image, image_to_textured_mesh, wait_for_job, ...)
        v
[3daigc-mcp-http :8260]  a FastMCP adapter
        v
[3DAIGC-API :7842]  TRELLIS / mesh jobs, on the Spark GPU
        v
[this project]  loads the completed GLB/VRM in the viewport (a separate client path)
```

This path is complementary to Task Manager's own UI: the same
inference backend, a different, XR-native voice interface.

## Repositories and paths, DGX only

| Path                                                         | Role                                                            |
| ------------------------------------------------------------ | --------------------------------------------------------------- |
| `/home/sifr/xr-ai`                                           | NVIDIA's `xr-ai`: the hub, STT/TTS/VLM servers, agent samples   |
| `/home/sifr/xr-ai/agent-samples/3daigc-vlm-example`          | The voice VLM plus 3DAIGC mesh orchestrator                     |
| `/home/sifr/3DAIGC-API`                                      | The inference API, port 7842                                    |
| `/home/sifr/3DAIGC-API/mcp`                                  | `3daigc-mcp-http` (port 8260), MCP tools over the completed API |
| `/home/sifr/Weftspun3DStudio/scripts/xr-spark-hub-proxy.mjs` | The optional Surface proxy, Galaxy XR to the Spark hub          |

Overlay config, a reference to copy:
`3DAIGC-API/mcp/yaml/xr_ai_3daigc_overlay.yaml`.

## Ports, DGX

| Port       | Service                                                                                  |
| ---------- | ---------------------------------------------------------------------------------------- |
| 7842       | `3DAIGC-API`                                                                             |
| 8260       | `3daigc-mcp-http` (`/mcp`)                                                               |
| 8088       | The `xr-ai` XR Media Hub web UI, over HTTPS                                              |
| 7880, 7882 | LiveKit (WebRTC) for the `xr-ai` hub                                                     |
| 8443       | The Surface's own `xr-spark-hub-proxy` (optional; forwards to `https://10.0.0.158:8088`) |

## Starting the stack, DGX

One command starts both the DGX hub and the Surface proxy, for
Galaxy XR:

```bash
bash /home/sifr/3DAIGC-API/mcp/scripts/start_xr_voice_full.sh
bash /home/sifr/3DAIGC-API/mcp/scripts/verify_xr_voice_stack.sh
```

DGX hub only, no Surface proxy (the headset gets a connection
refused on `10.0.0.32:8443`):

```bash
bash /home/sifr/3DAIGC-API/mcp/scripts/run_xr_ai_3daigc_stack.sh
```

Galaxy XR URL: `https://10.0.0.32:8443` (the Surface proxy,
forwarding to the DGX's own `:8088`), never the bare LAN IP, never
plain HTTP.

Prerequisites only, API plus MCP, no voice stack:

```bash
bash /home/sifr/3DAIGC-API/mcp/scripts/start_prerequisites.sh
```

MCP HTTP only:

```bash
bash /home/sifr/3DAIGC-API/mcp/scripts/run_http.sh
```

Monitor logs:

```bash
bash /home/sifr/3DAIGC-API/mcp/scripts/monitor_xr_ai_3daigc_stack.sh
```

Open the hub UI directly on the DGX LAN:
`https://10.0.0.158:8088` (accept the self-signed certificate), then
start the microphone and try "make a 3D model of this."

## Galaxy XR and router client isolation

Some routers block headset-to-DGX traffic (`10.0.0.224` to
`10.0.0.158`) while still allowing headset-to-Surface traffic
(`10.0.0.32`).

On the Surface, using `certs/localhost.pem` from `npm run
setup-https` (RFD 1058):

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
$env:XR_SPARK_HUB_URL = 'https://10.0.0.158:8088'
$env:XR_PROXY_PORT = '8443'
node scripts/xr-spark-hub-proxy.mjs
```

On Galaxy XR's Chrome: `https://<Surface-LAN-IP>:8443` proxies
straight to the Spark hub.

## MCP tools

A typical voice-agent flow: `upload_image` (a frame from the XR
camera), `image_to_textured_mesh` (queues a mesh job, for example
TRELLIS.2), `wait_for_job` (polls until complete, minutes on a
Spark), and optionally `generate_rig` with `rig_mode=template` for
an avatar.

Worker config:
`xr-ai/agent-samples/3daigc-vlm-example/yaml/3daigc_vlm_example_worker.yaml`,
with `daigc_mcp_url: http://localhost:8260`.

VLM backend: `model_backend: nim` uses a hosted NVIDIA NIM
(`NGC_API_KEY`); `local` runs an on-Spark `vlm-server` instead.

## Relationship to this project's own client

| Layer           | NVIDIA XR AI                                           | This project                                       |
| --------------- | ------------------------------------------------------ | -------------------------------------------------- |
| XR input        | Voice plus passthrough camera, through the `xr-ai` hub | WebXR controllers, World Library, the VRM viewport |
| 3D generation   | MCP, into `3DAIGC-API`                                 | Task Manager's own REST calls, into the same API   |
| Output          | Job files under the DGX's own `outputs/`               | Download, viewport load, and an RP1 publish        |
| Companion agent | An in-hub VLM agent                                    | A separate companion-chat handoff (open work)      |

## Troubleshooting

| Symptom                          | Check                                                                                        |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| The stack exits on start         | `curl -sf http://127.0.0.1:7842/api/v1/system/health`, then restart the API                  |
| The MCP probe fails              | Port 8260 already in use; `bash …/mcp/scripts/run_http.sh`                                   |
| The headset cannot reach `:8088` | Run `xr-spark-hub-proxy` on the Surface's own `:8443`                                        |
| A mesh job never finishes        | `monitor_xr_ai_3daigc_stack.sh`; check the Redis queue and GPU logs under `3DAIGC-API/logs/` |
| NIM errors                       | Confirm `NGC_API_KEY` is set, or switch the worker to `model_backend: local` plus `HF_TOKEN` |
