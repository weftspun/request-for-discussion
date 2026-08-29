---
title: "RFD 2089: Fly.io, not self-hosted podman quadlets, is the deployment target"
rfd: "2089"
state: published
scope: deployment target for fabric runtime services
---

## Problem

`rfd/203d-quadlets-on-fedora-44-instead-of-harvester` chose self-hosted
podman quadlets on Fedora 44, provisioned by the `infra` repo's
OpenTofu, and put Fly.io "off the table." Since then, real production
work on `zone-backend` (`multiplayer-fabric-uro`,
`multiplayer-fabric-crdb`) has run entirely against Fly.io: a genuine
crash-loop bug in `multiplayer-fabric-crdb` was found and fixed
against a real Fly deploy, and a real Burrito-wrapped `mix release` for
`uro` was built and verified against Fly's secrets model
(`config/runtime.exs`). The quadlet repos (`zone-backend-quadlet`,
`cockroach-crdb-quadlet`, `zone-server-quadlet`, `zone-baker-quadlet`,
`restic-backup-quadlet`, `gha-runner-quadlet`,
`sccache-cache-quadlet`) exist but were last pushed 2026-06-13, before
any of this real Fly.io deployment work happened.

## Decision

Use Fly.io as the real deployment target. This supersedes
`rfd/0061`'s choice of self-hosted podman quadlets on Fedora 44.

The `infra` repo (OpenTofu provisioning for the Fedora 44 quadlet
hosts) and all seven quadlet repos above are archived — tombstoned,
not deleted, so their history stays reachable, but they are no longer
the deployment path for anything. `multiplayer-fabric-crdb` and
`multiplayer-fabric-uro` on Fly.io are the real, currently-running
services this applies to first.

## References

- [`rfd/203d-quadlets-on-fedora-44-instead-of-harvester`](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive/tree/main/rfd/203d-quadlets-on-fedora-44-instead-of-harvester):
  the decision this supersedes. It now lives in
  `multiplayer-fabric-archive`, per `rfd/0106`.
- `v-sekai-multiplayer-fabric/zone-backend`, `docs/decisions/0011-fly-redeploy-scope-uro-and-crdb-only.md`:
  the prior Fly-app-loss record this RFD's Fly.io work continues from.
- `v-sekai-multiplayer-fabric/infra`, `v-sekai-multiplayer-fabric/zone-backend-quadlet`,
  `cockroach-crdb-quadlet`, `zone-server-quadlet`, `zone-baker-quadlet`,
  `restic-backup-quadlet`, `gha-runner-quadlet`,
  `sccache-cache-quadlet`: archived by this decision.

## Related

- `rfd/2090-uro-burrito-release`: the real production release shape
  this decision's Fly.io deploy of `uro` uses.

## Detail

{{< include DETAILS.md >}}
