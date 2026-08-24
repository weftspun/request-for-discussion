# RFD 103e: A Fly.io toplevel, and the 4090 as a worker node

**State:** abandoned
**Scope:** `weftspun_studio/`, `deploy/quadlet/`, the deploy target

## Problem

RFD 103a puts the whole stack on one box, with every port bound to
`127.0.0.1`. That is correct for one operator, and it is not a
product. Nobody but the person sitting at this machine can reach it.

RFD 1037 prices three rented GPU options for later, and picks this
box's own RTX 4090 first. RFD 101b already sized every catalog model
at that same 24 GB tier. Renting the tier this box already has is a
cost with no matching benefit, for one operator.

Two problems, one shape: this box should keep doing GPU work, and
something else needs to be the thing a user reaches.

## Decision

This design is abandoned. The split it proposes is not taken.

It rests on this box having an RTX 4090 that no rented tier improves
on. The box reports an RTX 3090. Nobody checked the premise, and RFD
101b's sizing and RFD 1037's pricing both assumed the same card.

The problem it names does not go away: a stack bound to
`127.0.0.1` reaches one operator, which is not a product. Whatever
replaces this must answer that, and must name the GPU it measured.

`DETAILS.md` stays unedited: the full split, the port it reused, and
what it left undone.

## Related

RFD 1013 makes `weftspun_studio` the API server this RFD relocates.
RFD 1017 gives the ports the worker adapter will implement. RFD 103d
names the same asset transport for a different gap, browser uploads.
RFD 1039 tracks what this RFD left open.
