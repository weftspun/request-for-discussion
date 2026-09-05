# Logbook: starforged.sqlite build

Built 2026-09-05 by
`2-contract/manuals-weftspun/scripts/build_starforged_sqlite.py`
from the `rsek/dataforged` JSON. Ships as
`7-service/service-sqlar-cas/docs/fixtures/starforged.sqlite`,
loaded by the browser demo via HTTP `Range: bytes=0-`.

## Measurement

| stage | size | notes |
|---|---|---|
| Input: `dist/starforged/dataforged.json` | 5.1 MB | same source as the HF dataset build |
| Output: `starforged.sqlite` | 984 KB | 9 tables + 3 indexes |
| **Reduction** | **~5×** | ETNF-shaped relational schema, no compression |

Household anchor: 984 KB is roughly the length of an AAA
battery's worth of bytes (small enough that the whole file
range-fetches into the browser in a single HTTP round-trip;
measured ~800 ms wall-clock — roughly a stacked penny of latency
against a typical uplink).

Row counts (asserted by `check_starforged_sqlite.py`):

- `moves` = 56
- `assets` = 90
- `oracles` = 250
- `encounters` = 23
- `truths` = 14
- `oracle_rows` = 4126
- `move_outcomes` = 152
- `asset_abilities` = 270
- `truth_options` = 42

## Apparatus

- **Schema:** ETNF per CLAUDE.md's carve-out for local SQLite
  work. Nine tables joined by foreign key. Distinct from the HF
  dataset's denormalized wide-row shape — same content, two
  presentations.
- **Indexes:** three, on the join keys the demo hits most
  (`move_outcomes.move_id`, `asset_abilities.asset_id`,
  `oracle_rows.oracle_id`).
- **Licence filter:** identical to the HF builder — CC-BY-NC-*
  rows dropped before the SQL insert, drop count printed.
- **Invariants asserted at build time** (rule 3, named-not-silent):
  every move has ≥1 outcome; every FK resolves; every oracle
  table's rows cover `[1, 100]` without gap or overlap.
- **Negative controls:** `check_starforged_sqlite.py --self-test`
  plants a missing outcome, an oracle gap at 51, and an orphan FK
  in an in-memory DB; asserts the checker fails on each.

## Range-fetch verification

`docs/starforged.js` fetches `fixtures/starforged.sqlite` with
`Range: bytes=0-`, sql.js loads the page pool, the demo boots
under a second wall-clock. Playwright scenario 1 (`Boot &
render`) asserts the load path end-to-end.

## Retractions

None. First build.

## Related

- RFD 2205 (Taskweft in Bao) — the fixture shape parallels
  `fleet.sqlite`.
- RFD 2208 (decision-point control surface) — the demo that
  reads the SQLite.
- `logbook-starforged-hf-dataset-build.md` — the parquet mirror
  of the same content.
