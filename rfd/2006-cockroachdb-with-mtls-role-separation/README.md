# RFD 2006: Cockroachdb with mtls role separation

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The stack needs a relational database reachable by the Elixir gateway
and the Phoenix zone backend. It must support schema migrations (DDL)
separately from application queries (DML) to limit blast radius if
application credentials are compromised.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
