# RFD 0103 details: dashboard setup, URL layout, verification, and the alternative

## One-line setup, recommended

This repository's own `vercel.json` already sets:

```env
VITE_ASSET_PATH=https://m3-org.github.io/loot-assets/
VITE_PUBLIC_DEMO=1
```

RFD 0098 gives the full public-build security checklist this
setting sits inside. Deploy from the Vercel dashboard or its CLI;
no extra environment variable is required unless one is overridden.

## Dashboard setup, by hand

1. Open the project on `vercel.com`, then Settings, then Environment Variables.
2. Add:

   | Name | Value | Environments |
   | --- | --- | --- |
   | `VITE_ASSET_PATH` | `https://m3-org.github.io/loot-assets/` | Production, Preview, Development |
   | `VITE_PUBLIC_DEMO` | `1` | Production, Preview; hides the API Status panel |

   Never set `VITE_API_ENDPOINT` on the public Vercel demo; a
   self-hosted build is where a user configures their own API.

3. Redeploy; an environment-variable change only applies to a new build.

## What happens at build time

```
npm run build
  -> verify-public-build-env
  -> npm run get-assets   (sees VITE_ASSET_PATH set, fetches icons only, no full clone)
  -> vite build
```

At runtime, manifests, models, and animations load from
`https://m3-org.github.io/loot-assets/…`. At build time, only the
trait-UI SVGs download into `public/loot-assets/icons/` (Vite
imports them directly, from `Load.jsx` and similar components).

## URL layout, GitHub Pages

GitHub Pages serves the legacy asset tree under `/loot/`:

| App path | CDN URL |
| --- | --- |
| Main manifest | `…/manifest.json` |
| Models manifest | `…/loot/models/manifest.json` |
| Model GLB | `…/loot/models/…` |
| Animations | `…/loot/animations/…` |

`src/library/lootAssetsConfig.js` rewrites every path automatically
once `VITE_ASSET_PATH` is set; no other code change is needed.

## Verify after a deploy

1. Open the deployed site, then DevTools, then the Network tab.
2. Confirm `manifest.json` loads from `m3-org.github.io`, not the Vercel origin itself.
3. Open Appearance; confirm the loot pack's trait groups load.
4. Confirm the bottom animation bar loads its FBX files from the CDN.

## Local development with the same CDN

In `.env`:

```env
VITE_ASSET_PATH=https://m3-org.github.io/loot-assets/
```

Then:

```powershell
npm run get-assets
npm run dev
```

No full `../loot-assets` clone is needed for CDN mode, only the
small icon set the build itself downloads.

## The bundled alternative

Remove `VITE_ASSET_PATH` from both the Vercel environment and
`vercel.json`. The build then shallow-clones the full
`m3-org/loot-assets` repository into `public/loot-assets`, a larger
deploy with no external CDN dependency, RFD 0093's own default mode.

## Security, on a public Vercel deploy

The disconnected-state UI names environment-variable keys
(`VITE_API_ENDPOINT`, and so on) but never their values, so that
alone is not a breach. Never set on Vercel:
`VITE_3DAIGC_API_KEY`, `VITE_AVATARSDK_CLIENT_SECRET`,
`VITE_THIRDWEB_SECRET_KEY`, or any Pinata or Alchemy secret; Vite
embeds every `VITE_*` variable directly in the client bundle. A
production build hides the API Status panel, the dev troubleshooting
tools, the endpoint editor, and the sidebar debug panel when
`VITE_PUBLIC_DEMO=1`. Audit periodically: Vercel, Settings,
Environment Variables, remove any secret-shaped `VITE_*` key found,
then redeploy.
