## Consequences

- The wire has no floating point; replication is deterministic across
  platforms.
- The packet speaks the predictive BVH's native int64-micrometer
  language, so position flows into the BVH with no conversion.
- Tying velocity to `PBVH_V_MAX_PHYSICAL_DEFAULT` closes a latent
  drift (the codec had an ad-hoc times-1000 scale that the BVH-sync
  review surfaced).
- Density, when it matters, comes from value delta-from-baseline
  rather than origin rebasing; entropy coding stays off the per-tick
  path because variable length breaks the fixed datagram layout.

## Confirmation

The `entity_packet` Plausible suite passes a 50000-vector roundtrip
and size sweep, and the engine's C++ decode matches the Lean golden
bytes on 64 vectors. The change lands on `feat/module-xr-grid` and
`feat/module-multiplayer-fabric`.

## Related repositories

- Spec model: `https://github.com/v-sekai-multiplayer-fabric/entity_packet`
- BVH consumer:
  `https://github.com/v-sekai-multiplayer-fabric/lean-predictive-bvh`
