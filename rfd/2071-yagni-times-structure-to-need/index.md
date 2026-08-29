---
title: "RFD 2071: YAGNI times structure to the need, in code and in the record"
rfd: "2071"
state: published
scope: decision records and build scripts
---

## Problem

Building structure ahead of the feature that needs it spends an
option and delays a return. Cheap code generation does not remove
either cost. Some decision records and build scripts in the project
carried structure ahead of a demonstrated need.

## Decision

YAGNI is a timing rule, not a thrift rule. Building structure ahead of
the feature that needs it spends an option and delays a return, and
cheap code generation does not remove either cost. The project builds
structure only when a real near-term need arrives. A decision record
keeps only its load-bearing sections: context, problem, design,
downsides, the road not taken, and confirmation. When a record no
longer describes the live plan, the record is marked superseded and
moved to the archive repository, [multiplayer-fabric-archive](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive).

The project applied this rule three times. It trimmed ceremony from
heavy decision records. It archived a superseded demo. It cut the
`build_msix` script down to the two platforms it serves. Each change
left working behavior unchanged.

## References

- Original record: `decisions/20260629-yagni-times-structure-to-need.md`
- Kent Beck, "The Cost YAGNI Was Never About":
  https://newsletter.kentbeck.com/p/the-cost-yagni-was-never-about
- [`_archive/README.md`](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive/blob/main/_archive/README.md) in
  `multiplayer-fabric-archive`: the archiving convention this rule
  points to

## Related

`rfd/2069-defer-loot-slice-hardening-until-needed`: an applied case of
the same timing rule.
