# RFD 1138: Where a range of motion comes from

**State:** prediscussion
**Feature:** the source of joint limits
**Scope:** `2-contract/swing-twist-kusudama`, `3-interactor/physics`

## Problem

A fit of 17 detected points to 104 unconstrained rotations folds bones
through each other and reports 0.022% of stature. Nothing in the loop
sees it, because the residual measures reprojection and so does the
referee. A joint bound would, and a bound needs a range of motion.

The only such data here is `addbio_*_rom` in the kusudama project.
CLAUDE.md blocklists AddBiomechanics `.b3d` as an IDENTITY source, for
a narrow and inequitable population. Bounding a joint angle is a
different use, and whether the objection follows the data into it has
never been decided. This asks rather than answers: no prior decision
was found, and inventing a citation would be worse than an open RFD.

## Decision

Open. Three candidate sources and what each costs.

**Constructed, from our own assets.** Sweep ANNY's pose library or a
licence-clean motion set through the rig and measure the envelope. True
by construction, reproducible, and narrower than a body: it measures
what the rig was authored to do.
**AddBiomechanics ROM.** Real bodies, already in the kusudama datasets.
The blocklist row is about identity and this is a joint angle, a
distinction to decide rather than assume.

**Our own photographs.** Circular: recovering 3D angles from single
uncalibrated views needs the limits the range would define. The blinded
holdout cannot source it and the cosplay library is validation only.

## Related

RFD 1134 records the fit behind this. RFD 1137 refuses a fitted pose as
a corpus subject until a bound exists.
