# RFD 2004: Castspell libgodot sandbox runtime scope

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`rfd/2001-zonefabric-roadmap-vs-mas-bandwidth-fps/index.md`, item 6,
commits to scoping how much of `libriscv`/`godot-sandbox`'s API
surface CastSpell effects actually need. This RFD is the detail that
item pointed to. It resolves the scoping question and decides to embed
a real, headless `libgodot` instance per zone instead of
reimplementing `godot-sandbox`'s narrow API. It also records a real
spike that proved the approach boots correctly.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
