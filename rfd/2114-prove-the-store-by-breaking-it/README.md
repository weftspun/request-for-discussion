# RFD 2114: Prove the store by breaking it

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

`fdbbackup start -d file:///backup/` does not write the backup to that
path. It makes a container under it, `backup-<timestamp>/`, and writes
there.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
