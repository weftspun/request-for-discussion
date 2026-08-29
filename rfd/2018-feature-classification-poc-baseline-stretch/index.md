---
title: "RFD 2018: Feature classification — proof of concept, baseline, stretch"
rfd: "2018"
state: published
scope: capabilities-table
---

## Problem

Each feature in the capabilities table needs a stated commitment
level. Free text does not state whether a feature is a proof of
concept, a shipped baseline, or a stretch goal. A maturity ladder, such
as alpha, beta, or stable, states how polished a feature is, not how
committed the project is to shipping it.

## Decision

Each feature in the capabilities table carries one of three commitment
tiers, instead of free text. A proof of concept demonstrates the idea
works end to end, in partial or throwaway form; it may be unreliable or
lossy, and nothing depends on it yet. The baseline is the committed
minimum the product ships; it works reliably across the target
platforms. A stretch goal goes beyond baseline; the project pursues it
if time allows, and cutting it does not block the release. This
three-tier classification was chosen over free text or a maturity ladder
(alpha/beta/stable), because it captures commitment, which is what
planning needs, not just maturity. A feature moves between tiers as it
matures or as commitment changes; the tier is the current call, not a
permanent label.

Initial triage: native video playback, scene baking via OpenUSD, spatial
audio, and speech are baseline; pen stroke creation (cassie) is a proof
of concept.

## References

- Decision drivers, considered options, and confirmation: `DETAILS.md`
- Original record: `decisions/20260606-feature-classification-poc-baseline-stretch.md`
- Capabilities table: `decisions/20260613-repository-and-capability-inventory.md`

## Related

`rfd/2014-art-game-loop-steel-thread/index.md` uses the cassie pen this
classification tiers as proof of concept.

## Detail

{{< include DETAILS.md >}}
