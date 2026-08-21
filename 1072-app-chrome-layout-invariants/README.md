# RFD 1072: App chrome layout invariants

**State:** committed
**Scope:** `App.jsx`, `App.css`, `TaskProgressBar.{jsx,css}`,
`src/pages/Appearance*`, `BottomDisplayMenu.jsx`

## Problem

The header, the task-progress bar, and the two side rails share one
coordinate space. Three regressions kept recurring: a fixed task bar
drifting over the header, an asymmetric collapsed-rail icon column,
and a side panel raised above the header in z-index instead of
repositioned.

## Decision

The task-progress bar stays in document flow, after
`.scene-controls-row`, never `position: fixed` over the header. The
right rail (`.weftspun-sidebar`) reads its top offset from a measured
`--app-content-top`, set on `:root`, never redefined on `.app`. A
fixed pixel top, or a chrome-calc top without that measured
variable, both regress this.

Both collapsed rails (`.sidebar`, `.weftspun-sidebar`) share one set
of `--collapsed-rail-*` tokens for width, icon size, gap, and
padding, defined once on `.app`. Neither rail takes a per-side
override.

Three z-index layers stack in one order: side panels at 998
(`--z-side-panel`), the header at 1001, the scene controls row at
1002. A side panel overlapping the header gets a `top` fix, never a
z-index raise past 998.

See `DETAILS.md` for the full token table, the forbidden-change
list, and the visual-check steps each rule's own checklist named.

## Related

RFD 1001 gives the shell these invariants live inside.
