---
title: "RFD 2122: The client is native, from entities-godot's gyre branch"
rfd: "2122"
state: published
scope: the Queen of the Gyre, and what a player runs to reach her
---

## Problem

RFD 2112 put the Queen's client in a browser and chose Lexical for the slash command field, which was the hard half and was built. The field was the wrong thing to optimise for.

A browser client is a second implementation of everything below that field. `client/src/cbor.js`
decodes what the ward publishes in a language sharing nothing with the decoder the rest of the fabric
uses; it reaches the ward over a WebTransport stack merely compatible with the ward's; it carries npm,
esbuild, and Playwright, which nothing else here needs; and it cannot enter XR, the point of the setting.

## Decision

The client is a Godot build from `entities-godot`, branch `gyre` — one of five entries in the
`fabric` manifest's `default.xml` that track something other than `main`.

The branch carries the parts already: `modules/http3` gives `WebTransportPeer` over the same
picoquic backend `queen`'s `src/wt.c` terminates and `transport-gateway` vendors, `modules/xr_grid`
gives the 100-byte `XRGridEntityPacket` that `lean-entity-packet` specifies, and
`modules/multiplayer_fabric` gives `FabricMultiplayerPeer`. This adds no engine code; it decides
which client is the client. `DETAILS.md` has the module mapping.

The slash command field becomes a `Control`, so RFD 2112's hard half stops being hard: a caret in a
`contenteditable` is a browser problem, and there is no browser. The ward does not change — `queen
serve` already speaks WebTransport. What changes is who connects.

## References

- RFD 2112 chose the browser client and is abandoned; RFD 2085 holds the setting; RFD 2111 sets the words transport layer and service; RFD 2047 is why the Queen terminates QUIC herself
- `lean-entity-packet` specifies the 100-byte packet both ends now share
- The module mapping, the transport path, and what happens to the web client: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
