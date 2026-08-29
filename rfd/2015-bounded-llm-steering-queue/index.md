---
title: "RFD 2015: Bound the LLM steering queue to avoid context overflow"
rfd: "2015"
state: published
scope: process
---

## Problem

The project steered an LLM with a task queue held only in the
conversation. An unbounded queue held only in conversation overflows
two scarce resources. The operator loses track of what is still open
versus done, and the model's context window fills up.

## Decision

The project steers an LLM by externalizing, bounding, and compacting the
task queue, instead of holding an unbounded queue in the conversation.
Decisions land as MADRs in the manuals, and in-flight work lands as PRs
or issues; the conversation holds only the active item, and the backlog
lives in durable, searchable storage. Work in progress stays bounded to
one concern per PR, merged before the next starts. Completed work is folded into durable artifacts (a changelog or
an MADR) and dropped from the working set, so finished items leave the
context window; a periodic summary checkpoint resets the working
context.

An unbounded queue held only in conversation overflows two scarce
resources: the operator loses track of what is pending versus done, and
the model's context window fills up. Externalizing avoids both.

## References

- Decision drivers, considered options, and confirmation: `DETAILS.md`
- Original record: `decisions/20260606-bounded-llm-steering-queue.md`

## Related

`rfd/2012-amend-pr-before-it-enters-the-queue/index.md` is the
work-in-progress discipline this queue relies on.

## Detail

{{< include DETAILS.md >}}
