# RFD 2026: Commit messages sentence case

**State:** committed

## Decision

See `DETAILS.md` for the full argument.

## Problem

A commit subject is the first line a reader meets in `git log`, a
blame, or a release note. Two conventions compete for how it reads.
Conventional Commits prefixes each subject with a machine-readable
type and optional scope, such as `feat:` or `fix(parser):`, and
lower-cases the summary that follows. Plain prose writes the subject
as an ordinary capitalised sentence. How should a commit subject in
this repo read?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
