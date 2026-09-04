# maskscore-rung-1-bootstrap join-key verification

Verifying RFD 2197's two join-key assumptions against the actual data in
`chibifire/maskscore-rung-1-bootstrap` (HF, snapshot 2026-09-04).

## What the RFD assumed

- `base ⋈ candidates` join key is `example_id`.
- `candidates ⋈ scores` join key is `candidate_id`.
- Six task-types, each with three sibling parquets at the repo root:
  `maskscore_rung_1_<task>.parquet` × 3.

## What the data holds

18 parquets on the repo. 15 at the root (`depth`, `keypoints`, `mesh`,
`multimodal`, `pose`), 3 under `speech/speech/` (naming variant
`maskscore_speech*`, no `rung_1` prefix, different directory layout).

Row counts and shared columns per task:

| task       | base rows | cand rows | score rows | base ∩ cand cols | cand ∩ score cols     |
| ---------- | --------: | --------: | ---------: | ---------------- | --------------------- |
| depth      |         1 |         2 |        128 | ∅                | `candidate`, `row_key` |
| keypoints  |         1 |         2 |        128 | ∅                | `candidate`, `row_key` |
| mesh       |         1 |         2 |        128 | ∅                | `candidate`, `row_key` |
| multimodal |         1 |         2 |        128 | ∅                | `candidate`, `row_key` |
| pose       |         1 |         2 |        128 | ∅                | `candidate`, `row_key` |
| speech     |        15 |       300 |        450 | ∅                | `candidate_axis`, `row_key` |

The RFD's `set(base.columns) & set(cands.columns)` check returns empty for
every task. Under the RFD's fallback ("publish the base table alone per
config"), the empty intersection would be read as _keys do not line up
cleanly_ and drop candidates+scores from the first pass. The data joins
cleanly; the check was wrong.

## Actual join keys

**Base ⋈ candidates:** `base.key = candidates.row_key`. Different names,
same semantic values.

| task       | base.key ∩ cand.row_key |
| ---------- | ----------------------: |
| depth      |               1 of 1 ✓ |
| keypoints  |               1 of 1 ✓ |
| mesh       |               1 of 1 ✓ |
| multimodal |               1 of 1 ✓ |
| pose       |               1 of 1 ✓ |
| speech     |             15 of 15 ✓ |

**Candidates ⋈ scores:** composite `(row_key, candidate)` for five tasks,
`(row_key, candidate_axis)` for speech. Not a single `candidate_id` column.
Every score row's composite maps to a candidate row (no orphan scores).

| task       | cand (row_key,cand) pairs | score composite unique | score rows / candidate |
| ---------- | ------------------------: | ---------------------: | ---------------------: |
| depth      |                         2 |                      2 |                     64 |
| keypoints  |                         2 |                      2 |                     64 |
| mesh       |                         2 |                      2 |                     64 |
| multimodal |                         2 |                      2 |                     64 |
| pose       |                         2 |                      2 |                     64 |
| speech     |                        30 |                     30 |                     15 |

Sixty-four score rows per candidate for the five non-speech tasks reflects
`view_index` in the score schema (per-view metrics, not per-candidate). The
wide row's `scores` field is therefore `list<struct>` inside each candidate
record, not a single struct.

## Speech is a schema variant, not a name variant

Speech differs on every axis the RFD groups tasks by:

| axis            | five non-speech tasks                       | speech                                |
| --------------- | ------------------------------------------- | ------------------------------------- |
| filename        | `maskscore_rung_1_<task>*.parquet`          | `maskscore_speech*.parquet`           |
| location        | repo root                                   | `speech/speech/`                      |
| candidate col   | `candidate`                                 | `candidate_axis`                      |
| score schema    | wide: `view_index, depth_l1, normal_l1, normal_dot` | long: `metric_name, metric_value` |
| base extras     | `poses`                                     | `canonical_text`                      |

Treating speech as one more entry in the same TASKS list will silently
mis-shape its scores column. It needs an explicit branch, or a separate
config emit path.

## Full column lists

```
[depth / keypoints / mesh / multimodal / pose : identical schema]
  base : ['key', 'task_type', 'dimension', 'input_column', 'input_asset',
          'input_asset_kind', 'poses']
  cand : ['row_key', 'candidate', 'rank', 'candidate_asset']
  score: ['row_key', 'candidate', 'view_index',
          'depth_l1', 'normal_l1', 'normal_dot']

[speech]
  base : ['key', 'task_type', 'dimension', 'input_column', 'input_asset',
          'input_asset_kind', 'canonical_text']
  cand : ['row_key', 'candidate_axis', 'rank', 'candidate_asset',
          'candidate_asset_kind', 'candidate_kind', 'candidate_target_text']
  score: ['row_key', 'candidate_axis', 'candidate_rank',
          'metric_name', 'metric_value']
```

## Bootstrap size is small on purpose

Five non-speech tasks have exactly one base row each. That is the whole
bootstrap for those tasks, not a truncated download. Total example rows
across the dataset after wide-row restructure: 5 × 1 + 1 × 15 = 20 rows.
RFD 2197's ~300 MB media estimate is off by orders of magnitude for the
bootstrap; the actual parquet payload is under 50 KB.

## What RFD 2197 needs amended

Before a join script gets written:

1. Rename `example_id` → `key` on base, `row_key` on candidates and scores in
   the join-plan snippet. The keys align 100 % once named right.
2. Replace `candidate_id` with the composite `(row_key, candidate)` for
   five tasks and `(row_key, candidate_axis)` for speech.
3. Drop the `set(base.columns) & set(cands.columns)` check as the join-key
   gate. The empty intersection is expected. Assert instead that the
   per-task expected join columns exist by name and their value-sets match.
4. Give speech its own emit branch: different filename glob, different
   candidate column, different score schema (long → nested `list<struct>`
   or pivoted before nesting). Cannot be a single string in the same TASKS
   list.
5. Make the scores field per candidate `list<struct>`: 64 per-view records
   per candidate (non-speech) or 15 per-metric records per candidate
   (speech). The RFD's current shape hints at one score record per
   candidate.
6. Revise the ~300 MB media estimate: 20 wide rows across the whole dataset
   at bootstrap scale. Storage question is trivial; viewer-rendering
   question is the same one.

## Reproducer

```
SCRATCH=<tmp>/maskscore-rung-1
hf download chibifire/maskscore-rung-1-bootstrap --repo-type=dataset \
   --include="maskscore_rung_1_*.parquet" --local-dir "$SCRATCH"
hf download chibifire/maskscore-rung-1-bootstrap --repo-type=dataset \
   --include="speech/speech/*.parquet" --local-dir "$SCRATCH"
# then the schema+key check script above.
```

## Status

Fallback per RFD 2197 (publish base alone, defer candidates+scores) is
_not_ triggered by the actual data. The join is deterministic once the
keys are named correctly. Surfacing to the coordinator for an RFD 2197
amendment before drafting the join script.
