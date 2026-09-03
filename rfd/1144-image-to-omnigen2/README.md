# RFD 1144: The image-to-OmniGen2 loop

**State:** published
**Feature:** loop 2 of the four-loop plan
**Scope:** `fourloops-plan.usda`

## Decision

Run loop 2 first among the four, and let it carry the measurements.

**The hazard is a silent skip.** The edit instruction comes from a text
input rather than from the filename. A filename that matches no key is
skipped without a word, which produces a run that reports success and
edits nothing.

`DETAILS.md` holds what the first runs measured: what OmniGen2 costs at
bf16 and at four bits, what EditScore costs, and what EditScore returns
for an instruction the edit actually matched. `fourloops-plan.usda` and
`fourloops-etnf.usda` both name that file as a source, so a quantity in
either layer is checked against a measurement rather than against a
recollection.

## Problem

Loop 2 is the smallest complete loop: OmniGen2 proposes an edited png,
EditScore scores it, OmniGen2 repairs. One propose stage, one scorer,
one repair arm, size M, and it runs second because the harness is the
only thing it waits on.

Being smallest makes it the one that measures the two components every
other loop also uses, so its numbers are the plan's numbers.

## Related

RFD 1143, RFD 1145 and RFD 1146 are the other three loops. RFD 1128
records four-bit tolerance for another model on the same card.
