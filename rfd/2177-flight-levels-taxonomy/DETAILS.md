# RFD 2177 details: tag schema, render script, citation

## Tag schema

Every RFD entry in `SERIALS.usda` or `SERIALS-vsekai-fabric.usda` may
carry a `flight_level` field:

```usda
def "S2177" {
    custom string slug = "flight-levels-taxonomy"
    custom string flight_level = "L3"    # optional: L1 | L2 | L3
}
```

Values are strings `"L1"`, `"L2"`, `"L3"`. Absent field means no
level classification; the RFD stays off the three per-level pages.

## Render script

`scripts/render_flight_level_pages.py` reads the tag from every
serial register and writes three files:

  pages/flight-level-1-operations.qmd
  pages/flight-level-2-coordination.qmd
  pages/flight-level-3-strategy.qmd

Each is a Quarto listing whose `contents:` names the `rfd/NNNN-slug/
index.md` paths of the RFDs tagged at that level. The listing sorts
by RFD number descending, matches the format of `pages/rfd.qmd`, and
regenerates on every render pass.

## Klaus Leopold citation

The Flight Levels model is Klaus Leopold's, first published as an
organizational-improvement framework. Cite as:

```yaml
cff-version: 1.2.0
type: book
title: >-
  Rethinking Agile: Why Agile Teams Have Nothing To Do With Business
  Agility
authors:
  - family-names: Leopold
    given-names: Klaus
year: 2018
publisher:
  name: LEANability
isbn: "978-3-903205-16-9"
url: https://www.klausleopold.com/rethinking-agile
```

## Trade-offs recorded

- **Tag, not new arc.** A structural namespace (site 5 = Level 1,
  site 6 = Level 2, site 7 = Level 3) was on the table and dropped.
  A tag is a data axis; a site is a URN axis. Levels change more
  often than URNs are allowed to, so a tag fits the churn.
- **Optional, not required.** Untagged RFDs stay in the register.
  Retrofitting 176 existing RFDs at once loses more than it gains.
- **Leopold's numbering (L1 = ops, L3 = strategy).** Renumbering him
  to match RFD-serial-lower-is-more-foundational was proposed and
  rejected: the flight-altitude metaphor is the naming, and a
  greenfield tag has no reason to invert its source.
