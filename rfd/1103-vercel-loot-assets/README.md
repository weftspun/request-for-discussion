# RFD 1103: Loot assets from a CDN, not a full clone, on Vercel

**State:** published
**Scope:** `vercel.json`, `src/library/lootAssetsConfig.js`

## Decision

Read assets from `m3-org.github.io/loot-assets/` (GitHub Pages)
instead of bundling them. `vercel.json` already sets
`VITE_ASSET_PATH` to that URL, alongside `VITE_PUBLIC_DEMO=1`; with
it set, `npm run get-assets` downloads only the trait-UI icon set
into `public/loot-assets/icons/`, not the full tree, and
`src/library/lootAssetsConfig.js` rewrites every asset path to the
CDN automatically. Removing `VITE_ASSET_PATH` reverts to the
bundled, full-clone mode RFD 1093 gives.

See `DETAILS.md` for the dashboard setup steps, the CDN URL layout,
the post-deploy verification steps, and the secret-variable audit
this mode still needs.

## Problem

RFD 1093's default asset fetch clones the full `m3-org/loot-assets`
repository at build time. A public Vercel deploy does not need every
asset bundled; it needs a small, fast build and a runtime source for
the rest.

## Related

RFD 1093 gives the bundled-clone default this RFD's CDN mode
replaces. RFD 1098 gives the public-build secret checklist this RFD
also names.
