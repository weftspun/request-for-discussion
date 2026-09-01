# RFD 2146: Bao is the secret store, cert-auth is the fence

**State:** discussion
**Scope:** weftspun-bao PKI + KV, every consumer that holds a
chibifire.com Intermediate CA v2 leaf.

## Problem

Task 19 moved four secrets from 1P into Bao, but the only way to
read them still went through the root token (in 1P). The chain was
"1P -> root token -> Bao -> secret -> API". Disconnecting 1P broke
DNS edits.

Meanwhile the workspace already has per-service TLS leaves under
`chibifire.com Intermediate CA v2` (RFD 2144 + RFD 2145), so every
identity that talks to Bao is already presenting a cert with a
distinctive CN. Nothing was using that identity for authorization.

## Decision

Enable Bao's `cert` auth backend and bind each service's Bao-issued
leaf to a role whose policies grant the minimum it needs. No more
tokens in code, no more root token in a config file, and 1P holds
only Bao's own bootstrap material (unseal key + root token as a
break-glass copy). Bao is the secret store; the cert is the fence.

Policies and roles are the whole design; both live in
`DETAILS.md` alongside a walkthrough of the DNS-edit path with
1P disconnected (the check that proved the fence works).

RFD 2144 defect #11's "orphan root token cannot be enumerated"
becomes less painful under this scheme: routine work does not use
the root token at all, so an orphan is a break-glass artifact only.

## Related

RFD 2140 (Bao on FDB), 2142 (bao-pki-zerotrust-service-tls, which
this RFD's role table implements), 2144 (DR — issued the leaves
this RFD binds), 2145 (cert lifetimes — the leaves rotate on the
90-day cadence this RFD depends on).
