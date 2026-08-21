# RFD 106d: Payment rails and the phygital registry, not part of the moat

**State:** abandoned
**Scope:** RFD 106a's own proprietary-area table

## Problem

RFD 106a's source document (this project's own moat overview)
listed two areas as current proprietary moat: payment rails
(x402/wallet, server-side secrets) and a phygital passport registry
(official garment serial IDs, NFC secure-URL validation, signed
digital-twin downloads). Both features are already abandoned, per
RFD 100c and RFD 100f, and both were fully stripped from the
codebase before RFD 106a was written. Carrying them forward as
"proprietary moat" restated a decision this project already
reversed.

## Decision

Extracted out of RFD 106a's own table, into this RFD, and marked
abandoned here too, matching RFD 100c and RFD 100f exactly. No code
implements either area today. A fork gains nothing by their absence,
since neither ships; RFD 106a's remaining three areas (trademark,
hosted AI, marketplace/personalization) are the real, current
proprietary boundary.

## Related

RFD 100c abandons the wallet, minting, and x402 payment rail. RFD
100f abandons the phygital passport, and records its own strip
complete: the passport code and documents are gone from the
codebase. RFD 106a is this RFD's own source table, corrected to
match.
