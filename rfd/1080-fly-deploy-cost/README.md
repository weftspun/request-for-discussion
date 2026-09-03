# RFD 1080: What the three Fly deploys cost

**State:** published
**Scope:** the deploy target

## Decision

Record it, from Fly's own published pricing page, against this
deployment's own real machine sizes, checked live with `flyctl`, not
estimated. See `DETAILS.md` for the full breakdown.

**Total: $0.012845/hour, $9.26/month, $111.12/year**, at today's
sizes: three `shared-cpu-1x` machines (two 512MB, one 256MB, the
last scaled from Fly's default 2-machine HA pair to one), a 3GB
Volume, and a 1GB Volume.

Not included: outbound bandwidth (usage-based, has a free tier
before per-GB billing), and any future Tigris usage RFD 1073's
still-open fetch-path work would add.

## Problem

`weftspun-studio`, `weftspun-character-taxonomy`, and
`weftspun-usd-viewer` all run as real, billed Fly Machines and
Volumes now. No record states what that costs, hourly, monthly, or
yearly.

## Related

RFD 1062 gives the Fly.io toplevel. RFD 1076 gives the `apps/` split
across three Fly apps. RFD 1079 gives `versitygw`'s removal, no
change to this total since it ran inside an already-billed machine.
