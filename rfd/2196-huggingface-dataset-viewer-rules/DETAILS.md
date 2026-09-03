# HuggingFace dataset viewer rules — how to author, how to fix

## The viewer's contract, verbatim from what it enforces

| Rule | What breaks if you skip it | Error surface |
|---|---|---|
| Row group ≤ 300 MB | Scan limit exceeded | `Parquet error: Scan size limit exceeded: attempted to read <N> bytes, limit is 300000000 bytes` |
| One row shape per split | Viewer picks arbitrary schema | Missing columns, silent NULLs |
| Image column = `struct<bytes:binary, path:string>` | No thumbnails | Column shows as a struct blob |
| Shards under `data/` with `train-XXXXX-of-YYYYY.parquet` | Auto-indexer skips them | "Preview" badge, no viewer |
| Whole-commit under HF's job limits | Auto-convert job dies | `JobManagerCrashedError` |
| LFS-backed for >10 GB pushes | Xet finalize times out | `RuntimeError: Internal error: timed out reading request body` |

## Rule 1 — one wide row per example (denormalize)

The HF viewer paginates one wide table per split. Split into satellite
tables (Hermes / ETNF / 6NF style) and the viewer's `train[0..N]`
browsing collapses. Rules:

- One row per logical example. NULLs are fine.
- Nested lists and structs are fine (multiple images per row,
  conversation turns) — one row per example still.
- Do NOT emit `entity`, `entity_score`, `entity_conversation` as
  separate parquet files thinking the viewer will join them.

Companion skill: `hf-datasets-no-etnf`.

## Rule 2 — row groups ≤ 300 MB

The viewer scans one row group at a time when the reader requests a
page. Above 300 MB it hard-fails. With images embedded (~1 MB each), a
1000-row shard is one 1 GB row group by pyarrow default — always
oversized.

Write with:

```python
pq.write_table(tbl, path,
               compression="zstd", compression_level=9,
               row_group_size=100)   # 100 rows × ~1 MB = ~100 MB
```

`row_group_size` is the maximum number of rows per group. Set it so
`rows_per_group × avg_row_bytes < 200 MB` (30 % safety margin).

For an already-published shard, rewrite in place — no re-extraction
needed:

```python
tbl = pq.read_table(path)
pq.write_table(tbl, path_tmp, compression="zstd",
               compression_level=9, row_group_size=100)
path_tmp.replace(path)
```

## Rule 3 — shards ~500 MB, named `data/train-XXXXX-of-YYYYY.parquet`

The auto-indexer scans `data/` for files matching that name pattern and
groups them into splits. Bigger shards (up to ~1 GB) work but slow the
viewer's first paint. Aim for ~500 MB for image-embedded data.

Layout examples:
```
data/train-00000-of-00110.parquet     # single split
data/train-...  data/validation-...   # multiple splits, same config
default/train-... other/train-...     # multiple configs (put configs at top)
```

## Rule 4 — image column = `struct<bytes:binary, path:string>`

Exact Arrow type:

```python
import pyarrow as pa
image_type = pa.struct([("bytes", pa.binary()), ("path", pa.string())])
# single image per row
schema = pa.schema([..., ("image",  image_type)])
# multiple images per row (viewer renders a gallery)
schema = pa.schema([..., ("images", pa.list_(image_type))])
```

Row shape:
```python
{"bytes": <raw png/jpg bytes>, "path": "images/whatever.png"}
```

What does NOT work:
- `pa.binary()` alone (no thumbnail rendering)
- `{"path": "images/x.png"}` referencing a file elsewhere in the repo
- gzipping/zstd-ing the image bytes yourself (parquet's zstd handles it)

## Rule 5 — LFS + hf_transfer for large pushes

`huggingface_hub`'s default xet path stalls on multi-GB commits: the
CDN endpoint sits ESTABLISHED but transmits nothing, then the client
raises `RuntimeError: Internal error: timed out reading request body`
on the finalize call. Observed at 94 GB / 110 shards. Multiple retries
did not help; batching into 15-file commits did not help.

Reliable recipe:

```sh
pip install hf_transfer
HF_HUB_DISABLE_XET=1 \
HF_HUB_ENABLE_HF_TRANSFER=1 \
hf upload-large-folder \
  --repo-type dataset \
  REPO_ID LOCAL_DIR \
  --num-workers 8
```

Notes:
- `upload-large-folder` doesn't accept `--path-in-repo`. Structure
  `LOCAL_DIR` so its tree already matches the repo (put parquet under
  `LOCAL_DIR/data/`) and pass `LOCAL_DIR` itself.
- Symlinks are not followed — move or copy real files in.
- Per-file resume state is in `LOCAL_DIR/.cache/huggingface/`. An
  interrupted run resumes without re-hashing.
- Do NOT run two `upload-large-folder` processes against the same
  `LOCAL_DIR`.
- Deletes and small commits work fine over the standard
  `HfApi().create_commit` path; only large adds need the LFS+hf_transfer
  route.

Companion skill: `hf-upload-large`.

## Streaming download without doubling disk

`hf_hub_download(..., local_dir=…)` and `hf download --local-dir` write
the file to BOTH `~/.cache/huggingface/hub/…/blobs/` AND the requested
`local_dir` (on macOS the intended hardlink often becomes a copy). Cost
observed: 86 GB target dir → 170 GB actual disk.

For one-shot streaming pipelines, bypass the cache with direct HTTPS:

```python
import os, requests
from huggingface_hub import HfApi
TOKEN = HfApi().token or os.environ["HF_TOKEN"]
S = requests.Session()
S.headers["Authorization"] = f"Bearer {TOKEN}"

url = f"https://huggingface.co/datasets/{REPO}/resolve/main/{name}"
with S.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(1 << 22):
            f.write(chunk)
# process...
local_path.unlink()
```

For repeated reads, let the cache do its job — the doubling pays for
retry and dedup.

Companion skill: `hf-download-streaming`.

## Pitfall — shared images across rows

If your metadata references the same image path from multiple rows
(observed in `chibifire/editscore-reward-train`: `images/0_0.png`
referenced by 7 different rows), a naive `img2row: dict[str, int]` maps
each path to only the LAST row that claimed it. When the tar stream
delivers that image, all other claiming rows are orphaned and dropped
silently at the end.

Fix: `img2rows: dict[str, list[int]]` with `defaultdict(list)`, and on
each tar member deliver the bytes to every interested row. Bytes are
shared by reference — no memory blowup.

## Pitfall — auto-viewer job crash on legacy `.arrow` shards

A dataset saved with `datasets.save_to_disk` publishes as `.arrow`
shards plus `dataset_info.json` / `state.json`. HF tries to
auto-convert those to parquet in a job that has resource limits — it
died with `JobManagerCrashedError` on the ~5 GB `chibifire/editreward-bench`
input, leaving the viewer stuck as "Preview". Fix: convert to parquet
yourself, push under `data/`, and delete the `.arrow` shards and
`dataset_info.json` / `state.json` in the same commit.

## Non-goals for this RFD

- **Dataset card / README frontmatter** (task category, language, licence tags).
- **PII gating** — HF's access-control settings are per-repo, out of scope here.
- **Splits & configs directory conventions** — the auto-detector handles
  the common cases; a dedicated RFD if we hit an ambiguous layout.
- **`datasets.Features` explicit definition** — unnecessary when the
  Arrow schema is unambiguous (it is, for our columns).

## Related RFDs

- RFD 2183 — retrain OmniGen for layer decomposition (consumer of these datasets)
- RFD 2193 — editscore as reproducibility bar (consumer)

## Reference commit set

- `chibifire/editreward-bench` — commit `057671b9…`, `.arrow` → parquet, viewer restored.
- `chibifire/editscore-rl-train` — post-fix commit (row_group_size=100), 110 shards under `data/`.
- `chibifire/editscore-reward-train` — post-fix commit, 97,256 rows written, no silent drops.
