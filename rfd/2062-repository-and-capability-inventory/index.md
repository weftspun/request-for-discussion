---
title: "RFD 2062: Repository and capability inventory for the multiplayer fabric"
rfd: "2062"
state: published
scope: org-wide repository and capability index
---

## Problem

The landing page carried the full repository list, a
capability-to-branch table, and a deployment description. Those facts
already had homes elsewhere, so the landing page drifted every time a
fact changed somewhere else. No single record owned the org-wide
repository and capability inventory.

## Decision

This record is the one place that owns the org-wide repository and
capability inventory. The landing page used to carry the full
repository list, a capability-to-branch table, and a deployment
description; those facts already have homes elsewhere, so the landing
page drifted every time a fact changed. The landing page now links
here instead of restating the list. Each capability maps to the
engine feature branch in `godot` that implements it, and its tier
follows the feature-classification record. The inventory spans the
full `v-sekai-multiplayer-fabric` org plus the repos still on
`V-Sekai-fire`, grouped by area: engine, runtime services, service
images, rendering and shaders, spatial and verification, tooling,
infrastructure, and archived repos. Keeping one page as the source of
truth costs hand maintenance, but it stops the drift a second copy
caused.

## References

- Full capability table and the complete repository listing by area:
  `DETAILS.md`
- Original record:
  `decisions/20260613-repository-and-capability-inventory.md`
- Org: [v-sekai-multiplayer-fabric](https://github.com/v-sekai-multiplayer-fabric)

## Related

- `rfd/2057-vertical-slice-repository-map`: the narrower map of just
  the loot-action vertical slice.
- `rfd/2018-feature-classification-poc-baseline-stretch`: the tier
  classification each capability follows.

## Detail

{{< include DETAILS.md >}}
