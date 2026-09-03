# RFD 1151: Which axes the survey weights

**State:** discussion
**Feature:** allocating corpus and clip time across axes
**Scope:** `6-datasource/anny-render-corpus/render_mtoon_frames.py`,
`placeholder_cards.py`, `CORPUS_DESIGN.md`

## Decision

Persona species is weighted by the survey, because the survey measures
it: humanoid 50, semi-humanoid 38, robot 6, animal 2, plant 2, other 1,
monster 0 per cent.

Skin tone stays uniform, as a decision rather than a default. No
published mapping from residence to Monk exists, and running the survey
through one built for the purpose put Monk 10 at 0.19 per cent, two
frames of 900, which is where the defect is largest.

Every category carries a floor of 1.5 seconds, including one measured
at zero, and axes with no data get a card naming them, so a clip cannot
imply coverage it does not have.

## Problem

A sweep across an axis has to allocate time or samples somehow.
"Uniform" and "by population" make different claims, so choosing by
taste makes a claim without saying so.

The Nem x Mila Social VR Lifestyle Survey, n=1,012, measures avatar
species directly. It does not measure skin tone. It measures residence,
and its sample is 73.3 per cent Japan.

## References

- `DETAILS.md` carries the allocation and the six cards.

## Related

RFD 1150 gives the tone ladder. RFD 1141 sends artifacts.
