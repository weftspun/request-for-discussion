# RFD 1174: Publish the security rules against SOC 2 and ISO 27001

**State:** discussion
**Feature:** an outside reader verifies the workspace's security posture
**Scope:** `CLAUDE.md`, `BLOCKLIST.md`, a new `SECURITY-CONTROLS.md`

## Decision

Publish the rules against two known frames: SOC 2 (2017 Trust Services
Criteria, revised 2022) and ISO/IEC 27001:2022 Annex A. Neither replaces
a rule; each names one under an identifier the outside reader already
knows. Documentation-only, FOSS: no auditor, no certified ISMS, no
third-party attestation.

The mapping lives in a new `SECURITY-CONTROLS.md`. Each row cites its rule
by file and line and its control by identifier and version. A row without a
rule states a gap and holds no identifier.

`scripts/check_security_controls.py` gates it: resolve every citation,
verify every identifier against a machine-readable register beside the
mapping, fail on either miss, negative control included. `DETAILS.md`
carries the coverage table, the gap list, and the argument for two frames
rather than one.

## Problem

The workspace's rules live in `CLAUDE.md` and `BLOCKLIST.md`. An outside
reader who asks "do you meet SOC 2?" or "which ISO 27001 controls apply?"
receives a paragraph, not a control identifier. Coverage the rules already
give reads as absent.

## References

1. Coverage table, gap list, and the two-frame argument: `DETAILS.md`
2. Unwritten until `committed`, and costed in `DETAILS.md`: the gate
   `scripts/check_security_controls.py` and both control-register CSVs

## Related

RFD 1000 (conventions). RFD 1125 (AI-trope gate).
