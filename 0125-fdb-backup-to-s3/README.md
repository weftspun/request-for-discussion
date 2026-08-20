# RFD 0125: Continuous backup from FoundationDB to Tigris

**State:** discussion
**Feature:** continuous backup of the Fly cluster to an S3 bucket
**Scope:** `6-datasource/store/fly`

## Problem

The cluster has no backup. A cluster with no backup holds data that one
mistake removes.

FoundationDB backup is continuous by design. `fdbbackup start` writes a
snapshot and then keeps a mutation log, so a restore can choose a point
in time. This is the behaviour we want. We do not need a cron job.

## Decision

**1. Use Tigris, through Fly.** The bucket `weftspun-fdb-backup` exists.
Fly injects `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`AWS_ENDPOINT_URL_S3`, `AWS_REGION` and `BUCKET_NAME` into each machine.

**2. Keep the secret out of the URL.** `fdbbackup` accepts
`blobstore://key:secret@host/...`. That form puts the secret in a
command line, in shell history, and in `ps` output for every process on
the machine. Use a blob credentials file instead. The URL names
`key@host` and `fdbbackup` resolves the secret at connect time from a
file that only root can read.

**3. Run one backup agent for each machine.** The agent does the work.
`fdbbackup` only submits the job. The agent is a *client* of the
cluster, so under mutual TLS it needs its own certificate, key, CA and
verification rule. An agent without them connects to nothing.

**4. Give the agent a wider trust bundle than the servers.** The object
store's certificate comes from a public CA. FoundationDB has no separate
TLS policy for blob store connections, so the agent must trust the
public roots as well as ours. The `fdbserver` processes must not. See
`DETAILS.md`.

## State: this does not work yet

The configuration is written and deployed. No backup runs. FoundationDB
cannot resolve the object store's hostname on Fly.

The error is `lookup_failed` (1041), not a TLS error and not a
credential error. `DETAILS.md` holds the evidence and the three
hypotheses this replaced.

## Related

RFD 0124 covers the cluster's TLS and the CA that issues to it.
