# RFD 1146: The latent-to-Pixal3D loop

**State:** discussion
**Feature:** loop 4 of the four-loop plan
**Scope:** `2-contract/weftspun-manuals/fourloops-plan.usda`

## Problem

Loop 4 is the only one that leaves the image plane. Pixal3D proposes a
latent state, then views, then a glb; EditScore scores; and the repair
arm forks between VoxHammer and OmniGen2. At size XL it is the largest
of the four, and it is the only loop with a router.

The router decides which repair arm runs, and it decides on a statistic
nobody has calibrated.

## Decision

Build it, and treat the router as uncalibrated until measured.

The statistic is spread over mean, and a spread above 0.15 selects the
latent arm. `routerCalibrated` is 0 in the plan, so that threshold is a
starting value rather than a result. A router that picks the wrong arm
produces a repair that cannot help, and the loop still terminates.

**The hazard is an arm that cannot take what the loop holds.**
VoxHammer raises `NotImplementedError` outside stub mode, and it takes
a mesh where the loop carries a latent. So the arm passes through
`/extract` first, and a route that skips that step fails inside the
tool rather than at the boundary.

## Related

RFD 1143, RFD 1144 and RFD 1145 are the other three loops. RFD 1122 is
the goal, and RFD 1132 lists what converts.
