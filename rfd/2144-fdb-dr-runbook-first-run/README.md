# RFD 2144: The DR runbook runs, and the CA it needed lands

**State:** discussion
**Scope:** weftspun-fdb, weftspun-bao, Personal 1Password vault

## Decision

Mint the break-glass CA at DR-time, stash to `op://Personal/FDB-CA/`,
execute the R2-primary restore, and land the follow-ups the run surfaces:
Bao secret hygiene, R2 key rotation, Tigris fan-out refresh, scale to
three at `double` redundancy. The CA in 1P closes RFD 2141's prereq; the
runbook stops being theatre.

RFD 2141's phases 2–3 rotate the machine leaves to certificates the
restored Bao PKI mount signs, once Bao is unsealed against the restored
FDB. Until then, the cluster runs on the break-glass CA.

`WEFT_FDB_CLUSTER_ID` was not stored, so a fresh one was minted and
written to 1P as `weftspun-fdb cluster id`. Coordinator addresses
change on a rebuild anyway, so the identity change rides along.

Measurements — R2 snapshot age, `fdbrestore` timings, twelve inline
defects the runbook did not name — move to `DETAILS.md`.
`logbook-rfd2144-dr-runbook-first-run.md` records what was measured
during the run itself.

## Problem

RFD 2143 called its own DR runbook theatre because RFD 2141's break-glass
CA was not in 1Password. On 2026-09-01, `weftspun-fdb`, `weftspun-bao`,
`spot-broker` and `chibifire-com` were gone from Fly. Tigris and R2 both
survived — compute lost, storage kept — so the runbook had to run.

## Related

RFD 2134, 2135, 2140, 2141 (prereq landed here), 2143 (runbook executed).
