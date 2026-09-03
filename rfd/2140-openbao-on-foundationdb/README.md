# RFD 2140: OpenBao on FoundationDB

**State:** discussion
**Feature:** FoundationDB as the storage backend for the secrets manager
**Scope:** weftspun-bao on Fly.io; the OpenBao fork at weftspun/openbao

## Decision

Restore the FoundationDB backend from Vault v1.14.8 (last MPL-2.0
release), connecting to the existing weftspun-fdb cluster over 6PN.
The port rewrites three interfaces that diverged after the fork:
`ListPage`, interactive transactions (`BeginTx`/`BeginReadOnlyTx`
with Commit/Rollback), and pins the FDB 7.3.79 Go binding
(`headerVersion = 730`). Build tag `foundationdb`, `CGO_ENABLED=1`.

Deployment files in weftspun/service-openbao. The bao machine carries
only the FDB client library and connects to the cluster via a TLS
client certificate. Interface details and deploy measurements are
in DETAILS.md.

## Problem

OpenBao dropped every storage plugin when it forked from Vault
v1.14.x. The weftspun-fdb cluster already runs three machines with
double redundancy, TLS, and backup, and raft on a single shared-cpu
machine has no replication path.

## Verification

`bao status`: Storage foundationdb, unsealed. KV v2 at `secret/`,
anchor creds written from weftspun-fdb over 6PN. Root in 1Password.

## Related

RFD 2109 (FDB as the store), RFD 2134 (cluster TLS).
