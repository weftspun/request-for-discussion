# RFD 2197: Restructure maskscore-rung-1-bootstrap for the HF viewer

**State:** discussion
**Feature:** rework `chibifire/maskscore-rung-1-bootstrap` into one wide-row shape per task-type so the HF viewer renders it
**Scope:** dataset repository only; no change to the source-of-truth generators

## Decision

Republish `chibifire/maskscore-rung-1-bootstrap` as **six configs, one per
task-type** (`depth`, `keypoints`, `mesh`, `multimodal`, `pose`,
`speech-audio`), each with its base + candidates + scores tables joined
into one wide row per example under `data/<config>/train-*.parquet`. Media
satellites (`renders/`, `speech/`, `poses/`, `scores/`) get referenced by
content-hash path or inlined as `struct<bytes, path>` per RFD 2196 rule 4,
depending on file size. See `DETAILS.md` for the join plan and media
strategy.

## Problem

The current repository violates RFD 2196 rules 1 and 3: 18 parquets at the
repo root (not under `data/`), organised as six task-types × three
satellite tables each. HF viewer preview and viewer both red because the
auto-indexer finds no `data/train-*.parquet` layout it can group into a
split. Plus 887 non-parquet files (128 render PNGs, 512 more renders, 150
WAV, 180 VTT, 131 NPZ) whose relationship to the parquet rows the viewer
cannot infer.

## Non-goals

Source-of-truth generators (unchanged); rung-2/3/4 datasets; complete
schema audit; media-hosting choice if satellites exceed HF's ceiling.

## Related

RFD 2196 (HF viewer rules), RFD 2165 (maskscore stub emit), RFD 2166
(maskscore cineform bundle), RFD 1173 (edit-reward corpus).

This RFD was drafted by an AI and read by a human before it shipped.
