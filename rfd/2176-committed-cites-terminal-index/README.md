# RFD 2176: Index of committed/published RFDs citing terminal RFDs

**State:** committed
**Feature:** documentation index for stale citations from settled RFDs
**Scope:** every `committed` or `published` RFD that cites an
`abandoned` or `moved` RFD

## Decision

This RFD is the citable index for settled-to-terminal citation drift; a Lean-verified audit found 39 pairs, and only 11 real-drift pairs need per-RFD follow-up.

## Problem

Settled decisions leaning on withdrawn ones read as authoritative, so this class of drift is higher severity than RFD 2174 (open-to-abandoned index)'s open-to-abandoned class.

Of the 39 pairs:

- 14 retraction chains. The RFD is the retraction (2168-2175, 2159). Correct as-is.
- 14 historical framing pairs in published loop-RFDs (1030, 1143-1147 cite RFD 1122; 1020-1060 cite the pre-MaskScore (edit-reward corpus) RFD 1019). Weakly stale; the framing was correct when written.
- 11 real drift pairs. A settled decision references a terminal RFD without acknowledging the retraction chain. Per-pair successor annotations in [DETAILS.md](DETAILS.md).

## Details

Same pattern as RFD 2174. The 14 retraction chains need no action. The 14 historical-framing pairs stay as-is (retitling a published RFD to name a successor for a citation that describes a superseded problem framing does more damage than the drift). The 11 real-drift pairs migrate on next edit; DETAILS.md names each successor.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1000 (RFD conventions).
Companion: urn:oid:1.3.6.1.4.1.66606.1.2.2174 (open-to-abandoned).
Verified by: Lean 4 spec in `scratchpad/rfd_check/RfdSoundness.lean`.

This RFD was drafted by an AI and read by a human before it shipped.
