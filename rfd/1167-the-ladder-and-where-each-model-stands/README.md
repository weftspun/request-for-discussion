# RFD 1167: The ladder, and which rung each model is on

**State:** ideation
**Feature:** where the accelerator work actually stands
**Scope:** `2-contract/manuals-weftspun`

## Problem

RFD 1166 ranks what is worth doing and not what has been done. The two
are read as one: a model near the top looks advanced when it may never
have been exported, and one near the bottom may be further along than
anything above it.

A rank is a judgment and a rung is a fact. One table for both lets an
opinion about value borrow the authority of a measurement.

## Decision

Six rungs, each a thing that either happened or did not:

    0  assessed    blocklist clear, checkout present
    1  exports     reaches ONNX at a fixed shape
    2  operators   the operator set is known and compared
    3  translates  the Dataflow Compiler accepts the graph
    4  quantises   optimize completes and writes a HAR
    5  runs        a HEF executes on the device

A model sits on the highest rung it has reached, and the rung below a
failure is where it sits: reaching 2 and failing 3 is rung 2.

`DETAILS.md` carries one table per rung. Most of the field is on rung
0, which is the finding rather than an embarrassment: eleven of twelve
candidates have never been exported, so the ranking beside them was
built from reading rather than running. RFD 1129's skill gives the
procedure for climbing and its order is this order.

## Related

RFD 1166 ranks the same models. RFD 1129 asks whether operators
compile. RFD 1130 measures the device.
