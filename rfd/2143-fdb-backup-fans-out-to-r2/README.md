# RFD 2143: FDB backup fans out to R2 for off-Fly durability

**State:** discussion
**Feature:** a second `fdbbackup` tag writes to R2 IA alongside the Tigris tag
**Scope:** weftspun-fdb (3 machines)

## Decision

A second `fdbbackup` tag `dr` writes concurrently to R2 IA
(`weftspun-fdb-dr`), reached via a second stunnel loopback listener
that adds the SNI FoundationDB does not send. R2 IA carries a 30-day
minimum storage duration and free egress. The `default` tag keeps
writing to Tigris; two destinations, one cluster.

R2 S3 credentials live in Bao at `secret/data/weftspun-fdb/r2-dr`,
cached as Fly secrets on `weftspun-fdb` because Bao's storage is FDB
and FDB cannot read Bao at boot. The Cloudflare API bearer token
stays in 1Password; the S3 keys are regenerated from it at DR time
rather than restored, so no long-lived material sits outside Bao.

**Gate:** `fdbbackup status -t dr` reports restorable and R2's newest
`data/` object is younger than `WEFT_BACKUP_MAX_AGE`.

**Negative control:** a machine started without `R2_ACCESS_KEY_ID`
runs `default` only, and the `dr` check reports critical rather than
passing on nothing.

## Problem

Today `fdbbackup` writes to Tigris (`fly.storage.tigris.dev`), Fly's
own object storage. A disaster naming "all Fly infra gone" takes the
backup with the cluster. Beside it: Bao holds the FDB CA key as
`type=internal`, and Bao's storage backend is FDB, so the CA rides
FDB backups. A restore that cannot read the backup cannot issue the
machine leaves the restored cluster needs.

## Related

RFD 2134, 2140, 2141, 2135. DR runbook in DETAILS.md.
