# RFD 2036: Forward renderer baked light

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The mobile tile renderer rations bandwidth across file, memory, and
network IO, and deferred rendering competes for it. The slice needs
predictable frame cost regardless of light count.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
