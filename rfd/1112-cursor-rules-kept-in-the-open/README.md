# RFD 1112: The Cursor rules, kept in the open

**State:** discussion
**Scope:** `rules/`

## Decision

A guard rule's design belongs in an RFD, not a raw `.mdc` file. Each
guard rule converts, one at a time: write the RFD it names, then
delete the `.mdc`, its content preserved, not duplicated. Once
converted, `rules/` no longer holds it.

A process rule stays. It names no product decision, so no RFD holds
it, and this repository publishes its operating workflow anyway, by
explicit choice, trading the usual DRY point-to-source rule for
transparency. `weftspun-moat-protected.mdc` and
`dgx-sync-reminder.mdc` stay too, unedited: RFD 1106 gives the
public-safe summary of the first, and this file gives the working
detail behind it, kept by the same transparency choice. See
`DETAILS.md` for the current per-file table.

## Problem

`rules/` held 34 raw `.mdc` files, moved unfiltered from
weftspun-3d-studio's own `.cursor/rules/` directory. No RFD covered
the set. RFD 1000's DRY policy says an RFD points to its source and
does not copy it. Each of these files was itself already a copy,
kept in sync by hand with the file of the same name in the app
repository. Twenty files remain, after the guard rules converted.

One file, `weftspun-moat-protected.mdc`, restates RFD 1106 in a more
raw form, and names revenue mechanisms RFD 1106 leaves out on
purpose. A second file, `dgx-sync-reminder.mdc`, names a private
machine's local IP address and file paths.

## Related

RFD 1000 names the DRY policy this RFD sets aside for a process
rule, and restores once a guard rule converts. RFD 1106 gives the
public-safe restatement of `weftspun-moat-protected.mdc`.
