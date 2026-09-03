# RFD 2003: Castspell sandbox package and manifest encoding

**State:** abandoned

## Decision

See `DETAILS.md` for the full argument.

## Problem

`rfd/2001-zonefabric-roadmap-vs-mas-bandwidth-fps/index.md`, item 4,
commits CastSpell's effect step to a sandboxed `libriscv` package.
This RFD is the detail that item pointed to. It settles three things.
The package stays a single `.elf` file. Its manifest is CBOR-LD. Its
runtime FFI boundary is the same bitpacked struct format `RFD 2010`
already uses for the zone tick.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
