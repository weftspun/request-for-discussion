# RFD 2058: Webtransport persistent framed stream

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The fabric's reliability classes ([fabric
channels](../2049-fabric-channels-as-reliability-classes/README.md))
run over ENet for the local slice. WebTransport carries the same
classes for the browser and Quest paths over one QUIC connection per
client. The picoquic WebTransport server goes silent within seconds
once four or more sessions connect: some clients never finish the
extended-CONNECT handshake, and once a few sessions are open every
client stops sending and receiving while the network thread stays
alive in `poll()`.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
