# RFD 1098: Two deploy modes, one build that fails on a secret leak

**State:** abandoned
**Scope:** `vercel.json`, `scripts/verify-public-build-env.mjs`

## Problem

A public demo build must show the viewport, VRM upload, and traits
UI, with no AI backend reachable and no server or LAN secret in the
shipped bundle. Any `VITE_*` variable set at build time gets inlined
into the browser bundle, so a wrong environment variable on Vercel
is a real leak, not a configuration typo.

## Decision

Two modes: local development, with `.env` (gitignored) pointing at
a real DGX backend, and the public Vercel demo, with
`VITE_PUBLIC_DEMO=1` and no client secret at all.
`scripts/verify-public-build-env.mjs` runs before every build and
fails it outright if a forbidden variable (an API key, an OAuth
secret, a LAN or Tailscale backend URL) is present. `VITE_PUBLIC_DEMO=1`
also swaps the XR Voice sidebar for a static demo preview instead of
a live DGX iframe.

See `DETAILS.md` for the exact forbidden-variable table, the
optional public-only variables, and the local verify command.

## Related

RFD 1093 gives the loot-assets CDN variable
(`VITE_ASSET_PATH`) this deploy mode also sets.
