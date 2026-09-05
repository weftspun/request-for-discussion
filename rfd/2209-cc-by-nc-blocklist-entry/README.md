# RFD 2209: CC-BY-NC as a blocklist entry

**State:** discussion
**Feature:** add `CC-BY-NC` (all versions) to CLAUDE.md's blocklist
alongside `CC-BY-SA`, and gate build scripts to drop CC-BY-NC rows
before shipping any derived corpus
**Scope:** every corpus builder that reads a mixed-licence source
document; today's concrete case is
`scripts/build_starforged_hf.py` and `build_starforged_sqlite.py`
against the dataforged repo

## Decision

Add a row to CLAUDE.md's "Blocklists" table:

    | **CC-BY-NC (all versions)** | non-commercial restriction propagates into anything derived from the row — same downstream-risk shape as CC-BY-SA — see below |

with a corresponding section in `BLOCKLIST.md` argued below. The
row is enforced two places:

1. **Build-script filter.** Any script that ingests a mixed-licence
   source reads each row's licence field and drops CC-BY-NC rows
   before the parquet or SQLite write. Reports the drop count as a
   rule-3 named-not-silent gate.
2. **CI on manuals-weftspun.** `scripts/check_starforged_hf.py`
   asserts `every row's licence == CC-BY-4.0` (or another
   commercial-clean licence the workspace already accepts). A
   CC-BY-NC row surviving the filter fails CI.

The rule does NOT ban *reading* CC-BY-NC content locally for
inspection. It bans CC-BY-NC rows from shipping in a derived
corpus, a training dataset, a demo fixture, or any artifact this
workspace publishes.

## Problem

Concrete case that produced this RFD: **dataforged** — the
community JSON rendering of the Starforged and Ironsworn SRDs at
`github.com/rsek/dataforged` — carries a mixed licence:

- `dist/starforged/*.json` — CC-BY-4.0. Ships.
- `ironsworn/` subtree — CC-BY-NC-4.0. Filtered out.
- Raster illustrations — CC-BY-NC-4.0. Filtered out.

Without the filter, `chibifire/starforged` on HuggingFace would
have shipped CC-BY-NC rows mixed with CC-BY-4.0 rows under a
single licence declaration. That is a licence-provenance failure
for downstream consumers who take the workspace at its word that
`chibifire/starforged` is CC-BY-4.0. The filter closes it. The
row on CLAUDE.md's blocklist ensures the *next* mixed-licence
source (dataforged is not going to be the last) inherits the same
handling by default rather than by anyone remembering.

The failure mode is the same as CC-BY-SA's — a share-alike or
non-commercial restriction that propagates into anything derived
from the row. Different clause, same downstream shape. The CC-BY-SA
row already on the blocklist is the argument this row mirrors.

## Non-goals

Not a rule against every restrictive licence — CC0, MIT, Apache,
CC-BY-4.0, and the other permissive licences the workspace
already accepts continue to. Not a rule against downloading
CC-BY-NC content for personal inspection (an operator reading the
Ironsworn PDF is fine; a corpus builder ingesting its text is not).
Not a rule against forking or citing CC-BY-NC works — attribution
of a source is different from shipping its content.

## Related

- CLAUDE.md's existing `CC-BY-SA` row — same shape, same argument.
- RFD 2205 (Taskweft in Bao) — the Starforged play surface whose
  corpus is the concrete case.
- Codebase: `2-contract/manuals-weftspun/scripts/build_starforged_hf.py`
  and `build_starforged_sqlite.py` — the reference filter
  implementations.
- Codebase: `2-contract/manuals-weftspun/scripts/check_starforged_hf.py`
  — the downstream CI assertion.

This RFD was drafted by an AI and read by a human before it shipped.
