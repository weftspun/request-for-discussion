---
title: "RFD 2020: Pin the engine to a frozen Godot 4.7 commit"
rfd: "2020"
state: published
scope: engine fork base commit
---

## Problem

The engine fork's base commit tracked a moving upstream. A base that
tracks a moving upstream lets patches shift underneath the assembly.
A green build could break the next day from upstream churn alone, with
no change to the fork's own feature branches.

## Decision

The engine fork carries many feature branches that the `merge` recipe
assembles onto a base. A base that tracks a moving upstream lets
patches shift underneath the assembly, so a green build can break the
next day from upstream churn alone. The fork's `master` pins to one
frozen upstream commit instead, currently tip `8a337510` (Godot
`4.7.0-beta`, per `version.py`). Every feature branch in the
`gitassembly` recipe stands alone on that base. The pin moves only by
a deliberate update to `master`, never by following upstream.

## References

- Full context, decision drivers, considered options, consequences,
  and confirmation steps: `DETAILS.md`
- Original record:
  `decisions/20260606-pin-engine-to-frozen-godot-4-7.md`
- `version.py` on the fork; the fork's git history for the mirrored
  upstream commit

## Related

- `rfd/2019-gitassembly-tag-release`: the tag fixes the assembly
  merged onto this pinned base.
- `rfd/2022-spatial-audio-patched-resonance-audio`: targets this fixed
  engine API.

## Detail

{{< include DETAILS.md >}}
