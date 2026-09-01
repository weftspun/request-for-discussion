# RFD 2145: Certificate lifetimes, from a risk-based ceiling

**State:** discussion
**Scope:** every private CA and leaf the workspace issues.

## Problem

RFD 2134, 2141, 2142 landed with 10-year CAs and 1-to-2-year leaves.
2144 minted a 10-year WebTransport intermediate on the same pattern.
The guidance predates CA/Browser Forum SC-081v3 (200 days now, 47 by
2029-03) and a Mozilla Root Store Policy that removes public trust
after 15 years of key material.

## Decision

    role                              notAfter       rotate every
    -----------------------------     ------------   ------------
    Root CA (private, offline key)    25 years       5 years, policy
    Intermediate CA                   3 years        1 year
    mTLS server + client (services)   90 days        <=45 days
    WebTransport leaf                 14 days        <=10 days
    Break-glass leaf (rare, gated)    2 years        on use, then revoke
    Break-glass CA (in 1P)            5 years        5 years

The root's `notAfter` is 25 years because RFC 5280 §4.1.2.5 makes the
field MANDATORY, not because rotation should wait that long. Offline
root: tiny compromise surface, expensive downstream re-issuance.
Rotation is a **5-year policy commitment**, enforced by
`check_anti_entropy.py`, not by cert validation. Intermediates and
leaves are the opposite: their `notAfter` IS the rotation gate.

`DETAILS.md` carries the citations (RFC 5280, Mozilla Root Store
Policy, CA/B Forum SC-081v3, NCSC, NIST SP 800-57 Pt.1 §5.3.6) and
the current-state audit.

## Related

RFD 2134, 2141, 2142, 2144. Each carries a retraction pointing here.
