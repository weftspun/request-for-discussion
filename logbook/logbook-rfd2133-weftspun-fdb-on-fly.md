# Logbook: minimum-double weftspun-fdb on Fly

Question: what does the smallest FoundationDB cluster that survives a
single-machine loss cost, and does datasource-store's existing recipe
stand it up unchanged.

## The apparatus

Fly.io, org `personal` (`k-s-ernest-ifire-lee`), region `sjc`. The image
is built from `6-datasource/store` at HEAD of `weftspun/main` (the CBOR
read-reply merge is in this HEAD but does not exercise here — that is
`store.cpp`, not `fdbserver`). `fly/fdb.toml` and
`fly/fdb-entrypoint.sh` unchanged from what the repository ships.

## What was done

    cd 6-datasource/store
    fly launch --config fly/fdb.toml --copy-config \
      --dockerfile fly/Containerfile.fdb \
      --name weftspun-fdb --region sjc --org personal --no-deploy --yes

    fly secrets set WEFT_FDB_CLUSTER_ID="$(openssl rand -hex 8)" \
      --app weftspun-fdb --stage

    for i in 1 2 3; do
      fly volumes create fdb_data --app weftspun-fdb --region sjc --size 1 --yes
    done

    fly deploy --config fly/fdb.toml --app weftspun-fdb --remote-only --ha=false

    fly scale count 3 --app weftspun-fdb --region sjc --yes
    fly machine start <the two `created` machines>   # scale leaves them stopped

## The measurement

Three machines, `shared-cpu-2x`, 2 GiB each, one 1 GiB `fdb_data` volume
per machine. Time from `fly deploy` to `[entrypoint] The database is
available` was under 30 seconds; the entrypoint's peer-discovery poll saw
`3 of 3 machines` at t=+9s, wrote the coordinator list, and
`configure new double ssd` reported `Database created` at t=+11s.

Cluster file:

    weft:f5d800cd147f561a@[fdaa:0:5132:a7b:167:d7c3:dd2:2]:4500,
                         [fdaa:0:5132:a7b:16f:3c5b:597a:2]:4500,
                         [fdaa:0:5132:a7b:5a3:6d12:8e67:2]:4500

TLS is off. The entrypoint logs it: `TLS off: no FDB_TLS_CERT_B64. Every
byte between these processes is in the clear.` That is the recorded
trade for standing this cluster up without a certificate flow, and it is
the reason there are no `[[services]]` and no public address: the only
reachable network is 6PN inside this org.

## What did not go as planned

**`fly launch --copy-config` rewrote the repo's fly/fdb.toml in place**:
it flattened the file, stripped every comment — including the S.CN
matcher retraction the file exists to carry — broke the dockerfile path
(prefixing a second `fly/`), and injected an `[http_service]` block with
`auto_stop_machines`, which is how the cluster's three machines later
got idle-stopped out from under a quorum. The deploy errors that
followed ("dockerfile not found: fly/fly/Containerfile.fdb"; the stopped
cluster) were all downstream of that one rewrite. The fix was
`git checkout -- fly/fdb.toml` and deploying with the repository's own
file, which was correct all along. Lesson: `fly launch` writes to the
config path it is given; point it at a scratch copy, never at a tracked
file that carries reasoning.

`fly scale count 3` created two more machines but left them in `created`
state. `fly machine start <id>` on each. The first retry failed with
`failed_precondition: unable to start machine from current state:
'created'` because the previous start had not fully released; a few
seconds' wait cleared it.

## What this settles

The existing recipe stands up minimum-double FDB unchanged, minus the
one path-resolution edit above. `WEFT_FDB_REDUNDANCY` defaults to
`double` in the entrypoint, `configure new double ssd` runs on the first
machine to reach the "database created" branch, and `locality_zoneid =
FLY_MACHINE_ID` gives each machine a distinct zone — so double keeps two
copies of every key and can lose one machine.

## What is still open

Backup. `fdbbackup start -d blobstore://... -w` is what makes the
cluster's pages durable outside itself, and this deploy has no blob-store
credentials set — the entrypoint logs `no blob store: backup is not
configured on this machine`. Wiring `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY` and `AWS_ENDPOINT_URL_S3` as secrets is the next
step to make this cluster survive its own machines. See
[FDB backups](https://apple.github.io/foundationdb/backups.html).
