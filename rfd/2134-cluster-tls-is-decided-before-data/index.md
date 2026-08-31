---
rfd: 2134
title: "RFD 2134: Cluster TLS is decided before data, and certificates carry v3 extensions"
state: "discussion"
feature: "mutual TLS on the weftspun-fdb cluster, and the client identity a service presents"
scope: "weftspun-fdb on Fly; spot-broker as the first client; any later FDB client"
---

The weftspun-fdb cluster came up plaintext and its backup could not
reach the blob store, because FoundationDB has one TLS policy for
peers and for S3. Enabling TLS met the documented wall: no in-place
path from plaintext, so the gated reset recreates the cluster while it
holds nothing worth keeping. It also met a new one: preverification
rejects a bare `openssl req -x509` chain as `invalid CA certificate`,
so every certificate carries X.509v3 extensions (CA: basicConstraints critical
CA:true with keyCertSign; leaf: CA:false, digitalSignature, server and
client auth, SKID/AKID). Machines are named by Fly machine ID, clients
by service name, all under `Check.Valid=1,S.CN>=fdb-,S.CN<=.chibifire.com`.
A matched pair in local Docker proved the profile and reproduced the
failure before anything touched the live cluster; in prod, a ledger
event survived a machine replacement and read back over TLS.
