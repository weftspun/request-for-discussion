# RFD 2084: Zstd compression for zone state

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

mas-bandwidth/fps assumes 10x bandwidth reduction via delta
compression against a baseline (RFD 2002). zstd provides
general-purpose compression that complements delta compression:

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
