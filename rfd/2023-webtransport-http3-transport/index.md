---
title: "RFD 2023: WebTransport over HTTP/3 transport"
rfd: "2023"
state: published
scope: engine network transport (modules/http3)
---

## Problem

The stack needs one client/server transport that carries reliable
control messages and high-rate unreliable state, over one connection,
on both native and web clients. The standard `MultiplayerPeer`
transports, ENet, WebSocket, and WebRTC, give none of this
combination. None of them give one connection with both datagram and
stream semantics across native and browser clients.

## Decision

The stack needs one client/server transport that carries reliable
control messages and high-rate unreliable state over a single
connection, on both native and web clients. The engine provides this
through `modules/http3` (`feat/module-http3`): WebTransport over
HTTP/3 and QUIC, with a native picoquic backend and a web/wasm
backend, exposed as the `HTTP3Client`, `QUICClient`, `QUICServer`, and
`WebTransportPeer` classes. One QUIC connection carries reliable
streams and unreliable datagrams together, so control messages and
high-rate state share a connection instead of two. This replaces
standard `MultiplayerPeer` transports (ENet, WebSocket, WebRTC), none
of which give one connection with both datagram and stream semantics
across native and browser clients.

## References

- Full context, decision drivers, considered options, consequences,
  and confirmation steps: `DETAILS.md`
- Original record:
  `decisions/20260606-webtransport-http3-transport.md`
- `modules/http3`: `quic_picoquic_backend.{cpp,h}`,
  `quic_web_backend.cpp`, `quic_web_glue.js`, `http3_client.{cpp,h}`,
  `quic_client.{cpp,h}`, `quic_server.h`
- Demos: `modules/http3/demo/wt_client_test.gd`, `wt_server_demo.gd`,
  `wt_browser_test.html`
- `lean/http3/PollingTermination.lean`

## Related

- `rfd/2020-pin-engine-to-frozen-godot-4-7`

## Detail

{{< include DETAILS.md >}}
