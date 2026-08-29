---
title: "RFD 2009: GHCR packages must be built by the repo that consumes them"
rfd: "2009"
state: published
scope: CI
---

## Problem

GitHub Container Registry ties package write access to the repository
whose `GITHUB_TOKEN` created the package. A cross-repo pull failed with
a 403 Forbidden error when the zone deploy tried to pull an image the
baker repo owned. A `workflow_run` trigger also fires only inside its
own repository, so a build workflow in one repo cannot trigger a deploy
in another.

## Decision

Each repository builds and publishes only the GHCR images its own deploy
uses directly. `multiplayer-fabric-baker` builds and owns
`godot-editor-double`. `multiplayer-fabric-zone` builds and owns
`multiplayer-fabric-zone-godot`, renamed from `godot-zone-double` to show
the new ownership. GitHub Container Registry ties package write access
to the repository whose `GITHUB_TOKEN` created the package, so a
cross-repo pull failed with 403 Forbidden when the zone deploy tried to
pull an image the baker repo owned. A `workflow_run` trigger fires only
inside its own repository, so the binary build workflow must live in the
same repo as the deploy it triggers.

## References

- Failure mode and follow-on consequences: `DETAILS.md`
- Original record: `decisions/20260506-ghcr-package-ownership-same-repo.md`

## Related

`rfd/2017-compiling-godot-engine/index.md` covers the engine build this
packaging wraps.

## Detail

{{< include DETAILS.md >}}
