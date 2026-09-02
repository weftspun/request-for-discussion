---
name: weights-live-on-huggingface
description: "Model weights and datasets live on Hugging Face (chibifire org), NOT in GitHub repos"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T02:51:30.009Z
---

Model weights and dataset payloads always live on Hugging Face,
never in a GitHub repo. The workspace's `default.xml` manifest
already carries this split with two remotes:

    <remote name="huggingface"          fetch="https://huggingface.co" />
    <remote name="huggingface-datasets" fetch="https://huggingface.co/datasets" />

**Why:** GitHub is for code and specs; HF is for weights, datasets,
and the LFS + safetensors + parquet tooling built for them. A repo
that ships a code artifact goes on `weftspun` (GitHub); a repo
that ships weights or a dataset goes on `chibifire` (HF).

**How to apply:**
- Trained LoRA adapters, merged models, quantized model variants ->
  `chibifire/<model-name>-<precision>` on HF via `huggingface`
  remote in the manifest.
- Trace corpora, reward-data snapshots, MaskScore stubs ->
  `chibifire/<dataset-name>-<split>` on HF via `huggingface-datasets`
  remote.
- Code (Elixir, C++, Python scripts, RFDs, sigs) -> `weftspun` on
  GitHub via the `weftspun` remote.

Recent examples (existing manifest entries):
    chibifire/anny-render-corpus-generated-train  (huggingface-datasets)
    chibifire/harmless-prompts-en-train           (huggingface-datasets)
    chibifire/artifacts-mmo-planner-traces-train  (huggingface-datasets)

Applied consequences for the 2026-09-01 session's leftovers:
- `6-datasource/vast-market-snapshots/` — parquet payloads should
  eventually land on HF as `chibifire/vast-market-snapshots-<date>`
  or similar, not on GitHub. The `snapshot.py` capture script stays
  on GitHub (it's code); the parquet output goes on HF.
- Any future EditScore-LoRA adapter we train belongs at
  `chibifire/editscore-lora-qwen3vl-4b-<task-type>` on HF, not in
  the code repo.
- The mirror plans discussed but not fired (Gemma-4-*, EditScore
  Qwen3-VL-8B/32B) all target `chibifire/` on HF.

Related: [[hardware-pivot-2026-09-01]], [[editscore-qwen3vl-mlx-works]],
[[rfd-2156-retraction-trail]].
