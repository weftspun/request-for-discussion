# RFD 2196: HuggingFace dataset viewer rules

**State:** discussion
**Feature:** authoring rules for HuggingFace dataset repos so the viewer renders
**Scope:** any dataset published under `huggingface.co/datasets/chibifire/*`

## Decision

Publish HuggingFace datasets as zstd-compressed parquet shards under
`data/`, one wide denormalized row per logical example, with row
groups <= 300 MB and images embedded as `struct<bytes:binary, path:string>`.
Skip ETNF/6NF normalization for anything destined for HF. Push with
LFS + `hf_transfer`, not xet, whose finalize call times out on multi-GB
commits.

The viewer's contract is enforced silently by an auto-indexer that
either succeeds or falls back to a "Preview" badge. The five rules and
the errors each surfaces are in `DETAILS.md`, one section per rule.

## Problem

Three rebuilds on 2026-09-03 (`chibifire/editreward-bench`,
`chibifire/editscore-rl-train`, `chibifire/editscore-reward-train`)
each failed a different silent gate: too-big `.arrow` shards
crashed the auto-viewer, xet finalize stalled at 6 KB/s and timed out
twice, and one dataset silently dropped every 2-image row because
shared image paths collided. Landing a dataset that renders needs
each of the five rules matched at author time, not fixed after the
push has happened.

## Related

Companion skills `hf-datasets-no-etnf`, `hf-parquet-image-column`,
`hf-upload-large`, `hf-download-streaming` are the single-page how-to
per rule. RFD 2183 (OmniGen layer decomp) and RFD 2193 (editscore
reproducibility bar) both consume datasets published under these rules.

This RFD was drafted by an AI and read by a human before it shipped.
