# RFD 0098 details: the deploy modes, the forbidden variables, and local verify

## The two modes

| Mode | Where | AI backend | Secrets |
| --- | --- | --- | --- |
| Local dev | `npm run dev`, on a PC or DGX | `VITE_API_ENDPOINT`, `DEV_API_PROXY_TARGET` | `.env`, gitignored |
| Public demo | Vercel (`vercel.json`) | None: viewport, VRM upload, traits UI only | No client secret |

## Setting up the Vercel demo

1. Import `weftspun/weftspun-3d-studio` in Vercel.
2. Framework preset: Vite, or use the repository's own `vercel.json`.
3. Build command: `npm run build` (runs `verify-public-build-env`, then `vite build`).
4. Output directory: `build`.

`vercel.json` sets two safe, build-time-only flags:

- `VITE_PUBLIC_DEMO=1`: hides the API status panel, shows
  user-facing "no AI backend" copy, and swaps the XR Voice sidebar
  (`XrAiPanel.jsx`, top of the left sidebar) for a static demo
  preview instead of a live DGX iframe. Mic, camera, and task
  handoff still need local development plus a real DGX Spark.
- `VITE_ASSET_PATH=https://m3-org.github.io/loot-assets/`: reads
  loot assets from a CDN instead of cloning the full asset
  repository in CI.

## What must never be set on Vercel

Every `VITE_*` variable inlines into the browser bundle:

| Variable | Why |
| --- | --- |
| `VITE_3DAIGC_API_KEY` | API bearer token |
| `VITE_AVATARSDK_CLIENT_SECRET` | OAuth secret |
| `VITE_THIRDWEB_SECRET_KEY` | Wallet secret |
| `VITE_PINATA_*`, `VITE_ALCHEMY_*`, `VITE_BASE_X402_*`, `VITE_VANA_*` | Service secrets |
| `VITE_HELIUS_KEY`, `VITE_OPENSEA_KEY` | Paid API keys |
| `VITE_API_ENDPOINT` pointing at a LAN/DGX/Tailscale address | Private infrastructure leak |
| `VITE_XR_HUB_URL` / `VITE_MSF_PUBLIC_URL` with `10.0.0.*` or a LAN IP | Private infrastructure leak; use a Tailscale Funnel HTTPS address on Vercel instead |
| `MSF_EDIT_KEY`, `MSF_DB_PASSWORD`, `VITE_3DAIGC_API_KEY` | Server or edit secrets; never a `VITE_*` name |
| `DEV_API_PROXY_TARGET` | Development-only; unused in a production build |

`npm run build` fails on Vercel or CI outright if any of these are
present (`scripts/verify-public-build-env.mjs`).

## Optional on Vercel, public client IDs only

| Variable | Purpose |
| --- | --- |
| `VITE_THIRDWEB_CLIENT_ID` | Public wallet client id |
| `VITE_AVATARSDK_CLIENT_ID` | Public AvatarSDK client id, no secret |
| `VITE_JOB_STATUS_PATH` | Only if a real public API URL is exposed |
| `VITE_XR_HUB_URL` | Local development or self-hosted only; unused on the Vercel public demo |

## Local development, unchanged

Copy `.env.example` to `.env`:

```bash
DEV_API_PROXY_TARGET=http://10.0.0.158:7842
VITE_API_ENDPOINT=/__dev_dgx_proxy
VITE_JOB_STATUS_PATH=api/v1/system/jobs
```

`DEV_API_PROXY_TARGET` is read only by the Vite dev server
(`vite.config.js`); it never reaches the client bundle. The DGX
proxy, HTTPS certs, remote logging, and IWSDK plugins are
development-only (`command === 'serve'`).

## Verify before a push

```bash
# Simulate Vercel, no local .env loaded
VERCEL=1 CI=1 VITE_PUBLIC_DEMO=1 \
  VITE_ASSET_PATH=https://m3-org.github.io/loot-assets/ \
  npm run build
```

## Full-stack, private

Run `3DAIGC-API` (`github.com/AlfaOmegaGrafx/3DAIGC-API`) on a real
GPU machine, and point a local `.env` at it. Never put a DGX URL on
Vercel; use a public HTTPS API, or keep AI generation local-only.
