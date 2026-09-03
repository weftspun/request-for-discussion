# RFD 2021: Require pr and merge queue on main

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The `manuals` repo had no branch protection on `main`. Changes landed
by pushing directly or by manually merging pull requests, with no
guarantee that a PR's checks ran against the tip it was about to join.
Two PRs can each pass against an older `main` and then conflict or
break the Quarto build once both land. How should changes reach `main`
so that every merge is reviewable and tested against the tip it will
actually join?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
