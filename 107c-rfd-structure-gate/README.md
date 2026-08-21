# RFD 107c: The RFD structure gate reads a CommonMark AST

**State:** committed
**Scope:** `scripts/check-rfd-structure.py`, `scripts/check-rfd-numbers.py`,
`scripts/requirements.txt`, `.pre-commit-config.yaml`,
`.github/workflows/checks.yml`

## Problem

This repository held 116 RFDs and one gate. That gate checked numbers.
Nothing checked the shape of a document, so the shape stayed an
agreement each writer kept from memory.

A measurement over all 116 found nine kinds of defect. The largest was
37 citations still in the old decimal form. The number gate looked for
those and reported 3. An RFD wraps its prose at about 72 columns, so a
citation splits across a line break, and a scan of the bytes cannot see
it. That gate measured the file. The rule is about the sentence.

## Decision

`scripts/check-rfd-structure.py` parses each `README.md` and `DETAILS.md`
into a CommonMark AST and checks the document against that tree. It
joins the inline text of a paragraph before it matches, so a wrapped
citation is one citation. It found all 37.

Each rule ran against all 116 RFDs before it became a rule. A rule that
needed an exception did not ship. The gate reads both its state list and
its README line limit out of RFD 1000, so document and gate cannot drift
apart. It takes one dependency, `markdown-it-py`, pinned. The number
gate keeps numbering only, and its weaker citation scan moved here.

## Related

RFD 1000 gives the conventions this gate measures. RFD 103f moves the
prose rules to a plugin, and this gate checks structure only.

See `DETAILS.md` for each rule, its count, the ungated conventions, the
line limit and the two things it turned up, the defects repaired, and
the negative controls.
