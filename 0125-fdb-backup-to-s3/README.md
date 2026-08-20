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

## State: two faults found and fixed, neither confirmed end to end

The configuration is written. No backup has run yet, and nothing has
been restored. Two separate faults were found, and both reported
themselves as something other than what they were.

**1. A missing file, reported as DNS.** With no port in the URL,
FoundationDB resolves the service name `https` through
`/etc/services`, which `debian:bookworm-slim` does not ship. Every
lookup failed as `lookup_failed` (1041), whose text reads "DNS lookup
failed". Fixed by `netbase` in the image and an explicit port.

**2. A family choice, reported as a connection failure.** FoundationDB
picks one address from the A and AAAA records and prefers IPv6, with
no fallback. Without working IPv6 egress every attempt returns
`ENETUNREACH`, reported as `connection_failed`. Fixed by
`knob_resolve_prefer_ipv4_addr` on the backup agent.

The second was hidden behind the first: the port had to be supplied
before the connection fault could be seen at all.

**What is confirmed.** Fault 2, on one host, by the error moving from
`connection_failed` to `backup_auth_missing` -- the connection
succeeding and deliberately bogus credentials being rejected after it.

**What is not.** Neither fix has run on Fly. The cluster was torn down
before the probe ran, and outbound IPv6 there behaved differently from
the host where fault 2 was confirmed, so it may be a third cause
wearing the same message. Do not read this RFD as "backup works".

Expect the next failure to be auth or region shaped rather than
connection shaped. That is progress, not a regression.

## Related

RFD 0124 covers the cluster's TLS and the CA that issues to it.
