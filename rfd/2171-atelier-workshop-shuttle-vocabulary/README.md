---
name: rfd-2171-atelier-workshop-shuttle-vocabulary
description: When naming what the workspace makes (the pipeline) and what leaves it (the deliverable), use "atelier-workshop" and "shuttle". Never "atelier" alone. Never rename the shuttle after nx-shuttle's separate use of the same word.
tools: Read, Write, Edit
---

# RFD 2171: The atelier-workshop / shuttle vocabulary

**State:** committed
**Feature:** naming the pipeline and the deliverable
**Scope:** public-facing prose, RFD titles, changelog entries

## Problem

The public tagline names two things: the pipeline that makes
characters and the deliverable that leaves it. "Workshop" alone was
doing both jobs and reads as generic. `nx-shuttle` already uses
"shuttle" (carrying a graph across to another runtime, weft-across-
warp). Without a settled vocabulary, prose drifts between studio,
pipeline, workshop, atelier.

## Decision

Two words, one each:

- **atelier-workshop** names the pipeline. The compound keeps the
  elegance of the French loanword for readers who know it, and the
  plain-English gloss for those who don't. Used in RFD titles,
  changelogs, and public prose whenever the process is meant. RFD
  2136's 10-rung gacha ladder is the concrete atelier-workshop.
- **shuttle** names what leaves it -- a portable VRM (rung 6 of RFD
  2136). Retained without change; `nx-shuttle` already uses it for
  the same weft-across-warp metaphor. The two uses do not conflict:
  one shuttles a character out, the other shuttles a graph across.

Never use "atelier" alone in shipping prose (loanword, pretentious
without the gloss). "Workshop" alone is permitted where context
already fixes it (the 2021 `character-workshop` decision doc stays).

## Related

Spine: chibifire.com public tagline; RFD 2136 (gacha critical path).
Applies to: this file and every subsequent public README.

This RFD was drafted by an AI and read by a human before it shipped.
