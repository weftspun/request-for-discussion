---
name: rfd-2182-identity-triangle-operator-market-customer
description: When writing about who runs the atelier-workshop, who consumes the shuttle, or which market the workspace competes in, use these three anchors. Operator is chibifire.com (K. S. Ernest (iFire) Lee). Customer is the V-Sekai social network. Market is avatar-first social VR. The shuttle takes a portable character INTO V-Sekai. Never name third-party social-VR trademarks; use generic vocabulary per CLAUDE.md.
tools: Read, Write, Edit
---

# RFD 2182: Identity triangle for operator, market, customer

**State:** committed
**Feature:** name the operator, the customer, and the market
**Scope:** RFD titles, public prose, README taglines, pitch material

## Problem

RFD 2171 fixed the vocabulary for the pipeline and the deliverable
but left three L3 gaps a reader could not close from the register:
who runs the atelier-workshop, who receives the shuttle, and which
market the workspace competes in.

## Decision

Three anchors, each named once:

- **Operator**: `chibifire.com` (K. S. Ernest (iFire) Lee, github.com/fire). The domain owns the atelier-workshop and ships the shuttle.
- **Customer**: the V-Sekai social network. The shuttle enters V-Sekai; a portable character becomes its owner's presence there.
- **Market**: avatar-first social VR. Generic vocabulary per CLAUDE.md's trademark rule; do not name any specific third-party social-VR platform in shipping prose.

The atelier-workshop-shuttle vocabulary (RFD 2171) plus this
triangle gives one canonical positioning sentence:

> chibifire's atelier-workshop shuttles characters into
> avatar-first social VR.

Customer (V-Sekai) drops out of the one-liner and lives in the
Decision list above; it is one destination inside the named market.

## Related

Companion to urn:oid:1.3.6.1.4.1.66606.1.1.2171 (vocabulary) and
urn:oid:1.3.6.1.4.1.66606.1.1.1106 (open/proprietary boundary,
which stops at the moat structure and leaves customer/market
unstated). CLAUDE.md's "Trademarks Stay Out of Shipping Artifacts"
constrains the market row.

This RFD was drafted by an AI and read by a human before it shipped.
