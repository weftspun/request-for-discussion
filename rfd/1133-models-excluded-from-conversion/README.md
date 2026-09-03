# RFD 1133: Models excluded from conversion

**State:** discussion
**Feature:** model conversion order

## Decision

Separate the exclusion from the ranking, and name which kind each
row is.

Every excluded model carries the blocklist entry, the RFD, or the
absence that excludes it. The kind decides what reopens the row. A
blocklist row reopens when the agreements change. An abandoned RFD
reopens when the roadmap returns to its scope. An unexplained mark
reopens the moment somebody reads the checkout it names.

`DETAILS.md` gives the three groups, the reason under each row, and
a retraction: the last three were first published as unfound, and
`default.xml` places all three.

## Problem

RFD 1132 ranks the models to convert for the accelerator, and it
carried a second table beside the ranking: ten model ids marked
blocklisted. One word covered three exclusions, and the word is
wrong for seven of the ten.

Three are blocklisted: CLAUDE.md excludes Qwen-Image-Edit, P3-SAM
and Krea 2. Four are abandoned, and RFD 1064 turned the roadmap
away from their scope. The last three are placed projects on
3-interactor carrying no recorded reason at all.

A reader who asks why a model is unranked gets one answer where
there are three, and two of the three can reverse.

## Related

RFD 1132 ranks the convertible models and cites this one. RFD 1016
inventories them. RFD 1041, RFD 1042 and RFD 1043 package the three
blocklisted models.
