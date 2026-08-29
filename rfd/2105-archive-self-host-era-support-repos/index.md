---
title: "RFD 2105: Archive the self-host-era support repos and the empty stubs"
rfd: "2105"
state: published
scope: org-wide repository lifecycle
---

## Problem

`rfd/0089` moved the deployment target to Fly.io and archived the seven
quadlet repos and `infra`. It did not reach the repos that supported
those quadlets from one step away. A verification queue that targets
quadlets, a casync CDN, a scoop bucket, and a Burrito packaging repo
all stayed active with no live consumer.

Two repos also carry no content at all. `vulkan-video-godot` holds
0 KB. `steamdeck` holds 1 KB. Both appear in the inventory as if they
hold work.

An active repo with no consumer costs a reader time. The reader cannot
tell a parked repo from a live one.

## Decision

Archive six repos. Each one is tombstoned, not deleted, so the history
stays reachable.

- `fabric-container-verify`: the `rfd/0056` quadlet verification queue.
  Every quadlet it targets is archived by `rfd/0089`.
- `fabric-casync-central`: 0 KB. No content was ever pushed.
- `fabric-scoop-central`: the scoop bucket for the Windows demo of
  `godot-loop-slice`, which is archived.
- `fabric-platform-central`: the `rfd/0065` Burrito and casync
  packaging path.
- `vulkan-video-godot`: 0 KB.
- `steamdeck`: 1 KB.

`fabric-godot-assembly` is archived and then restored on the same day.
It stays active. The `gitassembly` recipe of `rfd/0019` still composes
the engine.

The dormant Lean cores stay active. `rfd/0057` makes them the
canonical proven reference, and a reference repo needs no recent push.

## References

- Per-repo record, the open inconsistency, and the counts: `DETAILS.md`
- `rfd/2062-repository-and-capability-inventory`: the inventory this
  decision updates.

## Related

- `rfd/2089-flyio-over-podman-quadlets`: archives the quadlets that
  these repos support.
- `rfd/2065-fabric-platform-central-elixir-burrito-casync`: the
  decision that `fabric-platform-central` carries.

## Detail

{{< include DETAILS.md >}}
