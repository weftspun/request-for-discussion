# RFD 2073: Async fdb callback chain

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

``` create_transaction -> get(district) [async future] ->
on_district_read [callback: extract next_o_id] -> get(customer) [async
future] -> on_customer_read [callback: extract discount] ->
get(stock[0]) [async future] -> on_stock_read [callback: update stock,
next item] -> ... (loop for 5-15 items) -> set(oorder, new_order,
order_line[], stock[]) -> commit [async future] -> on_commit
[callback: send HTTP response] ```

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
