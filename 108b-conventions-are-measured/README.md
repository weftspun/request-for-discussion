# RFD 108b: Scale, up, forward and handedness are measured

**State:** discussion
**Feature:** checking rig conventions before they are used
**Scope:** `6-datasource/anny-render-corpus/check_conventions.py`

## Problem

Three defects came from assuming a convention, each producing a result
that looked correct. The 2D fit projected components 0 and 1 while the rig is Z-up, so the
solver rotated every body ninety degrees and reported 0.022% of stature.
`stature` measured the body's depth for the same reason, normalising by
0.434 where 1.660 belonged. The camera grid placed cameras at world
azimuth while its phrases claim a subject's front, so 96 frames labelled
"front view" were profiles.

None raised anything. A left-right swap is worse: it reprojects onto the
same pixels, reports the same residual and passes the referee, because
both measure reprojection.

## Decision

`check_conventions.py` measures four properties off the geometry and
refuses on a mismatch. `render_grid.py` runs it before rendering a
frame, and reports which checks could not run rather than passing over
them. `SKILL.md` gives the order and the traps.

Forward is the chest, the normal to the shoulder line. Gaze and feet are
secondary: on the hv_1 fit the chest and gaze agree to 2.8 degrees while
the feet sit 55.3 degrees away, so a stance is not a defect.

Handedness takes three witnesses. The `.R` against `.L` split cannot
catch a mirror alone, since `right` comes from the chest and the chest
mirrors with the body. Signed mesh volume and basis determinants do.

## Related

RFD 1086 records the fits these were written against. RFD 1089 encodes
the render order they guard.
