# RFD 1137: A frame set is delivered as one CineForm clip

**State:** discussion
**Feature:** encoding a render sweep for review and delivery
**Scope:** `7-service/service-cineform`, `1-transport/transport-cineform-tui`

## Problem

A 96-pose sweep left 192 files in a directory. Nobody reviews 96 PNGs,
and a directory carries no title, no licence and no statement of what
made it. The deliverables rule asks for a video intermediate with a
`.cff` beside it. The encoder for one was in the workspace and had never
been built, and the first attempt reached for a tool that is LGPL.

## Decision

The pair that exists does the work: `transport-cineform-tui` sends the
job, `interactor-cineform` encodes, and `service-cineform` owns the bus
and the runtime directory, every link Apache-2.0 or MIT.

`SKILL.md` gives the order, from a workspace with nothing built to a
clip on disk, and the order a clip takes when it explains a corpus row.
`domain.ex` and `problem.ex` make that order a taskweft plan whose goal
is `delivered`, which only a verified clip and citation satisfy. Frames
alone leave it false, and the planner names the step that did not run.

Three choices are settled rather than left to taste. The frame rate is
8 per second, so one second is one azimuth sweep and 60 would put all 96
frames inside 1.6 seconds. The pixel format is RGBA_4444, because a
render carries a matte. And both files take their name from the
citation's title, which must name what varies.

Measured here: 96 frames of 1024 by 1024, 402.7 MB of raw RGBA in, 23.4
MiB out, 554 ms in the encoder, about 173 frames per second, which is a
rounding error beside the render.

## Related

RFD 1136 enumerates the poses that make such a sweep. See `DETAILS.md`
for the measurements and what the clip does to a frame hash.
