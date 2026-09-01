# RFD 2147: Bao is critical infrastructure now

**State:** discussion
**Scope:** weftspun-bao, its consumers, its DR runbook.

## Problem

Bao was one machine, Shamir seal single share, operator+1P recovery
per restart. RFD 2140's `ha_enabled = "false"` fit that framing. RFD
2146 then moved every routine credential read, coordination write,
and policy check onto Bao. Every consumer now depends on Bao being
up, and RFD 2140's reliability budget is smaller than what routes
through Bao now needs.

## Decision

Bao's availability class rises to match its consumers'. Recovery
becomes hands-off, not operator-with-1P.

1. **Replicas across zones, coordinated over FDB.** `ha_enabled = true`,
   three Bao machines minimum (matching FDB's three-zone spread and
   fault-tolerance-1 posture); consumers hit `weftspun-bao.internal`.
2. **Auto-unseal.** HA without auto-unseal is theatre. A fleet
   restart returns the operator to the critical path. KMS-backed
   seal wrapper removes the human from routine restarts; the Shamir
   key in 1P stays as break-glass (RFD 2144 defect #11's day).
3. **Consumers cache what they can.** A bearer held for a few
   minutes puts Bao in the critical path only at cache expiry.
4. **No CDN proxy in front of workspace services.** CF-proxied
   records have Cloudflare terminating TLS at its edge, every byte
   plaintext at CF for the round trip. Workspace services stay
   DNS-only; edge cache, if needed, is Fly-side or origin-side.

Details, sub-decisions, migration in `DETAILS.md`. S2147.

## Related

RFD 2140, 2144, 2145, 2146.
