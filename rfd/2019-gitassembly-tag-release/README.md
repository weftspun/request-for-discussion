# RFD 2019: Gitassembly tag release

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The `merge` repo's `gitassembly` recipe builds the engine by merging
feature branches (`feat/module-xr-grid`, `feat/module-cassie`,
`feat/module-http3`, and the rest) onto the frozen Godot 4.7 base. The
base is pinned, but the feature branch tips are not: an assembly run
today and one next week can merge different branch SHAs and produce a
different engine. The cold-boot dependencies refer to the branches by
name, so "assemble these branches" alone is not a reproducible
artifact. What is the shareable, fixed reference for the assembled
engine?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
