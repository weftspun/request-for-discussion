# RFD 2067: Release tag progression dev beta rc

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`fabric-godot-packaging` produces native Linux packages, a Podman
quadlet package, an Android APK, and Windows MSIXes for the
loot-action loop-slice. All build workflows are manually dispatched
(`workflow_dispatch`) and accept a `version` input. Until now there
was no defined convention for what version strings to use at each
stage of a build's lifecycle, no incrementable counter within a stage,
and no agreed way to list tags in progression order.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
