---
title: "Taskweft — Manuals"
toc: false
---

Taskweft builds a loop where a person makes a character, dresses it,
and then either wears it or talks to it. This site is that project's
design record. It holds what was decided, what was measured, and what
has since been withdrawn.

## Start here

**New to this?** Read these three, in order. They take about fifteen
minutes together.

1. [**RFD 1171**](../1171-the-presence-loop-and-every-role-in-it/) —
   what the project is building, and which part every model plays.
2. [**RFD 1000**](../1000-conventions/) — how to read any document
   here. The states, the numbering, the section order.
3. [**Working agreements**](pages/agreements.qmd) — the standing
   constraints. What may enter a training corpus, and what may not.

## Everything else

[**RFDs**](pages/rfd.qmd) — the design records. Sort by state to see
what is settled and what is still open.

[**Serials**](pages/serials.md) — the register. Every number this site
has allocated and every one it has retired.

[**Logbook**](pages/logbook.qmd) — what was measured, with enough
apparatus to run the test again.

## Two things that will confuse you first

**Documents here contradict themselves on purpose.** When a number
turns out to be wrong, the correction goes _next to_ the original
rather than replacing it. So a document may say a thing and then
withdraw it a paragraph later. That is not an editing failure. A reader
who knows which roads are dead ends is better off than one who only
knows where the road ends today. Look for the paragraph in bold capitals
— that is usually a retraction.

**A number is an identity, not a date.** RFD 1171 is not newer than RFD
1170 in any meaningful sense, and a low number is not obsolete. Serials
are allocated once and never reused, because each one is the last arc of
an OID under the 66606 Private Enterprise Number. Renaming a document
does not renumber it.

## What holds it together

Where a document states a measurement or a rule, a script checks that
statement against live code. Drift fails a command instead of being
found six months later. `check_anti_entropy.py` walks those pairs and
reads every one of them rather than sampling.
