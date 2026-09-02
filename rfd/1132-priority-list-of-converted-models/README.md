# RFD 1132: Priority list of converted models

**State:** abandoned
**Feature:** model conversion order

## Problem

RFD 1016 inventories fifteen deep learning models. Nothing says
which to convert for the accelerator first, so the order is decided
by whoever picks one up.

Ten ids are excluded rather than ranked, and RFD 1133 says what
excludes each: three by the agreements, four by an abandoned scope,
three by nothing found. One model has been measured. An order built
from guesses reads the same as one built from evidence.

## Decision

Rank by evidence, and say which rank rests on what.

RF-DETR keypoint is first because it is the only model with a
measured export: 825 nodes over 22 operators, every one inside the
allowlist. It is also the only one with a measured obstacle, which
is worth more than an untested candidate.

Excluded models are not ranked here. RFD 1133 carries them, one
group per kind of exclusion, because a blocklist row and an
abandoned scope reopen on different events. Everything else is
unranked pending a census, and the gate that produces one exists.

`DETAILS.md` gives the table, the measurement behind the first
entry, and what each remaining model needs before it can be ordered.

## Related

RFD 1016 inventories the models. RFD 1133 carries the excluded ones.
RFD 1036 packages each as an image. RFD 1026 sizes them. RFD 1122
covers the keypoint chain.
