# Logbook: two checks, a stopped backup, and curl's signing limits

Question: logbook-rfd2134 left backup liveness as a hand check. What
did closing that item find, and does the resulting gate hold a deploy?

This closes that entry's open item. Constraint set by the operator:
CI has no production access, and the spend keeper's authority must not
grow a monitoring pattern, so the checks run on the cluster machines,
where the credentials already are (RFD 2135).

## The apparatus

weftspun-fdb (3 machines, double, mutual TLS), datasource-store PRs
#6 through #9, foundationdb 7.3.76, curl 7.88 (bookworm), busybox
httpd, Fly machine checks. Rehearsals in local Docker on
debian:bookworm-slim.

## Finding: fdbbackup start defaults to stop-when-done

Two production submissions self-completed at their first restorable
point. The probe's running_backup guard caught both:
`running=false seconds_behind=122`: a lag that still read healthy on
a backup that had quietly finished. Continuous requires `-z`. With it,
`running_backup: true` and the lag settled to 16.6 seconds. Every
earlier "in progress" report, including the local versitygw runs, had
been a backup on its way to stopping.

## Finding: curl 7.88 signs SigV4 queries unsorted and unencoded

The first freshness probe listed the bucket. The matrix, run against
Tigris through the hop:

    query                                        result
    list-type=2&max-keys=8                       200
    list-type=2&prefix=data&max-keys=3           403 SignatureDoesNotMatch
    list-type=2&max-keys=3&prefix=data           200
    ...&prefix=data/  (sorted, raw slash)        403
    ...&prefix=data%2F (sorted, encoded slash)   403
    continuation-token=... (sorted, encoded)     403

Parameters must be pre-sorted, and no value may need encoding, which
rules out slashes in prefixes and every continuation token. A probe
that cannot paginate cannot find the newest object, so the shipped
probe reads `status json` instead: `last_restorable_seconds_behind`
(advances only after durable blob writes) plus `running_backup`.
The working hand-checks had been accidentally alphabetical.

## Finding: the roll gate holds

`cluster_health` fails until the data state is healthy and
`max_zone_failures_without_losing_data` is at least 1. On its own
deploy, after each machine restart the log shows
`data_healthy=no zone_tolerance=1`, the re-replication window in
which a second restart would stall shards under double redundancy,
and the roll waited. All three machines converged to 2 of 2 checks
passing.

## The volumes, while the hood was open

944 MB of disk used against 0 MB of key-value data (disk-queue
preallocation, two fdbserver processes per machine), 0.4 GB free on
the fullest storage server. All three volumes extended 1 GB to 10 GB
in place, filesystem grown online, no restart: 3% used after.

## What is still open

Nothing pages. RFD 2135's duty-hours section argues that is correct
for a one-operator shop (fail-closed over fail-alerting) and names
the two conditions under which paging becomes worth adding.
