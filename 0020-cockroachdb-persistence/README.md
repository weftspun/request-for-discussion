# RFD 0020: CockroachDB persistence for catalog facts

**State:** committed
**Scope:** `weftspun_studio/`

## Problem

RFD 0019 builds an API server. An API server must keep its data.

The fact store in `WeftspunStudio.FactStore` holds facts in memory.
An Agent rebuilds the store from the RFD 0016 inventory at every
boot. A trust change dies when the node stops, and a retracted fact
comes back.

RFD 0016 records that catalog facts change fast. A license gate
vetoes a model, a benchmark moves a recommendation, and a backend
drops a model. The store must keep those changes.

## Decision

**Use SQLite for storage, and Ecto for the mapping.** Each service owns one file.
`Ecto.Adapters.SQLite3` drives it through `ecto_sqlite3`.

The problem above is unchanged. Catalog facts must survive a restart, and an Agent rebuilt at
every boot loses a retraction. Only the store changed.

### Retracted on 2026-08-20: the CockroachDB decision

The decision this RFD published is withdrawn. It stays written below, because it records what
was true and because most of it carried over.

    Use the V-Sekai CockroachDB build for storage, and Ecto for the
    mapping. The V-Sekai build lives at
    `https://github.com/v-sekai/cockroach`, from the Oxide Computer
    build of CockroachDB 22.1. The project already depends on that build
    elsewhere, so the same build keeps one database version across the
    work.

    CockroachDB speaks the PostgreSQL wire protocol. Ecto drives it
    through `Ecto.Adapters.Postgres`, and no separate adapter is
    necessary.

RFD 0067 reranked CockroachDB against FoundationDB and kept it. That RFD is now abandoned, and
`weftspun/cockroach-local` is archived and out of `default.xml`, so this decision pointed at a
repository that no longer takes changes.

### What carried over

Ecto carried over, and so did the mapping. The move is an adapter swap.

The natural keys carried over, and the reason changed. This RFD adopted them because
CockroachDB gives no gap free `SERIAL`. They stay because a catalog fact has a natural key, so
an integer id would be a second name for the same row.

### What left

`migration_lock: false` left. This RFD names it as a constraint, because CockroachDB has no
PostgreSQL advisory lock. That constraint went with the database.

The cluster left. `mix weftspun.crdb` is deleted, 104 lines that installed a binary, started a
node and stopped it. The `cockroach_local` dependency is gone from every `mix.exs`.

### The risks, revisited

This RFD named three. Two are answered and one is not.

**"CockroachDB 22.1 is old."** It called a version move a separate decision. That decision
arrived as a different one, and the risk is now spent rather than resolved.

**"The suite needs a running cluster."** It recorded that a developer without one sees 16
failures. A file needs no server, so that is gone. `weftspun-studio` now runs 110 tests with
two failures, and neither touches the database.

**"A second store is a second source of truth."** Unchanged. The HTTP surface still reads the
in-memory store, so the two can still drift, and pointing the router at `EctoFactStore` is
still the next step. Changing the engine did not address it.

### Evidence

Three merged changes rather than an intention. `weftspun-studio` and
`weftspun-character-taxonomy` both moved, and `cockroach-local` is archived.

One claim was checked rather than assumed, because an earlier draft of this amendment had it
backwards. The `facts` table carries `tags` as `{:array, :string}`, and SQLite takes it:
`ecto_sqlite3` stores an array as JSON, and it round-trips and queries through `json_each`. No
schema change was needed, and a retraction claiming otherwise would have invented a migration.

### Scope

This RFD covers `weftspun_studio/`. `character_taxonomy/` runs under RFD 0065 and moved in the
same sweep, for the same reason.

See `DETAILS.md` for the schema, local setup, the settings, the risks, and the status.
