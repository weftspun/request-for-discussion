# Logbook: bao connected to FDB cluster, credential rotation, 1Password persistence failure

Question: does bao connect to the existing weftspun-fdb cluster over
6PN with mutual TLS, and can the root token and KV secrets be
rotated and backed up to 1Password.

## The apparatus

OpenBao v2.0.0-HEAD (weftspun/openbao, feat/foundationdb-storage).
FDB 7.3.79, cluster weftspun-fdb (3 machines, double redundancy,
mutual TLS). Fly app weftspun-bao, shared-cpu-1x 512 MB, sjc.
1Password CLI v2 with biometric unlock.

## What was done

Rewrote `entrypoint-fdb.sh` from a co-located single-node fdbserver
to a cluster client. The entrypoint decodes TLS material from Fly
secrets, writes the cluster file, verifies cert/key modulus match,
waits for cluster health via `fdbcli status`, then exec's bao.
Removed the fdbserver deb from `Dockerfile.fdb` (client-only).

Backed up existing bao KV to 1Password before the switch, then
initialized bao on the cluster FDB, unsealed, enabled KV v2, and
restored `secret/fdb/tls-anchor`, `secret/fdb/blobstore`, and
`secret/vastai/api`.

Rotated the root token via `auth/token/create` with
`no_parent:true` and root policy. Revoked the old token (confirmed
HTTP 403).

## What did not go as planned

**`FDB_CLUSTER_FILE` is reserved.** The Fly secret carrying the
cluster connection string was named `FDB_CLUSTER_FILE`. The FDB
client library treats that environment variable as a file path, not
content; `fdbcli` tried to open a file named
`weft:f5d800cd147f561a@[fdaa:...]:4500:tls,...` and failed with
error 1515 (no cluster file found). Renamed to `FDB_CLUSTER_CONTENT`.

**`generate-root` is not supported on OpenBao 2.0.0.** The endpoint
returns "unsupported operation". Root token rotation used
`auth/token/create` with `no_parent:true` instead.

**1Password `op item create` does not persist on biometric timeout.**
Three `op item create` calls returned exit code 0 with item IDs.
All three IDs are unreachable on subsequent `op item get`. The
`op item edit` path to an existing item (`d7fx6rayd6o43sie5joxinfyte`)
did persist. The FDB CA key from the RFD 2141 rotation was among the
lost items; this is the second loss of the CA key.

## The measurement

Cluster health after bao connected (from `fdbcli status`):

| metric              | value                        |
|---------------------|------------------------------|
| processes           | 6                            |
| zones               | 3                            |
| machines            | 3                            |
| redundancy          | double                       |
| replication health  | Healthy                      |
| fault tolerance     | 1 machine                    |
| moving data         | 0.000 GB                     |

Bao init on cluster FDB: 1 key share, threshold 1, init to
unsealed in under 3 seconds. KV v2 mount and three secret writes
all succeeded on first attempt.

Root token rotation: create returned the new token, revoke of the
old token succeeded, old token confirmed dead (HTTP 403), new
token confirmed live (HTTP 200 on `secret/metadata?list=true`).

Deploy time from `fly deploy` to `FDB cluster available` log line:
under 15 seconds (cluster file written, TLS material decoded, fdbcli
poll succeeded on first try). Bao listener started at ~t+25s.
