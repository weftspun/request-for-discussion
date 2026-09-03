# RFD 2112: Lexical for the slash command interface

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`fabric-store-domain/src/queen.c` is the Queen of the Gyre. Its
`main()` takes `play|check <cycles> [seed] [sparks]`, founds a ward,
runs the cycles, prints a chronicle, and exits. There is no socket, no
server, and no instance that outlives the run. The README says the
same thing from the other side: the game has no renderer, no client,
and no engine, and what you can see of it is what you can `SELECT`.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
