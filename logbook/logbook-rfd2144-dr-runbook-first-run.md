# Logbook: the DR runbook runs on the day the cluster is gone

Question: RFD 2143's DR runbook was theatre as of 2026-08-31, and on
2026-09-01 the cluster was gone. What actually happened, and how far
does what shipped match what the RFD described?

## The apparatus

`fly` v0.4.92 on darwin/arm64, `op` v2.39.0 with 1Password desktop
integration on, `openssl` from macOS 25.5, FoundationDB 7.3.76 on the
Fly side. Tigris `weftspun-fdb-blob` and R2 `weftspun-fdb-dr` both
present at start of run. `weftspun-bao root`, `weftspun-fdb-dr s3`,
`Cloudflare R2 weftspun DR`, `OpenBao FDB CA — unseal key and root
token` all present in the Personal vault.

## Finding: five inline defects, none named in the runbook

RFD 2144 DETAILS lists them. Two are process (WEFT_FDB_CLUSTER_ID not
stored anywhere, `notesPlain` exposing Bao secrets to a routine
inspection). Three are tooling (Fly `storage create` refusing an
existing name, health checks fail-closed on first deploy, `zsh`
`read -p` silent in the tool's `!` context).

## Finding: R2 held a restorable snapshot 0.19 days old

    Restorable: true
    Snapshot totalBytes = 99 644
    MinRestorableVersion 102067092357 (maxLogEnd -0.19 days)
    MaxRestorableVersion 118325089881 (maxLogEnd -0.00 days)

RFD 2143's measurement on 2026-08-31 was `Sum of key-value sizes =
0 MB`. The 99 644 bytes agrees: this is Bao's PKI mount metadata and
its internal system tables, which is what "0 MB user data" leaves out.

## Finding: the break-glass CA closes RFD 2141's prereq

Break-glass CA minted at DR-time, stashed to 1P
`op://Personal/FDB-CA/{cert,key}`. That is exactly the slot RFD 2141
named as the missing piece. The rotation phases 2–3 still have to run
once Bao is back — the break-glass CA does not remain the cluster CA
— but the "runbook is theatre" line in RFD 2143's DETAILS no longer
holds.

## Finding: cluster identity was minted fresh

`WEFT_FDB_CLUSTER_ID` was not stored anywhere and had to be minted at
DR-time. `openssl rand -hex 8`, stashed to 1P as `weftspun-fdb cluster
id`. Coordinator addresses change on a rebuild anyway, so the identity
change rides along.

## The timeline, measured

    T+0      fly apps create weftspun-fdb
    T+~2m    fly secrets set --stage (R2, CLUSTER_ID, first pass)
    T+~5m    first deploy (plaintext), machine 8d1d2ebed71158 allocated
    T+~8m    mint leaf, stage TLS secrets, redeploy
    T+~9m    "The database is available." under mTLS
    T+~10m   fdbbackup describe: Restorable: true
    T+~10m   fdbrestore start -w -r $R2_URL → State: queued, 0 files
             (see next finding — no backup_agent)
    T+~15m   fdbrestore abort; start backup_agent by hand under mTLS;
             fdbrestore start -w again
    T+~16m   State: completed. 819 files, 127 919 bytes, restored to
             version 118325089881. `fdbcli status` reports replication
             healthy, sum of key-value sizes 0 MB (agrees with the
             pre-disaster measurement in RFD 2143), disk space used
             424 MB (log-apply of ~16 billion versions of mostly-empty
             log commits).

## Finding: the entrypoint spawns no backup_agent for R2-only

The config-writer in `fdb-entrypoint.sh` gates the `[backup_agent]`
block on `backup=1`, which is set only inside the AWS_* block. An
R2-only setup — the DR case, by construction — spawns no agent, and
`fdbrestore` queues forever with no worker to pick it up. Restore
State stayed `queued`, Blocks 0/0, BytesWritten 0 through 20 polls.

Workaround for this run: start `backup_agent` by hand over SSH, with
`--blob-credentials`, `--knob_http_request_aws_v4_header=true`, and
the four mTLS flags. `setsid nohup ... </dev/null &` and the process
survived the SSH close. Restore then moved from `queued` to `running`
to `completed` in about 90 seconds.

Fix landed same session in `fdb-entrypoint.sh` (see close-out below);
control: `pgrep -a backup_agent` on a machine with `R2_*` set and no
`AWS_*` set returns exactly one pid.

## Finding: Bao restored on chibifire.com Root chain, break-glass retired

Bao's own image built cleanly from `weftspun/service-openbao`, but two
inline defects surfaced before it would start: `openssl genpkey` for
its listener key emitted PKCS#8 with explicit ECDSA parameters that
Go's `crypto/x509` rejects with `invalid ECDSA parameters`, and the
same encoding on the break-glass CA cert made Go refuse the CA file
too. Fix: mint the listener key with `openssl ecparam -name
prime256v1 -genkey -noout` and mint a separate P-256 CA for the Bao
listener; FDB stays on the P-384 break-glass CA because CGO consumers
(the FoundationDB Go binding) accept the explicit-params form.

Bao then unsealed against restored FDB, PKI mount reappeared with its
two issuers (chibifire.com Root, chibifire.com Intermediate), and the
FDB machine cert plus Bao's own FDB client cert both rotated onto
Intermediate-signed leaves in the RFD 2141 phases-2-3 pattern. The
break-glass CA was dropped from `FDB_TLS_CA_B64` and lives on only in
`op://Personal/FDB-CA/` as the break-glass slot RFD 2141 named.

Three orphan root tokens accumulated during rotation attempts; they
were purged after enabling `disable_unauthed_generate_root_endpoints
= false` in `service-openbao/config-fdb.hcl` and running the
`generate-root/attempt` ceremony with the current unseal key.
`bao operator rekey` similarly runs after
`disable_unauthed_rekey_endpoints = false`; the new unseal key round-
trips through a seal / unseal cycle.

## Finding: cluster scaled to 3 zones under `double`

Two new machines cloned via `fly machine clone --detach`; Bao issued
their fdb-server leaves before they started, so the entrypoint's
per-machine cert refusal did not fire. `fdbcli configure double`
after all three joined; the cluster reports 3 zones / 3 coordinators
/ fault tolerance = 1 machine, replication (Re)initializing then
Healthy. This is what RFD 2143 requires before real writes.

## Finding: R2 keys stored in Bao, rotation deferred

`bao kv put secret/weftspun-fdb/r2-dr access_key_id=... ...` writes
the current DR-time R2 credentials into the source-of-truth slot
RFD 2143 named. Cloudflare's public REST API does not expose R2 S3
key creation programmatically (probed `/r2/api-tokens`,
`/r2/s3_access_keys`, `/r2/temp-access-credentials` — all 404 with
the DR bearer's scope; only `/r2/buckets` returns 200), so the
rotation-and-revoke half of RFD 2143 step 8 becomes a dashboard task,
filed as followup.

## The final state

- `weftspun-fdb`: 3 machines, sjc, `double` redundancy, fault
  tolerance 1 zone, all certs on chibifire.com Intermediate. R2
  backup fanned out via the fixed entrypoint; Tigris fan-out pending
  fresh keys.
- `weftspun-bao`: single machine, unsealed, storage foundationdb,
  PKI mount with two issuers restored, `disable_unauthed_*_endpoints
  = false` on the listener so the recovery ceremonies work if needed
  again. Root token and unseal key rotated end-of-DR; the ONE source
  of truth for each is the CONCEALED field on `weftspun-bao root`.
- 1P: `FDB-CA cert`/`FDB-CA key` (break-glass, retired from live
  trust), `weftspun-fdb cluster id`, `weftspun-bao root`
  (rotated CONCEALED root + unseal, empty notesPlain), `weftspun-fdb-
  dr s3` (DR-time R2 keys — will be superseded by the CF dashboard
  rotation in followup task 16).

## What is still open

- **Task 11 parked at operator request:** `spot-broker` and
  `chibifire-com` remain gone from Fly. Bao's PKI is up, so
  restoring them is a matter of minting client leaves and deploying
  from their fly.toml files.
- **Task 16 (R2 rotation):** dashboard-only per finding above.
- **`weftspun-fdb-dr s3` in 1P** still holds the DR-time R2
  credentials; task 16 replaces it.

## Measurement: RTO and RPO

**RPO:** the R2 snapshot restored was 0.19 days old (about four and a
half hours before the run started), well inside the 10-day snapshot
interval RFD 2143 configures. Bao's data recovered to the same point.

**RTO:** from `fly apps create weftspun-fdb` to `The database is
available under mTLS` was about 9 minutes; from the same start to
`fdbrestore` finished was about 16 minutes; from the same start to
Bao unsealed against the restored FDB was about 45 minutes; from the
same start to 3 machines under `double` was about 90 minutes. Six of
the twelve inline defects (RFD 2144 DETAILS) each cost a redeploy
cycle of about 3 minutes; without them the same run would land in
about 20 minutes total. This is the number to compare against on the
next DR.
