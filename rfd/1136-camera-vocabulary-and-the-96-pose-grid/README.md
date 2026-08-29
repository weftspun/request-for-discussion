# RFD 1136: Views are named in the ecosystem's camera vocabulary

**State:** discussion
**Feature:** naming camera directions, and a grid of them as training data
**Scope:** `7-service/service-livebook/priv/python/weft_loop.py`

## Problem

This workspace named views in degrees. "Pitch -90, yaw 0" says nothing
about what a picture shows, and a reader has to hold the up axis and the
rotation order in their head to find out.

The cost was not cosmetic. Loop 1 scored view 0 of its sequence for three
rounds and got 0.0 each time. View 0 is a camera directly beneath a
standing figure. The degrees were on the page the whole time.

## Decision

Name a view in the vocabulary fal's Multiple-Angles LoRA is conditioned
on: 8 azimuths at 45 degree steps, 4 elevations at -30, 0, 30 and 60, and
3 distances at 0.6, 1.0 and 1.8. It then reads the same to a person, a
tagger and a generator.

`camera_prompt` converts parameters to the prompt and `camera_parameters`
converts back, both exactly. A camera the table does not name is a refusal
rather than the nearest phrase, because a snapped name describes a picture
nobody rendered. `describe_camera` is the lossy direction and says so,
naming the band that holds a camera and refusing outside it.
`sample_camera` draws inside a band, and its seed is required.

The 96 cells are enumerated in `test_weft_loop.py`, not sampled, and that
found the front view's band wrapping through zero.

Only the phrase table is used. Qwen-Image-Edit is blocklisted and those
weights are gated, so neither is loaded. `logbook/CITATION.cff` cites it.

## Related

RFD 1134 records the run where the unnamed view cost three rounds. See
`DETAILS.md` for the grid proposed as constructed training data.
