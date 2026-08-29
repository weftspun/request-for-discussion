---
title: "RFD 2130: Every repository we have authority over states what it is made of"
rfd: "2130"
state: discussion
scope: the CITATION.cff gate, and the three categories of authority it rests on
---

## Problem

`CLAUDE.md` has required a `CITATION.cff` in every repository since the conversion off `meta`,
and nothing enforced it. Fourteen repositories had one and the rest did not, which made the file
read as a habit of the Lean workspaces rather than as a rule. This project already calls that
shape of rule a suggestion: a claim no command can falsify does not defend itself.

The reason to want it is provenance. A repository's dependency file cannot hold a journal
article, a vendored subtree, or the design somebody else published. `interactor-ward` is the
case that shows it: a clone of one repository, vendoring a second and a third, implementing a
published design, against numbers proved in four Lean workspaces, none of it visible in a
manifest.

## Decision

**A gate.** `mix check authority` fails when a repository this organisation has authority over
carries no `CITATION.cff`. It asks two things, because presence is the weaker half: the file
must have a `title:`, and it must have a `references:` key. Provenance is why the file exists,
and one with no references reads as current while saying nothing. A repository genuinely built
on nothing states `references: []` and means it.

**Authority and authorship are different questions, and one list had been answering both.**
There are three categories, not two:

- **Ours outright.** Every gate applies.
- **A fork we maintain.** It sits on our own remote, so it is ours to push to and ours to add
  files to: the licence, `CITATION.cff` and `.DS_Store` gates all reach it. Its README does not,
  because editing that forks a document upstream owns and this project would carry the diff
  forever.
- **Another organisation's.** Membership is not authority, so nothing here writes to one at
  all — not a README and not a `CITATION.cff`.

Only the third is out of reach. The middle category is the correction: excusing a fork from the
licence and citation gates confused "we did not write the prose" with "we may not add a file",
and left the repositories whose provenance most needs stating as the only ones never asked for
it. A fork is upstream's code plus a branch nobody upstream has, and nothing else in the tree
says which is which.

## What it found

Twenty-one repositories, including `datasource-foundationdb`, `idtx-flow` and `entities-godot`,
which are exactly the three the old boundary excused.

## References

- `CLAUDE.md`, "Citation": the rule this gate enforces
- RFD 2124: the Fine gate, added under the same argument
