# RFD 0120 details: path changes, the new deploy convention, and open work

## Repo map

| Old path (in `weftspun-3d-studio`) | New repo |
| --- | --- |
| `apps/weftspun_studio/` | `weftspun/weftspun-studio` |
| `apps/character_taxonomy/` | `weftspun/weftspun-character-taxonomy` |
| `apps/usd_viewer_app/` | `weftspun/weftspun-usd-viewer` |
| `thirdparty/3d_studio/` | `weftspun-3d-studio`'s own repo root, `3d_studio/` |
| `thirdparty/android-xr-face-bridge/` | `weftspun-3d-studio`'s own repo root, `android-xr-face-bridge/` |

`git subtree split --prefix=apps/<app>` only carries history for
commits where that content already lived under `apps/<app>/`. Each
new repo's history starts at RFD 0076's move into `apps/`, not the
project's full history; the fuller history stays in
`weftspun-3d-studio`'s own git log.

## The `/opt/weftspun/<repo>/` convention

The self-hosted Quadlet deploy (RFD 0058) used to `rsync` one
monorepo checkout to `/opt/weftspun/src`, and every `.build` unit's
`File=` path pointed inside it. With three repos, `weftspun-studio`'s
own `scripts/deploy-weftspun-quadlet.sh` now:

1. Syncs itself to `/opt/weftspun/weftspun-studio` (an `rsync` of the
   working copy, as before).
2. Clones or `git pull --ff-only`s `weftspun/weftspun-usd-viewer`
   directly from GitHub to `/opt/weftspun/weftspun-usd-viewer`.
3. Installs `weftspun.network` (from `weftspun-studio`'s own
   `deploy/quadlet/`) plus every `.build`/`.container`/`.volume` unit
   found under either app's own `deploy/quadlet/`.

Each `.build` unit's `File=` path now reads
`/opt/weftspun/<repo-name>/...`, one directory per repo instead of
one path inside a monorepo. `character_taxonomy` needs no quadlet
entry here; it deploys to Fly alone, with no self-hosted or
cross-app dependency.

## Removed, not moved

- `scripts/ci.sh`: built the JS suite, the Elixir suite, and both
  container images from one checkout. No longer applies with three
  separate repos.
- `scripts/studio-test.sh`, and its `.pre-commit-config.yaml` hook:
  ran `weftspun_studio`'s own `mix test`. Removed from
  `weftspun-3d-studio` along with the last hook that file had; each
  split repo needs its own CI, not yet built.
- `scripts/push_gallery_to_vgw.exs`: pushed proof assets to
  versitygw's S3 API. Already dead before this split, since RFD 0079
  removed versitygw.

## Open work

Each split repo needs its own CI (JS test and build for
`weftspun-usd-viewer`, `mix test` for `weftspun-studio` and
`weftspun-character-taxonomy`), not yet built. The self-hosted
Quadlet deploy script is updated but not re-run against a live host
since this split; a first run after this change should be treated
as a fresh deploy, not an incremental one.
