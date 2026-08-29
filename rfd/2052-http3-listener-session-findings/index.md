---
title: "RFD 2052: One transport listener per authority pending http3 multi-session fixes"
rfd: "2052"
state: published
scope: WebTransport/HTTP3 module, multi-session routing
---

## Problem

The four-player contention smoke test drives one
`WebTransportPeer.create_server` listener with four concurrent client
sessions. Replies reach only one session, regardless of
`set_target_peer` or `get_packet_peer`. A session teardown during
traffic also aborts the process with a double free, and a second
`create_server` call in the same process fails.

## Decision

The four-player contention smoke drives one
`WebTransportPeer.create_server` listener in the merged assembly with
four concurrent client sessions. Incoming datagrams from every
session multiplex into the server's packet queue correctly, but
replies reach only one session regardless of `set_target_peer` or
`get_packet_peer`, and a session teardown during traffic aborts the
process with a double free. A second `create_server` in the same
process fails with "server already listening", so the backend holds
one listener per process. Until the module carries per-session peer
routing and clean teardown, the loop runs one listener per authority
process, attributes requesters in the message body rather than by
transport peer id, and verifies the authority's resolutions at the
harness against the Lean golden vectors. The four-player smoke
verifies authoritative resolution (64 rounds matching the golden
vectors from four concurrent clients) while grant delivery waits on
the reply-routing fix. The loot and combat wire parities stay
unaffected, because a single session per listener works end to end.

A server that opens a bidirectional stream per reliable message needs
the stream credit to carry them. `picowt_set_transport_parameters`,
which runs per connection, raises `initial_max_stream_id_bidir` and
`initial_max_stream_id_unidir` to `0x3F` along with the flow-control
limits. `picowt_set_default_transport_parameters`, which runs once for
the `picoquic_quic_t`, raises neither: it sets
`is_reset_stream_at_enabled` and `max_datagram_frame_size` and nothing
else. A server that takes only the second one holds the default credit,
so a fourth session finds none left, and the exhausted credit blocks
the connect-accepted response on the control stream, which leaves that
session short of the open state.

## References

- The upstream fix, its landed pattern, and post-fix behavior:
  `DETAILS.md`
- Original record:
  `decisions/20260612-http3-listener-session-findings.md`
- Fix: `https://github.com/v-sekai-multiplayer-fabric/godot/pull/56`

## Related

- `rfd/2023-webtransport-http3-transport`: the HTTP/3 transport this
  finding constrains.

## Detail

{{< include DETAILS.md >}}
