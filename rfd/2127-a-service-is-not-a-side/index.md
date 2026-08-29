---
title: "RFD 2127: A service is not a side, and sits past the ring at 7"
rfd: "2127"
state: discussion
scope: where a packing of sides is checked out, and what the numbers mean
---

## Problem

RFD 2111 gives this stack six words that name a position in the code, and the workspace is a
hexagon with six numbered sides. It also says plainly that "service" names a deployment set
rather than a position, and it removes `service/` from the checkout along with seven other
directories that named how a thing was built rather than what it does.

That decision left a real thing with nowhere to live. `service-zone` and `service-behaviour`
exist, and each holds no code: a membership, why the membership is what it is, and the manifest
that runs its members together. Neither is in `default.xml`, so neither is ever checked out,
and the RunPod work needed a third one. A container image that packs a transport layer and an
interactor is exactly that thing, and it had been put in the interactor's repository for want
of anywhere better.

## Decision

**A service is checked out at `7-service/`.** Past the ring rather than on it. The ring is 1 to
6 and a service packs sides rather than being one, so it sorts after the sides it packs and a
reader cannot mistake it for a seventh position.

**`0-` is not free for it.** That number is reserved for metadata about the fabric itself,
which is a third kind of thing: not a position in the code, and not a packing of positions.
`0-infrastructure/logbook` holds it.

**`service/` unnumbered is still refused**, for the reason RFD 2111 refused it. An unnumbered
directory is where whatever nobody classified collects, and that is the drift the six words
exist to stop. The number is what stops `7-service/` from becoming that.

**The recomposition rule needs no change.** `Check.Manifest.path_recomposes` drops a leading
digit and joins with the child, so `7-service/see-through` rebuilds `service-see-through`
exactly as `1-transport/runpod` rebuilds `transport-runpod`. This was checked rather than
assumed: the gate passes over 52 projects with the new side in place.

**What a service holds.** The composition and nothing else: which images run together, why the
membership is what it is, the endpoint it runs on, and the release ladder. `service-zone`
already writes it this way — "Nothing here is a copy. Each member is its own repository and its
own image."

## What this does not decide

**`service-zone` and `service-behaviour` are not yet in the manifest.** Both belong at
`7-service/`. Both READMEs still say "edge plane", a compound RFD 2111 retired, so adding them
turns `mix check words` red until they are rewritten. That is a small change and a separate one.

## References

- RFD 2111: the six words, and the eight directories it removed
- RFD 2121: the earlier amendment of RFD 2111 against the tree
