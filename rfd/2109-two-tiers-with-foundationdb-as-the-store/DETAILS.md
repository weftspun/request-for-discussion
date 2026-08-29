## Egress is the cost, and the store is not

Bandwidth per client sets the bill. `rfd/0100` caps a client at 256
kbps, and egress scales with concurrent clients and hours played. No
deployment runs, so no monthly figure exists.

## The database is not what the money buys

Measured ceilings, `run_id = fly-shared-1x-1g` and `local-16core` in
`data/measurements/`: 2159.1 ops/s on one Fly `shared-cpu-1x`, and
6086.5 ops/s on a 16 vcpu workstation. Both are the concurrency 32 row,
which is the highest the probe ran.

```sql
SELECT run_id, ops / seconds AS ops_per_sec
FROM read_parquet('throughput.parquet') WHERE concurrency = 32;
```

Presence never reaches the store. A pose is transient, and the next
tick supersedes it. Persistent writes are login, avatar change, and
room join.

## Stores considered

The search ran under four rules: FOSS, non-viral license, relational
form, and linear scaling. Rust was banned and then unbanned during the
search, which returned TiDB to the list.

| Store             | Outcome                                                              |
| ----------------- | -------------------------------------------------------------------- |
| FoundationDB      | Chosen. Apache 2.0, C++, linear, write-optimized                     |
| TiDB              | Viable, not chosen. Apache 2.0, MySQL wire, so `myxql` connects      |
| YDB               | Viable, not chosen. Apache 2.0, C++, and no Ecto adapter exists      |
| Apache Ignite     | Viable, not chosen. Apache 2.0, Java, and no Ecto adapter exists     |
| YugabyteDB        | Vetoed                                                               |
| Stock PostgreSQL  | Blocklisted for operational reasons, which are vacuum and heap bloat |
| SQLite            | Rejected. Weaker constraint enforcement than the requirement         |
| CockroachDB       | Source-available since 2019, so it fails the FOSS rule               |
| Citus             | AGPL, so it fails the non-viral rule                                 |
| MariaDB, MySQL    | GPL, so they fail the non-viral rule                                 |
| ScyllaDB, MongoDB | AGPL or SSPL, so they fail the non-viral rule                        |
| DuckDB, for OLTP  | 0.919 ms point read, the slowest of four measured in `rfd/0103`      |
| Rivet 2.0         | Apache 2.0. Actor logic is TypeScript. See the section below         |

TiDB is the option that keeps relational form with no adapter work. It
costs more processes, because a cluster wants PD, TiDB servers, and
three TiKV nodes. It also carries MySQL's weaker constraint set, with
no EXCLUDE constraints and no DOMAIN types.

## Rivet 2.0, examined

An earlier draft of this record excluded Rivet because its SDK is
TypeScript and it has no Elixir or Godot client. That reason is not
accurate, and this section replaces it.

Rivet reaches an actor without an SDK. Raw HTTP goes to
`https://api.rivet.dev/gateway/{actorId}/request/{...path}`, and a raw
WebSocket goes to
`wss://api.rivet.dev/gateway/{actorId}@{token}/websocket/{...path}`.
So a Godot client can connect. The repository's own `Vanilla HTTP API`
documentation page is a `TODO` stub, so that path is real and
undocumented.

What Rivet is, verified from the repository: Apache 2.0, 60.7 percent
Rust, and pushed on 2026-08-07. The engine has four parts. Pegboard
orchestrates actors, Gasoline runs durable execution, Guard routes
traffic, and Epoxy is a multi-region key-value store over EPaxos. Self
hosting is one binary or `docker run -p 6420:6420 rivetdev/engine`.
Storage is SQLite for local development, FoundationDB for self-hosted
deployments, or Postgres.

The fit is genuine on one point. An actor per room with the
`onWebSocket` handler is a presence relay, and
`options: { canHibernateWebSocket: true }` makes an empty room cost
nothing.

The reason to decline is the comparison Rivet draws. Its published
figures measure against Kubernetes: about 20 ms cold start against 6 s
for a pod, and 0.6 KB per actor against 50 MB. This project's
alternative is a BEAM process, not a pod. Phoenix already supplies a
process per connection, a process per topic, PubSub fan-out, and
supervision. A BEAM process spawns in microseconds and sits in the same
size order as 0.6 KB.

Adopting Rivet moves room logic into TypeScript and adds a Rust engine.
That is two runtimes replacing one, against this record's two-tier
decision.

Three Rivet features have no Elixir equivalent to hand: Guard's
multi-region routing, Epoxy's multi-region consensus, and Gasoline's
durable execution. A global player base is the case that would justify
revisiting this.

## The trade this record accepts

`rfd/0103` states the FoundationDB limits directly. A query is valid
only when one Get or one GetRange satisfies it. No joins. No `or`. No
aggregates in the database, so filtering and grouping run in Elixir.
One Between clause per query, on an indexed field.

Those limits bite reporting, and reporting does not use this store.
`data/measurements/` already holds the analytical record as zstd
Parquet, and `lean-duckdb` already reads it. DuckDB supplies the joins
and the aggregates.

Point-read latency from `rfd/0103`: 0.405 ms for a new transaction per
read, and 0.157 ms inside one transaction. PostgreSQL 16 measured
0.084 ms, so FoundationDB is 4.8 and 1.9 times that, in the same order
rather than a different one.

## Open questions

**Player-hosted zones, or server-hosted.** A client that hosts its zone
brings its own upstream, so capacity grows with players rather than
with the bill. This record picks server-hosted and does not price the
alternative.

**Interest management.** `lean-interest-mgmt` exists, and it is the
lever that moves the 256 kbps figure. Nothing in this record changes
that number.

**Server authority.** A relay is not server-authoritative, so a client
can assert a false pose. `rfd/0046` does not hold for presence. That is
tolerable for social VR and wrong for the loot-action combat loop.

**WebTransport interoperation.** Whether the Godot client of `rfd/0023`
speaks to a Phoenix endpoint is untested here. WebSocket is the
fallback, at a cost in latency.

**How many FoundationDB processes, and where.** One machine hosting
every process is one failure domain. Real availability needs separate
machines, and this record does not fund them.
