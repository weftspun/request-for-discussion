---
title: "RFD 2026: Commit messages use sentence case without Conventional Commits prefixes"
rfd: "2026"
state: published
scope: git commit message style
---

## Problem

Repositories here run no tooling that reads a Conventional Commits
type prefix. A `feat:`, `fix:`, or `chore:` prefix buys nothing
without that tooling, and it pushes the actual meaning after a colon.
Picking the right type prefix for each commit also needs per-commit
judgement.

## Decision

A commit subject opens with a capital letter and reads as a plain
sentence, such as "Add the macOS and Windows release workflows". It
carries no `feat:`, `fix:`, `chore:`, or `type(scope):` prefix, and no
trailing period. The body, where present, states what the change
makes true of the system and why. The repos here run no tooling that
consumes a Conventional Commits type, so a machine-readable prefix
buys nothing and pushes the meaning after a colon; sentence-case prose
keeps the meaning at the front and needs no per-commit judgement about
which type applies.

## References

- Full context, decision drivers, considered options, consequences,
  and confirmation steps: `DETAILS.md`
- Original record:
  `decisions/20260609-commit-messages-sentence-case.md`

## Related

- `rfd/2025-tenseless-continuous-present-voice`: a commit body states
  what the change makes true of the system, the same way comments and
  docs do.

## Detail

{{< include DETAILS.md >}}
