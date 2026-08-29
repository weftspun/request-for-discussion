---
title: "RFD 2063: Project state lives in repo markdown, not in agent auto-memory"
rfd: "2063"
state: published
scope: project-state record keeping across agent sessions
---

## Problem

Project state lived in an agent's private auto-memory. A fact in
private auto-memory desyncs silently, because no diff reviews it and
it does not travel with the code. The project had no single,
versioned home for decisions, open work, and dead ends.

## Decision

Project state lives in three versioned repo-root markdown files, not
in an agent's private auto-memory. `CHANGELOG.md` holds decisions and
completed, verified work. `OPEN_GAPS.md` holds unfinished work and
open problems. `TOMBSTONES.md` holds dead ends and disproven
hypotheses. Each fact has exactly one home, and it moves between files
as its status changes. Auto-memory stays thin: it holds only durable
behavioural rules plus one pointer telling a future session to read
the three docs first. A fact in repo markdown travels with the code
it describes, shows up in review, and goes stale visibly the moment
the code changes; a fact in private auto-memory desyncs silently,
because it is not reviewed in diffs and does not travel with the
code.

## References

- Full drivers, considered options, consequences, and confirmation:
  `DETAILS.md`
- Original record:
  `decisions/20260616-repo-markdown-single-source-of-truth-for-project-state.md`

## Related

- `rfd/2025-tenseless-continuous-present-voice`: the voice
  `OPEN_GAPS.md` and `TOMBSTONES.md` state current truth in, while
  `CHANGELOG.md` reads like commit messages.

## Detail

{{< include DETAILS.md >}}
