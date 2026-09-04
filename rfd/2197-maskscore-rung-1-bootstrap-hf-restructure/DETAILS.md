# maskscore-rung-1-bootstrap HF restructure — join plan and media strategy

## Current shape (observed 2026-09-03)

The HF repo `chibifire/maskscore-rung-1-bootstrap` currently holds:

```
maskscore_rung_1_<task>.parquet             ×6   # base tables per task-type
maskscore_rung_1_<task>_candidates.parquet  ×6   # candidate generations per row
maskscore_rung_1_<task>_scores.parquet      ×6   # scores per candidate

renders/  ×512                                    # PNG render frames
speech/   ×351   ( 150 WAV, 180 VTT, 21 other )   # aligned audio + captions
poses/    ×4                                      # PNG pose overlays
scores/   ×2                                      # ancillary score dumps
```

Total 887 files, 18 parquets. All 18 parquets at repo root; no `data/`
directory. HF viewer sees no auto-indexer layout it can group and returns
`viewer=false, preview=false`.

## Target shape

```
data/depth/train-*.parquet          # base ⋈ candidates ⋈ scores, wide row
data/keypoints/train-*.parquet
data/mesh/train-*.parquet
data/multimodal/train-*.parquet
data/pose/train-*.parquet
data/speech-audio/train-*.parquet   # if speech is a task-type, else fold into multimodal
```

Six configs (one per task-type) under a single dataset repo. Each config
paginates independently in the viewer. Row shape per config:

| field | type | notes |
|---|---|---|
| `example_id` | string | join key across the three source tables |
| `input_*` | (task-specific) | from the base table |
| `candidates` | `list<struct<candidate_id, generation, ...>>` | from candidates table joined on example_id |
| `scores` | `list<struct<candidate_id, score, ...>>` | from scores table joined on candidate_id |
| media columns | see below | inline or referenced |

Nested lists preserve the one-to-many without dropping to satellite files
(RFD 2196 rule 1). The `struct-of-lists` vs `list-of-struct` question is
settled by RFD 2196 rule 6: pick the shape the parquet actually holds and
declare it that way in `dataset_info.features`.

## The join plan

For each task-type, three tables become one:

```python
base  = pq.read_table(f'maskscore_rung_1_{task}.parquet').to_pandas()
cands = pq.read_table(f'maskscore_rung_1_{task}_candidates.parquet').to_pandas()
scores= pq.read_table(f'maskscore_rung_1_{task}_scores.parquet').to_pandas()

# candidates → nested list per example_id
cands_by_ex = cands.groupby('example_id').apply(
    lambda g: g.drop(columns='example_id').to_dict('records')
).rename('candidates')

# scores → nested list per candidate_id, then joined into candidates
scores_by_cid = scores.groupby('candidate_id').apply(
    lambda g: g.drop(columns='candidate_id').to_dict('records')
).rename('scores')

# fold scores into each candidate record
def attach_scores(cand_list):
    for c in cand_list:
        c['scores'] = scores_by_cid.get(c['candidate_id'], [])
    return cand_list

wide = base.set_index('example_id').join(cands_by_ex.apply(attach_scores))
```

Two join-key assumptions to verify against the actual data before writing:

- **`example_id` is the join key in `_candidates`.** If the column is
  actually `row_id`, `stem`, `key`, or task-specific, use the actual name.
  Verify by `set(base.columns) & set(cands.columns)` for each task.
- **`candidate_id` is the join key from `_candidates` to `_scores`.** Same
  caveat; verify per-task.

Fallback if the join keys don't line up cleanly: publish the base table
alone per config for the first pass, and defer candidates+scores until the
join can be scripted deterministically.

## Media strategy

887 non-parquet files sit outside the parquet columns today. The
disposition per file kind:

| kind | count | strategy |
|---|---:|---|
| `renders/*.png` | 512 + 128 | inline as `struct<bytes, path>` per RFD 2196 rule 4 if under ~1 MB each; else keep at path, add column `image_path: string`, note viewer will not thumbnail |
| `speech/*.wav` | 150 | inline as `struct<bytes, path>` with `bytes: binary`; viewer plays audio inline |
| `speech/*.vtt` | 180 | inline as `text: string` column (WebVTT is small text) |
| `poses/*.png`  | 4 | inline |
| `scores/*.*`   | 2 | fold into the scores column of the row if applicable, else document as ancillary |

The join step reads media by path and embeds bytes into the row it belongs
to (identified by filename stem matching `example_id`). Files whose
example_id cannot be inferred stay at their satellite path and get named
in the dataset card as unreferenced-but-preserved.

Total inline media budget check: 512 renders × 400 KB + 150 wav × 500 KB +
etc. ≈ 300 MB. Comfortably under HF's per-shard limits with `row_group_size`
chosen per RFD 2196 rule 2.

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

The old root-level parquets and the old satellite directories can be
deleted in the same commit that lands the new layout, since the viewer
will not index the old shape and consumers of the old shape (if any exist)
should read from the source-of-truth generators anyway.

## Estimated effort

- Verify join keys per task-type: 30 min (six tables × two checks each).
- Write the join script: 2-4 h depending on whether keys are consistent.
- Media inlining: 1-2 h.
- Re-upload + verify viewer: 1 h.
- **Total: half a day to a day**, plus whatever the join-key surprises cost.
