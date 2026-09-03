# RFD 2137: RFD reports share one sheet

**State:** discussion
**Feature:** the page template an RFD report is published from
**Scope:** any RFD published as a page; the PERT sheet's design system

## Decision

One template, `template.html` in this directory, in the PERT sheet's
design system: Libre Franklin over IBM Plex Mono, the
paper/ink/critical/done/steel tokens, light and dark themes resolved
at the token level. To publish a report, copy the file, replace every
bracketed slot, and keep the worked example's shape.

The layout encodes the agreements rather than describing them:

- the serial header and stamps mirror the RFD frontmatter;
- every measurement table carries its baseline row, and the chosen
  row takes the green rail;
- the figure is an inline SVG in currentColor with labelled arrows,
  one claim, stated again in its aria-label;
- the retraction block is bordered in the accent and sits in place,
  next to what it retracts;
- the controls card lists each planted defect the gate caught;
- the provenance foot points at the logbook, the PRs, and the
  command to re-run, and pairs physical measurements with a
  household-object equivalent.

## Problem

RFD reports published as pages have no shared shape: each one
reinvents its header, its tables, and its palette, and the working
agreements the documents encode (retractions in place, baselines
beside numbers, controls named) have no slot a page reminds an author
to fill.

## Verification

The worked example filling the slots is RFD 2134, so the template is
demonstrated by a report that shipped rather than by lorem.
