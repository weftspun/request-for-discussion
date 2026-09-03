# RFD 2123: A second webtransport implementation

**State:** moved

## Decision

See `DETAILS.md` for the full argument.

## Problem

One disagreement about the contract, and three integration defects
found while building. The distinction matters, because only the first
is the thing a second implementation exists to produce: it is a claim
the fabric makes about its own wire, contradicted by two stacks that
share no code. The other three are properties of the libraries this
pair happens to use, and a third implementation on a fourth stack
would not have found them.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
