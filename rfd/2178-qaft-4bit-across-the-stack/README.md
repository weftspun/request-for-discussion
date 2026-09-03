# RFD 2178: QAFT 4-bit across the model stack

**State:** discussion
**Feature:** target every model in the atelier-workshop at 4-bit
Quantization-Aware Fine-Tuning
**Scope:** every model row in RFD 1102's task catalog

## Problem

RFD 1027 committed QAFT-first as the default weights format. RFD
2139 (abandoned) surveyed the stack: only Gemma-4-12B ships a true
upstream QAT Q4_0 release. Wan-VACE, Pixal3D, VoxHammer, MoGe-3, and
the audio-panel models run at published precision. The plan needs a
per-model position: which model is QAFT'd, when, at what compute cost.

## Decision

Every model in the atelier-workshop targets QAFT 4-bit. Three classes track where each stands.

Class A (upstream QAFT available): use verbatim. Gemma-4-12B QAT
Q4_0 today.

Class B (upstream QAFT feasible locally): workspace produces one
from published weights via a QAFT fine-tune on the RTX 3090. Small
models (Qwen3-TTS-1.7B, Kimodo, SkinTokens, MoGe-3, rf-detr-Seg,
WavLM, wav2vec2, ipa-whisper) fit in one overnight run each.

Class C (upstream QAFT infeasible locally): Wan-VACE 14B, Pixal3D
24 GB base. QAFT needs multi-day runs; parked until compute expands
or an upstream Q4 release lands.

See [DETAILS.md](DETAILS.md) for the per-model class, size, and
compute estimate. See RFD 1027 for the QAFT-first rule.

## Related

Extends RFD 1027 (QAFT-first, committed). Consumed by RFD 2167
(voice-reward distillation, parked, needs Class B Qwen3-TTS QAFT).

This RFD was drafted by an AI and read by a human before it shipped.
