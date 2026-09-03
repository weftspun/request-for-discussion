# RFD 2107: Janet scripting over a c taskweft core

**State:** abandoned

## Decision

See `DETAILS.md` for the full argument.

## Problem

| Part | Job | Language | | ------------- |
------------------------------------------------------- | -------- | |
h2o | HTTP ingress and reverse proxy. Connection termination. | C | |
Janet | Routing glue, configuration parsing, dynamic scripting. |
Janet | | `libtaskweft` | HTN state-space search, graph traversal,
game state. | C | | Godot | Client and visualization frontend,
GDExtension and C++. | C++ | | FoundationDB | State, reached through
`libfdb_c`. | — |

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
