---
title: "RFD 2000: Conventions"
rfd: "2000"
state: published
scope: all files
---

## Decision

This repository writes Request-for-Discussion documents in the Oxide
style, the same style `weftspun/request-for-discussion` uses. Each RFD
lives in its own folder, `rfd/NNNN-kebab-title/`, not a single flat
file. Each RFD has a state: prediscussion, ideation, discussion,
published, committed, abandoned, or moved.

Each RFD's `index.md` has a `## Problem` section before `## Decision`.
The `## Problem` section states, in one short paragraph, what is wrong
or missing today, and why that matters. A reader must understand the
problem before they read the decision.

Quarto renders the folder through `index.md`, and its frontmatter
carries the title, the number, the state, and the scope.

The repository writes prose in ASD-STE100 Simplified Technical
English. Code and identifiers do not follow STE. STE applies to
documents, comments, and user-visible text.

The repository keeps designs in one place. `decisions/` holds MADR
records, one point decision each, dated. An RFD points to a MADR, a
source file, or another RFD. It does not copy the source.

A section belongs in `index.md` when a reader needs it to reach the
decision. A measurement, a verification log, a status table, or a deep
walkthrough goes to a sibling file, `DETAILS.md`, in the same RFD
folder. The `index.md` names that file under `## References` and pulls
it in at the end with `{{< include DETAILS.md >}}`, so one page renders
whole and the short form stays readable on its own.

`decisions/` (MADR, `YYYYMMDD-title.md`) still records a single point
decision. `rfd/` records a longer-lived design that can carry a
proposal forward and get amended over time. The project migrates
existing MADR files into `rfd/` gradually. Once a MADR file has a
matching `rfd/NNNN` folder, delete the MADR file. Do not keep a
pointer stub. Git history still holds the deleted file's content and
its old path.

An RFD number is four decimal digits. The first digit names the organization and
this repository uses **2**; the last three are the serial. A new RFD takes a serial
`SERIALS.usda` does not already list, and appends a row for it.

The digits were hexadecimal from 2026-08-20 to 2026-08-25, and 119 of the 129 RFDs
here wore a number that has now changed. An OID arc is decimal, so a hex document
number needed a conversion at every crossing between the folder name and the arc.
RFD 2010 was arc 4106 and nothing in the name said so.

The old rule said to check this listing and "not any other repo's own numbering",
which was the right instruction for a space this repository owned alone, and it did
not own it alone. `weftspun/request-for-discussion` numbered from 0000 up as well,
and 113 numbers named a document in both places, so a citation of the bare number
0021 identified nothing.
The organization digit is what makes the old instruction safe: another organization
cannot reach digit 2, so there is nothing to coordinate.

The digit is a short name for an arc under an IANA Private Enterprise Number. PEN
66606 is assigned to iFire, and RFC 9371's assignment is
itself the delegation, so no arc below it is registered with anybody.

One arc under the PEN names a namespace rather than a site: `66606.1` is documents,
and a site sits under that. weftspun is `66606.1.1`, this repository is
`66606.1.2`, `v-sekai/manuals` reserves `66606.1.3` and `fire/manuals` reserves
`66606.1.4`. So RFD 2010 is `urn:oid:1.3.6.1.4.1.66606.1.2.2010`, and the last arc
is the four digits the folder name already writes.

`SERIALS.usda` lists every serial this site has allocated. A serial is appended
once, never removed and never reused, because it is the last arc of an OID and an
arc names one document for as long as it exists. `scripts/check-rfd-serials.py`
holds it against the tree and against its own previous revision, so a renumbering
fails on the serials that go missing.

`ALIASES.md` is deleted rather than extended to a third column. The decimal serial
equals the pre-hex number in all 129 rows it held, so an old number resolves by
prepending the organization digit rather than by a lookup. A hex number from the
five days between does not resolve by rule, and that is the cost of the deletion.

## References

- RFD style: `weftspun/request-for-discussion`, `0000-conventions`
- STE spec: https://www.asd-ste100.org/
- STE linter: the `simplified-technical-english` Claude Code plugin

## Related

See `pages/rfd.qmd` (rendered as `pages/rfd.html`) for the live, sortable index.
