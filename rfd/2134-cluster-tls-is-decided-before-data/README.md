# RFD 2134: Cluster TLS is decided before data, and certificates carry v3 extensions

**State:** discussion
**Feature:** mutual TLS on the weftspun-fdb cluster, and the client identity a service presents
**Scope:** weftspun-fdb on Fly; spot-broker as the first client; any later FDB client

## Decision

Mutual TLS from a private CA, per-machine certificates named by Fly
machine ID, and one client certificate per consuming service, all
carrying X.509v3 extensions, because FoundationDB's preverification
rejects a bare `openssl req -x509` CA as `invalid CA certificate`.
The profile, the local Docker proof with its negative control, and the
full procedure are in DETAILS.md.

The known wall is recorded in datasource-store's fdb-entrypoint and
held exactly: there is no in-place path from a plaintext cluster to a
TLS one, because `:tls` is part of a coordinator's address and the
coordinated state on disk names addresses that no longer exist. The
gated `WEFT_FDB_RESET=1` wipe is the remedy, so TLS is decided before
there is data worth keeping; this cluster held one test event.

A client is a TLS peer like any other: it presents its own leaf
(`CN=fdb-spot-broker.chibifire.com`) through the `FDB_TLS_*` env vars
libfdb_c reads, and verifies the cluster with the same rule the
cluster uses (`Check.Valid=1,S.CN>=fdb-,S.CN<=.chibifire.com`).

## Problem

The weftspun-fdb cluster came up plaintext, and its backup could not
reach the blob store: FoundationDB uses one TLS policy for peers and
for S3, so a cluster with no trust store cannot speak HTTPS to Tigris.
Turning TLS on after the fact hit two walls, one known and one new.

## Verification

A matched pair in local Docker before any push: v3 certificates form a
database; the previous extension-less certificates reproduce the
production failure on the same server and rule. In prod, a ledger
event survived a full machine replacement and read back over TLS.
