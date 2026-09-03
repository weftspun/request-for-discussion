# RFD 2028: Hexagonal core ports adapters

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Components in the stack span several languages (C, C++, Python,
Elixir, GDScript), run as separate processes, and each binds to
hardware, a GPU, the network, or an engine runtime. A component has to
stay testable without its device, replaceable without a rewrite of its
callers, and composable with components written in another language. A
shared monolith or a single in-memory object model does not hold
across those boundaries.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
