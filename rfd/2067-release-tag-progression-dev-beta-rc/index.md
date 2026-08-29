---
title: "RFD 2067: Release tags progress chronologically through dev, beta, rc, and release"
rfd: "2067"
state: published
scope: fabric-godot-packaging release tag convention
---

## Problem

Plain lexicographic sort, and `--sort=version:refname`, both give the
wrong cross-stage order for release tags. The `beta` string sorts
before `dev` alphabetically, even though `beta` comes later in the
pipeline. A bare `v0.1.0` also sorts before every suffixed
pre-release form, as a string prefix.

## Decision

Release tags for `fabric-godot-packaging` use semver pre-release
identifiers: `v<major>.<minor>.<patch>-<stage>.<N>` for a pre-release,
and the bare `v<major>.<minor>.<patch>` for a final release. The stage
runs `dev`, `beta`, `rc`, then release; the counter stays unpadded,
because ordering does not depend on it. Tags are always created in
forward chronological order, so `git tag --sort=creatordate` recovers
the correct progression. Neither plain lexicographic sort nor
`--sort=version:refname` gives the right cross-stage order: `beta`
sorts before `dev` alphabetically even though it comes later in the
pipeline, and bare `v0.1.0` sorts before every suffixed pre-release
form as a string prefix. The `version` workflow input maps directly to
`LOOP_PKG_VERSION`; any version containing a `-` builds as a
pre-release, and a bare version builds as a full release.

## References

- Full tag-format table, workflow examples, downsides, and rejected
  alternatives: `DETAILS.md`
- Original record:
  `decisions/20260624-release-tag-progression-dev-beta-rc.md`

## Related

- `rfd/2065-fabric-platform-central-elixir-burrito-casync`: a release
  workflow that produces tags under this convention.

## Detail

{{< include DETAILS.md >}}
