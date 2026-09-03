# RFD 2090: Uro burrito release

**State:** moved

## Decision

See `DETAILS.md` for the full argument.

## Problem

`zone-backend`'s root `Dockerfile` (used for local `docker-compose`)
boots `uro` via `iex -S mix do ecto.create, ecto.migrate, run
priv/repo/test_seeds.exs, phx.server`. This is dev-shaped on purpose —
seeding `test_seeds.exs` on every boot is fine for local development —
but `build-image.yml` reused the same root `Dockerfile` for its
`ghcr.io` image, described as "consumed by
`v-sekai-multiplayer-fabric/infra` via the `gateway_image`/`uro_image`
tofu variable." `rfd/0089` archives `infra`. Even without that, using

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
