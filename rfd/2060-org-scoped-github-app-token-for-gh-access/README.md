# RFD 2060: Org scoped github app token for gh access

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Repository operations against
[`v-sekai-multiplayer-fabric`](https://github.com/v-sekai-multiplayer-fabric)
— archiving, renaming, pushing, editing settings — run through `gh`
from a working environment. `gh` was authenticated with a personal
OAuth token (`gho_`, scopes `gist, read:org, repo, workflow`). The
`repo` scope is not org-scoped: it grants read/write/**admin/delete**
on every repository the personal account can reach, across every org
and every private repo. A mistyped owner in a destructive command, or

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
