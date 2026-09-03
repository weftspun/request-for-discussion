# RFD 2110: H2o libriscv as a rivet actor

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

| Item | Value | | ---------------- |
------------------------------------------------------------ | | Port
| The `PORT` environment variable | | Readiness | The port must open
within 30 seconds, by default | | Shutdown | `SIGTERM`, then 25
seconds grace, then `SIGKILL`, by default | | Raw HTTP | Arrives under
`/request/*`, which the runner strips | | WebSocket | Clients use the
`rivet` subprotocol | | Per-actor config | CBOR `input`, with
`command`, `args`, and `env` |

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
