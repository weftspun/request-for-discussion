# RFD 2209: CC-BY-NC blocklist entry — details

## The BLOCKLIST.md section to add

Below the `CC-BY-SA` section, add:

    ### CC-BY-NC (all versions)

    A non-commercial restriction on a row propagates into any
    corpus, dataset, or artifact that ships the row. The
    workspace's deployments (VRChat, service demos, HF datasets,
    trained models) are commercial in the sense the licence
    excludes — sales, ad-supported distribution, and paid access
    are all on the table for shipped work, and a licence that
    reserves them defeats the downstream question before it is
    asked.

    Same shape as CC-BY-SA's row. Different clause (non-commercial
    vs. share-alike); the downstream cost of ignoring it is the
    same.

    **Concrete case (2026-09-05):** dataforged
    (`github.com/rsek/dataforged`) carries a mixed licence.
    `dist/starforged/*.json` is CC-BY-4.0 and ships as
    `chibifire/starforged` on HuggingFace. The `ironsworn/`
    subtree and raster illustrations are CC-BY-NC-4.0 and are
    filtered out by `scripts/build_starforged_hf.py` before the
    parquet write. `scripts/check_starforged_hf.py` asserts every
    surviving row is CC-BY-4.0 as a rule-3 named-not-silent gate.

    **What is not banned.** Reading CC-BY-NC content for
    inspection, citing it in an RFD, or naming it as a source is
    fine. Shipping its content in a derived corpus is the case
    this row covers.

## Filter implementation shape

Every builder that ingests a mixed-licence source carries the
same three-step shape:

1. Read the source row.
2. Consult the row's licence field (dataforged tags each entry;
   other sources may need per-source lookup logic).
3. If `licence in {"CC-BY-NC-4.0", "CC-BY-NC-3.0",
   "CC-BY-NC-SA-*", "CC-BY-NC-ND-*"}`, drop the row and
   increment a counter.

At the end of the build, print the drop count and a per-licence
histogram of dropped rows. A silent skip reads as a pass; rule 3
says name the count. The reference implementation is in
`scripts/build_starforged_hf.py` from the current session.

## Verification

- **Positive:** `check_starforged_hf.py` reads the shipped
  parquet shards and asserts `every row's licence == CC-BY-4.0`.
- **Negative control** (rule 2): the checker's `--self-test`
  mutates one row's licence field to `CC-BY-NC-4.0` in memory
  and asserts the checker fails on that row.
- **Builder self-test:** `build_starforged_hf.py --self-test`
  runs against a small hand-built fixture with a planted
  CC-BY-NC row and asserts the row is dropped, the drop count is
  1, and the output does not contain the row's id.

## Related retractions

None. The blocklist row is additive; no earlier decision is
withdrawn. The corresponding CC-BY-SA row on the blocklist is not
touched.

This RFD was drafted by an AI and read by a human before it shipped.
