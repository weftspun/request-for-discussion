## The nine stores, and why each one failed

The store must satisfy four constraints at the same time: free and open
source, reachable from a second machine, a native Windows server, and
linear scaling per machine. It must also supply an ordered byte keyspace,
atomic multi-key commits, and read-write conflict detection for the fence.

| Store                                        | Why it failed                                                                               |
| -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| sqlite-in-sqlite, RocksDB, LeanStore, FASTER | Embedded. No second machine can reach the data.                                             |
| TiKV, Cassandra, ScyllaDB, LeanStore         | No native Windows server.                                                                   |
| TiKV, LeanStore                              | Snapshot isolation. `check_fence` has no mechanism.                                         |
| FASTER                                       | A hash index. No ordered range reads.                                                       |
| Cassandra                                    | Partition size limits against 10 GiB actors. No isolation across partitions.                |
| Zenoh, iceoryx2 tunnels and gateways         | Message transport, not a store. Asynchronous replication gives split-brain and silent loss. |
| Ra                                           | A Raft library. You write the store yourself, on the BEAM this plane exists to leave.       |
| FerretDB and MongoDB forks                   | The wrong data model. Transactions have time and size limits.                               |

Two stores satisfy all four constraints: FoundationDB, if it can be built
for Windows, and sharded PostgreSQL.

A message transport cannot replace the store. If a commit is acknowledged
locally and sent later, a machine that stops loses an unknown number of
commits, and it does so silently. If the commit waits for a remote
acknowledgement, it pays a network round trip. The local speed was the
missing guarantee.

## What the build already shows

- `release-7.3` and `main` both complete `cmake` configure on Windows.
- The Windows disk path is complete in `release-7.3`.
  `fdbrpc/include/fdbrpc/AsyncFileWinASIO.actor.h` exists under
  `#ifdef WIN32`. It implements `IAsyncFile` over `boost::asio`, which uses
  IOCP on Windows. `AsyncFileKAIO` is `#ifdef __linux__`.
  `Net2FileSystem.cpp` selects KAIO only on Linux and falls through to
  `Net2AsyncFile` elsewhere. **Nothing needs a rewrite, and io_uring is not
  a blocker in 7.3.**
- The Flow actor compiler is Python on `main`, and the C# implementation is
  a fallback behind `FDB_USE_CSHARP_TOOLS`. An earlier estimate called the
  C# compiler a blocker. It is not one.
- `lattice-world-weft/weft-warp-loop` builds Flow, including the asio
  layer, green on `windows-latest`, with no Windows patch to the source.

Windows IORing is not used. Its operation set started read-only, it needs
Windows 11 or Server 2022, and it makes a storage engine faster that must
first compile. `AsyncFileWinASIO` already supplies IOCP through
`boost::asio`.

## Dependencies that stop the build

Each one was found by a failure, and each one cost a full CI round:

- `jemalloc`. Configure stops without it.
- `fmt`. Configure stops without it.
- Jinja2. `flow/protocolversion/protocol_version.py` generates
  `ProtocolVersion.h`.
- Boost needs `format`, `asio` and `lockfree`. Upstream's Windows workflow
  installs a component list that is enough to configure and not enough to
  compile.

The official `foundationdb/build` image removes all of these on Linux. Use
it instead of a dependency list.

## Cost, measured

`bench_vfs 2000` on one machine, in operations per second per core. The
unit is the one `weft/limits.hpp` uses.

| Operation                  | Local file | FoundationDB, one node | FoundationDB, consensus |
| -------------------------- | ---------- | ---------------------- | ----------------------- |
| Insert, one commit each    | 262,438    | 941                    | 433                     |
| Insert, one commit for all | 618,078    | 399,456                | 315,869                 |
| Point read                 | 2,056,234  | 1,892,751              | 2,027,633               |
| Scan                       | 12,149,044 | 14,370,707             | 15,144,402              |

Read the first row with care. The local file column uses
`journal_mode=MEMORY` and sets no `synchronous` value, so it is not
durable. A durable local SQLite gives 2,008 commits per second per core,
not 262,438. FoundationDB passes it at about four concurrent writers,
because FoundationDB groups commits and a file per writer cannot.

**Reads are already at parity.** A point read costs 2,027,633 against a
local file's 2,056,234. No store choice can improve the read rows. The
choice is decided on the commit row alone.
