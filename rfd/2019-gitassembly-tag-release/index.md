---
title: "RFD 2019: Cut gitassembly tag releases for the assembled engine"
rfd: "2019"
state: published
scope: merge repo / assembled-engine release tagging
---

## Problem

The `merge` repo's `gitassembly` recipe assembles the engine by
merging feature branches onto a base branch. Branch tips move, so a
branch name alone does not point at one fixed tree. A consumer pinning to a branch name could point at a tree that
later changed under it.

## Decision

The `merge` repo's `gitassembly` recipe assembles the engine by merging
feature branches onto the frozen Godot 4.7 base. Branch tips move, so
a name alone does not point at one fixed tree. The project cuts an
immutable, timestamped tag for each assembly instead. `elixir
update_godot_v_sekai.exs` runs the assembler and pushes only the tag,
in CalVer form `v<YYYY.MM.DD.HHMM>-multiplayer-fabric`, to
`v-sekai-multiplayer-fabric/godot`. The moving branch stays local, so
a new tag never overwrites an older assembly. Consumers, including
`godot-images` and the cold-boot steps, pin to a tag, not to a branch
name.

## References

- Full context, decision drivers, considered options, consequences,
  and confirmation steps: `DETAILS.md`
- Original record: `decisions/20260606-gitassembly-tag-release.md`
- `merge` repo `CONTRIBUTING.md`

## Related

- `rfd/2020-pin-engine-to-frozen-godot-4-7`: the tag fixes the
  assembly merged onto that pinned base.

## Detail

{{< include DETAILS.md >}}
