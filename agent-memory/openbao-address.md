---
name: openbao-address
description: "Where the workspace's OpenBao server lives and how to reach it"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-01T22:22:34.249Z
---

The workspace OpenBao is Fly app `weftspun-bao` (region sjc,
`weftspun-bao.fly.dev` externally). Fly `.fly.dev` DNS is blocked
from the Claude sandbox, so reach it via `fly proxy 8200:8200 -a
weftspun-bao` and talk to `https://127.0.0.1:8200`.

**Auth is mTLS 1.3 with `tls_require_and_verify_client_cert=true`.**
Server CA is `chibifire.com Intermediate CA v2` (baked into the fly
container as `BAO_TLS_CA_CHAIN_B64` / `BAO_TLS_CERT_B64` /
`BAO_TLS_KEY_B64`). A client that talks to it needs a cert signed
by that same CA, plus a bao token/auth method on top. Storage is
FoundationDB (`storage "foundationdb"` in `/bao/config/config.hcl`
inside the container).

The Mac at `/Users/ernest.lee/` had NO such client cert as of
2026-09-01 — every `*.pem` under `$HOME` was checked, none issued
by that CA. So this workstation cannot authenticate directly; a
session that needs to read from bao must ask the operator to run
the auth step themselves (either mint the client cert from the CA
key stored elsewhere, or paste the value once).

Related: [[vast-rental-workflow]] describes what the retrieved API
key is used for.
