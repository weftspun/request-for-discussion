# RFD 1099: One cheat sheet, every operator command, machine plus folder plus command

**State:** published
**Scope:** every operator script under `scripts/`, on both the Surface and the DGX

## Decision

One file, kept in sync both ways: DGX edits push to the Surface with
`bash scripts/sync-changes-to-pc.sh --retry-until-complete`, which
also mirrors to the Surface desktop automatically when this file
itself changed. Every entry states machine, folder, command, and
what the command does, in that order. A dedicated section 21 names
every deprecated command and its replacement, so an old note does
not silently resurface. Section 22 states the same four-part format
as the rule agents themselves must follow when giving a command.
Secrets never appear here: API keys and tokens live only in `.env`
or local MCP config.

See `DETAILS.md` for the full inventory, all 22 sections, from repo
paths and SSH through the spatial fabric, the Sneeze engine, and
deprecated commands.

## Problem

Two machines, two roles, and roughly twenty separate operational
areas (sync, the dev server, the DGX API, model smoke tests, XR
logging, the spatial fabric, and more) each carry their own start,
stop, and verify commands. An agent or a developer needs one place
naming which machine, which folder, and which exact command, not a
memory of which of a dozen scripts is current.

## Related

RFD 1086 gives the Surface/DGX topology this cheat sheet's sync
commands depend on. RFD 1095 and RFD 1100 give the XR voice stack
and the spatial fabric this sheet's own section 19 also covers. RFD
1119 gives the general hardware rule; this sheet documents one
team's own reference deployment against that rule, not a
requirement for running the project elsewhere.
