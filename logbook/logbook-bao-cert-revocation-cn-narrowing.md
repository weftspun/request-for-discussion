# Logbook: revoking a Bao cert-auth identity when the entry is a shared wildcard

**Date:** 2026-09-03
**Session:** MPS (`mps-45994b.agents.weftspun`)
**Related:** RFD 2195 (Bao Tailscale sidecar; Revocation section)

## What happened

MPS-Dataset session (`mps-dataset-68764.agents.weftspun`) was revoked
by operator instruction. Its cert authenticated through the shared
`auth/cert/certs/agents-weftspun` entry, which had
`allowed_common_names=*.agents.weftspun` and covered CUDA too. So the
revocation had to remove one CN without dropping the entry.

## What did not work

`bao write pki/revoke serial_number=<X>` recorded the revocation in
the PKI store and emitted `error building CRLs: x509: issuer
certificate doesn't contain a subject key identifier` — a bao
intermediate config issue, but also irrelevant here: the cert-auth
method does not consult the CRL by default. A revoked cert still
authenticates.

## What did

Three steps, in this order:

1. Read the current `auth/cert/certs/agents-weftspun`, preserve the
   `certificate`, `token_policies`, `token_ttl`, `token_max_ttl`,
   `display_name` fields, replace `allowed_common_names` with an
   explicit list that excludes the revoked CN. Write it back.
2. `bao kv metadata delete agents/<revoked-cn>` — remove the
   coordination-store row so peers don't see a stale identity.
3. Update the 1Password item: annotate `REVOKED 2026-09-03` with the
   reason, keep the cert body for audit.

Effective immediately. No CRL, no reload, no restart. `pki/revoke` on
the serial(s) still runs alongside for the audit trail even though
cert-auth ignores it.

## Detection floor

The shared-wildcard case is the interesting one; the per-CN case is
easier and covered in the RFD 2195 runbook. This entry exists to name
the extra step the wildcard case adds: preserve the entry, narrow the
CN list, versus delete the entry.

## Verdict

Pattern shipped in RFD 2195 DETAILS's Revocation section. Next
revocation should follow that; this entry stays as the event that
produced it.

This RFD was drafted by an AI and read by a human before it shipped.
