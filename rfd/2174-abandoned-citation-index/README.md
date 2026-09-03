# RFD 2174: Index of open RFDs citing abandoned RFDs

**State:** committed
**Feature:** documentation index for stale citations to abandoned RFDs
**Scope:** every open RFD that cites an abandoned or moved RFD

## Decision

This RFD is the citable index for open-to-abandoned citation drift; the 32 pairs sit in DETAILS.md, and individual RFDs migrate their citations when next touched.

## Problem

An audit found 32 pairs of (open RFD, abandoned RFD it cites). Not all are drift: a retraction chain legitimately cites what it walks back, and RFDs 2168 (wholebody detector retraction) and 2169 (studio-core abandonment) do exactly this. The class of concern is open RFDs that lean on an abandoned RFD's decision as if it still holds, without knowing the citation went stale.

Concentrations: RFD 1122 (wholebody detector, abandoned by 2168) cited by 11 open RFDs; RFD 1166 (See-Through scoring plan) cited by 7; RFDs 1049-1052 (abandoned model images) cited by 1133 and 1171; RFD 1019 (strangler-fig studio core, abandoned by 2169) cited by 4.

## Details

Each pair in DETAILS.md is annotated with what the citing RFD's claim depends on and where the successor lives. Cheaper than 32 amendments; provides one URN to cite when a reader hits a stale reference and needs the successor without a rewrite pass. Pattern established by RFD 2173 (Qwen3-VL swap index).

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1000 (RFD conventions).
Applies to: 30-plus open RFDs; see DETAILS.md for the full list.

This RFD was drafted by an AI and read by a human before it shipped.
