---
title: "RFD 2113: FoundationDB on Windows, built from source"
rfd: "2113"
state: discussion
scope: store platform support, build toolchain, packaging
---

## Problem

`rfd/0109` selects FoundationDB as the store. The store must now also run
on Windows. It must run the server, not only the client. A Linux virtual
machine on the Windows host does not count.

FoundationDB supplies no Windows binaries. Release 7.3.76 has deb, rpm,
`.so`, x86_64 and aarch64 assets. A scan of the last 60 releases finds no
Windows, MSI, DLL or EXE asset.

Upstream looks like it tests this, and it does not. The
`windows-boost-test.yml` workflow has a step with the name "Configure and
Build". That step runs only `cmake ..`. No step after configure runs on
Windows.

## Decision

**Build FoundationDB for Windows from source.** Nine other stores were
examined. Each one failed on the same two constraints: a native Windows
server, or a store that a second machine can reach. `DETAILS.md` lists
them.

**Use clang-cl. Do not use MSVC.** Flow uses GNU `__attribute__` syntax in
many files. It has never compiled with `cl.exe`. Use Ninja with clang-cl,
and set the MSVC environment first. An attempt with the default MSVC
toolset failed on `__PRETTY_FUNCTION__` and `swift_attr`. Those errors were
the wrong compiler, not defects in FoundationDB.

**Build Linux in the official image**, `foundationdb/build`. The image has
all dependencies. Linux is the control. A red Windows job has no meaning
until Linux is green.

**Package with fpm on Linux and macOS. Use FoundationDB's own MSI on
Windows.** `packaging/msi/` already holds the WiX sources and
`cmake/FindWIX.cmake`.

**If the port fails, use sharded PostgreSQL.** It supplies a native Windows
server today. The cost is per-shard replication and promotion, built by
hand.

## References

- The nine stores, the evidence, and the measurements: `DETAILS.md`
- Work in progress: `v-sekai-multiplayer-fabric/foundationdb`, branch
  `portability-consensus`
- `rfd/2109-two-tiers-with-foundationdb-as-the-store`: why the store is FoundationDB.

## Related

- `rfd/2114-prove-the-store-by-breaking-it`: how a built store is verified.

## Detail

{{< include DETAILS.md >}}
