---
title: "RFD 2007: Godot double precision template_release for zone servers"
rfd: "2007"
state: published
scope: zone-server
---

## Problem

Zone servers needed a Godot engine build that matches the physics and
networking precision the rest of the stack uses. An editor build
carries import and export tools a zone server does not need, making it
larger and slower to start. Without a fixed build target, the headless
zone server role had no matching binary.

## Decision

Zone servers build the Godot engine as `target=template_release
precision=double`, with no Mono module. The build source is the V-Sekai
fork `V-Sekai-fire/multiplayer-fabric-build@b27142e94`. Double precision
matches the physics and networking precision the rest of the stack uses.
`template_release` carries no import or export tools, so it is smaller
and starts faster than an `editor` build, and it fits the headless role a
zone server runs.

The AlmaLinux 9 build environment must include `libstdc++-static`,
because `template_release` links libstdc++ statically. The resulting
binary is named `godot.linuxbsd.template_release.double.x86_64` and runs
with the `--headless` flag.

## References

- Original record: `decisions/20260501-godot-double-precision-template-release-for-zone.md`

## Related

`rfd/2017-compiling-godot-engine/index.md` covers the engine build
tooling this target uses.
