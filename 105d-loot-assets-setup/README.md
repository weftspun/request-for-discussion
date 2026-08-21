# RFD 105d: Loot assets, fetched, never committed

**State:** published
**Scope:** `public/loot-assets/`, `scripts/loot-assets-paths.mjs`, `scripts/ensure-loot-assets.mjs`

## Problem

Loot asset binaries have no place in this project's own git
history. `github.com/m3-org/loot-assets` already holds them as the
source of truth; committing a second copy here would duplicate that
data and drift from it.

## Decision

Never commit the binaries. `npm run get-assets` clones
`m3-org/loot-assets`, and links or inlines it depending on
environment: a sibling clone linked into `public/loot-assets` for
local development, a shallow clone straight into `public/loot-assets`
for Vercel and CI (`npm run build` runs `get-assets` first). `git
push` carries only app code; `public/loot-assets/` stays gitignored.
App code reads `/loot-assets/…` with no import-path change
(`src/library/lootAssetsConfig.js`).

See `DETAILS.md` for the local layout, the quick-start commands, and
the CDN alternative for a bundle-free Vercel build.

## Related

RFD 1067 gives the CDN-manifest alternative
(`VITE_ASSET_PATH=https://m3-org.github.io/loot-assets/`) this
RFD's `vercel.json` sets by default.
