---
name: vast-api-notes
description: Vast.ai HTTP API filter syntax + hot-band analysis method
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T02:46:18.911Z
---

Direct HTTP is the reliable path; the installed `vastai` CLI at
`~/Library/Python/3.9/bin/vastai` is broken (Python 3.9 can't parse
its `match` statements). Use `curl` against `console.vast.ai/api/v0/`
with `Authorization: Bearer $VAST_API_KEY`.

**API key** lives in OpenBao at `secret/vast/api_key`, field
`value`. Access via mTLS cert-auth as `vast-buyer` — see
[[openbao-address]] for the fly proxy + cert flow.

**Filter syntax on `/bundles/`:** GET with URL-encoded `q=<json>`.
Fields need `{"field":{"op":value}}` wrapper. `{"gpu_name":"X"}` and
POST-body `q` both return 0; only GET-with-`{"eq":...}` works.

Working RTX 3090 spec-filter:

    q={
      "gpu_name":{"eq":"RTX 3090"},"num_gpus":{"eq":1},
      "rentable":{"eq":true},"cuda_max_good":{"gte":12.4},
      "disk_space":{"gte":100},"reliability2":{"gte":0.98},
      "direct_port_count":{"gte":1},"limit":50,
      "order":[["dph_total","asc"]]
    }

**Total market ~4,000 rentable offers.** Server caps `limit` at
~4,010. One fetch gets the whole market.

**Cheapest-tier hosts often fail to spin** — two consecutive
`nvidia/cuda:12.4.0-base` rentals on bottom-price offers failed on
2026-09-01 (one "GPU error, unable to start instance", one image
never pulled). Skip rank 1-2 by dph; pick from rank 3-5 with
reliability >= 0.99.

**Cross-GPU-family value shape** (measured 2026-09-01, pooled 3
snapshots): best `$/dlperf-hour` in the market is on **RTX 4090**
($0.00128), not 3090 ($0.00162) or 5090 ($0.00162). 4090 at
$0.136/hr with dlperf=107 is the Pareto floor across all three.

**Hot band Wilson analysis:** `$0.18-$0.22` is the churn-hottest
band for single 3090s (Wilson 95%-lower 0.53), `$0.28-$0.35`
runner-up (0.47), `$0.10-$0.14` cool (0.28). Hot != efficient.

Market snapshots in ETNF Parquet at
`6-datasource/vast-market-snapshots/`; capture script is
`snapshot.py` in that dir.

Related: [[openbao-address]], [[hardware-pivot-2026-09-01]].
