# RFD 2142: Zero-trust service TLS via OpenBao PKI

**State:** discussion (implemented 2026-09-01; see RFD 2146 for the role/policy map)
**Feature:** mTLS on the bao listener and cert-based service auth
**Scope:** weftspun-bao, spot-broker, weft-warp-burrito

## Problem

Services on 6PN read secrets from bao over plaintext HTTP. The root
token in 1Password is for emergencies; sharing it with services is
the credential distribution problem bao exists to solve. Any 6PN
neighbor can observe or modify traffic to the listener.

The FDB root CA key is lost a second time (the replacement from RFD
2141 was stored via `op item create`, which returned an item ID but
did not persist the item). Chaining under that CA is not possible
without rotating FDB again.

## Decision

Bao's PKI secrets engine becomes a standalone root CA for service
auth. The FDB CA (`fdb-ca.chibifire.com`) stays separate for
cluster mutual TLS.

1. Mount `pki/` and generate a root CA inside bao.
2. Issue a listener cert; enable TLS on `:8200`.
3. Enable the TLS cert auth backend. Each service presents a client
   cert signed by bao's PKI and receives a scoped token for its
   KV paths.
4. Elixir services use `libvault` (hex.pm) as the vault client.

**Gate:** bao rejects a plaintext request to `:8200`.
**Negative control:** a request with no client cert, or with an
expired cert, returns 403.

## Related

RFD 2140 (bao on FDB), RFD 2141 (FDB TLS rotation).
