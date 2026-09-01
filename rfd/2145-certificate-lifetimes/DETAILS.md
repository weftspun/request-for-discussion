# RFD 2145 details: citations, current-state audit, exceptions

This RFD was drafted by an AI and read by a human before it shipped.

## Why the root cert has an expiry at all

RFC 5280 §4.1.2.5 makes `notAfter` a MANDATORY field on every X.509
certificate. There is no valid X.509 leaf, intermediate, or root that
carries no expiry. So the question is not "should the root have an
expiry" but "how far out do we set the field that has to be there".

    The validity period for a certificate is the period of time from
    notBefore through notAfter, inclusive. […] To indicate that a
    certificate has no well-defined expiration date, the notAfter
    SHOULD be assigned the GeneralizedTime value of
    99991231235959Z.
    -- RFC 5280 §4.1.2.5

RFC 5280 permits the "never expires" sentinel (`99991231235959Z`) for
certs the issuer treats as having no defined end date. Some private
CAs use it. This RFD does not, for two reasons. First, OpenSSL prints
`notAfter=Dec 31 23:59:59 9999 GMT` and some X.509 parsers reject the
year field as out of range: RFC 5280 requires UTCTime for years
1950-2049 and GeneralizedTime after, so pre-1994 parsers and some
embedded stacks fail. Second, the intent ("this cert never expires,
we rotate on schedule") is invisible to anyone reading the cert.
25 years is long enough that the field is not the rotation gate, and
short enough that every stack we ship to handles it.

## Why the ROTATION on the root is 5 years, not 25

Three converging bodies of guidance land in the same window.

**Mozilla Root Store Policy §7.1** removes public-trust for a root CA
whose key material is more than 15 years old:

    For a Root CA certificate trusted for server authentication,
    Mozilla will remove the websites trust bit when the CA key
    material is more than 15 years old.
    -- Mozilla Root Store Policy v2.9, 2023-09

Our root is private, so Mozilla does not force our hand. The industry
consensus reflected in that number is that 15 years is the outer edge
before cryptographic parameters and operational discipline drift
enough to warrant re-mint.

**NCSC in-house PKI principles: "keep certificate lifetimes as short
as practical".** No fixed year on the root. The phrasing is
deliberate. Short as practical, taking rotation cost into account.

    Certificates should have lifetimes that are as short as practical,
    while balancing the operational overhead of renewal.
    -- NCSC "In-house public key infrastructure — PKI principles"

**NIST SP 800-57 Part 1 §5.3.6 (key lifetimes).** Recommends both
"originator usage period" and "recipient usage period" bounded.
Public-key signing keys used to certify other keys are the highest-
value keys in the system and thus have the tightest recommended
cryptoperiod. Not a specific year, but a directional bound.

Five years is the smallest rotation cadence at which the CA ceremony
is a set-piece event we prepare for rather than an emergency. Half of
that is the "start scheduling the next ceremony" trigger.

## Why the intermediates get 3 years

An intermediate CA is online (or at least reachable) whenever it signs
a leaf. Its compromise surface is bigger than the root's. Rotating it
under 5 years is standard private-PKI practice. 3 years keeps the
cadence at "annual re-mint of a new one, run for a year, retire the
older one". A two-CA overlap window costs nothing and lets the
trust-store update propagate.

CA/B Forum's SC-081v3 vote (2025-04) sets public TLS leaf lifetimes on
a schedule (200 days now, 100 by 2027-03, 47 by 2029-03). The root
and intermediate lifetimes for publicly-trusted CAs are already
15 years (Mozilla). Our private intermediates run inside that number,
at 1/5 of it, because we control the whole chain and can rotate
cheaply.

## Why the leaves get 90 days / 14 days

**mTLS server + client (services): 90 days.** Aligns with the
Let's Encrypt cadence the industry has run for a decade without
incident. Matches CA/B Forum's 2027 target for public TLS. Short
enough that a compromised leaf is a real cost to the attacker.

**WebTransport leaf: 14 days.** Chrome enforces 14 days as the maximum
validity for a certificate cited in `serverCertificateHashes`. Longer
and the browser refuses the QUIC handshake. Not a policy choice on
our side. It is what the protocol accepts.

## Current state, 2026-09-01

Every live cert in the workspace and how it stacks up against this RFD:

    cert                                          notAfter        row of table
    ------------------------------------------    -----------     -----------------
    chibifire.com Root CA                         2036-08-28      root: 10y set, 25y max. Fine, keep.
    chibifire.com Intermediate CA                 2031-08-30      intermediate: 5y set, 3y max. RETRACT, rotate.
    chibifire.com WebTransport Intermediate CA    2036-08-29      intermediate: 10y set, 3y max. RETRACT, re-mint at 3y.
    weftspun-fdb-ca (break-glass, in 1P)          2031-08-31      break-glass CA: 5y set, 5y max. Fine.
    Bao listener leaf                             2028-09-01      service leaf: 2y set, 90d max. RETRACT, re-mint at 90d.
    FDB machine leaves (Bao-issued)               ~2026-10-01     service leaf: 30d set, 90d max. Fine, keep.
    Admin client cert (DR-time)                   2026-10-01      break-glass leaf: 30d set, 2y max. Fine (deliberately short).
    wt-control-gate-v2 (test leaf)                2026-09-11      WebTransport: 10d set, 14d max. Fine.

Five items are out of compliance with the table (three certs, two
missing gates). Followup task 18 covers bringing them into
compliance.

## Exceptions this rule does not cover

**Cross-signed certs during CA rotation.** RFD 2141's phases 2-3 mint
a leaf that chains to both the old and new intermediate for the
rotation window. That leaf's `notAfter` is whichever chain is
shorter. The transition window is the specific case where two CAs
overlap for a bounded time. Not covered here. RFD 2141 covers it.

**External CAs.** Nothing this RFD says binds a certificate issued by
Let's Encrypt, ZeroSSL, or a paid public CA. Those follow whatever
their issuer says.

**Client certs used only by machine identity (workload).** SPIFFE-
style short-lived (1 hour) X.509 SVIDs would sit under this row too
if we adopted them. Today we do not, so the row is not in the table.

## Sources

Cited in `.cff` files alongside this document so a citation gate can
walk them without parsing prose:

- `references/10-rfc5280.cff` (mandatory `notAfter`, §4.1.2.5)
- `references/20-mozilla-root-store-policy.cff` (15-year public-trust cap)
- `references/30-cabforum-sc081v3.cff` (200 → 100 → 47 day schedule)
- `references/40-ncsc-pki-principles.cff` ("as short as practical")
- `references/50-nist-sp-800-57-part1.cff` (cryptoperiod framing)
- `references/60-webtransport-servercerthashes.cff` (14-day WT ceiling)
