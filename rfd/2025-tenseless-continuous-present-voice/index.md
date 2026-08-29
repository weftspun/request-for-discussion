---
title: "RFD 2025: Comments and docs use a tenseless continuous-present voice"
rfd: "2025"
state: published
scope: prose style for comments, docs, and decision records
---

## Problem

A comment written as history, such as "added a cache", names a
past moment. A comment written as a plan, such as "will solve this",
describes a future moment. A reader cannot check either kind of
comment against the code in front of them.

## Decision

A comment written as history ("added a cache") or as a plan ("will
solve this") describes a moment that has passed or has not yet
arrived, so a reader cannot check it against the code in front of
them. The project writes every comment, doc page, and decision record
in a tenseless continuous-present voice: each sentence states what is
currently true of the system. An unfinished area reads as a present
gap ("the parser handles no Unicode escapes yet"), not as a task or a
past edit. This rules out past-tense edit narration, future or
imperative planning, and aging temporal qualifiers such as "now" or
"previously". A sentence that states a present truth stays correct as
long as the code stays the same, and goes stale visibly the moment the
code changes.

## References

- Full context, decision drivers, considered options, consequences,
  and confirmation steps: `DETAILS.md`
- Original record:
  `decisions/20260607-tenseless-continuous-present-voice.md`

## Related

- `rfd/2026-commit-messages-sentence-case`: a commit body states what
  the change makes true of the system, the same voice.

## Detail

{{< include DETAILS.md >}}
