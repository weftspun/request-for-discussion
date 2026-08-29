## Context and problem statement

`zone-backend`'s root `Dockerfile` (used for local `docker-compose`)
boots `uro` via `iex -S mix do ecto.create, ecto.migrate, run
priv/repo/test_seeds.exs, phx.server`. This is dev-shaped on purpose —
seeding `test_seeds.exs` on every boot is fine for local development —
but `build-image.yml` reused the same root `Dockerfile` for its
`ghcr.io` image, described as "consumed by
`v-sekai-multiplayer-fabric/infra` via the `gateway_image`/`uro_image`
tofu variable." `rfd/0089` archives `infra`. Even without that, using
a test-seeding dev image for a real production deploy is a real
correctness problem, not a stopgap worth keeping.

`config.exs`'s `COMPILE_PHASE` flag existed to let `mix compile`
(the Docker build step) succeed with no real secrets present, by
returning a placeholder value instead of raising. This only works
because `iex -S mix ...` (not a compiled release) re-evaluates
`config.exs` fresh at container start, this time with
`COMPILE_PHASE=false` and real Fly secrets in the environment. A real
`mix release` does not have this second evaluation: `config.exs` and
`prod.exs` are baked in once, at build time, forever. Deploying an
actual OTP release needed a different mechanism for secrets entirely.

## Considered options

1. **Keep the `iex -S mix` boot shape for production**, and rely on a
   different image build for the archived `infra` consumer. Rejected
   with `infra`'s archival — nothing consumes that image path anymore,
   and the seeded test data on every boot was never appropriate for a
   real deploy regardless.
2. **A real `mix release`, config moved to `config/runtime.exs`,
   Burrito wrapping it into a single static executable.** Standard
   Phoenix production pattern (`runtime.exs`) plus this org's own
   established Burrito precedent (`rfd/0065`).
3. **A real `mix release` without Burrito**, shipped as a normal
   `_build/prod/rel/uro` directory inside a slim Erlang-installed
   runtime image. Avoids the Zig/Burrito build dependency, but the
   runtime image then needs a matching Erlang/OTP install instead of
   just CA certs, and this org already has a working Burrito toolchain
   and precedent from `fabric-platform-central`.

## Decision outcome

Chosen: **option 2.** `mix.exs` gains a `releases:` block:

```elixir
defp releases do
  [
    uro: [
      steps: [:assemble, &Burrito.wrap/1],
      burrito: [
        targets: [
          linux_musl: [os: :linux, cpu: :x86_64, libc: :musl]
        ]
      ]
    ]
  ]
end
```

`linux_musl` matches Fly's own runner and this repo's existing
Alpine-based images, avoiding a glibc/musl mismatch between the build
and run stages.

`config/runtime.exs` now holds everything that previously depended on
`Helpers.get_env`/`COMPILE_PHASE`: `URL`, `ROOT_ORIGIN`,
`FRONTEND_URL`, both `Repo`s' connection config and CockroachDB mTLS
SSL options, `Uro.Endpoint` (port, secret key base, HTTPS options),
`cors_plug`'s origin, `joken`'s signer, `Turnstile`'s secret,
`pow_assent`'s OAuth2 provider list, the mailer, `ex_aws`/S3 config,
OpenTelemetry's endpoint, and `aria_storage`'s bucket/DB path — all
gated under `if config_env() == :prod do`, so `dev.exs`/`test.exs`
(which already define their own complete, static `Uro.Repo` config)
are unaffected. `config.exs`/`prod.exs` keep only what is genuinely
safe to bake in at compile time: `ecto_repos`, `hammer`, logger
format, `pow`'s static config, and similar.

`Uro.Config.Helpers` (the `COMPILE_PHASE` module) is deleted —
confirmed via `grep -rln "Uro\.Config\.Helpers\|compile_phase"
lib/` that nothing outside `config/*.exs` referenced it.

`lib/uro/release.ex` adds `Uro.Release.migrate/0`, run via the
release's own `eval` command
(`bin/uro eval "Uro.Release.migrate()"`), since a compiled release has
no `mix` tasks at runtime — `mix ecto.migrate` does not exist inside
it. This runs `Ecto.Migrator.with_repo/2` against
`Uro.Repo.Migration` only, matching `AGENTS.md`'s documented DDL/DML
role split.

`docker/uro/Dockerfile` is a real two-stage build: a build stage
(Elixir/Alpine, plus `zig`, `cmake`, `ninja-build`, and the
`riscv-none-elf-gcc` toolchain `.github/workflows/casync-interop.yml`
already installs, for `WeftWarpBurrito.SandboxNif`'s `c_src` build)
running `mix release uro`, and a runtime stage that is just
`alpine:3.20` plus `ca-certificates` — no Elixir/Erlang install at
all, since Burrito's output is fully static.
`docker/uro/fly-start.sh` runs `Uro.Release.migrate/0`, then `exec`s
`start` — the script `AGENTS.md` has described for a while but which
never actually existed in this repo.

## Consequences

Good: a real production boot path exists that does not depend on the
now-archived `infra` repo, does not seed test data on every start, and
matches this org's own established Burrito precedent
(`rfd/2065-fabric-platform-central-elixir-burrito-casync`). The
runtime image needs nothing but the static binary and CA certs
(outbound TLS to CockroachDB, S3-compatible storage, and OTLP all need
real CA verification), which is a smaller, simpler runtime surface
than an Erlang-installed image.

Bad: the build stage is heavier than before — Zig, CMake, Ninja, and a
RISC-V cross-compiler, on top of what `mix compile` already needed per
`zone-backend`'s own `docs/decisions/0017`. `config/runtime.exs` is a
real, sizeable file (over 150 lines) that concentrates every
deploy-time secret in one place; a mistake there is a real production
config bug, not a compile error.

## Confirmation

Verified locally before this record, not assumed: `MIX_ENV=prod mix
release uro` (with the `riscv-none-elf-gcc` toolchain on `PATH`)
produces `burrito_out/uro_linux_musl`, confirmed via `file` to be a
real `ELF 64-bit LSB executable, x86-64 ... statically linked,
stripped`, about 20MB. Running it with placeholder prod secrets
(`URL`, `ROOT_ORIGIN`, `DATABASE_URL`, `PHOENIX_KEY_BASE`, etc. set)
via both `start` and `eval` genuinely boots `Uro.Application`: real
`Postgrex` connection attempts to the given (unreachable, in this
local test) `DATABASE_URL`, and a real
`[info] Running Uro.Endpoint with Bandit 1.6.11 at 0.0.0.0:<port>
(http)` log line confirming the HTTP listener actually started. Not
yet done: an actual Fly deploy of this image (`zone-backend` PR #52 is
open, not yet merged as of this record).
