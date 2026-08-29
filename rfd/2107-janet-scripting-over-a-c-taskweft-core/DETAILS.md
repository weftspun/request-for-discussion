## Role split

| Part          | Job                                                     | Language |
| ------------- | ------------------------------------------------------- | -------- |
| h2o           | HTTP ingress and reverse proxy. Connection termination. | C        |
| Janet         | Routing glue, configuration parsing, dynamic scripting. | Janet    |
| `libtaskweft` | HTN state-space search, graph traversal, game state.    | C        |
| Godot         | Client and visualization frontend, GDExtension and C++. | C++      |
| FoundationDB  | State, reached through `libfdb_c`.                      | —        |

The boundary that matters is between Janet and `libtaskweft`. Janet
holds what changes often and runs rarely. The C core holds what runs on
every tick.

## The database keeps its record set

FoundationDB stays, so the records that describe it stay in force:

| Record     | What it holds                                         |
| ---------- | ----------------------------------------------------- |
| `rfd/0075` | FoundationDB over CockroachDB, for a write-heavy load |
| `rfd/0073` | The async callback chain `libfdb_c` requires          |
| `rfd/0074` | Binary value encoding for FDB values                  |
| `rfd/0084` | zstd compression for batched zone-state values        |
| `rfd/0097` | Pubsub in userspace, with FDB as the durable log      |
| `rfd/0103` | Uro on `ecto_foundationdb`                            |
| `rfd/0002` | taskweft value narrowing in the FDB value encoding    |

`ecto_foundationdb` and `ecto-bench-tpcc` therefore keep a live
consumer, and `rfd/0006`'s CockroachDB with mTLS does not describe this
tier's store.

## Claims, and what is not measured

Three claims come with this tier:

- Startup is fast.
- Memory stays under 10 MB.
- Execution speed is near native.

None of the three is measured in this project. `data/measurements/`
holds throughput and latency parquet for a FoundationDB probe and the
libh2o host, and nothing for Janet or for a C taskweft core.

A record that states this tier's ceiling needs a measurement of this
tier. A number extrapolated from a 32-worker probe is not a measurement
of 1000 concurrent users, and this project keeps no such extrapolation.

## Why Rust is out

Rust is blocklisted for this project. The core is C, and the C bindings
Janet loads are the native-module boundary. This removes the option of
a Rust core with C bindings, which is otherwise the common shape for
this pattern.

## What this replaces

`libtaskweft` in C replaces the Elixir NIF form of taskweft.
`V-Sekai-fire/multiplayer-fabric-taskweft` is the re-entrant temporal
HTN planner and ReBAC engine today, and it is an Elixir NIF. A C
library with Janet bindings is a different artifact, and whether it is
a rewrite in that repository or a new repository is open.

`rfd/0093` compiles taskweft relation expressions to linear automata.
That evaluation model is what the C core implements, and the record
survives the language change.

## Open questions this record does not settle

This record is abandoned, so none of the four questions below stay
open in the form they take here. Each one asks where a part goes in a
four-part stack that the project does not build. The records that
carry the same subject forward are these.

`rfd/0109` places Elixir and the store. The tier is Elixir plus
FoundationDB, and `rfd/0103` puts Uro on `ecto_foundationdb`, so the
Elixir tier drives the database path. `rfd/0110` places the guest
runtime and the transport. One pinned Godot build hosts libriscv
guests through its `sandbox` module and terminates WebTransport
through its `http3` module, and no Janet layer exists to compete with
either. `rfd/0108` closed the first and third questions before it was
abandoned in turn.

The four questions stay written below as the record left them.

**Which part talks to FoundationDB.** `rfd/0073` drove `libfdb_c`
callbacks from the libh2o event loop, when h2o was the whole server. If
h2o is ingress and reverse proxy only, the loop that drives the
callbacks may belong to `libtaskweft` instead. Janet has no `libfdb_c`
binding in this project today.

**Where Elixir goes.** The four parts name no Elixir. `zone-backend` is
Uro, a Phoenix and Elixir application, and it is the live identity,
zone-directory, and planner service with a push on 2026-08-08.
`rfd/0090` is its production release shape, and `rfd/0103` puts it on
`ecto_foundationdb`. Nothing here retires it, and nothing here places
it.

**Whether Janet replaces the libriscv guests.** `rfd/0094` keeps a UGC
game loop where guests arrive as CDN-delivered riscv64 ELFs, run under
libriscv, and are gated by ReBAC per `rfd/0092`. Janet is also a
dynamic layer loaded at runtime. Two runtimes for user code is one more
than the tier argument allows.

**Where the game transport lives.** `rfd/0008` and `rfd/0023` put game
traffic on WebTransport over HTTP/3, and `rfd/0088` chose picoquic and
picotls over h2o's own QUIC. If h2o terminates HTTP as ingress, the
record that says which part terminates a WebTransport session does not
exist.
