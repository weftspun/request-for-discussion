---
name: rfd-2172-tenseless-continuous-present-voice
description: When writing prose (code comment, RFD, changelog, README, PR description) in this workspace, state what is currently true of the system. Rule out past-tense edit narration, future or imperative planning, and aging temporal qualifiers.
tools: Read, Write, Edit
---

# RFD 2172: Prose speaks in the tenseless continuous present

**State:** committed
**Feature:** prose voice for code comments, RFDs, and changelog entries
**Scope:** every `.md`, `.qmd`, and code-comment file in the workspace

## Decision

Prose in this workspace states what is currently true of the system; every sentence describes behaviour a reader can check against the code in front of them.

## Problem

Comments and prose drift out of sync with code as the system changes. A comment written as history ("added a cache", "we removed the old path") or as a plan ("will solve this", "TODO: wire X") describes a moment that has passed or has not yet arrived; a reader cannot check it against the code in front of them. RFD 2025 (sinew voice ADR, migrated) settled the rule; this RFD promotes it to a workspace convention.

## Three habits ruled out

- Past-tense edit narration ("removed the legacy path"). Git holds history.
- Future or imperative planning ("will add", "TODO"). RFDs and issues hold plans.
- Aging temporal qualifiers ("now", "currently", "previously"). A qualifier that goes stale on the next edit signals the sentence should have described a truth.

Unfinished areas read as present gaps ("the parser handles no Unicode escapes yet"), not as tasks. A stale sentence signals a real divergence from the code, which makes review catch it.

## Related

Promotes: RFD 2025 (sinew voice ADR).
Companion to RFD 1125 (two prose gates) and CLAUDE.md's trope-density check.

This RFD was drafted by an AI and read by a human before it shipped.
