---
title: "RFD 2090: uro deploys as a Burrito-wrapped mix release, not iex -S mix"
rfd: "2090"
state: published
scope: zone-backend (uro) production boot shape
---

## Problem

`zone-backend`'s root `Dockerfile` boots `uro` for local
`docker-compose` use via `ENTRYPOINT iex -S mix do ecto.create,
ecto.migrate, run priv/repo/test_seeds.exs, phx.server` — a dev-shaped
boot that seeds dummy test data on every start. `build-image.yml`'s
own header said its built image is "consumed by
`v-sekai-multiplayer-fabric/infra` via the `gateway_image`/`uro_image`
tofu variable"; `rfd/0089` archives `infra`, so that path no longer
exists either. `zone-backend` needs its own real production build,
not a dev image and not a dependency on an archived repo.

`config/config.exs` used a `COMPILE_PHASE` environment flag
(`Uro.Config.Helpers.get_env/2`) so the Docker _build_ step could run
`mix compile` without real secrets present: `iex -S mix` re-evaluates
`config.exs` on every invocation, so the container's actual boot
command re-ran `mix` a second time with `COMPILE_PHASE=false` and real
secrets in the environment. A real OTP release (`mix release`)
evaluates `config.exs`/`prod.exs` once, permanently, at build time —
there is no second pass at boot — so this trick does not carry over to
a real release at all.

## Decision

Build `uro` as a real OTP release, wrapped by
[Burrito](https://github.com/burrito-elixir/burrito) into one
self-contained, statically-linked executable (musl libc, bundled
ERTS), cross-compiled via Zig. `mix.exs` gains a `releases:` block
targeting `linux_musl` (matching Fly's runner and this repo's existing
Alpine-based images).

Every deploy-time secret or URL moves to `config/runtime.exs`
(`if config_env() == :prod do ... end`), which a real release
genuinely re-evaluates every time it starts. `config.exs`/`prod.exs`
keep only what is safe to bake in at compile time. The `COMPILE_PHASE`
flag and `Uro.Config.Helpers` are deleted — confirmed unused anywhere
outside `config/*.exs` before removal.

`lib/uro/release.ex` adds `Uro.Release.migrate/0`: a compiled release
has no `mix` tasks at runtime, so this runs `Ecto.Migrator` directly
against `Uro.Repo.Migration` (`gateway_admin`, DDL-capable) — never
`Uro.Repo` (`gateway_writer`, DML only), matching `AGENTS.md`'s
documented role separation. `docker/uro/fly-start.sh` is the script
`AGENTS.md` has described for a while (migrate as `gateway_admin`,
then serve as `gateway_writer`) but which never actually existed in
this repo until now.

## References

- `v-sekai-multiplayer-fabric/zone-backend` PR #52.
- `config/runtime.exs`, `lib/uro/release.ex`, `docker/uro/Dockerfile`,
  `docker/uro/fly-start.sh`.

## Related

- `rfd/2089-flyio-over-podman-quadlets`: the deployment target this
  release ships to.
- `rfd/2065-fabric-platform-central-elixir-burrito-casync`: Burrito's
  prior use elsewhere in this org.

## Detail

{{< include DETAILS.md >}}
