---
title: "RFD 2016: Checking the sccache build cache"
rfd: "2016"
state: published
scope: build
---

## Problem

The project had no reliable way to confirm that sccache used the
shared remote bucket and was healthy. A misconfigured cache degrades
silently. The build still succeeds even when the shared cache is not
in use. Inferring health from build time or a debug log needs secrets
or log parsing.

## Decision

To confirm sccache is using the shared remote bucket and is healthy, run
`sccache --show-stats` and read three lines. `Cache location` must read
`s3, name: chibifire-sccache` with the project's key prefix; `Local
disk` means the `SCCACHE_*` environment is not set in that shell. `Cache
errors` must be `0`; a non-zero count means a credentials, endpoint, or
connectivity problem. `Cache hits` versus `Cache misses` shows the
payoff, rising across builds. This one command was chosen over inferring
health from build time or reading a debug log, because a misconfigured
cache degrades silently — the build still succeeds even when the shared
cache is not in use — and one command needs no secrets and no log
parsing.

On Windows this is wrapped as a `sccheck` PowerShell function (alias
`scc`). The bash equivalent filters the same command with `grep`.

## References

- Windows/bash commands, decision drivers, and further reading: `DETAILS.md`
- Original record: `decisions/20260606-checking-sccache.md`

## Related

`rfd/2017-compiling-godot-engine/index.md` sets up the sccache backend
this check verifies.

## Detail

{{< include DETAILS.md >}}
