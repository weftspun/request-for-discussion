# Logbook: FDB VFS embed into ecto_sqlite3, retracted

RETRACTED, MINE. The claim was that `EXQLITE_USE_SYSTEM=1` plus loading
datasource-store's `weft_fdb_vfs` static lib as a SQLite extension into
the same shared `libsqlite3.so.0` would make the Repo's connections open
databases with pages in FoundationDB. It builds, tests pass in dev
(plain-file SQLite), and the process holds one SQLite instance with the
VFS in its registry — the invariant I named as the crux. But the Repo
segfaults the first time ecto_sqlite3 opens a real handle.

## The apparatus

spot-broker at commit `904398a`
(`the FDB client compiled into ecto_sqlite as a SQLite VFS`), deployed
to Fly. FDB cluster `weftspun-fdb` up in the same org, `fdbcli --exec
"status minimal"` from the broker's own container returns `The database
is available`. Extension `/app/weft_fdb_vfs.so` present, links against
the same `libsqlite3.so.0` the exqlite NIF links (386 KB stub, verified
with `ldd`).

## What the run proved

    /app/bin/spot_broker eval "SpotBroker.Vfs.load!()"     → returns clean
    /app/bin/spot_broker eval "... Repo.start_link(pool_size: 1) ..."  → SIGSEGV

The extension loader path is fine: `weft_fdb_start()` runs, the FDB
network thread starts, `weft_vfs_register(1)` registers weft_fdb as
process default. The segfault fires during the first `sqlite3_open_v2`
that ecto_sqlite3 issues through the default VFS — i.e. the first
xOpen the VFS's own C code is asked to serve from a caller that is not
datasource-store's own thread-per-core loop.

## Why

datasource-store's `store.cpp` opens SQLite databases from
`std::thread` instances the store spawns itself and pins one per shard.
`fdb_vfs.c`'s per-handle state relies on that ownership — the store's
own README calls this out: "a caller never opens a database ... the
plane owns every handle, which is what keeps one owner and one fence
per database." The fence is not an operational nicety, it is the state
`fdb_vfs.c` looks up on every xRead/xWrite. An external caller
(ecto_sqlite3's DBConnection worker) has no fence, and the VFS
dereferences state that is not there.

This is a *design mismatch*, not a bug in either half. The store's VFS
was purpose-built to serve one owner and one fence, and asking it to
serve arbitrary threads is asking it to be something it is not.

## What replaces it

The bus. spot-broker reverts to commit `178529d` (the iceoryx2 endpoint):
the store binary runs inside the broker's container as the FDB client;
Elixir owns the bus NIF and speaks to the store over iceoryx2. That is
the pattern the store was designed for — one owner per avatar, same
machine, shared memory — and matches the workspace's standard shape of
two endpoints on a bus. STORE_READ replies come back CBOR (indefinite
array of rows, each a definite array of text or null cells) per the
cheap-or-nasty rule.

## What this settles

An off-the-shelf `SQLite VFS` interface is not a contract you can
satisfy behind an owner-and-fence design without touching the design.
The next time someone reaches for a similar embed — a NIF wrapping a
static lib that expects specific caller invariants — the read the
library's own README says about ownership and check whether the caller
can uphold it *before* the extension shim is written. `fdb_vfs.c`
line 1: "SQLite runs in a native process ... [the store] owns every
handle" is exactly the sentence I skipped.

## The bus deploy, after this retraction

Two more walls, both mine, both now in the record:

**CRLF shebang.** Fly reported `/app/start.sh: No such file or
directory` on a file that was present and executable. Git on Windows
had written CRLF into the checkout, making the interpreter path
`#!/bin/sh\r` — a file that does not exist. `.gitattributes` with
`*.sh text eol=lf` fixes it at the source.

**Stubs before init.** The NIF segfaulted in `iox2_node_builder_create`.
The harness dlopens libiceoryx2 through Chromium-style generated stubs,
and a stub called before `native_harness::InitializeStubs` is a jump
through a null pointer. `weft::load_bus()` is the init; `store.cpp`'s
main calls it on line one of its setup and the NIF did not. One guarded
call fixes it, verified in the image: `Nif.open(1, 1)` returns
`{:ok, ref}`.

With both fixed the deploy is green end to end: the store process runs
under Elixir supervision (`store: 1 shards, one database for each
avatar`), StoreBus opens the avatar and commits the events schema into
FoundationDB, Bandit listens on the 6PN address, and an authenticated
`GET /status` returns keeper state with the ledger read back over the
bus as CBOR. The unauthenticated request returns 401 — the zero-trust
control, exercised in prod.
