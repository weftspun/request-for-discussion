# RFD 2044: Lean4 kernel cores flat c host adapters

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The hexagonal cores (`rfd/2028-hexagonal-core-ports-adapters`) hold
dependency-free domain logic that Godot, the Elixir backend, and a CLI
all bind. The team wants strong spec and proof guarantees on that
logic without linking a heavy language runtime into every host. The
`idtx-flow` repository already explores this shape in its
`LEAN_KERNELS_HOST_ADAPTERS` investigation.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
