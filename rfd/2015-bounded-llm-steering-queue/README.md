# RFD 2015: Bounded llm steering queue

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

We steer an LLM by appending tasks to a queue as we go — this manuals
session is the canonical example, with dozens of incremental requests.
An unbounded queue overflows two scarce resources: the operator's
personal context (you lose track of what is pending versus done) and
the model's context window. How do we keep steering open-ended without
overflowing either?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
