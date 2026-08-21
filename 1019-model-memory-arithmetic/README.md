# RFD 1019: Model memory arithmetic

**State:** published
**Feature:** capacity planning

## Problem

RFD 1010 says what each model is. It does not say what each model
costs. A reader cannot size a machine from the inventory alone.

## Decision

Compute the memory from the parameter count. RFD 101a records the
result per model.

## The rule

bf16 holds one parameter in 2 bytes. The weight bytes are therefore
the parameter count multiplied by 2.

```
weight bytes = parameters x 2
weight GB    = parameters in billions x 2
```

This document counts 1 GB as 1,000,000,000 bytes. The GiB figure is
smaller by 7 percent.

See `DETAILS.md` for the three costs that come after the weights,
and the safe rule for one resident model.

## Related

RFD 1010 lists the models. RFD 101a applies this rule to each one.
RFD 1022 checks the rule against a measured model.
