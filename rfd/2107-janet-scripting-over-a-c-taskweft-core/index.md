---
title: "RFD 2107: Janet scripting over a C taskweft core, behind h2o"
rfd: "2107"
state: abandoned
scope: zone server tier, taskweft implementation language
---

## Problem

`rfd/0083` built the zone server as native libh2o with FoundationDB.
The tier held. Its cost was questioned, and `zone-server-h2o` was
archived on 2026-08-08 on the argument that a fourth runtime was more
than the project could carry.

The archive removed the host and left no answer to what serves a zone.
Candidate answers came and went inside one session: an Elixir epoll
server, then h2o with a taskweft NIF, then a CockroachDB variant of
this record. None reached the site.

A tier needs one record. Without it, each session re-derives the stack
from memory, and the inventory in `rfd/0062` describes a host that is
gone.

## Decision

Four parts, each with one job:

- h2o is the frontend HTTP ingress and the reverse proxy. It terminates
  the connection. It does not hold game logic.
- Janet is the dynamic layer: routing glue, configuration parsing, and
  scripting.
- `libtaskweft` is a C library carrying the heavy work: HTN
  state-space search, graph traversal, and game state. It exposes C
  bindings, and Janet loads it as a native module, `.so` or `.dylib`.
- Godot is the client and the visualization frontend, over GDExtension
  and the C++ API.

FoundationDB stays the database, reached through the `libfdb_c` C API.
`rfd/0075` stands, and CockroachDB is not the store. `rfd/0073`'s async
callback chain is the integration pattern, because `libfdb_c` is
callback-based and needs an event loop to drive it.

Rust is out. The core is C. `zone-server-h2o` is unarchived and is the
host repository again.

## References

- The claims this rests on, what is not measured, and the open
  questions: `DETAILS.md`
- `v-sekai-multiplayer-fabric/zone-server-h2o`,
  [fabric-flow-adapters](https://github.com/v-sekai-multiplayer-fabric/fabric-flow-adapters)

## Related

- `rfd/2083-zone-server-h2o-replaces-godot-fabriczone`: the host this
  amends rather than replaces.
- `rfd/2075-fdb-over-cockroachdb-for-zone-state`: the database choice
  this keeps.
- `rfd/2093-compile-taskweft-to-linear-automata`: the taskweft
  evaluation model the C core implements.

## Detail

{{< include DETAILS.md >}}
