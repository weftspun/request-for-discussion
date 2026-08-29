## The child contract

| Item             | Value                                                        |
| ---------------- | ------------------------------------------------------------ |
| Port             | The `PORT` environment variable                              |
| Readiness        | The port must open within 30 seconds, by default             |
| Shutdown         | `SIGTERM`, then 25 seconds grace, then `SIGKILL`, by default |
| Raw HTTP         | Arrives under `/request/*`, which the runner strips          |
| WebSocket        | Clients use the `rivet` subprotocol                          |
| Per-actor config | CBOR `input`, with `command`, `args`, and `env`              |

The engine calls `POST /api/rivet/start` on `RIVET_PORT`. That is the
runner's interface, not the child's. The child sees a plain port.

The `rivet` subprotocol is the one non-obvious requirement. h2o's
WebSocket upgrade path must accept it.

## What one process per room deletes

The old host held many zones in one process. Rivet holds one room per
process, so the machinery for the first case has no subject.

| Record     | Status under this decision                                   |
| ---------- | ------------------------------------------------------------ |
| `rfd/0072` | Unnecessary. Worker dispatch across zones in one process     |
| `rfd/0082` | Unnecessary. Keyspace design for many zones in one server    |
| `rfd/0086` | Unnecessary. The engine owns placement, so gossip has no job |
| `rfd/0080` | Narrows. Slotmap storage for one room's entities             |
| `rfd/0094` | Applies. The CBOR input names the guest, as this record uses |
| `rfd/0092` | Applies. ReBAC still gates which principal loads which guest |

Fault isolation improves as a side effect. A guest fault kills one
room's process, not every room. `rfd/0095` wanted that from Bubblewrap,
and process-per-actor supplies it.

## The actor input, from `container-runner/src/input.rs`

Four optional fields, CBOR-encoded per the RivetKit convention:

| Field     | Type                     | Meaning                                         |
| --------- | ------------------------ | ----------------------------------------------- |
| `command` | `Option<Vec<String>>`    | Replaces the CLI command template entirely      |
| `args`    | `Vec<String>`            | Appended after the command template             |
| `env`     | `HashMap<String,String>` | Extra environment variables for the child       |
| `port`    | `Option<u16>`            | The child's local port, also exported as `PORT` |

Anything omitted falls back to the CLI template, which is
`rivet-container-runner -- <command...>`. An omitted `port` falls back to
the runner's `--child-port`.

Two properties matter for a zone. The decoded input is also the actor's
persisted state, so a woken actor restores the same launch spec. Unknown
fields are ignored rather than rejected, so adding a field does not break
actors that wake on an older binary.

So a room's scene, its guest, and its tuning all travel in the actor
input. No zone-side registry is needed.

## Packaging

`container-runner/Dockerfile.release` builds a standalone linux/amd64
`rivet-container-runner` binary, described in its own comments as the
artifact users curl into their Dockerfile. Extract it with a build
targeting `artifact`, and the output is one x86_64 ELF.

The zone image is therefore the engine build plus that binary as the
entrypoint, with the engine command after `--`. `godot-images` already
publishes engine images to GHCR, so this adds an entrypoint rather than
a pipeline.

## The pinned engine, verified

The tag `v2026.06.27.1907-multiplayer-fabric` is annotated, and it
resolves to commit `2cecde75`. Its `version.py` reports major 4, minor
7, patch 0, status beta.

`fabric-godot-core` publishes no GitHub releases, so the tag page offers
source archives only. A build step is required, and `godot-images`
already publishes engine images to GHCR. `rfd/0009` puts that build in
the consuming repository.

Modules present at that tag, checked against the tree:

| Module                                           | Role                           |
| ------------------------------------------------ | ------------------------------ |
| `sandbox`                                        | libriscv guest execution       |
| `http3`                                          | WebTransport over QUIC         |
| `multiplayer_fabric`, `multiplayer_fabric_asset` | The zone and its assets        |
| `xr_grid`                                        | Presence, head and hand orbs   |
| `openxr`, `webxr`                                | XR on desktop and on web       |
| `cassie`, `speech`, `tinyexr`                    | Authoring, voice, HDR textures |

One build therefore serves three roles: the client, the zone server, and
the guest host. No h2o, no Janet, and no separate guest runtime.

No `resonance` module appears at this tag. `rfd/0022` describes spatial
audio through a patched Resonance Audio, and whether that arrives as
core changes rather than a module is unverified. Check it before you
rely on spatial audio.

## A second child kind, kept in reserve

`container-runner` hosts any process that listens on `PORT`, and the
CBOR `command` field selects the binary. So a second child kind costs no
architecture, only a build.

The candidate is h2o with libriscv in C. Its one advantage is memory per
process, because a headless Godot process is larger than a small C
binary. With one process per room, that difference multiplies by the
room count.

Neither figure is measured here. Measure the resident size of the
headless build, divide the machine's memory by it, and compare the
result to the expected room count. Build the C child only if that
comparison fails.

`rfd/0095` found one runtime serving two unlike guest classes, and it
split them with a domain ABI and Bubblewrap. Process-per-actor splits
them without either mechanism.

## The transport, settled by the runner's source

`container-runner` is TCP-only. Forcing HTTP/3 through it is not
possible, and four facts in its source say so.

| Fact                                                                      | File           |
| ------------------------------------------------------------------------- | -------------- |
| Forwards to `http://127.0.0.1:{child_port}` and the `ws://` form          | `src/proxy.rs` |
| Readiness is `TcpStream::connect((Ipv4Addr::LOCALHOST, child_port))`      | `src/child.rs` |
| "HTTP/WebSocket (arriving over Rivet's tunnel) to the child's local port" | `src/main.rs`  |
| No `udp`, `quic`, `http3`, or `h2` appears in the runner source           | all four files |

A UDP-only child never reports ready, because readiness is a TCP
connect. `TCP_NODELAY` also does not appear in the runner source, so
Nagle is unmitigated there.

Rivet's own gateway has no QUIC yet, and WebTransport is planned rather
than shipped.

### Two sockets in one child

The zone process listens twice.

- A TCP port satisfies Rivet's contract and carries the control plane.
  Rivet proxies it, readiness passes, and the actor lifecycle works.
- A UDP port carries game traffic outside Rivet's tunnel, with the
  engine's `http3` picoquic module on it. The host maps that port.

One process, one actor, two sockets. Rivet never touches the pose
stream, so `rfd/0008`, `rfd/0023`, `rfd/0049`, `rfd/0058`, and
`rfd/0088` all stand.

### What that shape costs

Rivet's gateway does not route the UDP port, so a client needs the host
address and port. Something must publish it, and that is a zone
directory. `rfd/0109` left the Uro role optional, and this design
requires it.

### If the pose stream runs on WebSocket instead

That is workable and worse. Three mitigations are mandatory: set
`TCP_NODELAY` on the child socket, send one latest-pose frame per tick,
and keep the frame at the 100 bytes of `rfd/0053`.

It stays wrong under loss. Head-of-line blocking costs about one round
trip, which at a 50 ms RTT delays roughly three ticks and then delivers
stale poses. WebSocket also gives no way to discard queued frames, so
`rfd/0049`'s unreliable state channel has no transport.

### Measure before building

`container-runner/examples/e2e-test/load-test.mjs` opens WebSockets
through the gateway, pings, and reports `p50`, `p95`, `p99`, and `max`
in milliseconds. Run it against a Godot child and compare `p95` to the
15.6 ms tick.

`rfd/0096` states the rule this follows. Ranking transports from
documentation produces wrong answers.

## Cost and risk

One OS process per room is heavier than one BEAM process per room. The
room count decides whether that matters, and this record does not know
it.

Rivet adds a Rust engine to operate. That is a dependency to run, not a
language to write in, because the zone is C.

`pegboard-gateway` and `pegboard-gateway2` both exist in the
repository, so that layer changes actively. Pin a version.

## What stays open from RFD 2109

**Where Elixir and Uro sit.** Identity and the room directory still
need a home. Rivet has namespaces and its own API, and neither
replaces an identity service. `rfd/0090` is Uro's live release shape.

**Interest management.** `lean-interest-mgmt` is still the only lever
on the 256 kbps figure of `rfd/0100`.

**Server authority.** A zone process that runs the simulation can be
authoritative, unlike the relay of `rfd/0109`. So `rfd/0046` returns as
reachable rather than ruled out.
