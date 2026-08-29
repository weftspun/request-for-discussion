---
title: "RFD 2068: sccache with GitHub Actions cache for Godot container builds"
rfd: "2068"
state: published
scope: fabric-godot-images CI build cache
---

## Problem

The `fabric-godot-images` CI build lost its `docker/build-push-action`
layer cache when the build moved to plain `podman build`. Every push
then recompiled the Godot engine from scratch, spending 30 to 60
minutes each run. An earlier Tigris S3 sccache bucket also needed an
external account, five repo secrets, and ongoing cost.

## Decision

The `fabric-godot-images` CI build gets a compiler-output cache back
by wiring sccache to the native GitHub Actions cache backend,
`SCCACHE_GHA_ENABLED=true`. The previous `docker/build-push-action`
layer cache was lost when the build moved to plain `podman build` to
match the rootless-podman-plus-quadlet standard, so every push
recompiled the Godot engine from scratch, spending 30 to 60 minutes
each run. `ACTIONS_CACHE_URL` and `ACTIONS_RUNTIME_TOKEN` mount into
the container as podman build secrets, not build args, so they never
bake into an image layer. Every GHA runner sets these two values
automatically, so no repo secret is needed. This replaces the earlier
Tigris S3 sccache bucket, which needed an external account, five repo
secrets, and ongoing cost.

## References

- Full Containerfile and workflow changes, downsides, and rejected
  alternatives: `DETAILS.md`
- Original record:
  `decisions/20260624-sccache-github-actions-cache-for-godot-builds.md`

## Related

- `rfd/2016-checking-sccache`: an earlier sccache-checking record for
  the build cache.

## Detail

{{< include DETAILS.md >}}
