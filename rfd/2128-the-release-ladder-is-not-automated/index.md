---
title: "RFD 2128: The release ladder is gated and not automated"
rfd: "2128"
state: discussion
scope: how a service is released, and what a machine may not decide
---

## Problem

A service packs several repositories into one deployable thing, so it is where a release is
cut. Nothing said what a version number means here, and a version number that means nothing is
read as though it means something. A tag called `rc` implies somebody ran the thing and looked
at the result; if it was cut because a build went green, it implies something nobody did.

## Decision

**Four rungs, in order: `dev`, `beta`, `rc`, `release`. No rung is skipped.** A tag is
`vX.Y.Z-<rung>.N`, or `vX.Y.Z` for the last rung. A version reaches `rc` only if it has stood on
`beta`, and `beta` only if it has stood on `dev`.

`ladder/ladder.py` decides whether a proposed tag is a legal step, from the tags that already
exist. It refuses a skipped rung, a hole in a rung's numbering, a tag cut twice, a prerelease
numbered from zero, and a rung that is not one of the four. `proof/test_ladder.py` holds fifteen
cases, and each is a step somebody would want to take in a hurry, which is the only time the
rule matters.

**Nothing automates a promotion, and that is the design rather than an omission.** Each rung is
a claim about evidence a machine cannot supply. `beta` says somebody installed it somewhere
real. `rc` says somebody ran the production settings and looked at the layers. `release` says
somebody decided. A workflow promoting on a green build would assert all three on nobody's
authority, and the value of the ladder is exactly that the claims are true.

So CI refuses an illegal tag and never creates a legal one. The gate is on a person's decision,
not a substitute for it.

## What this does not decide

**What evidence each rung requires.** The ladder checks the order of the rungs, not what was
done on them. A service may state its own evidence for `rc`; this states that a machine cannot
be the one to assert it.

## References

- RFD 2127: what a service is
- RFD 2129: the budgets a release is measured against
