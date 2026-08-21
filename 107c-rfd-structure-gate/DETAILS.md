# RFD 107c details: each rule, its count, and what it repaired

## How the rules were chosen

Every candidate rule ran against all 116 RFDs before it became a check.
A rule that held with no exception shipped. A rule that needed an
exception list did not, and appears under "Measured and not gated"
below, with its count, because an omitted check reads exactly like a
passing one.

The survey script parsed each `README.md` and `DETAILS.md` with
`markdown-it-py` and counted heading sequences, preamble fields, states,
citations, and sibling files. It is not kept, because
`check-rfd-structure.py` now asserts what it measured.

## The rules, and what each measured

| rule | held before the gate |
| ---- | -------------------- |
| One level-1 heading, and it opens the document | 116 of 116 |
| Title reads `RFD <num>: <title>`, number equals the directory | 116 of 116 |
| A metadata paragraph sits under the title | 116 of 116 |
| Its fields are State, then Feature, then Scope | 116 of 116 |
| State is a value RFD 1000 lists | 115 of 116 |
| Problem, Decision, References and Related keep that order | 116 of 116 |
| A `## Decision` section is present | 114 of 116 |
| Every citation resolves to a directory or an ALIASES.md row | 116 of 116 |
| No citation uses the old decimal form | 84 of 116 |
| A README names its `DETAILS.md` | 87 of 89 |
| `DETAILS.md` reads `RFD <num> details: <title>` | 94 of 95 |
| A README is 40 lines or fewer | 108 of 116 |

Two of these need their exception stated, because the number above is
not 116 and the rule still shipped.

**A `## Decision` section.** The two without it are RFD 104a and
RFD 104e. Both carry `State: moved`, which means another repository now
develops the RFD, and a moved RFD states only where it went. The gate
requires a Decision unless the state is `moved`, and that holds at 116
of 116.

**A retracted decision renames its own heading.** RFD 1043 heads its
section "Decision, as published and now retracted". The gate matches a
heading that starts with `Decision` and a comma, so a retraction in
place does not have to hide behind the original title.

## Measured and not gated

**A `## Problem` section.** 111 of 116. The five without one are
RFD 1000, RFD 100c, RFD 100f, RFD 104a and RFD 104e. Two are abandoned,
two are moved, and RFD 1000 is the conventions document itself. The
carve-outs would outnumber the signal, so the gate checks the position
of Problem and not its presence.

**A `## Related` section.** 111 of 116. RFD 1014, RFD 1015, RFD 1016 and
RFD 1017 end at their Decision, and RFD 104a has no section at all. The
four look like omissions rather than a choice, and adding a section to
somebody else's RFD is an edit this work did not make.

## The line limit, and the two things it turned up

RFD 1000 stated "under 40 lines" and 8 of 116 READMEs exceeded it, at 41,
43, 46, 82, 93, 131, 152 and 179 lines. Five were long because they
carried a retraction in place, which `CLAUDE.md` requires, and that read
as a conflict between two house rules.

It was not one. A retraction stays next to what it retracts, and after a
move the thing it retracts is the detail, which lives in `DETAILS.md`.
So the retraction goes there too and the rule is unbroken. All eight
READMEs were split on that reading, and no retraction was deleted.

Splitting them turned up the second thing. With the eight fixed, **12
READMEs sat at exactly 40 lines**. Twelve files landing on one number is
not chance, so the bound the corpus keeps is inclusive and RFD 1000's
"under 40" was off by one. The document was corrected to "40 lines or
fewer" and the gate reads the number from that sentence.

Three of the eight needed real compression rather than a move: RFD 1079,
RFD 107a and RFD 107b state a long decision, and their READMEs went from
131, 152 and 182 lines to 39 each. Nothing was dropped. Every removed
section either moved into `DETAILS.md` or was already there in fuller
form, which is why three of them could go without a replacement.

## The defects the measurement found, and the repairs

| defect | count | repair |
| ------ | ----- | ------ |
| Citations in the old decimal form | 37 in 32 files | Rewritten from the ALIASES.md map. The substitution keeps the same four characters, so every line wrap is unchanged |
| `State: pre-discussion` | 1, RFD 1040 | Corrected to `prediscussion` |
| A state RFD 1000 does not list | 2, RFD 104a and RFD 104e | `moved` added to RFD 1000, because the use predates the list |
| A `DETAILS.md` no README named | 2, RFD 1076 and RFD 107b | A pointer line added before Related, where the other 87 put it |
| A `DETAILS.md` with a title of its own | 1, RFD 1000 | Retitled `RFD 1000 details: numbering` |
| READMEs over the line limit | 8 of 116 | Split into `README.md` and `DETAILS.md`, retractions included |
| RFD 1000's limit was off by one | 1 | Corrected to "40 lines or fewer", which is what 12 READMEs already sit on |
| A heading written twice on one line | 1, RFD 107a's `DETAILS.md` | `## What exists, and what does not## What exists, and what does not` |
| An RFD after the migration cannot pass | latent | See below |

The last one had not fired yet. `check-rfd-numbers.py` required an
ALIASES.md row for every directory. ALIASES.md maps an old number to a
new one, and an RFD written after the migration has no old number. This
RFD is the first such RFD, and it would have failed the gate that
records how it is numbered. The check now reads the migrated range out
of the table and applies only inside it.

## Why an AST, in a repository that had no dependency

The gap is measurable rather than theoretical. The byte scan found 3 of
the 37 unmigrated citations. The other 34 sat across a line break, and
`RFD` on one line with `0019` on the next is two unrelated tokens to a
regular expression and one citation to a reader.

Widening the expression to allow a newline would repair that one case.
It would not repair the next one, because the class of defect is reading
markup as text. The AST is where the distinction lives, and every later
rule here reuses it: the metadata fields come from the strong-emphasis
tokens rather than from counting asterisks, and the section spine comes
from heading tokens rather than from lines that start with a hash.

`markdown-it-py` is pinned in `scripts/requirements.txt`. A parser change
would move what the gate sees, and a gate that changes verdict without a
diff is not a gate.

## The negative controls

`python scripts/check-rfd-structure.py --self-test` builds a small tree
for each case and asserts the verdict. One case is a clean tree that
must pass. Fifteen are known-bad trees that must fail:

    title number disagrees with the directory
    the title is not the first block
    a second level-1 heading
    no metadata paragraph
    a state RFD 1000 does not list
    Scope written before Feature
    an unknown metadata field
    no Decision section
    Decision written before Problem
    a decimal citation split across a line break
    a citation that resolves nowhere
    a DETAILS.md the README never names
    a DETAILS.md titled for another RFD
    a README past the line limit RFD 1000 gives

`check-rfd-numbers.py` carries six of its own, including the pair that
bounds the migrated range: a number inside it with no row must fail, and
a number above it with no row must pass.

Both self-tests run before the gate itself in
`.github/workflows/checks.yml`, so each proves it can reject before it
judges the repository.
