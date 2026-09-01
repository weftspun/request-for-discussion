# Logbook: cert-auth on Bao, and the DNS edit that ran without 1P

Question: task 19 landed the four DR-time secrets in Bao. The next
step was making Bao's own root token stop being the gate. What did
enabling cert-auth actually cost, and did it work end to end?

## The apparatus

weftspun-bao (single machine, unsealed, `chibifire.com Intermediate
CA v2` on the listener), five per-service leaves signed by that
intermediate (RFD 2144's rotation output), one operator admin cert
signed directly by the Root, `op` desktop-app integration active for
the last root-token read.

## Finding: five policies + four roles is the whole thing

Policies land as four HTTP POSTs to `sys/policies/acl/*`, roles as
four to `auth/cert/certs/*`, an enable call to `sys/auth/cert`.
Nine calls total, all returned within their 8s max-time. Bao restart
was not needed. The `admin-v2` role was upgraded from RFD 2145's
DNS-only binding to the full admin bundle
(`admin,dns-editor,pki-issuer,fdb-config-reader`); the earlier
narrower binding was overwritten by the new POST, which is what a
Bao role update does.

## Finding: intermediate-signed leaves need the intermediate in
the client-side bundle

First verification pass presented leaf-only certs and got empty
policy lists back. Root cause: `BAO_TLS_CA_CHAIN_B64` on the Bao
listener is the chibifire.com Root only, so the TLS handshake
cannot build the chain for an intermediate-signed leaf. The client
has to send `leaf + intermediate`; the `bundle.pem` files RFD 2144
already produced for each service leaf work as-is. Presenting the
bundle succeeded on the first retry.

The alternative — put the intermediate in `BAO_TLS_CA_CHAIN_B64` on
the listener — was considered and rejected: keeping the intermediate
out of the listener trust store means an intermediate-only leaf can
never present without also presenting its signing intermediate,
which is a small but real defense-in-depth.

## Finding: cert-only DNS edit works

`scratchpad/cf-bearer.sh` is 17 lines of `curl` — cert to Bao,
token from Bao, bearer from Bao, `Authorization: Bearer` to
Cloudflare. Verified 2026-09-01 against the actual `spot.chibifire.com`
CNAME entry in the chibifire.com zone: the entry was read back and
its `content` field agreed with `spot-broker.fly.dev`. No `op read`
in the entire path.

## Finding: negative controls fire on the exact denial shape

- `spot-broker-app` cert -> reads `fdb/cluster-id` (ok, value
  starts `ee02`) -> reads `cloudflare/edit-zone-dns` -> **HTTP 403
  `permission denied`**.
- `fdb-cluster` cert -> reads `fdb/cluster-id` (ok) -> reads
  `cloudflare/edit-zone-dns` -> **HTTP 403 `permission denied`**.

Both denials return exactly `"errors":["permission denied"]` with
no policy names in the body. Nothing about what the policy is
called leaks back to the caller.

## What is still open

- **Cert rotation and role rebinding**: leaves rotate on the 90-day
  cadence RFD 2145 sets. When a leaf is re-issued, its DER hash
  changes and `auth/cert/certs/<role>` still points at the previous
  one. A small watcher against `pki/` events (or a nightly cron)
  needs to re-run `bao write auth/cert/certs/<role>
  certificate=@<new-leaf>`. Filed as a followup.
- **Per-app secret paths under `secret/apps/<name>/*`** are empty
  today. `spot-broker` has no runtime secrets in Bao yet; when the
  operator adds `VAST_API_KEY`, `SB_GH_CLIENT_ID/SECRET`,
  `SB_TOKEN_SECRET`, `BROKER_TOKEN`, they land under
  `secret/apps/spot-broker/*` and the existing `app-reader-spot`
  policy already covers them.
- **Root-token break-glass**: the root token stays in 1P
  (`weftspun-bao root/password`). Routine work no longer uses it.
