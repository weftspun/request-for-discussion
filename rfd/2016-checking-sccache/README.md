# RFD 2016: Checking sccache

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Native builds route compilation through sccache
(https://github.com/mozilla/sccache) backed by a shared DigitalOcean
Spaces bucket (`chibifire-sccache`, region `tor1`), so object files
are cached across machines and CI (see
`rfd/2017-compiling-godot-engine/index.md`). The failure mode is
silent: if the `SCCACHE_*` environment is missing, the credentials are
wrong, or the region/endpoint is off, sccache quietly falls back to a
local disk cache — or records read/write errors — while the build

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
