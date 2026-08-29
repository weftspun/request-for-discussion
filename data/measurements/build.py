#!/usr/bin/env python3
"""
Emit this session's measurements as Parquet, zstd, in essential tuple
normal form.

ETNF matters here for a specific reason. The obvious shape is one wide
"measurement" table with columns for latency, throughput, size and
capability, most of them null on any given row. That table has an
explicit join dependency that no superkey implies, so it carries
redundancy and update anomalies: the machine's kernel version would
repeat on every latency row, and a correction would have to touch all
of them.

Splitting by fact type fixes that. Each relation below has a key that
determines every non-key attribute, and none decomposes further without
losing a join dependency.

  run           run_id                       -> host and machine facts
  run_software  (run_id, component)          -> version
  latency       (run_id, subject, operation) -> median, p99, min, samples
  throughput    (run_id, concurrency)        -> ops, aborts, seconds
  size          (run_id, subject, metric)    -> bytes
  capability    (run_id, probe)              -> result, detail

Units are explicit in column names. Latency is nanoseconds because the
smallest measurement here is 90 ns and the largest is 68 ms, and one
unit across that range avoids a conversion error in the reader.

A null in `median_ns` means the run did not finish, not that it took
zero. `capability.result` carries that case for the busy-poll ring.
"""
import duckdb, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
con = duckdb.connect()

# ---------------------------------------------------------------- run
runs = [
    # run_id, host_class, region, machine_type, vcpus, memory_kb, kernel, note
    ("fly-shared-1x-256",  "fly",   "iad", "shared-cpu-1x", 1,  212188, "6.12.91-fly",
     "rfd/0096 transport probe, 256 MB"),
    ("fly-shared-1x-1g",   "fly",   "iad", "shared-cpu-1x", 1, 1048576, "6.12.91-fly",
     "tpcc scaling probe, 1 GB"),
    ("fly-6pn-pair",       "fly",   "iad", "shared-cpu-1x", 1,  212188, "6.12.91-fly",
     "rfd/0096 two machines over 6PN"),
    ("local-16core",       "local", None,  "workstation",  16, 65793648, "6.18.33.1-microsoft-standard-WSL2",
     "container on WSL2"),
    ("ci-container",       "local", None,  "container",    16, 65793648, "6.18.33.1-microsoft-standard-WSL2",
     "zsh2o-ci image, FoundationDB colocated"),
]
con.execute("""CREATE TABLE run(
  run_id VARCHAR PRIMARY KEY, host_class VARCHAR, region VARCHAR,
  machine_type VARCHAR, vcpus INTEGER, memory_kb BIGINT,
  kernel VARCHAR, note VARCHAR)""")
con.executemany("INSERT INTO run VALUES (?,?,?,?,?,?,?,?)", runs)

# ------------------------------------------------------- run_software
software = [
    ("ci-container", "foundationdb", "7.3.43"),
    ("ci-container", "postgresql", "16"),
    ("ci-container", "duckdb", "1.x"),
    ("ci-container", "fdb-relational-server", "4.12.18.0"),
    ("ci-container", "openjdk", "21.0.11"),
    ("ci-container", "zstd", "libzstd"),
    ("local-16core", "foundationdb", "7.3.43"),
    ("local-16core", "ecto_foundationdb", "0.7.6"),
    ("local-16core", "erlfdb", "1.2.1"),
    ("local-16core", "elixir", "1.17.3"),
    ("fly-shared-1x-1g", "foundationdb", "7.3.43"),
    ("fly-shared-1x-1g", "ecto_foundationdb", "0.7.6"),
    ("fly-shared-1x-1g", "erlfdb", "1.2.1"),
    ("fly-shared-1x-1g", "elixir", "1.17.3"),
]
con.execute("""CREATE TABLE run_software(
  run_id VARCHAR, component VARCHAR, version VARCHAR,
  PRIMARY KEY (run_id, component))""")
con.executemany("INSERT INTO run_software VALUES (?,?,?)", software)

# ------------------------------------------------------------ latency
# (run_id, subject, operation, median_ns, p99_ns, min_ns, samples)
latency = [
    # rfd/0096 guest transport
    ("fly-shared-1x-256", "af_unix", "seqpacket_rtt",   8910,  48000,  8750, 20000),
    ("fly-shared-1x-256", "af_unix", "stream_rtt",      9520,  28860,  9210, 20000),
    ("local-16core",      "af_unix", "seqpacket_rtt",  59821,   None, None, 20000),
    ("local-16core",      "af_unix", "stream_rtt",     50181,   None, None, 20000),
    ("local-16core",      "shm_ring", "busypoll_rtt",     110,    110,   90, 20000),
    # rfd/0096 6PN, 100-byte payload
    ("fly-6pn-pair", "6pn", "udp_rtt_peer_a",   879700, 2332600, None, 498),
    ("fly-6pn-pair", "6pn", "udp_rtt_peer_b",   833800, 1873400, None, 500),
    ("fly-6pn-pair", "6pn", "udp_rtt_loopback",  19300,    None, None, 500),
    ("fly-6pn-pair", "6pn", "udp_rtt_loopback_b",21400,    None, None, 500),
    # rfd/0097 FoundationDB as a bus
    ("ci-container", "fdb_memory_engine", "commit",              2975300, 3872000, None, 300),
    ("ci-container", "fdb_ssd_engine",    "commit",              2396600, 3071000, None, 300),
    ("ci-container", "fdb_memory_engine", "watch_fire",         12115100,13873700, None, 100),
    ("ci-container", "fdb_ssd_engine",    "watch_fire",         12053100,13439500, None, 100),
    ("ci-container", "fdb_memory_engine", "versionstamp_append", 2521900, 3635100, None, 300),
    ("ci-container", "fdb_ssd_engine",    "versionstamp_append", 2952700, 3876800, None, 300),
    # rfd/0098 libriscv snapshot
    ("ci-container", "libriscv_script_guest", "serialize_to",       800,   1200, None, 200),
    ("ci-container", "libriscv_script_guest", "deserialize_from",  1900,   7300, None, 200),
    ("ci-container", "libriscv_script_guest", "fork_construct",     300,    500, None, 200),
    ("ci-container", "libriscv_engine_guest", "serialize_to",  12370200,17063000, None, 200),
    ("ci-container", "libriscv_engine_guest", "deserialize_from",15227000,20206500,None, 200),
    ("ci-container", "libriscv_engine_guest", "fork_construct",   384200, 976900, None, 200),
    # rfd/0101 zstd wire, compression CPU
    ("ci-container", "zstd_l1_nodict",      "compress_frame",  42400, None, None, 400),
    ("ci-container", "zstd_l3_nodict",      "compress_frame",  44800, None, None, 400),
    ("ci-container", "zstd_l1_prefix_prev", "compress_frame",  63300, None, None, 399),
    ("ci-container", "zstd_l3_prefix_prev", "compress_frame",  66500, None, None, 399),
    ("ci-container", "zstd_l1_prefix_ack2", "compress_frame",  68000, None, None, 398),
    ("ci-container", "zstd_l1_prefix_ack4", "compress_frame",  68200, None, None, 396),
    ("ci-container", "zstd_l1_prefix_ack8", "compress_frame",  63900, None, None, 392),
    ("ci-container", "zstd_prefix",         "decompress_frame",17300, None, None, 400),
    # rfd/0103 relational engines, point operations
    ("ci-container", "postgresql16",  "point_select",     84000,  None, None, 1),
    ("ci-container", "duckdb",        "point_select",    919100,  None, None, 1000),
    ("ci-container", "duckdb",        "point_update",   1190400,  None, None, 1000),
    ("ci-container", "duckdb",        "scan_200k",      3500000,  None, None, 1),
    ("ci-container", "duckdb",        "read_parquet",   1000000,  None, None, 1),
    ("ci-container", "fdb_c_client",  "point_get_newtxn", 405000, 532000, None, 2000),
    ("ci-container", "fdb_c_client",  "point_get_sharedtxn",157000,269000,None, 2000),
    ("ci-container", "frl_4_3_6_0",   "point_select_20k", 45259000,66866000,None,1000),
    ("ci-container", "frl_4_3_6_0",   "point_select_2k",  12779000,31740000,None, 300),
    ("ci-container", "frl_4_12_18_0", "point_select_2k",   8632000,13272000,None, 300),
    ("ci-container", "frl_4_3_6_0",   "insert_row",       14080000, None, None,2000),
    ("ci-container", "frl_4_12_18_0", "insert_row",       15920000, None, None,2000),
    # ecto_foundationdb, TPC-C shape
    ("local-16core", "ecto_foundationdb", "indexed_query",     558000,  800000, None, 300),
    ("local-16core", "ecto_foundationdb", "read_modify_write",3548000, 5022000, None, 300),
]
con.execute("""CREATE TABLE latency(
  run_id VARCHAR, subject VARCHAR, operation VARCHAR,
  median_ns BIGINT, p99_ns BIGINT, min_ns BIGINT, samples INTEGER,
  PRIMARY KEY (run_id, subject, operation))""")
con.executemany("INSERT INTO latency VALUES (?,?,?,?,?,?,?)", latency)

# --------------------------------------------------------- throughput
# ecto_foundationdb read-modify-write, 1000 districts over 100 warehouses
throughput = [
    ("fly-shared-1x-1g", 1,  4014, 0, 10.00),
    ("fly-shared-1x-1g", 2,  8840, 0, 10.00),
    ("fly-shared-1x-1g", 4, 14487, 0, 10.00),
    ("fly-shared-1x-1g", 8, 16081, 0, 10.01),
    ("fly-shared-1x-1g",16, 17633, 0, 10.01),
    ("fly-shared-1x-1g",32, 21677, 0, 10.04),
    ("local-16core",     1,  2774, 0, 10.00),
    ("local-16core",     2,  6325, 0, 10.00),
    ("local-16core",     4, 12433, 0, 10.00),
    ("local-16core",     8, 21597, 0, 10.00),
    ("local-16core",    16, 44690, 0, 10.03),
    ("local-16core",    32, 61108, 0, 10.04),
]
con.execute("""CREATE TABLE throughput(
  run_id VARCHAR, concurrency INTEGER,
  ops BIGINT, aborts BIGINT, seconds DOUBLE,
  PRIMARY KEY (run_id, concurrency))""")
con.executemany("INSERT INTO throughput VALUES (?,?,?,?,?)", throughput)

# --------------------------------------------------------------- size
size = [
    ("ci-container", "libriscv_script_guest", "elf_bytes",           4016),
    ("ci-container", "libriscv_script_guest", "snapshot_bytes",     41864),
    ("ci-container", "libriscv_engine_guest", "elf_bytes",       84982776),
    ("ci-container", "libriscv_engine_guest", "snapshot_bytes",  67148424),
    ("ci-container", "zstd_raw",              "frame_bytes",        44800),
    ("ci-container", "zstd_l1_nodict",        "frame_bytes",         3727),
    ("ci-container", "zstd_l3_nodict",        "frame_bytes",         3239),
    ("ci-container", "zstd_l1_prefix_prev",   "frame_bytes",         2980),
    ("ci-container", "zstd_l3_prefix_prev",   "frame_bytes",         2774),
    ("ci-container", "zstd_l1_prefix_ack2",   "frame_bytes",         3014),
    ("ci-container", "zstd_l1_prefix_ack4",   "frame_bytes",         3015),
    ("ci-container", "zstd_l1_prefix_ack8",   "frame_bytes",         3006),
    ("ci-container", "duckdb",                "parquet_200k_bytes", 320000),
    ("ci-container", "duckdb",                "peak_rss_bytes",  108984730),
    ("ci-container", "fdb_relational_server", "rss_bytes",       164626432),
    ("ci-container", "postgresql16",          "table_200k_bytes",16777216),
]
con.execute("""CREATE TABLE size(
  run_id VARCHAR, subject VARCHAR, metric VARCHAR, bytes BIGINT,
  PRIMARY KEY (run_id, subject, metric))""")
con.executemany("INSERT INTO size VALUES (?,?,?,?)", size)

# --------------------------------------------------------- capability
capability = [
    ("fly-shared-1x-256", "bwrap_unshare_all_root",   "pass", None),
    ("fly-shared-1x-256", "bwrap_unshare_net",        "pass", None),
    ("fly-shared-1x-256", "bwrap_unprivileged_uid1000","pass", None),
    ("fly-shared-1x-256", "ifaces_inside_unshare_net","pass", "1 link"),
    ("fly-shared-1x-256", "ifaces_outside",           "pass", "4 links"),
    ("fly-shared-1x-256", "io_uring_setup",           "pass", "fd 3"),
    ("fly-shared-1x-256", "io_uring_disabled_sysctl", "pass", "0"),
    ("fly-shared-1x-256", "memfd_create",             "pass", None),
    ("fly-shared-1x-256", "udp_bind_in6addr_any",     "pass", "binds, wrong reply source per Fly"),
    ("fly-shared-1x-256", "fly_global_services",      "pass", "172.19.15.243 AF_INET"),
    ("local-16core",      "bwrap_unshare_all_root",   "fail", "docker blocks userns"),
    ("local-16core",      "io_uring_setup",           "fail", "EPERM, docker seccomp"),
    ("local-16core",      "shm_ring_busypoll_20k",    "pass", None),
    ("fly-shared-1x-256", "shm_ring_busypoll_20k",    "timeout", "no completion in >8 min, both procs R at 24% cpu"),
    ("ci-container",      "fdb_watch_limit",          "limit", "10000 then error 1032 too_many_watches"),
    ("ci-container",      "libriscv_determinism_script","pass","two replays byte identical"),
    ("ci-container",      "libriscv_determinism_engine","pass","two replays byte identical"),
    ("ci-container",      "libriscv_serialize_flat_arena","fail","FEATURE_DISABLED, needs use_memory_arena=false"),
    ("ci-container",      "frl_setautocommit_4_3_6_0","fail", "Not implemented setAutoCommit"),
    ("ci-container",      "frl_setautocommit_4_12_18_0","pass", None),
    ("ci-container",      "frl_update_planner_4_12_18_0","fail","SemanticException, operands not compatible"),
    ("local-16core",      "efdb_composite_primary_key","fail","MatchError on [:d_id, :d_w_id]"),
    ("local-16core",      "efdb_multifield_index_fdb71","fail","ArgumentError in erlfdb_transaction_get_mapped_range"),
    ("local-16core",      "efdb_multifield_index_fdb73","pass","1 row, either field order"),
]
con.execute("""CREATE TABLE capability(
  run_id VARCHAR, probe VARCHAR, result VARCHAR, detail VARCHAR,
  PRIMARY KEY (run_id, probe))""")
con.executemany("INSERT INTO capability VALUES (?,?,?,?)", capability)

# ------------------------------------------------------------- verify
for t in ("run", "run_software", "latency", "throughput", "size", "capability"):
    n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    orphans = 0
    if t != "run":
        orphans = con.execute(
            f"SELECT count(*) FROM {t} WHERE run_id NOT IN (SELECT run_id FROM run)"
        ).fetchone()[0]
    print(f"{t:14} rows={n:4}  orphan_run_id={orphans}")
    if orphans:
        sys.exit(f"referential integrity failed in {t}")

os.makedirs(OUT, exist_ok=True)
for t in ("run", "run_software", "latency", "throughput", "size", "capability"):
    con.execute(
        f"COPY {t} TO '{OUT}/{t}.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    print(f"wrote {OUT}/{t}.parquet  {os.path.getsize(f'{OUT}/{t}.parquet')} bytes")
