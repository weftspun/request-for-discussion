# RFD 1067 details: the sibling repositories, and what each found

## The decision as published, and its three reasons

Keep CockroachDB. RFD 1020 stands.

The case against CockroachDB does not transfer, for three reasons.

1. `h2o-bench-tpcc`'s case for FoundationDB is TPC-C write throughput
   at MMO scale. `weftspun_studio` and RFD 1065's taxonomy write
   catalog facts, job records, and trait ids, nowhere near that load.
2. The one Ecto-compatible path, `ecto-fdb-relational`, embeds a JVM
   through a Rustler NIF. Its own ADR history permanently accepts no
   crash isolation, a JDK and Rust build step, and no per-call
   timeout. That trades Postgrex's plain socket for a real regression.
3. Raw FoundationDB, `h2o-bench-tpcc`'s own pick, drops SQL and Ecto
   entirely, so adopting it means rewriting every `Ecto.Schema` this
   project holds by hand, for throughput this load does not need.

The dead-fork risk is real, and not a throughput question. It is open
work, not a reason to move today.

## Retracted on 2026-08-20, reason by reason

The reasoning above stays in place because it records what was true, and because two of its
three reasons were answered rather than found wrong.

**Reason 2 was answered by a repository that no longer exists.** It rejected FoundationDB
because the one Ecto-compatible path embedded a JVM through a Rustler NIF, with no crash
isolation, a JDK and Rust build step, and no per-call timeout. That path was
`ecto-fdb-relational`, and it is archived. Its own last merged change reverted a bump because
main did not compile.

**Reason 3 was answered by the shape that replaced it.** It rejected raw FoundationDB for
dropping SQL and Ecto, which would mean rewriting every `Ecto.Schema` by hand.
`datasource-store` is not raw FoundationDB. It is SQLite with a VFS whose pages live in the
cluster, so SQL comes back, and no JVM comes with it. This RFD never assessed that shape,
because it did not exist here when the RFD was written.

**Reason 1 is still correct and never argued for moving.** Our load is nowhere near TPC-C at
MMO scale, so throughput was not the reason to keep CockroachDB and it is not the reason to
leave. Nothing about reason 1 changed.

So the retraction is narrow. Two reasons were removed by events, one was never load bearing,
and the open work this RFD named as the real risk is what remains.

**The dead-fork risk was the open item, and it is the part that aged badly.** The RFD called it
real, not a throughput question, and deferred it as open work rather than a reason to move
today. Today arrived.

## What this leaves unanswered

RFD 1020 picks CockroachDB and this RFD said it stands. RFD 1020 is still `discussion` and now
rests on a reranking that has been retracted, so it needs its own reading rather than
inheriting this one.

`character_taxonomy/` runs on CockroachDB per RFD 1065. Archiving the datasource does not move
that application, so somebody has to decide what it runs on. This retraction does not decide
it.

## The rerank table

| Rank     | Store                               | Ecto path                                            | What the sibling work found                                                                                      |
| -------- | ----------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1 (kept) | CockroachDB                         | `Ecto.Adapters.Postgres`, unmodified                 | Boring. PostgreSQL wire protocol, plain Postgrex socket. Already running under RFD 1020, RFD 1058, and RFD 1065. |
| 2        | FoundationDB Relational Layer (FRL) | `ecto-fdb-relational`, a Rustler NIF embedding a JVM | Works, at a real permanent cost. See below.                                                                      |
| 3        | mvsqlite (SQLite on FDB)            | none                                                 | A ~3s p90/p95/p99 latency ceiling under concurrency, and no Ecto adapter exists.                                 |
| 4        | Raw FoundationDB                    | none                                                 | Highest measured write throughput, and no SQL layer at all.                                                      |

## `weftspun/h2o-bench-tpcc`: FoundationDB over CockroachDB, for a different case

Its `rfd/0006-fdb-selection.md` picks raw FoundationDB over
CockroachDB, for a TPC-C-style MMO backend written in C against
`libh2o`. It gives three reasons. TPC-C is 88% writes, and FDB's
log-structured MVCC gives lower write latency than CockroachDB's Raft
path at that scale. FDB 7.3.79 is under active Apple development. By contrast,
"CockroachDB's v-sekai fork is a dead engine with no upstream
activity." The C API needs no JVM, no JNI, and no gRPC bridge.

None of these reasons name a workload `weftspun_studio` or
`character_taxonomy` actually carries. Both write catalog facts, job
records, and RFD 1065's trait ids, not an MMO's tick-rate traffic.

## `weftspun/ecto-fdb-relational`: the Ecto-compatible path, and its real cost

Three ADRs, in its `rfd/0001.md`, trace the same path this project
would need to keep Ecto and gain FoundationDB. ADR 0001 talks gRPC to
a separate `fdb-relational-server` process. ADR 0002 proposes an
embedded JVM through a Rustler NIF as an opt-in second transport. ADR
0003 replaces gRPC outright with that embedded transport, because
running two transports correctly cost more than the team could keep
funded.

ADR 0003's own "Consequences" section names what that final shape
costs, permanently. A JVM segfault, a native OOM, or a panic crossing
the Rust/JNI boundary takes down the whole BEAM node, with no crash
isolation. A JDK and a Rust toolchain become hard prerequisites to
`mix compile`, not only to run tests. Every call blocks a Rustler
`DirtyIo` scheduler thread, with no per-call timeout wired up.

Postgrex, by contrast, is a plain socket protocol library with none
of those costs. RFD 1058 grounds its whole zero-trust design in
predictable, boring processes. RFD 1059 asks for a build that runs
in one command on a laptop. A JDK-and-Rust compile prerequisite, and
a store that can crash the whole node, work against both.

## `weftspun/mvsqlite-tpcc-bench`: a measured ceiling, not a FoundationDB property

Its README records a known finding. Both fresh- and
contended-cluster sweeps clamp p90/p95/p99 latency to a
near-identical ~3.0 second value. This holds at every terminal count
of 4 or more. Root cause:
`sqlite-jdbc`'s fixed 3000ms `busy_timeout`, not FoundationDB itself,
tracked upstream at `weftspun/mvsqlite#11`. No Ecto adapter to
mvsqlite exists in any `weftspun` repository, so this path is not
available to `weftspun_studio` regardless of that finding.

## The one point that survives scrutiny

`h2o-bench-tpcc` RFD 1006's claim that the V-Sekai CockroachDB fork
this project pins is unmaintained upstream is a genuine risk. It is a
security-patch and long-term-support risk, not a throughput argument.
RFD 1020 already accepts pinning one tag deliberately. Track this in
RFD 1057's open work. Revisit it if the fork stays dark long enough
to matter, and not as a reason to adopt FoundationDB today.

## Sources

- `weftspun/h2o-bench-tpcc`, `rfd/0006-fdb-selection.md`
- `weftspun/ecto-fdb-relational`, `rfd/0001.md` (ADR 0001-0003)
- `weftspun/ecto-bench-tpcc`, README "Status / honest gaps"
- `weftspun/mvsqlite-tpcc-bench`, README "Known finding"
- `weftspun/scenario-tpcc-bench`, README (CockroachDB dropped as a
  comparison target there, for reasons specific to that repo's scope)
