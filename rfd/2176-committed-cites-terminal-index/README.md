# RFD 2176: Index of committed/published RFDs citing terminal RFDs

**State:** committed
**Feature:** documentation index for stale citations from settled RFDs
**Scope:** every `committed` or `published` RFD that cites an
`abandoned` or `moved` RFD

## Problem

A Lean-verified audit found 39 pairs of (committed/published →
terminal). Higher severity than RFD 2174's open→abandoned class:
settled decisions leaning on withdrawn ones read as authoritative.

- **14 retraction chains** — the RFD is the retraction (2168-2175,
  2159). Correct as-is.
- **14 historical framing** in published loop-RFDs (1030, 1143-1147
  cite RFD 1122; 1020-1060 cite the pre-MaskScore RFD 1019). Weakly
  stale; the framing was correct when written.
- **11 real drift** — a settled decision references a terminal RFD
  without acknowledging the retraction chain. Per-pair successor
  annotations in [DETAILS.md](DETAILS.md).

## Decision

Same pattern as RFD 2174: this RFD is the citable index. The 14
retraction chains need no action. The 14 historical-framing pairs
stay as-is (retitling a published RFD to name a successor for a
citation that describes a superseded problem framing does more damage
than the drift). The 11 real-drift pairs migrate on next edit;
DETAILS.md names each successor.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1000 (RFD conventions).
Companion: urn:oid:1.3.6.1.4.1.66606.1.2.2174 (open→abandoned).
Verified by: Lean 4 spec in
`scratchpad/rfd_check/RfdSoundness.lean` (metatheorems typecheck;
counterexamples printed by `Report.lean`).

This RFD was drafted by an AI and read by a human before it shipped.
