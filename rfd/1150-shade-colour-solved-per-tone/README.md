# RFD 1150: Shade colour is solved per tone, not multiplied

**State:** discussion
**Feature:** skin tone equity in a toon material
**Scope:** `6-datasource/anny-render-corpus/anime_materials.usda`,
`check_anime_materials.py`, `anime-materials.cff`

## Decision

The multiplier is solved per tone to hold the separation at dE 12.
`anime_materials.usda` stores the tone identities and the target and
nothing else, because the multiplier, the shade colour and the achieved
separation all follow from those.

The dark end is bounded and reported rather than clamped: dE 12 at Monk
10 needs shade L\* 2.9, and the gate prints what each tone reached.

Applying a scale defined on photographs of real skin to a toon material
is a substitution, recorded as one. No anime skin-tone standard exists.

## Problem

MToon extends glTF `pbrMetallicRoughness` rather than replacing it, so
the lit colour is `baseColorFactor` and the extension adds a shade
colour nothing in PBR constrains. Somebody has to choose it.

The obvious choice, one multiplier for every tone, fails on equity.
At `x0.6` the lit-to-shade separation is dE 17.28 at Monk 1
and dE 4.83 at Monk 10, a factor of 3.6. The terminator is the shading
cue a detector reads, so one multiplier builds a detection gap into the
corpus that would later present as a model defect.

## References

- `DETAILS.md` carries the ladder and the solved multipliers.

## Related

RFD 1149 gives the material. RFD 1151 decides which axes are weighted.
