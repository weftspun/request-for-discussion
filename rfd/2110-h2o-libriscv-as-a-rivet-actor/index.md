---
title: "RFD 2110: One pinned Godot build, hosted as a Rivet actor"
rfd: "2110"
state: discussion
scope: zone server implementation, orchestration, guest delivery
---

## Problem

`rfd/0109` makes the server tier an Elixir presence relay. A relay is
not server-authoritative, and it runs every room in one BEAM node, so
one fault reaches every room.

The h2o and libriscv work in `zone-server-h2o` already exists.
`rfd/0083` built the host, and `rfd/0094` keeps `thirdparty/libriscv`
and `thirdparty/QCBOR` vendored so they do not rot. What that host
lacked was orchestration. `rfd/0072`, `rfd/0082`, and `rfd/0086` exist
only because one process had to hold many zones.

No record asks whether something else can supply the orchestration.

## Decision

A zone is a child process under Rivet's `container-runner`, one process
per room. The child is headless Godot, which the runner documentation
names directly.

The engine is pinned to one tag,
`v2026.06.27.1907-multiplayer-fabric`, which resolves to commit
`2cecde75` and reports Godot 4.7.0 beta. That tag's `modules/` already
carries `sandbox` for libriscv guests, `http3` for WebTransport,
`multiplayer_fabric` and `multiplayer_fabric_asset` for the zone,
`xr_grid` for presence, and `openxr` with `webxr` for XR.

So one engine build is the client, the zone server, and the guest host.
No C host is needed to load an `.elf`, because `sandbox` does it, and
`rfd/0037` already makes generated behavior sandboxed RISC-V.

The tag carries no release artifacts, because the repository publishes
no GitHub releases. `godot-images` builds it and publishes the container
image, which is what `container-runner` needs. `rfd/0009` puts that
build in the consuming repository.

Rivet supplies what the old host hand-rolled. It cold-starts the
container, injects `PORT`, spawns the binary as a child, and proxies
gateway traffic to `127.0.0.1:<child port>`. The engine owns placement,
routing, and lifecycle. Rivet is Apache 2.0 and self-hosted.

The child contract is small. Listen on `PORT`. Open it within the
readiness timeout, 30 seconds by default. Handle `SIGTERM` and exit
within the grace period, 25 seconds by default. Raw HTTP arrives under
a `/request/*` prefix that the runner strips. WebSocket clients use the
`rivet` subprotocol.

One process per room removes the multi-zone problem. The binary hosts
one room, so it needs no zone routing and no cross-zone authority.
`rfd/0072`, `rfd/0082`, and `rfd/0086` become unnecessary, and
`rfd/0080` narrows to one room's entities.

The CBOR actor input names the child command, its args, and its env,
and it names the scene or guest the room loads. That is `rfd/0094`'s
guest delivery, moved to the actor boundary.

A C child, h2o with libriscv, stays possible and is not built. Its only
advantage is memory per process, and that advantage is unmeasured.
Build it when a measurement forces it.

FoundationDB backs both the Rivet engine and the zone state, so
`rfd/0109`'s store selection stands. This record amends only
`rfd/0109`'s server tier.

## References

- The contract, what it deletes, and the transport question:
  `DETAILS.md`
- `https://rivet.dev/docs/deploy/container-runner/`

## Related

- `rfd/2083-zone-server-h2o-replaces-godot-fabriczone`: the decision
  this reverses, because the zone returns to Godot.
- `rfd/2037-generated-behavior-sandboxed-riscv`: the libriscv path
  inside the engine.
- `rfd/2020-pin-engine-to-frozen-godot-4-7`: the pinning practice this
  applies to one named tag.
- `rfd/2109-two-tiers-with-foundationdb-as-the-store`: the store and the
  relay this replaces.

## Detail

{{< include DETAILS.md >}}
