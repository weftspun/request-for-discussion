---
title: "RFD 2064: GitHub repos use kebab-case; local checkout dirs keep build-native names"
rfd: "2064"
state: published
scope: repository naming across all orgs
---

## Problem

GitHub repository names carried no fixed case convention. A build
that consumes a sibling repository by path, such as a CMake
`add_subdirectory` or a homebrew `resource`, hardcodes a directory
name in its own case. A repository rename could break that hardcoded
path.

## Decision

GitHub repository names are kebab-case, for example `combat-core`,
`loot-core`, `mount-drift`, and `vr-bridge`. Local checkout directory
names match what the build expects instead. Where a repo is consumed
as a sibling by path — a CMake `add_subdirectory`, a CI `path:`, a
homebrew `resource` — the local directory keeps the snake_case name
the build hardcodes, so local `mount_drift` maps to remote
`sinew-mocap/mount-drift`. Where no build path depends on the
directory name, the local directory may match the kebab-case repo
name instead. Old remote URLs keep working through GitHub's automatic
redirects, so a rename does not break an existing clone or CI
checkout. This gives uniform, discoverable remote names without
touching the build files that hardcode sibling directory paths;
fully propagating kebab-case into those build files stays out of
scope here.

## References

- Full drivers, considered options, consequences, and confirmation:
  `DETAILS.md`
- Original record:
  `decisions/20260621-kebab-case-repos-snake-case-local-checkouts.md`

## Related

- `rfd/2009-ghcr-package-ownership-same-repo`: another repo-naming and
  ownership convention.

## Detail

{{< include DETAILS.md >}}
