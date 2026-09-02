# RFD 2169: Abandon the strangler-fig studio core; the ladder is MaskScore

**State:** published
**Feature:** documentation retraction
**Scope:** `rfd/1019-strangler-fig-studio-core`

## Problem

RFD 1019 proposed growing an Elixir application beside the browser
client and taking studio responsibilities from it one at a time. The
plan assumed a DGX + CUDA backend, the JavaScript catalog as
authoritative first, and CockroachDB persistence. Later work walked
back each premise, and the strangler fig stopped growing.

## Decision

Abandon RFD 1019. The workspace laddered up via MaskScore instead:
RFD 1173's multimodal pipeline is the substrate now — Qwen3-VL as
the reasoning core, MaskScore constructing edit triples, EditScore
(RFD 1157) scoring them. The Rung 1 corpus (RFD 2164, 5 stubs
shipped) and its schema module (RFD 2165.1) are the current spine.

Carried forward: facts-not-rows (ETNF is that model's descendant);
hexagonal ports (the 1-7 directory numbering is that shape).

Abandoned: the Elixir studio core beside the JS client (no parity
check ran, no responsibility migrated); DGX + CUDA + Nx/EXLA
(CLAUDE.md now names the local desktop GPU as the only compute,
RunPod and Vast.ai blocklisted); JS catalog as authoritative (the
per-model RFDs 1038-1052 and RFD 1102 ship the inventory differently).

## Related

Retracts: urn:oid:1.3.6.1.4.1.66606.1.1.1019
Superseded by: urn:oid:1.3.6.1.4.1.66606.1.1.{1173,1157}

This RFD was drafted by an AI and read by a human before it shipped.
