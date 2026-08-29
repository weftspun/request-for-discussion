## Context and problem statement

RFD 2112 read the problem as a text field. `service-store/src/queen.c` had no client at
all when it was written, and the visible gap was that a player had nowhere to type. So the
document spent its length on the field: a decorator node is one block to the caret, an atom node
in ProseMirror can hold the caret and needs a plugin to correct it, and Meta tests the mobile
and IME paths at scale. Lexical was the right answer to that question.

The question aged badly. `queen` now has `serve`, `src/wt.c`, and `src/transport_tcp.c`; the
ward is entities with places, and a subscriber's slice is decided by an interest filter. The
field is the smallest part of a client for that. What matters is who decodes the packet, which
QUIC implementation carries it, and whether a player can stand in the zone rather than look at
it.

## What the browser client costs

Three costs, none of which is the field.

A second decoder. `client/src/cbor.js` is a JavaScript implementation of what the ward
publishes. Every wire change is now two changes that must agree, and nothing checks that they
do. `lean-entity-packet` models the packet in Lean with a `packet_golden.csv` of canonical
bytes, and the JavaScript is not held to those vectors.

A second transport. The browser's WebTransport is whatever the browser ships. `queen` terminates
QUIC with picoquic and picotls, and `transport-gateway` vendors both precisely so that one
implementation and one TLS library run on both ends. A browser client gives that up and replaces
it with compatibility, which is a thing you find out about in the field.

No XR. RFD 2085's setting is a ring station a player is inside. A browser field can show a
slash command and cannot put anybody anywhere.

## The parts already on the branch

`entities-godot` at `gyre` carries the client's whole stack as engine modules. This decision
adds no engine code; it selects.

| Module                       | What it provides                                 | What it replaces           |
| ---------------------------- | ------------------------------------------------ | -------------------------- |
| `modules/http3`              | `WebTransportPeer`, `quic_picoquic_backend.cpp`  | the browser's WebTransport |
| `modules/xr_grid`            | `XRGridEntityPacket`                             | `client/src/cbor.js`       |
| `modules/multiplayer_fabric` | `FabricMultiplayerPeer`, zone, snapshot, journal | `client/src/main.js` state |
| `modules/sqlite`             | a local store for what the client caches         | nothing; new               |

`FabricMultiplayerPeer` documents WebTransport as its example backend and notes that a peer must
open independent streams per packet, which WebTransport does. That is the same property
`service-store/CLAUDE.md` states from the server side: a datagram is one message and a
stream FIN is the boundary, so no framing layer exists on either end.

## The transport path

A player's client opens `WebTransportPeer.create_client(host, port, "/wt")` against the port
`queen serve` binds. `src/wt.c` terminates the session in the Queen's own process — no
`webtransportd`, per RFD 2047 and the rule in `CLAUDE.md`. Entity state arrives as
`XRGridEntityPacket`, 100 bytes, delta coded, filtered by interest before it is sent.

The client is therefore a subscriber and nothing more privileged. `Weft.Authority` decides which
controller drives an avatar, the ward checks a command's rebac relations on receipt, and a
native client has no more standing than a browser one did.

## What happens to the web client

`service-store/client` is not deleted by this document. It is four source files, two
Playwright specs, and three npm dependencies, and none of it is on the CI path — `ci/inside.sh`
runs `queen` and never runs npm. It can be removed in a change of its own, which is where the
argument about whether to keep a browser build as a fallback belongs.

What this document settles is that it is not the client. Nothing new is written against it, and
the slash command surface is built as a Godot `Control` against the modules above.

## Hazards

The build is the cost. A native client is compiled per platform from an engine fork, and a
browser client is served. `fabric-godot-assembly` and `godot-images` exist for exactly this, so
the cost is known rather than new, but it is real and it is paid on every platform.

The branch is a fork of a fork. `gyre` sits on top of `multiplayer-fabric`, which merges
fourteen feature branches on top of Godot's `master`. A client pinned there inherits that merge
surface. The manifest states the branch, which is the minimum; nothing here pins a commit.

The field regresses before it improves. RFD 2112's field works today. A `Control` that shows a
parameter as an inline block has to be written, and the first version of it will be worse than
the Lexical one. That is accepted for the same reason as the build cost: the field was never the
part that determined whether this client was right.

## Consequences

RFD 2112 is abandoned. `service-store/client` — Lexical, esbuild, the Playwright specs and
the JavaScript decoder — stops being the client. Removing it is its own change in its own
repository and is not assumed by this document.

The cost is a build. A browser client is served; a native client is compiled per platform from
an engine fork, which is slower to produce and heavier to distribute. That is accepted, because
the alternative was paying for a second decoder and a second transport forever to avoid paying
for a build once.
