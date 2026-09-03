# RFD 2063: Repo markdown single source of truth for project state

**State:** abandoned

## Decision

See `DETAILS.md` for the full argument.

## Problem

An agent working a project over many sessions accumulates project
knowledge: what is decided, what works, what is still open, which
avenues are dead. That knowledge has to live somewhere a future
session can read it. A file-based agent auto-memory is the convenient
place to put it, but auto-memory is not reviewed in diffs and does not
travel with the code. When the code moves and the memory does not, the
two desync, and a memory that names a file, function, or flag that no
longer exists reads as authoritative while being wrong. Where should

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
