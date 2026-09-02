# RFD 2169: Abandon the strangler-fig studio core; the ladder is MaskScore

**State:** published
**Feature:** documentation retraction
**Scope:** `rfd/1019-strangler-fig-studio-core`

## Problem

RFD 1019 proposed growing an Elixir application beside the browser
client and taking studio responsibilities from it one at a time. The
plan assumed a DGX + CUDA backend, the JS catalog as authoritative
first, and CockroachDB persistence. Every premise was walked back.

## Decision

Abandon RFD 1019. The workspace laddered up via MaskScore instead.
Gemma-4-12B (QAT Q4_0, Apache-2.0, local) is the reasoning core --
Gemma runs the vision + IPA panel today, produces the text-stub
instructions, and RFD 2167 targets it as the fine-tune base.
MaskScore constructs edit triples, EditScore (RFD 1157) scores them.
The Rung 1 corpus (RFD 2164, 5 stubs shipped) and its schema module
(RFD 2165.1) are the current spine. RFD 1173's Qwen3-VL wording is
drift and needs its own update.

Carried forward: facts-not-rows became ETNF; hexagonal ports became the 1-7 directory numbering.

Abandoned: the Elixir studio core beside the JS client (no parity
check ran); DGX + CUDA + Nx/EXLA (local desktop GPU is the only
compute now, RunPod/Vast.ai blocklisted); JS catalog authoritative
(per-model RFDs 1038-1052 and RFD 1102 ship it differently);
CockroachDB persistence (RFD 1067 walked it back; replaced with
sqlite-fdb + S3-compatible streaming backup (RFD 2143) + OpenBao
(RFD 2140)).

## Related

Retracts: urn:oid:1.3.6.1.4.1.66606.1.1.1019
Superseded by: urn:oid:1.3.6.1.4.1.66606.1.1.{1173,1157}

This RFD was drafted by an AI and read by a human before it shipped.
