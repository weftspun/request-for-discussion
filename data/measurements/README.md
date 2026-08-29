# Measurements: rfd/0096 through rfd/0103

Raw timing, size and capability data behind those records. Parquet,
zstd, essential tuple normal form.

Rebuild with `python3 build.py out`. It needs only `duckdb`.

## Why six files and not one

The obvious shape is one wide `measurement` table with columns for
latency, throughput, size and capability, most of them null on any row.

That table carries an explicit join dependency that no superkey
implies, so it has redundancy and update anomalies. The kernel version
would repeat on every latency row, and correcting it would mean
touching all of them.

Splitting by fact type removes that. Each relation below has a key that
determines every non-key attribute, and none decomposes further without
losing a join dependency.

| Relation       | Key                          | Determines                                              |
| -------------- | ---------------------------- | ------------------------------------------------------- |
| `run`          | `run_id`                     | host class, region, machine type, vcpus, memory, kernel |
| `run_software` | `run_id, component`          | version                                                 |
| `latency`      | `run_id, subject, operation` | median, p99, min, samples                               |
| `throughput`   | `run_id, concurrency`        | ops, aborts, seconds                                    |
| `size`         | `run_id, subject, metric`    | bytes                                                   |
| `capability`   | `run_id, probe`              | result, detail                                          |

`build.py` checks that no child row references a missing `run_id`, and
fails rather than writing if one does.

## Conventions

**Latency is nanoseconds everywhere.** The smallest value here is 110
and the largest is 45259000. One unit across that range removes a
conversion error in the reader.

**Sizes are bytes.** Not KB, not MB.

**A null `median_ns` means the run did not finish.** It does not mean
zero. The busy-polled shared-memory ring on `shared-cpu-1x` is that
case, and `capability` records it as `timeout` with the reason.

**`ops_per_sec` is not stored.** It is `ops / seconds`, and storing a
derived column invites the two disagreeing.

## Reading it

```sql
-- throughput against machine size
SELECT r.host_class, r.vcpus, t.concurrency,
       t.ops / t.seconds AS ops_per_sec, t.aborts
FROM read_parquet('throughput.parquet') t
JOIN read_parquet('run.parquet') r USING (run_id)
ORDER BY r.vcpus, t.concurrency;
```

```sql
-- every point-read engine, fastest first
SELECT subject, operation, median_ns / 1e6 AS median_ms, samples
FROM read_parquet('latency.parquet')
WHERE operation LIKE 'point_%'
ORDER BY median_ns;
```

## What each run is

| `run_id`            | What                                                               |
| ------------------- | ------------------------------------------------------------------ |
| `fly-shared-1x-256` | Fly `shared-cpu-1x` 256 MB, `iad`, transport and capability probes |
| `fly-shared-1x-1g`  | Fly `shared-cpu-1x` 1 GB, `iad`, TPC-C scaling                     |
| `fly-6pn-pair`      | Two Fly machines in `iad` over 6PN                                 |
| `local-16core`      | 16-core workstation, container on WSL2                             |
| `ci-container`      | `zsh2o-ci` image, FoundationDB colocated                           |

Every Fly app was destroyed after its run.

## Caveats that the numbers do not carry

`ci-container` runs put FoundationDB and the load generator on the same
host, so no network hop is included.

Single-node FoundationDB has no replication. A `double` or `triple`
cluster commits slower.

`frl_4_3_6_0` and `frl_4_12_18_0` were measured through the JDBC
driver. `ecto-fdb-relational` v0.2 removed that transport, so those
rows describe the server rather than that adapter's current path.

The `fly-shared-1x-256` transport rows and the `local-16core` transport
rows are not the same hardware, and the ring result inverts between
them for that reason.
