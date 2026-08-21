# RFD 1046 details: the three RFDs this rule removed

## What each one was

RFD 1018 picked nx-ggml, and RFD 1013 replaced it, yet RFD 1018
stayed in the index as a live decision. RFD 1020 sketched a
clean-room alpha wrap algorithm RFD 101f's fallback already made
unneeded. RFD 1044 picked a training approach for a model that needs
data RFD 1040 has not finished producing.

## What the rule left in place

This session deleted RFD 1018, RFD 1020, and RFD 1044 under this
rule. RFD 101f keeps its existing fallback, with no successor RFD
promised.

Committed work already under way, such as RFD 1040 and RFD 1041, is
not this rule's target.

Each deleted number keeps a row in `ALIASES.md`, because the RFDs
above still cite it. Deleting a directory does not delete a citation,
and RFD 107c's gate reads those rows when it checks that every
citation resolves.
