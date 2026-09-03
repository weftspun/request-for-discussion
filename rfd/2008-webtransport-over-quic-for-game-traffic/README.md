# RFD 2008: Webtransport over quic for game traffic

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The zone server needs low-latency bidirectional communication between
clients and the Godot game server. HTTP/1.1 and WebSocket both run
over TCP, which head-of-line blocks on packet loss and degrades
real-time game state.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
