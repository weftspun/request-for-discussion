---
name: holding-a-port-against-a-reference
description: Hold a shading model, a converter or a codec port against the implementation it was ported from, pixel for pixel, instead of trusting that it was transcribed correctly. Use when reimplementing something that already has a reference, when a spec and its implementations disagree, or when a port renders something that merely looks right.
---

# Holding a port against a reference

A port transcribed from a specification is a claim. The reference implementation is the thing
people actually see, and where the two differ the reference usually wins, because that is what
a viewer will compare against.

This found a factor of pi in MToon and a V flip in a UV loader. Both looked right until
measured.

## Pick a comparison with no fitting in it

The cheap version renders both and eyeballs them. That measures the renderer, the camera, the
tessellation and the tone mapping all at once, and cannot say which one moved.

Instead make the geometry analytic. A unit sphere under an ORTHOGRAPHIC camera framed exactly
to it gives pixel (u, v) the normal (u, v, sqrt(1 - u^2 - v^2)), so the model can be evaluated
at precisely the normal the render used. No plateau finding, no fitting, no shared camera
convention to get wrong.

Then switch off everything except the term under test: global illumination, ambient, tone
mapping, colour management, with the output colour space linear. What remains is the term the
port claims to implement.

## Know the noise floor before reading the result

An 8-bit readback quantises at 1/255 = 0.0039, so a residual under that sits inside the
instrument. A float32 buffer quantises at 1.19e-07. State which applies before comparing, or a
match gets reported that the instrument could not have distinguished.

## A constant ratio is a convention, not a bug

If the residual is a uniform scale across every parameter value, the shapes agree and
something applies a factor. Look for it in BOTH implementations before deciding which is
wrong: MToon's spec omits a 1/pi that the Godot port writes by hand and three.js inherits from
its BRDF, so the spec text was the outlier.

## Two controls the comparison needs

**The unscaled comparison must FAIL.** If the gate only asserts that the corrected form
matches, it cannot tell a real correction from a coincidence, and a later change that removed
the need for the correction would pass.

**The reference must be shown to have rendered something.** A comparison against an empty
frame agrees with everything.

## When it cannot be exact, say so rather than loosening

Shadow maps against ray-traced occlusion, or two engines' global illumination, differ for
reasons the port has no part in, so a per-pixel comparison measures the renderers instead.
Measure something coarser -- a coverage fraction, a plateau colour -- and record which axis
stays unmeasured rather than widening the tolerance until it passes.

## Chain it rather than restarting it

A second port of the same model is held against the first, which is held against the
reference. `mtoon.slang` agrees with `mtoon.py` to 7e-08, and `mtoon.py` agrees with three-vrm
below the readback floor, so the compiled kernel reaches the reference through two
differentials instead of being trusted because it came off the same page.
