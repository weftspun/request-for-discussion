# RFD 105d details: environments, layout, and the scripts

## What happens per environment

| Environment | What happens |
| --- | --- |
| Local dev (Surface/DGX) | `npm run get-assets` clones to `../loot-assets`, links `public/loot-assets` to that clone. |
| Vercel / CI | `npm run build` runs `get-assets` first: a shallow clone lands straight inside `public/loot-assets`, and Vite bundles it into `build/`. |
| `git push` | Only app code moves. `public/loot-assets/` is gitignored, a junction locally, a build-time clone in CI. |

A pointer file, `loot-assets.source`, sits at the repository root.

## Quick start

```powershell
cd C:\Users\alfao\Documents\GitHub\Weftspun3DStudio
npm run get-assets
npm run dev
```

```bash
# DGX
cd /home/sifr/Weftspun3DStudio
npm run get-assets
```

## Local layout

| Path | Role |
| --- | --- |
| `C:\Users\alfao\Documents\GitHub\loot-assets` | The git clone of `m3-org/loot-assets`. |
| `Weftspun3DStudio\public\loot-assets` | A junction or symlink to that external clone. |
| App URLs | `/loot-assets/manifest.json`, `/loot-assets/models/…`, and so on. |

Override the clone location with `LOOT_ASSETS_EXTERNAL_DIR` in
`.env`. A Windows-only re-link: `.\scripts\link-loot-assets.ps1`, or
`npm run link-assets`.

## Vercel deploy

`vercel.json` calls `npm run build`, which runs `npm run get-assets
&& vite build`. On Vercel, the `VERCEL=1` environment variable makes
the clone land inside `public/loot-assets` directly, no sibling
folder, no submodule, no manual asset upload.

RFD 1067 gives the CDN alternative this project can point manifests
at instead of bundling:

```env
VITE_ASSET_PATH=https://m3-org.github.io/loot-assets/
```

`vercel.json` sets this by default for Vercel deploys, an
icons-only build with the CDN read at runtime.

## Scripts

| Command | Purpose |
| --- | --- |
| `npm run get-assets` | Clone `m3-org/loot-assets` if missing; link or inline per environment. |
| `npm run link-assets` | Windows junction, `public/loot-assets` to `../loot-assets`. |

Implementation: `scripts/loot-assets-paths.mjs`,
`scripts/ensure-loot-assets.mjs`.
