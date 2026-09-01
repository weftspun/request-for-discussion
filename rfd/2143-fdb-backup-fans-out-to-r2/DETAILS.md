# RFD 2143 details: entrypoint changes and the DR runbook

## What was measured on 2026-08-31

`fdbbackup status` on `84e69ef2251558` reported the `default` tag
restorable and continuing to
`blobstore://...@fly.storage.tigris.dev:8443/weft?bucket=weftspun-fdb-blob`.
The cluster's `Sum of key-value sizes` was 0 MB, so the whole 944 MB
of FDB disk use is empty pages -- the safest possible moment to
introduce a second backup tag.

Bao's PKI mount was queried with the root token: `pki/keys` lists
two RSA keys, neither with exported material, and the intermediate
issuer's `key_id` is `a15acb18-...`. The CA key is not readable
outside Bao. The DR chain therefore relies on FDB backup + Bao
restore-in-place (Bao's storage is FDB), and the R2 destination is
what protects that chain from single-provider loss.

`Bao's storage_type` returned `foundationdb`. `fdbcli status` under
mTLS from an SSH console needed the four env vars the entrypoint
sets around fdbserver (`FDB_TLS_{CERTIFICATE,KEY,CA}_FILE` and
`FDB_TLS_VERIFY_PEERS`), which had to be set by hand in the shell.

## Credentials, and why they live where they do

Bao holds the source of truth for the R2 access key and secret at
`secret/data/weftspun-fdb/r2-dr` (KV v2). `weftspun-fdb`'s Fly
secrets `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`,
`R2_BUCKET`, `R2_REGION` are the bootstrap cache the entrypoint reads
before Bao can serve.

The layering forces this. Bao's storage backend is FDB. If the FDB
entrypoint tried to read Bao at boot to get its R2 creds, Bao would
not answer -- Bao needs FDB up first. So the entrypoint reads Fly
env, and rotation is a two-step: write the new secret to Bao, then
`flyctl secrets set` from Bao and roll the deploy. Bao stays the
source, Fly is the cache, and the two are in sync when the deploy
completes.

The Cloudflare API bearer token stays in 1Password
(`Cloudflare R2 weftspun DR`), because that is the identity you use
to mint new S3 keys at DR time. The S3 keys themselves are
regenerable from the bearer token, so no copy of them needs to sit
outside Bao waiting for a disaster.

## Entrypoint change

The existing `AWS_*` variables that drive the Tigris destination stay
as-is. A parallel set of variables drives the R2 destination:

    R2_ACCESS_KEY_ID
    R2_SECRET_ACCESS_KEY
    R2_ENDPOINT_URL       # https://<account>.r2.cloudflarestorage.com
    R2_BUCKET             # weftspun-fdb-dr
    R2_REGION             # auto

The entrypoint, when all five are set, does what it does for Tigris,
once more:

1. Writes `/etc/foundationdb/blob-credentials-r2.json` at mode 0600.
   `FDB_BLOB_CREDENTIALS` becomes `default_creds:r2_creds` so both
   destinations authenticate from one env var.
2. Resolves the R2 endpoint host once, writes a second stunnel
   config listening on `127.0.0.1:8444` with the R2 hostname as SNI,
   and appends the loopback line to `/etc/hosts` (a syscall away, so
   the loopback traffic stays plaintext and the public-chain check
   is stunnel's).
3. Writes `/etc/foundationdb/backup-url-r2` pointing at
   `127.0.0.1:8444`, `sc=0`, `region=auto`,
   `knob_http_request_aws_v4_header=true`. R2 refuses SigV2 the way
   Tigris does.
4. Registers a second `[backup_agent.2]` block in
   `foundationdb.conf`, so `fdbmonitor` keeps a second agent alive.
5. Once `fdbcli status minimal` reports the database available and
   `fdbbackup status -t dr` reports no previous backup, runs
   `fdbbackup start -t dr -z -d "$(cat backup-url-r2)"` once.
   Restarting a running tag is what makes a second start abort as
   "already exists" without naming which tag, so the guard fires on
   the state that the start call actually needs.

`backup-fresh.sh` grows a `--tag <name>` mode. Without a tag, it
keeps today's behavior (reads `status json`, writes
`/run/backup-fresh/health`). With `--tag dr` it parses
`fdbbackup status -t dr` for `restorable` and its last-complete log
timestamp, and writes `/run/backup-fresh/dr`. `fdb.toml` adds a
`[checks.backup_fresh_dr]` block polling `/dr`.

## The DR runbook (restore from R2, all Fly infra gone)

The premise: `weftspun-fdb`, `weftspun-bao`, `spot-broker`, and
`chibifire-com` no longer exist. 1Password holds the Bao unseal key,
the Bao root token, and the Cloudflare API bearer token. R2 holds
the last complete FDB backup, including Bao's PKI mount (Bao stores
in FDB).

1. In the Cloudflare dashboard, use the bearer token in 1P to mint
   a fresh R2 S3 access key/secret against the surviving
   `weftspun-fdb-dr` bucket. Copy both to a scratch note; do not put
   them back in 1P.
2. `flyctl apps create weftspun-fdb --org personal` and set:
   * `AWS_*` for a new Tigris bucket (or leave unset to skip Tigris
     until later)
   * `R2_*` from step 1
   * `WEFT_FDB_CLUSTER_ID` to the value in the archived `fdb.toml`;
     coordinator addresses change, cluster identity does not.
3. Deploy `fdb.toml` with `WEFT_FDB_MACHINES = "1"` and
   `WEFT_FDB_RESET = "1"`. The single machine forms a `single`
   redundancy cluster to receive the restore into.
4. Bootstrap a fresh CA whose key stays outside Bao, because the CA
   inside Bao is unreachable until Bao is up. Issue the machine leaf,
   set it as `FDB_TLS_CERT_<mid>_B64` / `FDB_TLS_KEY_<mid>_B64`.
5. `fdbrestore start -r "$(cat /etc/foundationdb/backup-url-r2)" -w`
   -- wait, because a background restore that fails on a
   loopback-broken stunnel does not surface until the next check.
6. When restore finishes, `fdbcli status` reports the restored key
   ranges and Bao's mount metadata is visible in FDB. Recreate
   `weftspun-bao` with its unseal key; Bao unseals against its
   restored FDB backend and its PKI mount reappears with the
   original CA usable again.
7. Rotate the machine leaf to one signed by the restored CA
   (RFD 2141 phases 2-3), then scale to three machines with
   `WEFT_FDB_MACHINES = "3"` and `WEFT_FDB_REDUNDANCY = "double"`.
8. Move the fresh R2 access key from the scratch note into Bao at
   `secret/data/weftspun-fdb/r2-dr`; revoke the old key from
   Cloudflare so no key material predating the DR still exists.
9. Recreate `spot-broker` and `chibifire-com` from their `fly.toml`
   files, deploy, verify checks.

## Break-glass CA note

Step 4 needs a CA whose private key is not inside Bao, because Bao
is what step 6 restores. RFD 2141's rotation writes the intermediate
key into `op://Personal/FDB-CA/{cert,key}` as part of that phase.
Until that RFD lands, this runbook is theatre: the DR bucket has the
data but the cluster cannot come up to accept it.

The measurement on 2026-08-31: the CA key is not yet in 1Password.
That is the first followup, and RFD 2141 is where it happens.

## What this RFD does not cover

- **Cross-region.** Tigris and R2 IA in one region are one regional
  outage away from being one destination. A second R2 region is a
  later change.
- **Backup encryption at rest.** FDB does not encrypt backup
  payloads. If R2 is compromised, the attacker has the database.
  `fdbbackup --encryption-key-file` is the fix; it needs its own
  key management story.
- **PITR window.** The Tigris tag today keeps 10-day snapshots
  (`Snapshot interval is 864000 seconds`). R2 keeps the same, at IA
  rates.
