# Logbook: chibifire/starforged HF dataset build

Published 2026-09-05 at
`https://huggingface.co/datasets/chibifire/starforged`. Built by
`2-contract/manuals-weftspun/scripts/build_starforged_hf.py` from
the `rsek/dataforged` community JSON of Shawn Tomkin's Starforged
SRD.

## Measurement

| stage | size | notes |
|---|---|---|
| Input: `dist/starforged/dataforged.json` | 5.1 MB | single-file JSON export from dataforged |
| Output: two-shard ZSTD parquet | 184 KB | `data/train-00000-of-00002.parquet` + `data/train-00001-of-00002.parquet` |
| **Reduction** | **~28×** | ZSTD level 9 on denormalized wide-row parquet |

Row count after the CC-BY-NC filter: **433** — 56 moves, 90
assets, 250 oracles, 23 encounters, 14 truths. Dropped rows
(CC-BY-NC-4.0 from the `ironsworn/` subtree): the count is
reported by the builder as a rule-3 named-not-silent gate;
recorded in the build log for the run that produced the published
shards.

Household anchor: 184 KB is about the size of a plain-text
paperback novel's worth of text; 5.1 MB is roughly a nickel of
disk (small enough that the reduction matters for viewer
latency, not for host cost).

## Apparatus

- **Row shape:** one wide row per logical content item; `kind`
  column keys the row type. Nested outcomes / abilities / oracle
  rolls stay inline as struct/list columns (per the
  `hf-datasets-no-etnf` skill).
- **Splits:** single `train` split. Rules corpus, not an ML
  training corpus.
- **Compression:** `pq.write_table(..., compression="zstd",
  compression_level=9)`.
- **Upload:** `hf-transfer`-enabled, per-shard incremental
  commits per the `hf-upload-incremental` skill.
- **Filter gate:** rows whose licence is CC-BY-NC-* are dropped
  before the parquet write; the count is printed.

## Viewer

Verified 2026-09-05: the first row loads in the HF viewer, the
`kind` filter surfaces the categories, nested outcomes render as
expandable JSON. Fixed one viewer error at publish
("size not coherent") by removing an unnecessary `configs:` block
from the README frontmatter — the auto-parquet indexer picks up
`data/train-*.parquet` on its own. Recorded as
[[hf-dataset-auto-parquet-no-configs]] in memory.

## Attribution

Dataset README and `CITATION.cff` name:

- Shawn Tomkin (author of the Starforged SRD), `ironswornrpg.com`,
  CC-BY-4.0.
- `rsek/dataforged` (community JSON rendering), MIT for
  scaffolding.

## Retractions

None. First publish.

## Related

- RFD 2205 (Taskweft in Bao) — the pilot the dataset supplies
  test vectors for.
- RFD 2209 (CC-BY-NC blocklist entry) — the doctrine the
  builder's filter enforces.
- `logbook-starforged-sqlite-build.md` — the SQLite mirror of
  the same content.
