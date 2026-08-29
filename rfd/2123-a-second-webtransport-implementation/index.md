---
title: "RFD 2123: A second WebTransport implementation, and the names that make room for it"
rfd: "2123"
state: discussion
scope: the WebTransport contract, who implements it, and what the transport repositories are called
---

## Problem

The fabric states its wire in `contract-wt`, `contract-entity-packet`, `contract-connection-fsm`
and `contract-http3-queue`, and implements it once. RFD 2088 chose that: "Client and server share
one proven QUIC stack instead of two different, independently verified ones." `transport-gateway`,
`transport-ingest` and the engine's `modules/http3` all vendor picoquic and picotls, so both ends
of every session run the same code.

That buys interoperability by construction and gives up the check. A wire implemented once
describes the program that implements it, and nothing establishes that the specification is
implementable from the specification. Every assumption both ends share passes every test the pair
can run. `contract-wt` already makes this argument for the engine's H3 stack and acts on it in
aioquic; nothing makes it for the transport layer.

## Decision

**A second implementation, on a stack that shares no code with the first.**
`transport-gateway-python` and `transport-ingest-python` terminate the same contract on `aioquic`,
which implements QUIC and TLS 1.3 in Python from the RFCs, and hand off over the iceoryx2 ring.
Khronos ratifies against two independent implementations for this reason.

Three stacks were considered and the choice turns on what each shares with the first. Binding
picoquic from Python was rejected because both ends would then run the same QUIC and the same TLS,
so the second implementation would test the binding rather than the contract. h2o was rejected
because its WebTransport is an unmerged pull request stacked on another unmerged pull request,
with tests unchecked, against an HTTP/3 stack h2o calls experimental; its QUIC is quicly and would
have qualified otherwise. `pywebtransport` shipped first here and was replaced: it refuses an EC
private key, and `contract-wt` records the Godot demo server generating a fresh P-256 certificate
on every run. `DETAILS.md` has the measurements.

**It carries no player traffic.** `transport-gateway-c`'s `PACKET_PATH.md` measures a scripting
runtime at 5.70 M/s against a 15 M/s bar, and 117.8 ns per runtime crossing against a 66.7 ns
per-packet budget. Those numbers stand and they are why policy lives in an interactor rather than
in the packet path. The Python pair produces agreement or disagreement, and no throughput claim
goes in a record without a measurement in `data/measurements/`.

**The language is what tells the four repositories apart.** `transport-gateway` becomes
`transport-gateway-c` and `transport-ingest` becomes `transport-ingest-c`. Two implementations of
one contract are distinguished only by how they are built, so RFD 2111's preference for names that
say what a thing does cannot separate them, and `transport-picoquic` is the precedent for naming a
transport repository after its stack. Naming the language rather than the library also survives a
change of library, which this record has already exercised: the Python pair moved from
`pywebtransport` to `aioquic` before it merged and neither name moved. Neither pair keeps the
unqualified name, because the unqualified name implies the other is a variant.

**The codec is emitted, never retyped.** `contract-entity-packet` gains a Python emitter beside
`EntityPacket/EmitC.lean`, so `lake exe packet_emit` writes the C header, the Python module and the
64 golden vectors from one run. A second implementation that reads the layout off the first tests
whether two people can copy a table.

**The ring is reached through the `iceoryx2` wheel.** The C repositories dlopen iceoryx2 through a
dispatch table generated from `iceoryx2.sigs`, so that "the harness builds on a machine that has
never seen iceoryx2" and because "iceoryx2 is Rust, and weft writes no Rust." A prebuilt wheel is a
runtime artifact rather than a build-graph edge and adds no second `.sigs` file. Bus access stays
behind one module in each repository so the choice is reversible.

**`contract-wt` stays where it is.** It runs the same `aioquic` this pair now runs, and it checks a
different subject: the engine's `modules/http3` as a client, where these check the transport layer
as a server. One Python stack in two places is less to keep current than two, and its roster client
is what caught `WebTransportPeer` tracking clients in one bool. What it does not give is a third
opinion, so a fault inside `aioquic` itself would go unseen by both.

## Consequences

The implementation contradicted one claim the fabric makes about its own wire before it carried a
byte of real traffic, which is the argument for it stated as evidence rather than as principle.
`transport-fanout` caps a slice at 64 records and calls 6400 bytes "comfortably inside one
message"; two stacks sharing no code put the limit at 11 records, and `datasource-queen`'s own
`WT_MTU_MAX` agrees with them rather than with the comment.

That is one finding, not a pile of them, and the count is worth keeping honest. Building the pair
also surfaced three defects in the libraries it uses — an EC key a stack would not load, a
subscriber buffer that drops the oldest of three sends, a datagram queue that wedges on an
oversized send. Those are real and cost real time, and a third implementation on a fourth stack
would not have found any of them. `DETAILS.md` keeps them apart for that reason.

The cost is a fourth transport repository and a second wire reader to keep in step. RFD 2122 named
that cost exactly — "every wire change is now two changes that must agree, and nothing checks that
they do" — and rejected a second implementation carrying player traffic for it. Checking that they
agree is what these two produce, so the cost lands where the benefit is.

## References

- RFD 2088 chose one QUIC stack on both ends; RFD 2122 rejected a second implementation on the
  player path and is not contradicted; RFD 2047 abandoned `webtransportd` and still governs the
  production path; RFD 2111 sets the name shape this amends for four repositories
- RFD 2049 for the reliability classes the two repositories split on, RFD 2096 for the measurement
  discipline, RFD 2108 for the rule that a lagging reader never stalls the writer
- `contract-entity-packet` for the layout, the emitter and the golden vectors; `contract-wt` for
  the same argument one stack earlier
- The measurements, the method, and the rename list: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
