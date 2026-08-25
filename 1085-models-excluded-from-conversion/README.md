# RFD 1085: Models excluded from conversion

**State:** discussion
**Feature:** model conversion order

## Problem

RFD 1084 ranks the models to convert for the accelerator, and it
carried a second table beside the ranking: ten model ids marked
blocklisted. One word covered three exclusions, and the word is
wrong for seven of the ten.

Three are blocklisted. CLAUDE.md excludes Qwen-Image-Edit, P3-SAM
and Krea 2, for quantisation damage and for licence terms. Four are
abandoned: RFD 1040 turned the roadmap toward character concepts,
and RFD 1031, RFD 1032, RFD 1033 and RFD 1034 record the pivot. The
last three name nothing this workspace holds.

A reader who asks why a model is unranked gets one answer where
there are three, and two of the three can reverse.

## Decision

Separate the exclusion from the ranking, and name which kind each
row is.

Every excluded model carries the blocklist entry, the RFD, or the
absence that excludes it. The kind decides what reopens the row. A
blocklist row reopens when the agreements change. An abandoned RFD
reopens when the roadmap returns to its scope. An unfound id reopens
when somebody finds what it names, or deletes it.

`DETAILS.md` gives the three groups, the reason under each row, and
what the seven mislabelled rows were checked against.

## Related

RFD 1084 ranks the convertible models and cites this one. RFD 1010
inventories them. RFD 1029, RFD 102a and RFD 102b package the three
blocklisted models.
