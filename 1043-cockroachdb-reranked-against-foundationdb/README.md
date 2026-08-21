# RFD 1043: CockroachDB, reranked against FoundationDB

**State:** abandoned
**Scope:** `weftspun_studio/`, `character_taxonomy/`

## Problem

RFD 1014 picked CockroachDB before sibling `weftspun` repositories
built and benchmarked FoundationDB, its Relational Layer, and
mvsqlite. One of them, `h2o-bench-tpcc`, picked FoundationDB over
CockroachDB, and called the CockroachDB fork this project pins "a
dead engine." Does that verdict carry over here.

## Retracted on 2026-08-20

**The decision below no longer holds.** `weftspun/cockroach-local` is archived and is out of
`default.xml`. `datasource-foundationdb` and `datasource-store` are forked in on side 6.

Abandoned here means the decision was in force and has been reversed. It does not mean nobody
acted on it. The reasoning stays in place because it records what was true, and because two of
its three reasons were answered rather than found wrong.

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

RFD 1014 picks CockroachDB and this RFD said it stands. RFD 1014 is still `discussion` and now
rests on a reranking that has been retracted, so it needs its own reading rather than
inheriting this one.

`character_taxonomy/` runs on CockroachDB per RFD 1041. Archiving the datasource does not move
that application, so somebody has to decide what it runs on. This retraction does not decide
it.

## Decision, as published and now retracted

Keep CockroachDB. RFD 1014 stands. See `DETAILS.md` for the
repository-by-repository evidence this reranking draws on.

The case against CockroachDB does not transfer, for three reasons.

1. `h2o-bench-tpcc`'s case for FoundationDB is TPC-C write throughput
   at MMO scale. `weftspun_studio` and RFD 1041's taxonomy write
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

## Related

RFD 1014 picks CockroachDB. RFD 103a and RFD 103b state the
zero-trust, one-command build. RFD 1041's taxonomy runs on
CockroachDB in `character_taxonomy/`. RFD 1039 gets the dead-fork
risk as a new open-work item.
