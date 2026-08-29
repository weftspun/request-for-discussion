# RFD 1106 details: the proprietary-area table and the architecture split

## What forking the repository does not grant

| Area                    | Why it stays proprietary                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Trademark               | "Weftspun", the Weftspun3DStudio branding, the logo, apparel designs. See this project's own `README.md`, Legal & Trademark section. |
| Hosted AI               | The commercial `3DAIGC-API` queue, model-matrix tuning, and quality gates, running on operator hardware.                             |
| Marketplace graph       | Curated mint paths, soulbound identity and equippable assets, official secondary listings.                                           |
| Personalization service | Optional, user-approved profile context for generation. A compute product, not a sale of raw user data.                              |

Two areas this page's own source document once listed here, payment
rails (x402/wallet) and a phygital passport registry, are gone from
this table. RFD 1109 gives why: both are abandoned, per RFD 1012 and
RFD 1015, and both were fully stripped from the codebase before this
page was even written. Listing them as a current proprietary moat
was incorrect.

## The architecture split

```
[Open OSS client]  --API-->  [Hosted 3DAIGC + billing + SLA]  (operator moat)
       |
       +--> Trademark + official drops (brand moat)
       +--> Marketplace / personalization loop (network moat)
```

Forking the repository grants the client source under its own
license. It grants nothing else: not the right to operate as
"Weftspun," and not access to the hosted AI or marketplace backends
this page names.

## What stays out of this document, on purpose

Internal strategy (pricing, ARR, the full revenue map) lives in
local-only files this session found and removed from public view
once discovered, not in any RFD; this repository's own history
carries that redaction as a real commit, not a silent one.
