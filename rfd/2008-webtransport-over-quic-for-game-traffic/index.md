---
title: "RFD 2008: Use WebTransport over QUIC for game traffic"
rfd: "2008"
state: published
scope: gateway/zone-server
---

## Problem

TCP-based transports, including HTTP/1.1 and WebSocket, suffer
head-of-line blocking on packet loss. This blocking degraded real-time
game state each time a packet was lost. The project needed a transport
for game traffic that did not carry this problem.

## Decision

All game traffic uses WebTransport, which runs HTTP/3 over QUIC. Clients
connect to the Elixir gateway on UDP port 443. The gateway proxies the
traffic into the Godot zone server on UDP port 7443. QUIC runs over UDP,
so it does not suffer the TCP head-of-line blocking that HTTP/1.1 and
WebSocket both carry on packet loss. That blocking was degrading
real-time game state under loss, which drove this choice over TCP-based
transports.

Datagrams carry game-state messages. Streams are avoided for ping/pong,
because a stream's half-close deadlock (the client must close its write
side before the server's response fires) is a bad fit for a fast
round trip.

## References

- Deployment consequences (Fly.io binding, Cloudflare proxy limit): `DETAILS.md`
- Original record: `decisions/20260501-webtransport-over-quic-for-game-traffic.md`

## Related

`rfd/2010-maglev-cycle-1-gateway-handshake/index.md` exercises this
transport from a real Godot client.

## Detail

{{< include DETAILS.md >}}
