---
title: "RFD 2115: A planner domain document is a cheap-layer surface"
rfd: "2115"
state: discussion
scope: planner domain encoding, CBOR-LD, taskweft, QCBOR
---

## Problem

RFD 2003 settled the cheap layer: CBOR-LD, `QCBOR` over `zcbor`, RFC 8949
section 4.2 determinism, and an offline `jsonld-cpp` authoring role against
a pure-C decode role. It scoped that to one artifact, the manifest inside a
sandboxed `libriscv` package.

A planner domain document is a different artifact. `taskweft/nif` reads one
as its input, `fabric-store-domain` carries one for the ward, and
`fabric-behaviour-domain` wants one when its planner decides what a body
does. Three repos, one artifact, and no recorded encoding, so each answers
alone. One already has: `DETAILS.md` records the encoder it reached for.

## Decision

**A planner domain document is a cheap-layer surface.** RFD 2003's
decisions apply to it unchanged. This RFD adds no terms of its own and
exists to widen that scope.

**The store plane holds it, and an edge serves it.** It is a row in SQLite
over the FoundationDB VFS, in the same database as the world it describes,
so it travels with that world at the speed of a page reference.
`aria-storage` holds packages and assets.

**Determinism holds for a local reason.** RFD 2003 wanted it for `casync`
deduplication, which these documents never reach. A ward replays from a
seed and compares fingerprints, so a document that encoded two ways for one
logical input would break the check that catches every other drift.

**The authoring tool lives wherever it is first needed.** No seam in it for
a second consumer that has not asked yet.

## References

- The encoder that prompted this, and what it got wrong: `DETAILS.md`
- `rfd/2003-castspell-sandbox-package-and-manifest-encoding`: every term
  this RFD reuses, and the reasoning behind each.

## Related

- `rfd/2093-compile-taskweft-to-linear-automata`: the planner this feeds.
- `rfd/2107-janet-scripting-over-a-c-taskweft-core`: the other consumer of
  a taskweft core in pure C.

## Detail

{{< include DETAILS.md >}}
