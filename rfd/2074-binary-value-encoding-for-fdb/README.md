# RFD 2074: Binary value encoding for fdb

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

1. Zero-copy deserialization: a packed struct can be cast directly
from FDB's `FDBKeyValue.value` pointer. No parsing step. The callback
handler does `(stock_val_t *)kv->value` and reads fields.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
