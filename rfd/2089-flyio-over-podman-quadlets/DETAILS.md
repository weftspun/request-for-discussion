## Context and problem statement

`rfd/0061` chose podman quadlets under systemd on self-hosted Fedora 44
hosts over both Fly.io and the earlier Harvester HCI plan, provisioned
by the `infra` repo's OpenTofu. Seven quadlet repos were created for
this: `zone-backend-quadlet`, `cockroach-crdb-quadlet`,
`zone-server-quadlet`, `zone-baker-quadlet`, `restic-backup-quadlet`,
`gha-runner-quadlet`, and `sccache-cache-quadlet`, each with an
`install.sh` and a real `.container` unit. All seven last received a
push on 2026-06-13.

Independently of that decision, real production work on `zone-backend`
continued against Fly.io. `docs/decisions/0011-fly-redeploy-scope-uro-and-crdb-only.md`
records a Fly app loss and a scoped redeploy of `multiplayer-fabric-uro`
and `multiplayer-fabric-crdb` only. That redeploy sat broken for weeks:
`multiplayer-fabric-crdb` crash-looped on every boot
(`/docker-entrypoint.sh: No such file or directory` — the image's real
entrypoint is `/cockroach/cockroach.sh`, confirmed via
`skopeo inspect --config docker://ghcr.io/v-sekai/cockroach:latest`;
whatever Dockerfile previously set that override was never committed
anywhere), and `multiplayer-fabric-uro` had 14 secrets staged but never
deployed.

This mismatch — a published RFD choosing quadlets, while the actual
service that exists and needs fixing runs on Fly — needed a real
decision, not a silent continuation of whichever path happened to have
momentum.

## Considered options

1. **Fix `zone-backend`'s Fly deploy, treat quadlets as the long-term
   target.** Keeps `rfd/0061` in force; the Fly.io fixes become a
   stopgap, and someone later ports `uro`/`crdb` to
   `zone-backend-quadlet`/`cockroach-crdb-quadlet`.
2. **Adopt Fly.io as the real target, tombstone the quadlet repos and
   `infra`.** Matches what has actually been built, verified, and
   deployed: a real `multiplayer-fabric-crdb` fix, confirmed live via
   Fly's own health checks and boot logs, and a real Burrito-wrapped
   release for `uro`, verified locally (a genuine static ELF binary
   that boots `Uro.Endpoint`, `Uro.Repo`, and `Uro.Repo.Migration`
   correctly).
3. Running both, service by service, avoids picking a single target
   but doubles the real ops surface `rfd/0061`'s own problem
   statement (Harvester's "full virtualization tier" wraps the same
   workloads twice) already argued against, for a different reason.

## Decision outcome

Chosen: **option 2.** Fly.io is the real deployment target.
`rfd/0061` is superseded. `infra` and all seven quadlet repos are
archived (GitHub's archive, not deletion — history stays reachable,
nothing currently depends on them being writable).

The concrete evidence this decision is grounded in, not asserted:

- `multiplayer-fabric-crdb`: three real, distinct bugs found and fixed
  by iterating against actual Fly boot logs, not guessed — the lost
  entrypoint, a missing `chmod +x` on its replacement, and a
  CockroachDB cert-lifetime rounding collision (the node cert
  requested the exact same lifetime as its CA; CockroachDB 22.1
  rejects a cert lifetime `>=` its CA's). Health check passing,
  `uro` database and `gateway_writer`/`gateway_admin` roles
  bootstrapped, confirmed live.
- `multiplayer-fabric-uro`: a real Burrito-wrapped `mix release`
  replaces the dev-shaped root `Dockerfile` (`iex -S mix do
ecto.create, ecto.migrate, run priv/repo/test_seeds.exs,
phx.server`, which seeded dummy test data on every boot). Verified
  locally: the release build genuinely produces a static, ~20MB ELF
  binary, and both its `start` and `eval` commands boot
  `Uro.Application` for real (`Uro.Repo`, `Uro.Repo.Migration`, and
  `Uro.Endpoint` with Bandit all start, confirmed via real Postgrex
  connection attempts and a real HTTP listener log line).
- `zone-backend-quadlet`'s `README.md` documents the same
  `DATABASE_URL`/`MIGRATION_URL`/mTLS-cert shape as `zone-backend`'s
  `AGENTS.md` already does for Fly — the two paths were never going to
  diverge in what they configure, only in where. Nothing about the
  quadlet path had a working, deployed instance to point to; the Fly
  path now does.

## Consequences

Good: one real, currently-working deployment target for
`zone-backend`'s two services, matching engineering effort already
spent and verified rather than requiring a second port to a path with
no live deployment. `rfd/0089`'s tombstoning also removes a real
source of drift: two competing, both-real deploy configs for the same
service (`AGENTS.md`'s Fly secrets vs. `zone-backend-quadlet`'s
`/etc/zone-backend/env`) is worse than committing to one.

Bad: this reverses a published, deliberate decision
(`rfd/0061`) made after weighing Harvester HCI, Fly.io, and quadlets
directly against each other. That record's own stated reasons for
excluding Fly.io are not re-litigated here in detail; this RFD
documents that the org's real, current choice is Fly.io, not a
re-derivation of why quadlets were rejected the first time. A future
RFD revisiting deployment target again should read both `rfd/0061`
and this record.

`zone-server-h2o` and `zone-client-godot` are not yet covered by a
real Fly.io production deployment; see `rfd/0091` and `rfd/0092`.

## Confirmation

`infra`, `zone-backend-quadlet`, `cockroach-crdb-quadlet`,
`zone-server-quadlet`, `zone-baker-quadlet`, `restic-backup-quadlet`,
`gha-runner-quadlet`, and `sccache-cache-quadlet` are archived,
confirmed via `gh repo view --json isArchived` on each.
`multiplayer-fabric-crdb`'s health check is passing on Fly, confirmed
via `fly machine status`. `multiplayer-fabric-uro`'s real release
build is verified locally; its actual Fly deploy is tracked as a
follow-up (`zone-backend` PRs #51, #52), not yet merged and deployed
as of this record.
