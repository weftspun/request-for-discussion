# DETAILS: CoAP + OSCORE NIF for taskweft

## The C ABI the NIF wraps

libcoap exposes a session-oriented API. The two calls this NIF needs
have essentially the shape of `weft_bus_nif.cpp`'s `open` + `ask`:

    /* create a CoAP client bound to a peer and an OSCORE keyset */
    coap_session_t *coap_new_client_session_oscore(
        coap_context_t *ctx, const coap_address_t *peer,
        coap_proto_t proto, coap_oscore_conf_t *oscore);

    /* send one CONFIRMABLE request and wait for the matching reply */
    coap_response_t coap_send_and_wait(
        coap_session_t *sess, coap_pdu_t *request,
        int timeout_ms, coap_pdu_t **reply);

The NIF binds one Elixir resource around `coap_context_t` +
`coap_session_t`, and one dirty-IO NIF function that owns the send +
poll loop end-to-end. Poll rather than block, because libcoap fires
one callback per received PDU and the NIF must reconcile that with
BEAM's scheduler contract.

## The Erlang shape

Modelled on `weft_bus_nif.cpp`:

    resource `#Reference<CoAPClient>` = %{
      ctx: coap_context_t*, sess: coap_session_t*,
      oscore_conf: coap_oscore_conf_t*
    }

    Taskweft.OpenPLC.CoAP.open(peer_uri, keyset) -> {:ok, ref} | {:error, _}
    Taskweft.OpenPLC.CoAP.ask(ref, method, path, body, timeout_ms)
      -> {:ok, code, payload} | {:error, _}
    Taskweft.OpenPLC.CoAP.close(ref) -> :ok

**Dirty IO scheduler.** A poll-until-match loop can block for the
whole timeout. Running on a normal scheduler would starve other work.
`ERL_NIF_DIRTY_JOB_IO_BOUND` matches how `spot_broker/c_src/store_bus_nif.cpp`
handles the same shape for FoundationDB commits.

**One session per peer.** libcoap sessions are stateful (OSCORE
sequence numbers, deduplication table). Sharing a session between
concurrent asks needs a serialising GenServer above the NIF, matching
`SpotBroker.StoreBus`'s pattern; the raw NIF is safe to hold in a
supervisor and pass through.

## OSCORE resource shape

An OSCORE security context is four fields:

    %Taskweft.OpenPLC.CoAP.Keyset{
      master_secret: <<...>>,          # 16 bytes
      master_salt:   <<...>>,          # 8 bytes (optional)
      sender_id:     <<...>>,          # per-endpoint
      recipient_id:  <<...>>           # per-endpoint
    }

libcoap serialises this into `coap_oscore_conf_t` via its own
edhoc-friendly parser (`coap_new_oscore_conf`). The Elixir side
holds the Keyset in ETS and rotates it under a rekey call; the NIF
tears down the old context and installs the new one atomically.

**Replay window.** OSCORE mandates a per-recipient replay window.
The NIF opts into libcoap's default (32-message sliding window); a
larger window is exposed as a configuration option once a scenario
needs it. Ordering across sessions is not something OSCORE promises;
the coordinator sequences its RECTGTN commands at a higher layer.

## Deployment: OpenPLC v4 CoAP plugin

OpenPLC v4 ships a plugin system for I/O and transports. The
matching server-side plugin `taskweft-openplc-coap` (a separate
first-class repo, MIT) links libcoap and libcoap-oscore, registers
the four resources from RFD 2150's table, and bridges each CoAP
request into OpenPLC's internal program-management API. That plugin
is parked with this RFD; it lands when this NIF does.

## Why not just call the OpenPLC v4 REST API

OpenPLC v4 already exposes a REST API over HTTPS + WebSocket for
its editor. For a local benchtop compile-and-run (this session's
RFD 2150 verification), that REST surface is the cheaper path and
this RFD does not block it. This RFD exists for the deployment
scenario the REST surface does not cover: a constrained UDP link to
a battery-powered target where TLS handshake cost is prohibitive and
IPv6 6LoWPAN is the wire.

## Staging

- **now**; parked. Design frozen, no code.
- **when needed**; a scenario names a constrained target; the NIF,
  the Elixir wrapper, and the OpenPLC plugin ship together.
- **later**; EDHOC (RFC 9528) key exchange replaces static keysets.

## What is deliberately not here

- A blessing of a specific OSCORE-in-libcoap version. `libcoap` from
  4.3.5 onwards ships OSCORE support; the exact version picks itself
  when the NIF lands.
- A bridge to CoAP Group Communication (RFC 7390); the coordinator
  addresses one runtime at a time, not a multicast group of them.
- COSE crypto primitives (RFC 8152); libcoap's OSCORE module carries
  them and this NIF does not re-expose them.
