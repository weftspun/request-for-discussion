---
name: rfd-2177-flight-levels-taxonomy
description: When tagging an RFD's altitude, use the flight_level field on its serial-register entry. Values are L1 (operations, single-team execution), L2 (coordination, cross-team value flow), L3 (strategy, portfolio bet). Follow Klaus Leopold's numbering (L1 = ground, L3 = altitude). Tagging is opt-in.
tools: Read, Edit
---

# RFD 2177: Flight Levels taxonomy for RFDs

**State:** committed
**Feature:** classify every RFD by which altitude of work it describes
**Scope:** `SERIALS-*.usda` schema, `scripts/render_flight_level_pages.py`,
`_quarto.yml` navbar, `pages/flight-level-*.qmd`

## Decision

Every RFD carries an optional `flight_level` tag, L1/L2/L3 (Flight Levels: execution / coordination / strategy), and three Quarto listings render from that tag; tagging is opt-in.

## Problem

An RFD describes a decision at some altitude of work (portfolio bet, cross-team coordination, or a single team's execution), but the register carries no field for that altitude. A reader wanting "all the strategy decisions" reads every RFD and infers.

## Details

  L1  Operations    how a single team executes; fast cadence
  L2  Coordination  how work flows across teams to deliver value
  L3  Strategy      portfolio decisions about where to invest

Numbering follows Klaus Leopold's original: L1 is ground, L3 is altitude, matching the flight-altitude metaphor. The register is greenfield for this axis, so no earlier convention needs inverting.

`scripts/render_flight_level_pages.py` reads the tag from every serial register and writes three Quarto listings under `pages/flight-level-{1,2,3}-*.qmd`. Navbar carries a Flight Levels dropdown. Untagged RFDs stay off the three pages.

See DETAILS.md for the tag schema, the render script's shape, and the Klaus Leopold citation.

## Related

RFD 1000 (RFD conventions), RFD 1053 (OpenUSD internal format), RFD 2174 (open-abandoned index) and RFD 2176 (committed-terminal index): same pattern of one document plus tag.

This RFD was drafted by an AI and read by a human before it shipped.
