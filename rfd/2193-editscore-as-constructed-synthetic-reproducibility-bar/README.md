# RFD 2193: EditScore as the constructed-synthetic reproducibility bar

**State:** discussion
**Feature:** replace sha256 byte-equality with a semantic reproducibility judge
**Scope:** `anny-render-corpus` and every constructed-synthetic renderer

Shelved 2026-09-03: waiting on two blockers named below.

## Decision

Replace sha256 byte-equality with EditScore (RFD 1157 reward
model) as the reproducibility judgment for constructed-synthetic
corpus. Reuses an instrument the workspace has; permits Metal-fast
rendering while keeping the bar honest.

## Problem

Measured on M2 Pro against `render_view.py`'s film: CPU one-thread
takes 32,592 ms per image, byte-identical; CPU default threads
4,364 ms and differs; Metal 545 ms and differs. Metal is sixty
times faster; three seed-zero runs produced three digests, so
divergence is GPU accumulation order.

Two blockers. First, `feature.editscore` in
`anny-render-corpus/pixi.toml` takes torch from a CUDA index with
no Apple wheels; the verifier does not run where needed. Second,
PITFALLS rule 2: the judge must separate a different render from
a 1/255 dither, or it is a rubber stamp. CLAUDE.md's 2026-09-02
condition-5 retraction permits a quantised verifier.

## References

Issue: `weftspun/weftspun-keypoint` 29; `anny-render-corpus/score_edits.py`.

## Related

RFD 1157 (EditScore reward), RFD 1173 (edit-reward corpus; MaskScore),
RFD 2196 (HF viewer rules), CLAUDE.md constructed-synthetic rule.

This RFD was drafted by an AI and read by a human before it shipped.
