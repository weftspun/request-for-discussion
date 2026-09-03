# RFD 2022: Spatial audio patched resonance audio

**State:** abandoned

## Decision

See `DETAILS.md` for the full argument.

## Problem

The zone server renders shared social-VR scenes where sound sources
need to be localized in 3D for every listener. Two things drive
presence: binaural HRTF rendering so a source is heard at the correct
azimuth and elevation over headphones, and audio probes that capture
how a room colors and occludes sound so a source baked behind a wall
does not leak through it. Godot's built-in `AudioServer` does stereo
panning and attenuation, but it has no HRTF path and no probe-based
spatialization. How should the engine produce HRTF spatial audio with
environmental probes?

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
