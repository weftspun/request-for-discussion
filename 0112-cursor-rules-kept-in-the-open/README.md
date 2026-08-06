# RFD 0112: The Cursor rules, kept in the open

**State:** discussion
**Scope:** `rules/`

## Problem

`rules/` holds 34 raw `.mdc` files, moved unfiltered from
weftspun-3d-studio's own `.cursor/rules/` directory. No RFD covers
the set. RFD 0000's DRY policy says an RFD points to its source and
does not copy it. Each of these files is itself already a copy, kept
in sync by hand with the file of the same name in the app
repository.

One file, `weftspun-moat-protected.mdc`, restates RFD 0106 in a more
raw form, and names revenue mechanisms RFD 0106 leaves out on
purpose. A second file, `dgx-sync-reminder.mdc`, names a private
machine's local IP address and file paths.

## Decision

This repository publishes its operating rules, not only its
architecture decisions. Keep `rules/` as a full, unfiltered copy, by
explicit choice. This trades the usual DRY point-to-source rule for
transparency, in this one named case. A reader gains the same agent
instructions the project's own maintainer runs under.

`weftspun-moat-protected.mdc` and `dgx-sync-reminder.mdc` stay too,
unedited. Neither file is wrong. RFD 0106 gives the public-safe
summary. This file gives the working detail behind it. See
`DETAILS.md` for the per-file table: which rules guard a feature an
existing RFD already covers, which are pure process with no matching
RFD, and which restate a published RFD.

## Related

RFD 0000 names the DRY policy this RFD sets aside for this
directory. RFD 0106 gives the public-safe restatement of
`weftspun-moat-protected.mdc`. RFD 0113 is the one new RFD this
table's own review produced.
