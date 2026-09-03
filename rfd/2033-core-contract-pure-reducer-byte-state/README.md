# RFD 2033: Core contract pure reducer byte state

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Every hexagonal core (`rfd/2028-hexagonal-core-ports-adapters`) needs
to be replayable, snapshot-able, fixture-testable, and
transport-agnostic. A core that hides mutable state behind methods
defeats all four.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
