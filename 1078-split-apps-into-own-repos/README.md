# RFD 1078: Split apps/ into their own repos

**State:** committed
**Scope:** `weftspun-3d-studio`'s `apps/`, `deploy/`, `scripts/`, and `thirdparty/`

## Problem

`weftspun-3d-studio` held three independently deployed apps
(`weftspun_studio`, `character_taxonomy`, `usd_viewer_app`) under one
`apps/` directory (RFD 104c), plus a large vendored browser client
and a companion APK under `thirdparty/`. A monorepo checkout, one
`scripts/ci.sh` building all three, and one shared self-hosted
deploy script no longer matched three apps with three separate Fly
deploy targets and no code sharing between them.

## Decision

Each app moved to its own repository, with history preserved by
`git subtree split --prefix=apps/<app>`, then pushed as that repo's
`main`: `weftspun/weftspun-studio`,
`weftspun/weftspun-character-taxonomy`, and
`weftspun/weftspun-usd-viewer`. `apps/`, `scripts/ci.sh`, and
`scripts/studio-test.sh` were removed from `weftspun-3d-studio`,
since none apply to a repo with no app code left. `deploy/`,
`.github/workflows/deploy-fly.yml`, and
`scripts/deploy-weftspun-quadlet.sh` moved into `weftspun-studio`,
the one app that requires the other two reachable.
`thirdparty/3d_studio/` and `thirdparty/android-xr-face-bridge/`
moved to `weftspun-3d-studio`'s own repo root, leaving that repo the
browser client and the companion APK only.

See `DETAILS.md` for the exact path changes, the new
`/opt/weftspun/<repo>/` deploy convention, and open follow-up work.

## Related

RFD 103a gives the Quadlet deploy this split's `deploy/` move
adapts. RFD 103c and RFD 104c give the repo-layout history this RFD
continues.
