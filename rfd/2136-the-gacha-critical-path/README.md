# RFD 2136: The gacha critical path

**State:** discussion
**Feature:** the plan of record for the public roll button, as a PERT network
**Scope:** the gacha demo; `page.html` beside this file is the report

## Problem

Nine activities stand between the current pipeline and a public roll
button, and without a network the next task is whichever one is
loudest. A pull is not a gacha item until its parts carry the
See-Through taxonomy (VALID_BODY_PARTS_V3, 23 tags; RFD 1121 audited
the canonical body against it), so the taxonomy work sits on the
schedule's spine, not its margin.

## Decision

One chain sets the date: **skin-mode rigging, taxonomy transfer,
assembly, pool, publish** — 13.2 expected working days, sigma 1.7.
`page.html` carries the network on a time axis, the estimate table
(t_e = (O + 4M + P)/6), and the slack on every non-critical edge.
The decision rule it encodes: A (skin-mode rig, the only research
risk) and H (hm08 partition) start together at day zero; nothing else
starts until one of them moves.

The spend infrastructure the pool leans on is laid and live: the
spot-broker as sole holder of the vast.ai key (RFD 2133), the
mutual-TLS FoundationDB cluster with its continuous Tigris backup
(RFD 2134), and the machine checks that watch both (RFD 2135). Two
items stay blocked on the operator: a valid vast.ai key in the
broker's secret, and the broker token wired into a caller.

## Verification

The finished foundation the network builds on is enumerated in the
report's green rail — image-to-mesh through the baked USD-to-Godot
path — and every activity row carries its O/M/P spread rather than a
single guess. The 10 absent attachment tags are wave 2 by RFD 1121's
own route, off-chart by design.
