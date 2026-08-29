---
title: "RFD 2116: The zone server is Elixir with epoll, in the h2o style"
rfd: "2116"
state: published
scope: zone server implementation, deployment tier
---

## Problem

`rfd/0083` replaced the Godot `FabricZone` server with `zone-server-h2o`, a native libh2o and FoundationDB server built with Fil-C. That tier works. `rfd/0095` records a Godot ELF that runs 57.9 million instructions and reads `project.godot` out of FoundationDB.

The tier is not affordable. It is a fourth language and a fourth runtime next to Elixir, CockroachDB, and Godot. Each one carries its own build, its own deployment, its own failure modes, and its own learning cost. `zone-server-h2o` is archived on GitHub for that reason.

An archive with no replacement record leaves the project with no answer to what serves a zone.

## Decision

The zone server is Elixir, on an epoll loop, in the style h2o uses. It is slower than the native tier. The project accepts the slower server, because it costs no fifth thing to build and operate.

The affordable tier is three parts, and the zone server is inside the first:

- Elixir, which holds the zone server and `zone-backend`.
- CockroachDB, which holds the state. `rfd/0006` returns to force.
- Godot, which is the client and the content tool.

"In the h2o style" names the shape, not the library. A small number of event loops own their own sockets, each loop reads without blocking, and no request holds a loop while it waits. The work that `rfd/0072`-`0084` did against libh2o does not port. Those records are retired by `rfd/0117`.

This supersedes `rfd/0083`.

## References

- The cost argument, what carries over, and what does not: `DETAILS.md`
- [`rfd/2083-zone-server-h2o-replaces-godot-fabriczone`](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive/tree/main/rfd/2083-zone-server-h2o-replaces-godot-fabriczone):
  the decision this supersedes.

## Detail

{{< include DETAILS.md >}}
