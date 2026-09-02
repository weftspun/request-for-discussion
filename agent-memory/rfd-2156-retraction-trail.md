---
name: rfd-2156-retraction-trail
description: Five compute-ladder retractions in the RFD 2156 session on 2026-09-01
metadata: 
  node_type: memory
  type: project
  originSessionId: 6af7ce67-cc66-41b2-8c13-0bc4c0cb6fde
  modified: 2026-09-02T02:52:50.575Z
---

RFD 2156 (VN-avatar cleanroom on MaskScore) descended a five-rung
compute ladder in one session. Every rung's dead bet is on the
record in `2156/DETAILS.md`. Do not reopen them:

1. **Rent RTX 3090 on Vast** — two cheapest-tier hosts failed to
   spin up. $0.003 spent. Kept `6-datasource/vast-market-snapshots/`
   as a byproduct.
2. **Qwen3-Omni-30B as omnibus (thinker+talker+OmniScore)** —
   team disbanded, no true-QAFT upstream, $7-15K to train ourselves.
   Retracted in favor of role-per-model.
3. **Gemma-4-31B-it-qat as visual-LLM base** — 62.6 GB fp16 exceeds
   shipping budget. Google publishes it (apache-2.0) but the mirror
   to `chibifire/` never fired.
4. **Gemma-4-E4B-it-qat + train EditScore LoRA ourselves** —
   retracted at scaffold stage. EditScore already published its LoRA
   over Qwen3-VL-4B; training a duplicate wastes compute.
5. **Vision-encoder split onto Hailo NPU via QFT** — parked. No
   Linux x86_64 DFC host, no Hailo hardware. Scaffold survives at
   `3-interactor/editscore-lora-gemma4-e4b/scripts/gate_vision_encoder.py`
   with a real ONNX export (`build/vision_encoder.onnx`) for when
   hardware arrives.

**What survived and was verified:**
- `mlx-community/Qwen3-VL-4B-Instruct-4bit` +
  `EditScore/EditScore-Qwen3-VL-4B-Instruct` on Mac mini, 0.9s load,
  1.9s first token. See [[editscore-qwen3vl-mlx-works]].
- Vast market ETNF snapshots (three point-in-times, 445 KiB each,
  Wilson-95%-lower hot-band analysis on pooled 3-snapshot evidence).

**Naming debt cleared 2026-09-01:** the scaffold repo was renamed
from `3-interactor/editscore-lora-gemma4-e4b` to
`3-interactor/editscore-lora-qwen3vl-4b` to match its actual base.
Manifest entry updated; DETAILS refs updated; pixi.toml and README
retitled.

Related: [[hardware-pivot-2026-09-01]], [[editscore-qwen3vl-mlx-works]],
[[vast-api-notes]], [[openbao-address]].
