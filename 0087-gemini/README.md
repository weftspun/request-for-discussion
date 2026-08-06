# RFD 0087: MindLink, a write-as-you-go memory protocol for an AI session

**State:** committed
**Scope:** `.brain/MEMORY.md`, `.brain/SESSION.md`, `.brain/LOG.md`, `.brain/SHARED.md`

## Problem

An AI coding session that starts with no memory of a prior session
repeats questions the user already answered, and a session that
only writes memory at the end loses everything if it ends without
warning. This project adopted MindLink for persistent memory, and
its protocol needed a written contract, not tribal knowledge in an
assistant's own instructions file.

## Decision

Read before doing anything else, and write as the session goes, not
in one batch at the end. At session start: read `.brain/MEMORY.md`'s
Core and User Profile sections first, fill Core if empty, then read
`.brain/LOG.md`'s last five entries (any `⭐`-prefixed entry always,
regardless of position), `.brain/SESSION.md` for the current task,
and `.brain/SHARED.md` for what other sessions have written. After a
context compaction, immediately re-read `.brain/MEMORY.md` and
`.brain/SESSION.md`; work must not continue before that. Default to
writing: a real preference, decision, gotcha, or scope change goes
into `.brain/MEMORY.md` immediately, not "I'll remember that."
`.brain/SESSION.md` updates at the end of every response.

See `DETAILS.md` for the full file map, the trigger categories that
require a write, and the end-of-session checklist.

## Related

None; this RFD is standalone AI-assistant tooling configuration, not
a design decision about the application itself.
