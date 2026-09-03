# RFD 2177: Flight Levels taxonomy for RFDs

**State:** committed
**Feature:** classify every RFD by which altitude of work it describes
**Scope:** `SERIALS-*.usda` schema, `scripts/render_flight_level_pages.py`,
`_quarto.yml` navbar, `pages/flight-level-*.qmd`

## Problem

An RFD describes a decision at some altitude of work (portfolio bet,
cross-team coordination, or a single team's execution), but the
register carries no field for that altitude. A reader wanting "all
the strategy decisions" reads every RFD and infers.

## Decision

Every RFD in the register carries an optional `flight_level` tag:

  L1  Operations    how a single team executes; fast cadence
  L2  Coordination  how work flows across teams to deliver value
  L3  Strategy      portfolio decisions about where to invest

Numbering follows Klaus Leopold's original. L1 is ground, L3 is
altitude, matching the flight-altitude metaphor. The register is
greenfield for this axis, so no earlier convention needs inverting.

`scripts/render_flight_level_pages.py` reads the tag from every
serial register and writes three Quarto listings under
`pages/flight-level-{1,2,3}-*.qmd`. Navbar carries a Flight Levels
dropdown. Untagged RFDs stay off the three pages; tagging is opt-in.

See `DETAILS.md` for the tag schema, the render script's shape, and
the Klaus Leopold citation.

## Related

RFD 1000 (conventions), RFD 1053 (OpenUSD internal format), RFD 2174
+ 2176 (citation-drift indexes, same pattern of one document + tag).

This RFD was drafted by an AI and read by a human before it shipped.
