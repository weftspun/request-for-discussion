# RFD 1149: MToon shades against the key light

**State:** discussion
**Feature:** the toon material and how it renders
**Scope:** `6-datasource/anny-render-corpus/mtoon.py`,
`mtoon_forward.py`, `mtoon.slang`, `check_mtoon_reference.py`

## Problem

The corpus needs an anime material beside its photographic one, and
MToon is what VRM avatars carry. Bound as a Mitsuba BSDF it rendered
lit-colour-to-black: the shade colour never reached film.

MToon paints shade where `dot(N, L) < 0`, and a physically based
integrator contributes nothing there because the light sits below the
horizon. Its ramp reads THE key light rather than each sampled
direction, which exceeds what a BSDF interface expresses. Rendering
`lit == shade` and `lit != shade` gave matching images, which settled
it by measurement rather than by argument.

## Decision

The model is `VRMC_materials_mtoon-1.0`, rendered by a forward
integrator that shades every hit against the key light with a shadow
ray. In Dr.Jit ops it widens under `llvm_ad_rgb`, so the forward path
is both correct and faster than the deferred one it replaced: 40.6 ns
per pixel against 62.2, with shadows the deferred path had dropped.

The port is held against `@pixiv/three-vrm` pixel for pixel rather
than trusted because it was transcribed from the spec.

## References

- `DETAILS.md` carries the measurements and the factor of pi.
  `SKILL.md` is the procedure for holding a port against a reference.

## Related

RFD 1150 decides the shade colour. RFD 1141 sends artifacts to
Hugging Face.
