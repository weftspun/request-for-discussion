# RFD 2144 details: what running the RFD 2143 runbook actually measured

## The disaster

On 2026-09-01, `fly apps list` for `personal` returned one row:
`artifacts-mmo-mcp`. The four apps the working agreements name as
placed — `weftspun-fdb`, `weftspun-bao`, `spot-broker`, `chibifire-com` —
were gone. Tigris `weftspun-fdb-blob` and R2 `weftspun-fdb-dr` both
survived, so the disaster matched RFD 2143's premise partially: compute
lost, object storage kept. The `personal` org's `weftspun-fdb-blob` bucket
showed in `fly storage list`; the R2 bucket showed as `Restorable: true`
under `fdbbackup describe`.

## The R2 snapshot, described from the recovered machine

    URL: blobstore://<key>@814b5215273d5479adb116d1fe1af696.r2.cloudflarestorage.com:8444/weft?bucket=weftspun-fdb-dr&region=auto&sc=0
    Restorable: true
    Snapshot:  startVersion=102067065919 (maxLogEnd -0.19 days)
               endVersion=102067092357  (maxLogEnd -0.19 days)
               totalBytes=99644  restorable=true  expiredPct=0.00
    ContiguousLogEndVersion: 118325089882 (maxLogEnd -0.00 days)
    MaxRestorableVersion:    118325089881 (maxLogEnd -0.00 days)

99 644 bytes of snapshot. RFD 2143's measurement on 2026-08-31 was
`Sum of key-value sizes = 0 MB`, and this snapshot's size agrees: the
cluster held Bao's PKI mount metadata and little else. The recovered
data is Bao's state at the moment the last log flushed, 0.19 days
before the describe (about four and a half hours before the run).

## The runbook and what it hid

Twelve defects surfaced during the run that the RFD 2143 runbook did
not name. They are named here so a second run does not rediscover
them.

**1. `WEFT_FDB_CLUSTER_ID` had no home.** The entrypoint requires it,
the fly.toml deliberately does not default it, and no 1P item held it.
A fresh one was minted (`openssl rand -hex 8`) and stored to 1P as
`weftspun-fdb cluster id`. Clients' cluster files change to the new
`weft:<newid>@<newcoords>` — because coordinator addresses change on a
rebuild anyway, the identity change costs nothing extra. Every future
DR needs to either mint fresh or restore this from somewhere, and the
runbook is now updated to say so.

**2. Bao root token and unseal key were in `notesPlain`.** The
`weftspun-bao root` login item stored both as free-text notes rather
than in CONCEALED fields. A routine `op item get --format=json` walk
that concealed only `CONCEALED`-typed fields printed both into the DR
session's transcript. Rotation moved to end-of-DR (`bao token
revoke -self`, `bao operator rekey`), and the notes field is empty
afterward.

**3. `fly storage create --name <existing>` refuses to reattach.** The
error is `Name has already been taken`. There is no CLI flag for the
attach case, and no other subcommand does it. The recovery got its
Tigris keys by way of the Tigris console (`fly storage dashboard
weftspun-fdb-blob`) and pasted them into `fly secrets set --stage`
from the operator's own terminal. A followup is a script that walks
this dance rather than a paragraph in the runbook.

**4. Health checks fail closed during initial deploy.** `backup_fresh`
and `backup_fresh_dr` publish a file only when the backup agents are
running and their newest object is fresh. On a fresh cluster with no
backup started, the files never appear, and the checks stay critical
past their grace periods. `--strategy immediate` is what makes the
deploy return anyway. Once the cluster is up and the DR-tag backup
starts, the checks recover on the next poll.

**5. `zsh` `read -p` never fires in the AI session's `!` context.**
The prompt is written to `/dev/tty` and the tool captures stdout, so
the user sees nothing, `read` returns an empty string, and the
following `fly secrets set` runs with empty values and rejects them.
The credentials pipeline switched to `op read | fly secrets set` via
shell substitution, which puts no value in the transcript regardless
of the shell.

**6. The entrypoint spawns no `backup_agent` for R2-only setups.**
`fdb-entrypoint.sh` gates the `[backup_agent]` config block on
`$backup = 1`, which is set only inside the AWS/Tigris credentials
block. R2-only bring-up — which is precisely the DR case — writes an
`fdbmonitor` config with no agents, and `fdbrestore` queues with no
worker to pick it up. The DR run's restore stayed in state `queued`
with 0 blocks progressing over twenty polls before the cause was
found. Workaround: start `backup_agent` by hand over SSH under mTLS.
Filed as followup: gate the block on `$backup = 1 || $backup_r2 = 1`
and pick `blob_credentials` from whichever file exists.

**7. `weftspun/service-openbao` is not in `default.xml`.** The DR
runbook needs the deployment config for `weftspun-bao`, and the
config lives in a repo that is not one of the manifest's 135
projects. The run cloned the repo by hand into scratchpad. Add it to
the goal manifest, or the next DR discovers this the same way. RFD
2140 references the repo but does not require it to be checked out.

**8. `openssl genpkey -algorithm EC` produces params Go rejects.**
The Bao listener refused to start with `x509: invalid ECDSA
parameters`. `openssl genpkey` with `-pkeyopt ec_paramgen_curve:P-256`
default-encodes the key in PKCS#8 with explicit ECDSA parameters,
which OpenSSL and CGO consumers (including the FoundationDB Go
binding) accept but Go's stdlib `crypto/x509` refuses. The fix is
`openssl ecparam -name prime256v1 -genkey -noout`, which writes the
traditional SEC1 `EC PRIVATE KEY` PEM with a named-curve OID that Go
accepts. `mint-fdb-leaf.sh` used the failing form and stayed that way
because its consumers are all CGO. Any key destined for a Go stdlib
TLS listener needs the SEC1 form. The break-glass CA generator has
the same defect on P-384; the Bao boot CA had to be minted in a
second scratchpad slot rather than reusing the FDB CA.

**9. Three different unseal keys in 1P, only one worked.** The
canonical `openbao-fdb-ca-init.json` in the OpenBao document, the
`unseal_key` CONCEALED field on the `weftspun-bao root` login, and
the base64 line under `Unseal key (base64):` in that login's
`notesPlain` all held different 44-character strings. The first two
failed unseal with `cipher: message authentication failed`
(AES-GCM auth tag mismatch = wrong key); the notes value succeeded.
The rekey history clearly outran the 1P hygiene — every rekey wrote
one place, and the two other slots kept their pre-rekey values. The
end-of-DR pass rewrote `unseal_key` (CONCEALED) with the working
value, cleared `notesPlain` of the leaked keys, and left a note
naming the stale init doc — the source of truth is now one field.

**10. OpenBao's `sys/rekey/init` returns 405 unsupported operation,
until enabled by a listener flag.** Vault registers the unauthenticated
Shamir rekey endpoints by default; OpenBao gates them on
`disable_unauthed_rekey_endpoints = false` inside the `listener "tcp"`
block. Without the flag, `internal/http/handler.go` skips
`mux.Handle("/v1/sys/rekey/init", ...)` and the endpoint returns 405.
The fix landed in `service-openbao/config-fdb.hcl` during the DR;
`bao operator rekey` then completed and the new unseal key is what
`op://Personal/weftspun-bao root/unseal_key` holds. **Verified:**
`bao operator seal` followed by `bao operator unseal <new-key>` cycles
without error.

**11. `sys/generate-root-token/attempt` returns 403; the
unauthenticated `sys/generate-root/attempt` is behind the same
listener flag.** OpenBao's authenticated variant (with `-token` in the
path) always returns `permission denied` to callers presenting a
client cert; the CLI hits this one by default. The unauthenticated
variant (Vault's original path, without `-token`) is only registered
when `disable_unauthed_generate_root_endpoints = false`. Same flag as
#10, filed the same way. The CLI's `-decode` operation itself calls
the authenticated status endpoint before decoding, so on this build
the decode step fails even after the endpoint is enabled — decode was
done locally in Python (XOR of the OTP against `base64.RawStdEncoding`
of the encoded token, per `sdk/helper/roottoken/decode.go`). The
recovered token was used to revoke three orphan root accessors this
DR had accumulated during rotation attempts; the new root token is
what `op://Personal/weftspun-bao root/password` holds. **Verified:**
`bao token lookup` under the new token reports `policies=[root]`,
`orphan=true`; only three accessors remain (was five).

**12. `awk -F=` truncates the trailing `=` in base64 values.** A
44-char base64-encoded 32-byte unseal key stored as 43 chars in 1P
during rekey capture, because `awk -F= '/^uk=/{print $2}'` splits
on `=` characters and returns only the field between the first two,
dropping any padding `=` at the end. Base64 decode of the 43-char
form still gave the correct 32 bytes (padding is optional in
`RawStdEncoding` and forgiving in most decoders), so the cluster
survived; the stored value was rewritten with the padding restored
for canonical hygiene. Fix: use `cut -d= -f2-` (which keeps
everything after the first `=`) or `sed 's/^uk=//'`.

## The break-glass CA

Minted P-384 self-signed root, five-year validity:

    fingerprint  71:D6:EE:B6:E1:93:78:F6:70:05:72:1D:F4:BD:24:3A:B7:C3:9A:91:28:FE:A2:D2:60:E5:B8:8F:0F:1E:0F:15
    subject      CN=weftspun-fdb-ca, O=chibifire
    algorithm    ECDSA P-384

Stored to 1Password: `FDB-CA cert` (uuid
`iwkxxgvlszvnidwfscr6asctpm`), `FDB-CA key` (uuid
`nkrahus5ruqycjqa2i3jsswd5y`). The leaves the run mints are P-256,
two-year, CN `fdb-<machine_id>.chibifire.com`, matching
`WEFT_FDB_TLS_VERIFY` (`S.CN>=fdb-,S.CN<=.chibifire.com`).

The break-glass CA does not become the cluster CA. Once Bao is
unsealed against the restored FDB, RFD 2141's phases 2–3 rotate every
leaf to a certificate signed by the CA Bao's PKI mount holds, and
`FDB_TLS_CA_B64` drops the break-glass anchor. The break-glass CA in
1P stays as a break-glass CA, for the next DR.

## The recovery, step by step

    T+0     fly apps create weftspun-fdb --org personal
    T+2m    fly secrets set --stage: R2_* (from op://), WEFT_FDB_CLUSTER_ID
    T+3m    First deploy: WEFT_FDB_MACHINES=1, WEFT_FDB_RESET=1, no TLS
            → machine 8d1d2ebed71158 allocated
    T+8m    Mint leaf for 8d1d2ebed71158 under break-glass CA
            fly secrets set --stage: FDB_TLS_CA_B64, FDB_TLS_CERT_*, FDB_TLS_KEY_*
            Second deploy: same env, TLS secrets active → cluster reforms mTLS
    T+9m    fdbcli status: "The database is available."
    T+10m   fdbbackup describe -d $R2_URL: Restorable: true
    T+10m   fdbrestore start -w -r $R2_URL

The full T+ timeline for the rest — Bao restore, cert rotation, scale
to three, key rotation — lands as it happens in
`logbook-rfd2144-dr-runbook-first-run.md`.

## What this RFD does not cover

- **A second DR without a running desk.** This run had a laptop with
  `op`, `fly`, and `openssl`. A DR where the laptop is also gone needs
  a break-glass laptop image, and RFD 2143's cross-region point holds.
- **Backup encryption at rest.** RFD 2143 named this as future work
  and it stays so. R2's copy of Bao's mount metadata is unencrypted.
- **Recovering `chibifire-com`.** The domain and cert setup was not
  part of this run; recreating it is a separate task.
