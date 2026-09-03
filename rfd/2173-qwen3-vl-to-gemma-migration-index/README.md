# RFD 2173: Qwen3-VL to Gemma-4-12B migration index

**State:** committed
**Feature:** documentation index for the reasoning-core swap
**Scope:** every open RFD that names Qwen3-VL as the reasoning core

## Decision

This RFD is the citable index for the Qwen3-VL to Gemma-4-12B swap; ten open RFDs still name Qwen3-VL, and each migrates its mention as follow-on when next touched.

## Problem

RFD 2169 (studio-core abandonment) named Gemma-4-12B (QAT Q4_0) as the reasoning core the workspace actually runs. RFD 1173 (edit-reward corpus, PR #179) followed with the substrate table swap. Ten open RFDs still name Qwen3-VL, but not all of those mentions are drift: some are load-bearing references to real artifacts.

Three classes of mention: aspirational future-intent (drift, fix); shipped-artifact facts (keep, EditScore's published LoRA is over Qwen3-VL-8B); measured runs (keep, RFD 2161 measured Qwen3-VL-4B MLX at 0.9 s load and 1.9 s first token). Bulk-swap erases the last two.

## Details

Per-RFD annotations sit in [DETAILS.md](DETAILS.md); each RFD retains its current text until otherwise edited. This RFD provides the citable pointer so a reader hitting a stale Qwen3-VL mention gets the reason without a rewrite pass across ten RFDs.

RFD 1157 (EditScore reward model) leads: its analysis of the Hailo HEF projector-drop against Qwen3-VL's mm_* tensor shape rewrites against Gemma's projector shape.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1173 (multimodal pipeline).
Anchor: urn:oid:1.3.6.1.4.1.66606.1.2.2169 (studio-core abandonment that carried the reasoning-core swap).
Applies to: RFDs 1089, 1157, 1163, 1167, 1168, 1169, 1170, 1171, 2161, 2167 (see DETAILS.md for per-RFD annotations).

This RFD was drafted by an AI and read by a human before it shipped.
