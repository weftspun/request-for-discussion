---
title: "RFD 2094: zone-server-h2o hosts the minimum UGC game loop"
rfd: "2094"
state: discussion
scope: zone-server-h2o, zone-guest-middleham, zone-guest-gyre, zone-guest-godot
---

## Problem

`zone-server-h2o`'s PR #22 removed the MUD subsystem (the phase-2
CDN-guest move). The first cut of that PR also deleted
`thirdparty/libriscv` and `thirdparty/QCBOR`, because their only
in-tree consumer was the MUD orchestrator. That deletion was wrong,
and the review that caught it exposed an undocumented decision.

`rfd/0092` defines _how_ the host gates guest access (ReBAC, a use
plane and an admin plane). No RFD defines _what_ the host repo must
implement to close a user-generated-content game loop. No RFD says
which repo is that host, or how many guests compose in one zone.

Without that decision on record, the same mistake repeats. A cleanup
of guest-adjacent code can delete host-side machinery that looks
orphaned but is load-bearing for the loop.

## Decision

`zone-server-h2o` is the host of the minimum UGC game loop. The loop
is: a principal with administrative capability loads guest programs,
and principals with normal capability interact with what those guests
run. Guests are CDN-delivered riscv64 ELFs, not in-tree code.

### What the host keeps vendored

- `thirdparty/libriscv`: the guest execution engine. It is not
  MUD-specific.
- `thirdparty/QCBOR`: the serialization layer for the host-to-guest
  ABI. The host must speak the same CBOR encoding the guests do.

Both stay in `zone-server-h2o` even while no in-tree consumer exists.
The QCBOR build wiring stays live in `CMakeLists.txt`, so the
vendored copy compiles in CI and does not rot.

### Two capability tiers

The tiers are `rfd/0092`'s two planes, bound to the ReBAC actions
that `src/gen/rebac.{c,h}` already generates from `lean-rebac-core`:

- **Administrative capabilities** (admin plane): fetch a guest ELF,
  load it, unload it, and grant it capabilities. These map to
  `REBAC_ACTION_MODIFY`, which `Action.minRelation` gates at
  `REBAC_RELATION_OWNER`. The orchestrator runs every admin check. A
  guest never reaches this plane.
- **Normal capabilities** (use plane): the verbs a running guest
  exposes to players. These map to `REBAC_ACTION_INTERACT` and
  `REBAC_ACTION_OBSERVE`. Observe is public. Interact needs a real
  relation.

### Guest composition

One zone process loads more than one guest, each as its own
`libriscv::Machine` and its own ReBAC subject (per `rfd/0092`). The
initial composition is:

- `zone-guest-middleham`: the game-logic guest, and the first to
  load. Its ELF recipe already worked in-tree, and it is the
  smallest.
- `zone-guest-gyre`: the presentation guest (the web client and its
  deploy), CDN-delivered on the same pipeline.
- `zone-guest-godot`: Godot rv64 under `rvlinux`. This is the stress
  test of the same capability table, not a separate design.

### What closes the loop

The minimum loop closes when three items land in `zone-server-h2o`:

1. A guest loader that links `thirdparty/libriscv` and boots one
   ELF. The last loader lived in `mud/orchestrator/main.cpp` and
   moved to `zone-guest-middleham`.
2. A capability table: which host functions a loaded guest may call,
   keyed by the guest subject's ReBAC relations, with QCBOR as the
   wire format.
3. `rebac_check` call sites at both tiers: at load time (modify,
   owner only) and per guest syscall (interact or observe).

Two prerequisites sit outside those three items. First, identity:
the server's TLS cert and key are still `NULL`/`NULL`, and the admin
plane cannot authorize a subject that does not exist. Second, an
artifact to fetch: `zone-guest-middleham`'s release workflow fails on
a `fabric-godot-core@feat/sandbox` checkout for libriscv, so no guest
ELF exists on a CDN yet.

## Consequences

- The `fly/Containerfile` libriscv build and the riscv64-musl cross
  toolchain stay removed until item 1 lands. Building a static lib
  that nothing links is dead image weight.
- Repo cleanups must treat `thirdparty/libriscv` and
  `thirdparty/QCBOR` as host infrastructure, not guest leftovers.
- The client-command path (parse a datagram payload, write an entity,
  gate it with `rebac_check`) can close a create-modify-observe loop
  before any sandbox work. That path is compatible with, and smaller
  than, items 1 through 3.

## References

- `v-sekai-multiplayer-fabric/zone-server-h2o` PR #22: the removal
  that exposed this decision.
- `v-sekai-multiplayer-fabric/zone-guest-middleham`,
  `zone-guest-gyre`, `zone-guest-godot`: the guests.
- `sinew-mocap/solve` org's `lean-rebac-core`,
  `Rebac/core/ReBAC.lean`: the source the C types generate from.

## Related

- `rfd/2092-rebac-gates-libriscv-guest-access`: the gating model
  this RFD binds to a host repo and a loop definition.
- `rfd/2079-sandboxed-godot-in-zone-server-h2o-via-raw-libriscv`:
  the sandboxing decision behind `zone-guest-godot`.
- `rfd/2083-zone-server-h2o-replaces-godot-fabriczone`: the rule
  that ReBAC types generate from `lean-rebac-core`.
