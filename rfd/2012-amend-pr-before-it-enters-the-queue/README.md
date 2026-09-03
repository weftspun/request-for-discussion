# RFD 2012: Amend pr before it enters the queue

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The merge queue captures a PR's head commit the moment its checks pass
and it is enqueued. While drafting the gitassembly tag MADR, a
correction was pushed to the PR branch seconds after enqueueing; the
queue had already snapshotted the earlier commit, so it merged the
draft and orphaned the fix. The correction had to land as a second PR.
How should a late fix to an in-flight PR be sequenced so it is not
lost to the queue?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
