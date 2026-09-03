# RFD 2195: Expose weftspun-bao privately via Tailscale

**State:** discussion
**Feature:** run Tailscale sidecar in the weftspun-bao Fly machine
**Scope:** `weftspun-bao` Fly app, `Dockerfile.fdb`, `entrypoint.sh`

## Decision

Add a Tailscale sidecar to the `weftspun-bao` Fly.io machine so
peers on the user's tailnet reach OpenBao at
`weftspun-bao.<tailnet>.ts.net:8200`. No public IP, no fly.toml
service exposure. Mutual-TLS at OpenBao's listener stays as the
second factor; Tailscale is transport only.

Container installs the Tailscale APT package and swaps its entry
point to a script that starts `tailscaled --tun=userspace-networking`
(Fly machines lack `/dev/net/tun`), runs `tailscale up` with
`TS_AUTHKEY`, then `exec dumb-init bao server -config=...`.

`TS_AUTHKEY` is a Tailscale admin-console auth key tagged
`tag:fly-bao` (ephemeral + reusable + pre-approved), set as a Fly
secret before deploy. Full steps + scripts in `DETAILS.md`.

## Problem

OpenBao is the workspace's PKI + KV store for agent secrets
(future: KV v2 at `agents/`, cert-auth issued via bao's PKI). It
runs on Fly at `weftspun-bao` (sjc, 1 machine, FoundationDB
backend, mTLS listener). Reaching it from any of the operator's
laptops or workstations without opening a public IP needs a
private overlay. Tailscale is what the workspace already uses for
that shape.

## Related

`weftspun-bao` Fly app (state summarised in DETAILS.md),
`weftspun-fdb` (FoundationDB backend), RFD 2142 (bao PKI zerotrust
service TLS), RFD 2146 (zerotrust roles first run).

This RFD was drafted by an AI and read by a human before it shipped.
