---
title: "RFD 2017: Compiling the Godot engine"
rfd: "2017"
state: published
scope: build
---

## Problem

Developers build the V-Sekai multiplayer-fabric Godot engine on two
different hosts from one workstation. Without a shared build cache,
each host recompiles the same objects, wasting time. The project also
needed a way to share cache objects across hosts without committing
access keys or other secrets.

## Decision

Developers build the V-Sekai multiplayer-fabric Godot engine on two
hosts from one workstation: Windows (PowerShell and MinGW) and WSL/Linux
(`linuxbsd`). The build standardizes on `sccache` as the only object
cache, wired in as the SCons compiler launcher through a `gscons` shell
function on each host. SCons's own `CacheDir` (`cache_path=`) stays
disabled, because sccache already caches every compiled object first;
running both would double-cache the same artifacts for no extra hits.

Cross-host sharing goes through sccache's S3-compatible storage backend,
not a shared filesystem directory. Only non-secret bucket coordinates
(`SCCACHE_BUCKET`, `SCCACHE_ENDPOINT`, `SCCACHE_REGION`) are configured
through environment variables; access keys live in a local AWS profile
or, in CI, in GitHub Actions secret variables, and are never committed.
`SCCACHE_BASEDIRS` strips the checkout root from compile paths so a
moved or renamed checkout keeps its cache hits.

## References

- Prerequisites, PowerShell/bash setup, CI wiring, troubleshooting, and
  further reading: `DETAILS.md`
- Original record: `decisions/20260606-compiling-godot-engine.md`

## Related

`rfd/2016-checking-sccache/index.md` verifies this cache is working;
`rfd/2007-godot-double-precision-template-release-for-zone/index.md`
uses this build for zone-server binaries.

## Detail

{{< include DETAILS.md >}}
