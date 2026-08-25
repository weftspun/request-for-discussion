# RFD 1107: The world package format, splats plus optional props

**State:** published
**Scope:** `worlds/*/world.manifest.json`, `worldSceneLoader.js`, `iwsdkWorldPackage.js`

## Problem

An explorable Gaussian-splat environment, with optional grabbable
mesh props, needs one manifest shape that both the main app's `/`
session and the `/xr` IWSDK lab can load, and needs a clear
separation from the spatial fabric this project also publishes to
(RFD 1100), since a splat-only world has no mesh props to publish
there at all.

## Decision

One manifest per world, `world.manifest.json`, naming a spawn point,
a Gaussian-splat environment (`type: gaussian_splat`, rendered by
Spark.js), and an optional `props[]` list, each with its own mesh
URL, transform, and interaction type. Three scene layers stay
strictly separate: `playerRoot` (the avatar), `worldRoot` (the
environment splat), `propsRoot` (interactable props); an avatar load
never replaces the world or its props, and a world load never
replaces the avatar. The environment splat is visual only; an
optional `environment.collider_url` supplies the walk mesh a splat
alone cannot.

See `DETAILS.md` for the manifest schema, the XR interaction mapping
on Galaxy XR, the world-generation and environment-scan API calls,
and the Redis-rehydrate recovery step.

## Related

**Unresolved duplicate:** weftspun-3d-studio's own
`thirdparty/m3/docs/WORLD_PACKAGE.md` covers the same topic, with
real content differences. Neither version is authoritative; that
reconciliation is still open. RFD 1100 gives the separate spatial
fabric this world format does not publish to on its own.
