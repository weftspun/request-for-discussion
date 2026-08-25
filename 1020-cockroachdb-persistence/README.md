# RFD 1020: CockroachDB persistence for catalog facts

**State:** committed
**Scope:** `weftspun_studio/`

## Problem

RFD 1019 builds an API server. An API server must keep its data.

The fact store in `WeftspunStudio.FactStore` holds facts in memory.
An Agent rebuilds the store from the RFD 1016 inventory at every
boot. A trust change dies when the node stops, and a retracted fact
comes back.

RFD 1016 records that catalog facts change fast. A license gate
vetoes a model, a benchmark moves a recommendation, and a backend
drops a model. The store must keep those changes.

## Decision

**Use SQLite for storage, and Ecto for the mapping.** Each service owns one file.
`Ecto.Adapters.SQLite3` drives it through `ecto_sqlite3`.

The problem above is unchanged. Catalog facts must survive a restart, and an Agent rebuilt at
every boot loses a retraction. Only the store changed.

This RFD published CockroachDB and withdrew it on 2026-08-20. The move is an adapter swap.
Ecto and the natural keys carried over. The cluster and `migration_lock: false` left.

This RFD covers `weftspun_studio/`. `character_taxonomy/` runs under RFD 1065 and moved in the
same sweep, for the same reason.

See `DETAILS.md` for the withdrawn decision as published, what carried over, the three risks
revisited, the evidence, the schema, local setup, the settings, and the status.
