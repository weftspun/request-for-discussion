---
title: "RFD 2109: Two tiers, with FoundationDB as the store"
rfd: "2109"
state: published
scope: tier count, store selection
---

## Problem

`rfd/0107` describes four runtimes: h2o, Janet, a C core, and Godot.
`rfd/0108` adds local C ABI guests to that host. One person cannot
carry four runtimes, and neither record is built.

The tier count moved three times in one day, and the store moved five
times, with no record of either. The database is not the constraint.
Bandwidth is.

No record names the tier count or the store. Without one, each session
re-derives a different answer.

## Decision

**Egress dominates the bill, and the store does not.** Bandwidth per
client sets the cost, and one node serves the database load. No probe
measures a running deployment, so this record carries no cost figure.

**Two tiers.**

- Zone client: Godot. Rendering, XR, IK, and local physics.
- Server: Elixir and Phoenix. Identity, room directory, and the
  presence relay.

The server relays presence rather than simulating it. Phoenix supplies
identity, sessions, and migrations, which a Godot server would need
written in GDScript.

**The store is FoundationDB**, through `ecto_foundationdb`. `rfd/0075`
stands, and it is Apache 2.0, C++, write-optimized, and linearly
scalable by process. `rfd/0103`'s limits are accepted, so no joins, no
`or`, and no aggregates in the database.

That trade holds because the relational need is analytical, and the
analytical half does not use this store. Event logs and measurements
stay zstd Parquet in essential tuple normal form, read by DuckDB.
OLTP access is point lookups by player and room identity.

**taskweft stays an Elixir NIF.** `V-Sekai-fire/multiplayer-fabric-taskweft`
already has that shape. Janet and the C `libtaskweft` are dropped.

This supersedes `rfd/0107` and `rfd/0108`.

## References

- The stores considered, Rivet examined, and the open questions:
  `DETAILS.md`
- `rfd/2075-fdb-over-cockroachdb-for-zone-state`

## Related

- `rfd/2103-uro-on-ecto-foundationdb`: the adapter and its limits.
- `rfd/2046-server-authoritative-simulation-deferred-rollback`: the
  authority model a relay does not provide.

## Detail

{{< include DETAILS.md >}}
