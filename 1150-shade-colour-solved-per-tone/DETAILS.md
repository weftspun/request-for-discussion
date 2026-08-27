# RFD 1150 details: the ladder, and why a multiplier fails to make one

## The flat multiplier, measured

| Monk | lit L\* | shade L\* at x0.6 | dE | solved multiplier for dE 12 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 94.2 | 77.0 | 17.28 | x0.7080 |
| 3 | 93.1 | 76.0 | 17.22 | x0.7072 |
| 5 | 77.9 | 63.2 | 15.15 | x0.6722 |
| 7 | 42.5 | 33.3 | 9.89 | x0.5316 |
| 9 | 21.1 | 15.3 | 5.89 | x0.3166 |
| 10 | 14.6 | 9.8 | 4.83 | x0.1770 |

One multiplier spans dE 4.83 to 17.28, a factor of 3.6. Equal RATIO gives unequal CONTRAST,
because CIELAB scales non-linearly in reflectance.

## Nothing derivable is stored

`anime_materials.usda` carries the ten tone identities and `targetDeltaE` and nothing else.
The multiplier, the shade colour and the achieved separation are all functions of those, so
`check_anime_materials.py` re-derives them and the layer cannot drift from the solver.

Five controls. Three reject: a scale missing tones, an unreachable target silently clamped,
and a LIGHT-ONLY scale, which is rejected as certifying nothing. A flat multiplier looks fine
when the dark end is absent, and that is how a corpus certifies an equity it never tested.

## The dark end is bounded

Holding dE at 12 needs shade L\* 2.9 at Monk 10, which is near black. The gate prints what
each tone achieved rather than clamping, so a tone that cannot reach the target is visible.

## The substitution, recorded

The Monk scale is defined on photographs of real skin; anime skin is an artistic choice.
Applying one to the other gives coverage of a perceptual range and claims nothing about a
population.

No anime skin-tone standard exists to use instead. Danbooru's tag group carries pale, fair,
light, tan, dark, very dark and black skin with no colour values, defined against "the usual
Eurasian skin tone", and its own forum records canonically dark-skinned characters being
redrawn as tans. Its `alternate_skin_color` tag also confirms that characters with non-human
skin have no Monk code and need a cell of their own.

CIELAB at D65 is authoritative upstream and the sRGB hex this layer carries is the published
conversion from it. That is a known substitution to replace with the CIELAB triple.

## Left unmeasured

The rendered dE at the exposure a viewer uses, which RFD 1149 records is pi times ours.
Subsurface: a 2048 square `sss.png` ships with the basemesh and nothing binds it, so an
albedo-only sweep understates how dark and light skin differ at a terminator.
