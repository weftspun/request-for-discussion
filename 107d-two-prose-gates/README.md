# RFD 107d: Two prose gates, marked per section

**State:** discussion
**Feature:** prose enforcement, and which rule reads which section
**Scope:** `1000-conventions/README.md`, `tropes-removal-model`

## Problem

RFD 1000 requires ASD-STE100 for every document here, and that rule was
written for one kind of writing but is applied to two.

ASD-STE100 is a controlled language for technical writing, and a schema table
is better under it. An argument is not, because a controlled vocabulary
flattens an argument into a specification. An essay also fails in a way
ASD-STE100 never describes, since it can read as though a model wrote it.
Neither kind owns a whole file either: a `DETAILS.md` carries a measurement
beside the reasoning that motivates it.

## Decision

**Technical writing answers to ASD-STE100**, through the existing enforcer:
code comments, error messages, procedures, any measurement or schema.

**An essay answers to `seeds/ai_trope.parquet`**, which already exists,
seeded from https://tropes.fyi. A `README.md` is an essay throughout. That
table assigns READMEs to ASD-STE100 today, and this RFD reverses it.

**A section names its own gate, in an HTML comment under its heading.** These
gates read a CommonMark AST, so the mark is a block token they see already.

**An unmarked section fails.** A silent skip reads exactly like a pass.

**A rule ships only after it runs against the corpus**, the bar RFD 107c set.
Three of the table's fifteen detectors cannot fire, so they wait on repair.

## Related

RFD 1000 states the rule this supersedes. RFD 103f moved enforcement to a
write-time hook, so this adds a hook and not a script. RFD 107c gives the
measure-first rule, and the reason these gates read an AST.
