# RFD 1000: Conventions

**State:** published
**Scope:** all files

## Decision

This repository writes Request-for-Discussion documents in the Oxide
style. Each RFD has a state: prediscussion, ideation, discussion,
published, committed, abandoned, or moved. A moved RFD names the
repository that now develops it.

Technical writing follows ASD-STE100 Simplified Technical English.
An essay follows the AI-trope gate, and a section names which one it
takes. RFD 1125 gives that rule. Code and identifiers follow neither.

The repository keeps designs in one place. The decisions directory
records durable decisions. The docs tree holds detailed designs.
An RFD points to its source. It does not copy the source.

Each RFD's `README.md` stays at 40 lines or fewer. It states the
problem and the decision, in the fewest lines that keep both true.
A measurement, a verification log, a deep walkthrough, or a code
sample does not fit. Move it to a sibling file, such as
`DETAILS.md`, in the same RFD folder, and name that file in one
line. A retraction moves with the rest, and stays next to what it
retracts, which after the move is the detail it corrects.

## References

- RFD style: `rfd-driven-architecture` skill
- Numbering rule and OID arc: `DETAILS.md`. Serials in use: `SERIALS.usda`
- STE spec: https://www.asd-ste100.org/ Tropes: https://tropes.fyi
- STE linter: the `simplified-technical-english` Claude Code plugin
  (`fire/claude-ste-plugin`). RFD 1063 records the move off a
  repo-local script.

## Related

See the DRY policy and the STE policy in `decisions/README.md`.
