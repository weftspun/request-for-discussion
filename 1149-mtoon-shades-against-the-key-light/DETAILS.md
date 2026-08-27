# RFD 1149 details: the measurements behind the material and the renderer

## Held against three-vrm, pixel for pixel

A unit sphere under an orthographic camera framed exactly to it, so pixel (u, v) carries
normal (u, v, sqrt(1 - u^2 - v^2)). No plateau finding and no fitting: our model is evaluated
at precisely the normal the render used. three 0.185.1, three-vrm 3.5.5, headless Chromium
through swiftshader, colour management off and the output colour space linear.

After dividing ours by pi:

| shadingToonyFactor | px compared | over 4/255 | p99 | max |
| ------------------ | ----------- | ---------- | ------ | ------ |
| 0.9 | 3048 | 0 | 0.0020 | 0.0025 |
| 0.5 | 3048 | 0 | 0.0020 | 0.0021 |
| 0.0 | 3048 | 0 | 0.0020 | 0.0021 |
| 1.0 | 3048 | 2 | 0.0018 | 0.1351 |

One 8-bit readback step is 0.0039, so three of the four agree below the noise floor of the
measurement. The two pixels at a hard ramp are the terminator rather than the model: the
sphere's tessellated normal disagrees with the analytic one by a hair and the step turns that
into the whole base-to-shade gap, which over pi is 0.1337 against the 0.1351 measured.

## The factor of pi, and which side is the outlier

Unscaled, theirs over ours is a near-constant 0.3167 to 0.3183 against 1/pi = 0.31831, flat
across every toony value, which is a uniform scale rather than a difference in shape.

Two independent implementations apply it by two different mechanisms. V-Sekai's Godot port
writes `vec3 lighting = lightColor / 3.14159;` into `mtoon_common.gdshaderinc:156` by hand,
and three-vrm inherits `RECIPROCAL_PI * diffuseColor` from three.js. The VRM 1.0 pseudocode
ends `color = color * lightColor` with no such term, so it is the spec text that omits what
every renderer does rather than a convention either engine invented.

A tone ladder feels this. CIELAB scales non-linearly, so one material at two exposures gives
two dE readings, and the targets have yet to be checked at the exposure a viewer uses.

## VRM0 and VRM1.0 are different parameterisations

The Godot port implements MToon 3.3, whose ramp is

    clamp((I - shadeShift) / (mix(1, shadeShift, shadeToony) - shadeShift), 0, 1)

and VRM 1.0 uses `linearstep(-1 + shadingToonyFactor, 1 - shadingToonyFactor, ...)`. `mtoon.py`
targeted the VRM0 form for one commit and now implements VRM1.0. A difference worth naming
because it silently inverts a term: VRM0 lerps the rim toward BLACK as `rimLightingMix` falls
and VRM1.0 lerps toward WHITE, so `rimLightingMixFactor` 0 leaves the rim at full strength.

## What a deferred G-buffer cost

| approach | ns/px | 4K frame | shadows |
| --- | ---: | ---: | :---: |
| Python forward, scalar_rgb | 102,000 | 848 s | yes |
| deferred G-buffer plus a Slang kernel | 62.2 | 0.516 s | **no** |
| wide forward, Dr.Jit, llvm_ad_rgb | 40.6 | 0.337 s | yes |

The deferred path silently dropped the shadow ray, which is the whole reason the test shape is
an abacus rather than a sphere: a convex shape cannot occlude itself. So it was slower AND lost
the thing the shape was chosen for.

## What the Slang kernel bought

`mtoon.slang` compiles to C++ and agrees with `mtoon.py` to 7e-08 against a float32 epsilon of
1.19e-07, which chains the validation to three-vrm through two differentials.

The forward integrator shades faster, so the kernel packs frames instead. The win there came
from the wrapper: Slang's CPU target emits scalar code and one call runs every thread group
serially:

    original pow, numpy float64   0.520 s per 4K frame
    numpy lookup table            0.231
    Slang, one thread             0.221
    Slang, group range threaded   0.062

Against a lookup table the kernel alone bought 4 per cent. Splitting the group range across
cores bought 3.8x, which belongs to the wrapper rather than to Slang.

## Left unmeasured

Whether the tone targets hold at the exposure a viewer uses, given the factor of pi.
`giEqualizationFactor`, which the model does not carry and the comparison set to zero.
Shadowing against three-vrm, where shadow maps and ray-traced occlusion legitimately differ,
so a per-pixel comparison measures the difference between two renderers.
