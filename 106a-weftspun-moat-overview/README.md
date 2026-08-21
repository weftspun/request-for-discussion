# RFD 106a: The open/proprietary boundary, in public words

**State:** published
**Scope:** licensing, trademark, the hosted service boundary

## Problem

The client source is open. A fork could read that as an invitation
to run as "Weftspun," or reuse the hosted AI and registry backends.
Nothing public states where the open license ends and the
proprietary service begins.

## Decision

Publish one page stating the split, with no pricing, revenue
target, or investor detail in it. The client (`LICENSE`) is open,
self-hostable under a different product name. Three areas stay
proprietary, not granted by the OSS license: the trademark, the
hosted `3DAIGC-API` with its model tuning and quality gates, and the
marketplace/personalization services built on it.

See `DETAILS.md` for the architecture split diagram and the
per-area table.

## Related

The public Vercel demo (`0098-public-deploy/`) runs the open client
with none of the proprietary services exposed. Trademark terms live
in this project's own `README.md` and `TRADEMARKS`. RFD 106d gives
the payment-rail and phygital-registry areas this page's own source
document once listed; both are abandoned, per RFD 100c and RFD
100f, and removed from this table.
