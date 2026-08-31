---
rfd: 2136
title: "RFD 2136: The gacha critical path"
state: "discussion"
feature: "the plan of record for the public roll button, as a PERT network"
scope: "the gacha demo; page.html beside this file is the report"
---

Nine activities stand between the current pipeline and a public roll
button. One chain sets the date: skin-mode rigging, taxonomy transfer,
assembly, pool, publish, at 13.2 expected working days with sigma 1.7.
`page.qmd` beside this file carries the network on a time axis, the
O/M/P estimate table, and the slack on every non-critical edge; its
decision rule is that A (skin-mode rig, the only research risk) and H
(hm08 partition) start together at day zero and nothing else starts
until one moves. The spend infrastructure the pool leans on is live
(RFDs 2133 through 2135); a valid vast.ai key and a wired broker token
remain on the operator. The 10 absent attachment tags are wave 2 by
RFD 1121's route, off-chart by design.
