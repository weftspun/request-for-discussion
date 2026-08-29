---
title: "RFD 2043: Progression hexagon — core, ports, and adapters"
rfd: "2043"
state: published
scope: progression hexagon (proof of concept)
---

## Problem

The profile, the valid inventory transitions, and the affinity gate
on arts need to be durable across a session. They also need to be
testable with no database. Progression had no structure that gave it
these properties.

## Decision

The profile and inventory rules — the profile, the valid inventory
transitions, and the affinity gate on arts — need to be durable across
a session and testable with no database. The project structures
progression as a hexagon. The core defines the profile and the
inventory, the valid transitions, and the affinity gate, as a pure
reducer. The driving port `profile_source` carries a profile load at
login. The driven port `commit_sink` carries a durable write of the
profile and the inventory. `zone-backend` with `cockroach` commits
through the mTLS store (`rfd/2006-cockroachdb-with-mtls-role-separation`).
`feat/module-sqlite` caches on the instance and stands in as a
degraded commit, and a fixture adapter holds a recorded profile for
CI.
The persistence degrades from the `cockroach` adapter to the
`feat/module-sqlite` adapter behind one `commit_sink`, so a slipping
commit path does not block the loop. Inventory transitions validate in
the core, so a bad transition fails a fixture rather than a live
write, and the affinity gate holds an art out of reach below its
requirement. The core validates inventory transitions against a
recorded profile fixture, and a drop commits through the adapter and
survives a round trip.

## References

- Original record: `decisions/20260611-hexagon-progression-core.md`

## Related

- `rfd/2006-cockroachdb-with-mtls-role-separation`: the mTLS store the
  `cockroach` adapter commits through.
- `rfd/2041-hexagon-loot-core`: the loot core whose drops this
  progression core persists.
