# RFD 1109: Payment rails and the phygital registry, not part of the moat

Extracted out of RFD 1106's own table, into this RFD, and marked
abandoned here too, matching RFD 1012 and RFD 1015 exactly. No code
implements either area today. A fork gains nothing by their absence,
since neither ships; RFD 1106's remaining three areas (trademark,
hosted AI, marketplace/personalization) are the real, current
proprietary boundary.

RFD 1106's source document (this project's own moat overview)
listed two areas as current proprietary moat: payment rails
(x402/wallet, server-side secrets) and a phygital passport registry
(official garment serial IDs, NFC secure-URL validation, signed
digital-twin downloads). Both features are already abandoned, per
RFD 1012 and RFD 1015, and both were fully stripped from the
codebase before RFD 1106 was written. Carrying them forward as
"proprietary moat" restated a decision this project already
reversed.

RFD 1012 abandons the wallet, minting, and x402 payment rail. RFD
1015 abandons the phygital passport, and records its own strip
complete: the passport code and documents are gone from the
codebase. RFD 1106 is this RFD's own source table, corrected to
match.

**State:** abandoned

This RFD was drafted by an AI and read by a human before it shipped.
