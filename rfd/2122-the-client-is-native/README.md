# RFD 2122: The client is native

**State:** abandoned

## Decision

See `DETAILS.md` for the full argument.

## Problem

RFD 2112 read the problem as a text field. `service-store/src/queen.c`
had no client at all when it was written, and the visible gap was that
a player had nowhere to type. So the document spent its length on the
field: a decorator node is one block to the caret, an atom node in
ProseMirror can hold the caret and needs a plugin to correct it, and
Meta tests the mobile and IME paths at scale. Lexical was the right
answer to that question.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
