---
title: "RFD 2106: Split the archive into its own repository"
rfd: "2106"
state: published
scope: manuals repository layout, archived records
---

## Problem

The manuals repository holds live design records and dead ones in the
same tree. `_archive/decisions/` holds 26 MADR records that are
rejected or superseded. A leading underscore keeps Quarto from
rendering them, so the site hides them, and the repository still
carries them.

Two RFDs are superseded and still render as current. `rfd/0089`
supersedes `rfd/0061` on the deployment target. `rfd/0011` is
superseded on the observability stack. A reader who opens either one
reads a dead design with no marking on the page.

Hiding a record from the site is not the same as retiring it. The
repository needs one place for retired records.

## Decision

Create `multiplayer-fabric-archive`, a public repository in this
organization. It is the standing home for retired records. It holds
plain Markdown, with no Quarto site, no build, and no checks, because
archived content does not change.

Move `_archive/`, its attachments, `rfd/0011`, and `rfd/0061` there.
Delete them here. Keep no pointer stub, per `rfd/2000-conventions`.

The archive repository carries the manuals history up to the split, so
each moved file keeps every commit that touched it at its original
path.

`rfd/0011` and `rfd/0061` keep their numbers. This repository does not
reuse a number after a move.

## References

- The link repairs a move forces, and the record of what moved:
  `DETAILS.md`
- `v-sekai-multiplayer-fabric/multiplayer-fabric-archive`

## Related

- `rfd/2000-conventions`: the no-pointer-stub rule this follows.
- `rfd/2071-yagni-times-structure-to-need`: the rule that sends a
  superseded record to the archive.
- `rfd/2062-repository-and-capability-inventory`: lists the new
  repository.

## Detail

{{< include DETAILS.md >}}
