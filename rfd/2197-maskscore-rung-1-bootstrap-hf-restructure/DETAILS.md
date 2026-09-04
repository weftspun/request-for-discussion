# maskscore-rung-1-bootstrap HF restructure: join plan and media strategy

## Amendment 2026-09-04: join keys, speech schema, media budget

The measurement that supersedes the join plan and media strategy below is
in `logbook/logbook-maskscore-rung-1-join-keys.md`. Read that entry before
touching a rewrite. What changed against the original draft:

1. **Base ⋈ candidates join key** is `base.key = candidates.row_key`, not
   `example_id`. Different column names on the two sides, same semantic
   values, 100 % membership every task.
2. **Candidates ⋈ scores join key** is composite `(row_key, candidate)` for
   the five non-speech tasks, `(row_key, candidate_axis)` for speech. There
   is no single `candidate_id` column.
3. **Speech is a schema variant**, not one more task-name in the same list.
   Different filename glob (`maskscore_speech*`, no `rung_1` prefix),
   different location (`speech/speech/`), different candidate column
   (`candidate_axis`), different score schema (long
   `metric_name`/`metric_value` vs the non-speech wide
   `view_index`/`depth_l1`/`normal_l1`/`normal_dot`), different base
   extras (`canonical_text` vs `poses`). Own emit branch, not a switch on
   task-name.
4. **Scores per candidate is `list<struct>`**. 64 per-view records per
   candidate for non-speech (from `view_index`), 15 per-metric records for
   speech (from `metric_name`/`metric_value`). Not one score row per
   candidate.
5. **Media budget** at bootstrap scale is under 50 KB total parquet
   payload. The 20 wide rows across the whole dataset (5 non-speech tasks
   at 1 base row each, plus 15 speech rows) make the earlier ~300 MB
   estimate wrong by orders of magnitude. Storage question is trivial;
   viewer-rendering question is unchanged.
6. **Join-key check** as originally scripted uses
   `set(base.columns) & set(cands.columns)`. That returns empty for every
   task, since the two sides use different names for the same semantic
   key, and under the RFD's own fallback ("publish the base table alone")
   would drop candidates+scores from the first pass. Wrong outcome on
   clean data. The check must become: per-task expected join columns
   exist by name, and their value-sets match.

The rest of this file is the original draft, kept for the record.
Sections superseded by the measurement carry a pointer at the top rather
than reflowing in place, so citations of the RFD's earlier wording still
resolve.

## Current shape (observed 2026-09-03)

The HF repo `chibifire/maskscore-rung-1-bootstrap` currently holds:

```
maskscore_rung_1_<task>.parquet             ×5   # base tables (non-speech)
maskscore_rung_1_<task>_candidates.parquet  ×5   # candidate generations per row
maskscore_rung_1_<task>_scores.parquet      ×5   # scores per candidate

speech/speech/maskscore_speech.parquet             # base (speech)
speech/speech/maskscore_speech_candidates.parquet  # cand (speech)
speech/speech/maskscore_speech_scores.parquet      # scores (speech)

renders/  ×512                                     # PNG render frames
speech/   ×351   ( 150 WAV, 180 VTT, 21 other )    # aligned audio + captions
poses/    ×4                                       # PNG pose overlays
scores/   ×2                                       # ancillary score dumps
```

Total 887 files, 18 parquets. 15 parquets at repo root, 3 under
`speech/speech/`. No `data/` directory. HF viewer sees no auto-indexer
layout it can group and returns `viewer=false, preview=false`.

The original draft placed all 18 parquets at repo root. Corrected above.

## Target shape

```
data/depth/train-*.parquet          # base ⋈ candidates ⋈ scores, wide row
data/keypoints/train-*.parquet
data/mesh/train-*.parquet
data/multimodal/train-*.parquet
data/pose/train-*.parquet
data/speech/train-*.parquet         # separate emit branch, see below
```

Six configs (one per task-type) under a single dataset repo. Each config
paginates independently in the viewer. Row shape per non-speech config:

| field          | type                                     | notes                                                          |
| -------------- | ---------------------------------------- | -------------------------------------------------------------- |
| `key`          | string                                   | from base; joins to `row_key` on candidates                    |
| `task_type`    | string                                   | from base (constant per config; keep to satisfy viewer schema) |
| `dimension`    | string                                   | from base                                                      |
| `input_column` | string                                   | from base                                                      |
| `input_asset`  | (binary or string ref)                   | from base; media strategy applies                              |
| `input_asset_kind` | string                               | from base                                                      |
| `poses`        | (task-specific)                          | from base                                                      |
| `candidates`   | `list<struct<candidate, rank, candidate_asset, scores: list<struct<view_index, depth_l1, normal_l1, normal_dot>>>>` | from candidates, with scores folded in per `(row_key, candidate)` |

Row shape for the speech config differs on three axes:

| field          | type                                     | notes                                                          |
| -------------- | ---------------------------------------- | -------------------------------------------------------------- |
| `key`          | string                                   | joins to `row_key`                                             |
| `task_type`    | string                                   | constant                                                       |
| `dimension`    | string                                   |                                                                |
| `input_column` | string                                   |                                                                |
| `input_asset`  | (media)                                  |                                                                |
| `input_asset_kind` | string                               |                                                                |
| `canonical_text` | string                                 | speech-only                                                    |
| `candidates`   | `list<struct<candidate_axis, rank, candidate_asset, candidate_asset_kind, candidate_kind, candidate_target_text, scores: list<struct<candidate_rank, metric_name, metric_value>>>>` | scores fold in per `(row_key, candidate_axis)`; note the score inner schema is long-form (metric_name/metric_value), not wide |

Nested lists preserve the one-to-many without dropping to satellite files
(RFD 2196 rule 1). The `struct-of-lists` vs `list-of-struct` question is
settled by RFD 2196 rule 6: pick the shape the parquet actually holds and
declare it that way in `dataset_info.features`.

## The join plan

For each non-speech task-type, three tables become one:

```python
base   = pq.read_table(f'maskscore_rung_1_{task}.parquet').to_pandas()
cands  = pq.read_table(f'maskscore_rung_1_{task}_candidates.parquet').to_pandas()
scores = pq.read_table(f'maskscore_rung_1_{task}_scores.parquet').to_pandas()

# scores → nested list per (row_key, candidate)
scores_by_pair = scores.groupby(['row_key', 'candidate']).apply(
    lambda g: g.drop(columns=['row_key', 'candidate']).to_dict('records')
).rename('scores')

# candidates → nested list per row_key, with scores folded in per pair
def build_candidates(g):
    out = []
    for _, r in g.iterrows():
        rec = r.drop(labels=['row_key']).to_dict()
        rec['scores'] = scores_by_pair.get((r['row_key'], r['candidate']), [])
        out.append(rec)
    return out

cands_by_rk = cands.groupby('row_key').apply(build_candidates).rename('candidates')

# base has one row per key; join on base.key = cands.row_key
wide = base.set_index('key').join(cands_by_rk, how='left')
```

Speech uses the same shape with three substitutions: file glob is
`speech/speech/maskscore_speech*`, `candidate` becomes `candidate_axis`
in every occurrence, and the score inner schema is
`candidate_rank`/`metric_name`/`metric_value` instead of
`view_index`/`depth_l1`/`normal_l1`/`normal_dot`.

Join-key verification gate before running the rewrite, per task:

- assert `'key' in base.columns` and `'row_key' in cands.columns and
  'row_key' in scores.columns`;
- assert `set(base['key']) == set(cands['row_key'])` and
  `set(cands[['row_key', <cand_col>]].itertuples(index=False))
   >= set(scores[['row_key', <cand_col>]].itertuples(index=False))`.

The empty-column-intersection fallback the original draft named ("publish
the base table alone per config") is not the failure mode on this data.
The keys align cleanly under the corrected names.

## Media strategy

887 non-parquet files sit outside the parquet columns today. The
disposition per file kind is unchanged from the original draft:

| kind             | count      | strategy                                                                                                                     |
| ---------------- | ---------: | ---------------------------------------------------------------------------------------------------------------------------- |
| `renders/*.png`  | 512 + 128  | inline as `struct<bytes, path>` per RFD 2196 rule 4 if under ~1 MB each; else keep at path, add column `image_path: string`  |
| `speech/*.wav`   | 150        | inline as `struct<bytes, path>` with `bytes: binary`; viewer plays audio inline                                              |
| `speech/*.vtt`   | 180        | inline as `text: string` column (WebVTT is small text)                                                                       |
| `poses/*.png`    | 4          | inline                                                                                                                       |
| `scores/*.*`     | 2          | fold into the scores column of the row if applicable, else document as ancillary                                             |

The join step reads media by path and embeds bytes into the row it belongs
to (identified by filename stem matching the row key). Files whose row
key cannot be inferred stay at their satellite path and get named in the
dataset card as unreferenced-but-preserved.

Inline media budget at bootstrap scale: 20 wide rows across the whole
dataset. Under 50 KB parquet payload before media inlining; well under
HF's per-shard limits regardless of media disposition. The original
~300 MB estimate was for a rung the bootstrap does not carry yet.

## Reference

The reference implementation script for the join + media inlining lives
alongside the source-of-truth generators, not in the dataset repo. Name
to be decided when the code is written; RFD 2165's stub-emit output
directory is the source path.

## The re-upload

Standard RFD 2196 rule 5 recipe:

```sh
HF_HUB_DISABLE_XET=1 HF_HUB_ENABLE_HF_TRANSFER=1 \
  hf upload-large-folder chibifire/maskscore-rung-1-bootstrap \
    upload_stage --repo-type=dataset --include="data/*/train-*.parquet"
```

The old root-level parquets and the `speech/speech/` parquets can be
deleted in the same commit that lands the new layout, since the viewer
will not index the old shape and consumers of the old shape (if any exist)
should read from the source-of-truth generators anyway.

## Estimated effort

- Verify join keys per task-type: 30 min (six tables, two checks each).
  Done 2026-09-04, results in the logbook entry.
- Write the join script per corrected spec: 2-4 h, including the
  speech-branch schema variant.
- Media inlining: 1-2 h.
- Re-upload + verify viewer: 1 h.
- **Total from here: half a day to a day.**
