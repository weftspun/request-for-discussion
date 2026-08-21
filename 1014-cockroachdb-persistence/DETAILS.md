# RFD 1014 details: reasoning, schema, setup, status

> **The store is SQLite now.** The section directly below retracts the CockroachDB decision
> and gives the reasons. The rest of this file is kept as written, because the schema, the
> modules and the seed all carried over unchanged, and because the parts that did not carry
> over are worth reading next to what replaced them.
>
> Read every mention of a cluster, a node, a port or `mix weftspun.crdb` as history. The
> sections below are marked where they stopped being true.

## Retracted on 2026-08-20: the CockroachDB decision

The decision this RFD published is withdrawn. It stays written here, because it records what
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

RFD 1043 reranked CockroachDB against FoundationDB and kept it. That RFD is now abandoned, and
`weftspun/cockroach-local` is archived and out of `default.xml`, so this decision pointed at a
repository that no longer takes changes.

## What carried over

Ecto carried over, and so did the mapping. The move is an adapter swap.

The natural keys carried over, and the reason changed. This RFD adopted them because
CockroachDB gives no gap free `SERIAL`. They stay because a catalog fact has a natural key, so
an integer id would be a second name for the same row.

## What left

`migration_lock: false` left. This RFD names it as a constraint, because CockroachDB has no
PostgreSQL advisory lock. That constraint went with the database.

The cluster left. `mix weftspun.crdb` is deleted, 104 lines that installed a binary, started a
node and stopped it. The `cockroach_local` dependency is gone from every `mix.exs`.

## The risks, revisited

This RFD named three. Two are answered and one is not.

**"CockroachDB 22.1 is old."** It called a version move a separate decision. That decision
arrived as a different one, and the risk is now spent rather than resolved.

**"The suite needs a running cluster."** It recorded that a developer without one sees 16
failures. A file needs no server, so that is gone. `weftspun-studio` now runs 110 tests with
two failures, and neither touches the database.

**"A second store is a second source of truth."** Unchanged. The HTTP surface still reads the
in-memory store, so the two can still drift, and pointing the router at `EctoFactStore` is
still the next step. Changing the engine did not address it.

## Evidence

Three merged changes rather than an intention. `weftspun-studio` and
`weftspun-character-taxonomy` both moved, and `cockroach-local` is archived.

One claim was checked rather than assumed, because an earlier draft of this amendment had it
backwards. The `facts` table carries `tags` as `{:array, :string}`, and SQLite takes it:
`ecto_sqlite3` stores an array as JSON, and it round-trips and queries through `json_each`. No
schema change was needed, and a retraction claiming otherwise would have invented a migration.

## Scope

This RFD covers `weftspun_studio/`. `character_taxonomy/` runs under RFD 1041 and moved in the
same sweep, for the same reason.

### Why CockroachDB

**Retracted.** The reasons below are sound and stopped applying. "One API server or many" was
the argument, and the load never grew into it. RFD 1043 measured the same thing from the other
side and kept CockroachDB anyway, and that RFD is now abandoned too.

CockroachDB gives one API server or many. A single node runs on a
developer machine. The same binary joins a cluster later. The API
server therefore grows without a database migration.

The wire protocol is the PostgreSQL protocol. A developer who knows
`psql` needs no new tool.

### Two constraints

**One left, one stayed.** `migration_lock: false` went with the database, because it existed
for CockroachDB's missing advisory lock. The natural keys stayed, for a better reason than the
one below: a catalog fact has a natural key, so an integer id would be a second name for the
same row.

CockroachDB has no PostgreSQL advisory lock. The Ecto migrator takes
such a lock by default. Every repository configuration therefore sets
`migration_lock: false`.

CockroachDB gives no gap free integer sequence. A `SERIAL` column
returns large scattered numbers. The `facts` table therefore uses the
model id as the primary key. A catalog fact already has a natural
key, so this costs nothing.

## The facts table

**Unchanged.** Every type here is portable, including `tags`. `ecto_sqlite3` stores an array as
JSON, and it round-trips and queries through `json_each`, which was measured rather than
assumed.

| Column        | Type          | Holds                                            |
| ------------- | ------------- | ------------------------------------------------ |
| `fact_id`     | `string`      | The model id. Primary key.                       |
| `content`     | `text`        | The label or the task text.                      |
| `category`    | `string`      | The client feature, such as `image_to_raw_mesh`. |
| `tags`        | `string[]`    | Type, host, and status.                          |
| `trust_score` | `float`       | Zero to one. Feedback moves it.                  |
| `hrr_vector`  | `bytea`       | The packed float64 phase vector.                 |
| `inserted_at` | `timestamptz` | Row creation time.                               |
| `updated_at`  | `timestamptz` | Last change time.                                |

The shape follows the hermes-agent holographic memory store, as RFD
1013 records.

`hrr_vector` holds the output of
`WeftspunStudio.FactVector.encode/2` as a packed binary. The width is
fixed at 1024 float64 phase angles, so a row takes 8 kilobytes. The
changeset derives the vector from the other columns. No caller
supplies it. A row therefore cannot hold a vector that disagrees with
its fields. RFD 1015 records the encoding.

Search reads the candidate rows and scores them in Nx. The database
applies the trust floor first. A phase similarity over a packed
tensor has no SQL form in CockroachDB 22.1, so the algebra stays in
Elixir.

## The seed database

The RFD 1010 inventory is the seed, not a fixed table.
`WeftspunStudio.Adapters.EctoFactStore.seed/0` writes it once. A
second run refreshes the same rows and adds no duplicate, because the
model id is the primary key.

After the seed the database is the record. Feedback moves a trust
score. A retraction deletes a row. The seed never overwrites those
later changes for a fact it does not name.

## Modules

| Module                                  | Role                                      |
| --------------------------------------- | ----------------------------------------- |
| `WeftspunStudio.Repo`                   | The connection pool.                      |
| `WeftspunStudio.Facts.Fact`             | The schema and the changeset.             |
| `WeftspunStudio.Adapters.EctoFactStore` | A `Ports.FactSink` adapter.               |
| `WeftspunStudio.Release`                | Migration and seed for a packaged binary. |

`EctoFactStore` is the durable twin of `FactStore`. Both implement
`WeftspunStudio.Ports.FactSink`, so a caller can take either one. The
port keeps the choice out of the caller.

A Burrito binary carries no Mix, so `mix ecto.migrate` cannot run
against it. `WeftspunStudio.Release` does the same work. The command
line offers `weftspun db migrate`, `weftspun db seed`, and
`weftspun db status`.

## Local setup

**Gone.** There is no cluster to start. The database is a file created on demand, so
`mix ecto.migrate` is the whole instruction and `mix test` needs nothing before it.

The `cockroach_local` library owns the host lifecycle. It resolves
the binary from `COCKROACH_BIN`, then `priv/cockroach/`, then the
path. A Mix task wraps it:

```
mix weftspun.crdb install   # fetch the V-Sekai 22.1 build
mix weftspun.crdb path      # print the binary in use
mix weftspun.crdb           # run a node in the foreground
```

`CockroachLocal.Provision` downloads the same V-Sekai release this
RFD selects, so a second source of the binary does not arise.

Create the schema and load the seed:

```
mix ecto.setup
WEFTSPUN_SERVE=0 mix run -e 'WeftspunStudio.Adapters.EctoFactStore.seed()'
```

The node listens on 127.0.0.1:26257 and stores data under `.crdb`.
That directory stays out of version control.

The node runs insecure, so the `root` user needs no password. Use
that setting on a developer machine only. A shared host needs
certificates.

## Settings

| Variable               | Default         | Holds                                        |
| ---------------------- | --------------- | -------------------------------------------- |
| `WEFTSPUN_DB`          | `1`             | Set to `0` to start with no connection pool. |
| `WEFTSPUN_DB_HOST`     | `127.0.0.1`     | Host name.                                   |
| `WEFTSPUN_DB_PORT`     | `26257`         | Port.                                        |
| `WEFTSPUN_DB_NAME`     | per environment | Database name.                               |
| `WEFTSPUN_DB_USER`     | `root`          | User name.                                   |
| `WEFTSPUN_DB_PASSWORD` | empty           | Password.                                    |
| `WEFTSPUN_DB_POOL`     | `10`            | Pool size in a release.                      |

The inventory commands need no database. `WEFTSPUN_DB=0` therefore
lets `weftspun models list` run on a host with no cluster.

## Risks

**This risk is unchanged, and the two below are spent.**

A second store is a second source of truth. The HTTP surface still
reads the in memory store, so the two can drift. The next step points
the router at `EctoFactStore` and deletes the Agent.

CockroachDB 22.1 is old. The Oxide build tracks that version. A move
to a later version is a separate decision.

The suite needs a running cluster. A developer with no cluster sees
16 failures. The test helper names the start command.

## Status

Done:

- The V-Sekai build runs as one local node.
- The `facts` table exists, with the category and trust indexes.
- `EctoFactStore` implements every `FactSink` callback.
- The seed writes 29 facts and repeats without a duplicate.
- 16 tests cover the seed, the search, the trust moves, and the
  retraction. The whole suite passes with 78 tests.
- `cockroach_local` provisions and runs the host, through
  `mix weftspun.crdb`. **Both are deleted.** The dependency is out of
  every `mix.exs`, and the Mix task went with it.

### The provisioner never reached the binary

`mix weftspun.crdb install` answered `:unsupported_target` on every
platform, and not only on Windows. Two faults stood in the way, and
`cockroach_local` had neither of them.

The task passed `:os.type()` to `Provision.install/2`. That returns an
`{os_family, os_name}` pair such as `{:win32, :nt}` or
`{:unix, :linux}`. The asset map is keyed `{:windows, :x86_64}`, thus
the two shapes never matched. `target/0` derives the pair now.

The task then passed `priv/cockroach` as the destination.
`install/2` appends `cockroach` itself, thus the binary landed in
`priv/cockroach/cockroach/` while `bin/1` read `priv/cockroach/`. It
installed, and then nothing could find it. The task passes `priv` now.

The V-Sekai release carries a Windows zip, a Linux tarball, and two
macOS tarballs. None of them was reachable before this.

### Where the suite runs

RFD 1038 moves development into a dev container. That container runs
Linux, thus it takes the Linux tarball.

`scripts/studio-test.sh` skips the suite when no node answers on
127.0.0.1:26257, and it names the start command. A hook that failed
instead would block a commit that touched no code.

Open:

- The router still reads the in memory store.
- A secure cluster needs certificates and a real user.
