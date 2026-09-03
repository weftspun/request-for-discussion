---
name: rfd-2182-identity-triangle-operator-market-customer
description: When writing about who runs the atelier-workshop, who receives the shuttle, or which market the workspace competes in, use these three anchors. Operator is chibifire.com (K. S. Ernest (iFire) Lee). Partner project is V-Sekai (iFire is a V-Sekai co-founder per the 2020-06-08 charter). Market is avatar-first social VR. Never name third-party social-VR trademarks; use generic vocabulary per CLAUDE.md.
tools: Read, Write, Edit
---

# RFD 2182: Identity triangle for operator, partner project, market

**State:** committed
**Feature:** name the operator, the partner project, and the market
**Scope:** RFD titles, public prose, README taglines, pitch material

## Problem

RFD 2171 fixed pipeline and deliverable vocabulary but left three
L3 gaps: who runs the atelier-workshop, who receives the shuttle,
and which market. An earlier draft named V-Sekai "Customer", which
implies a vendor→client relationship the 2020-06-08 V-Sekai charter
does not support — iFire is a V-Sekai co-founder.

## Decision

- **Operator**: `chibifire.com` (K. S. Ernest (iFire) Lee, github.com/fire). Owns the atelier-workshop; ships the shuttle.
- **Partner project**: V-Sekai (charter at `V-Sekai/manuals-vsk/decisions/20200608-vsekai-charter.md`). iFire is a founding team member; the shuttle enters V-Sekai because both projects share the same intent — open, self-hosted, remixable social VR.
- **Market**: avatar-first social VR. Generic vocabulary per CLAUDE.md; no third-party social-VR trademarks in shipping prose.

Canonical positioning:

> chibifire operates an atelier-workshop that shuttles characters
> into V-Sekai, its partner project in the avatar-first social-VR
> market.

## Purposes (Ibuka-shape, under V-Sekai's charter)

1. Make portable characters other people can take away — deliverable is data, not a service.
2. Walk the gacha ladder (RFD 2136) rung by rung; each stage measurable in isolation.
3. Score edits by reconstruction (MaskScore, RFD 1173), not intent.
4. Run on owned local compute only. Nothing rented.
5. License-clean provenance: `.cff` beside every payload.

## Related

RFD 2171 (vocabulary), RFD 1106 (open/proprietary boundary), V-Sekai charter (path above), Ibuka's 1946 Tokyo Tsushin Kogyo prospectus (structural reference).

This RFD was drafted by an AI and read by a human before it shipped.
