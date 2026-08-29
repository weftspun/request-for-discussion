---
title: "RFD 2117: Retire the h2o tier record set under YAGNI"
rfd: "2117"
state: published
scope: RFD lifecycle, records for the retired native tier
---

## Problem

`rfd/0116` replaces the native zone server with an Elixir epoll server, and returns the state to CockroachDB. That decision leaves 43 records that describe things the project does not build: a libh2o event loop, a FoundationDB C path, a libriscv guest runtime, and repositories that are already archived.

Every one of those records renders as live on the site. A reader cannot tell them from the records that still hold. Marking a record's state does not help a reader who arrives through search.

## Decision

Move all 43 records to `multiplayer-fabric-archive`, per `rfd/0106`. Keep no pointer stub, per `rfd/2000-conventions`.

`rfd/0071` supplies the rule. Structure arrives when a real near-term need arrives. A record whose subject the project does not build is structure ahead of need. Retiring it costs nothing, because the archive keeps it and the number stays reserved.

The same rule settles the 18 records whose case cut both ways. Four have a live consumer today and stay. Fourteen do not, and go. A record comes back when a need arrives for it, rewritten against the tier that exists then, rather than restored on the guess that it still fits.

Citations change in one way. A citation that names a full path, as `rfd/NNNN-slug`, becomes a link into the archive, because it names a location. A citation that names a bare number stays as it is, because it names a record.

## References

- The full list of 43, the four that stay, and the counts: `DETAILS.md`
- `rfd/2116-elixir-epoll-zone-server-in-the-h2o-style`: the decision
  that retires them.

## Detail

{{< include DETAILS.md >}}
