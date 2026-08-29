---
title: "RFD 2108: Local C ABI zone guests, with fan-out inside the tick"
rfd: "2108"
state: abandoned
scope: zone guest boundary, pubsub fan-out, h2o routing
---

## Problem

`rfd/0107` makes h2o the ingress and the reverse proxy, and it leaves
the guest boundary open. `rfd/0094` has guests arrive as CDN-delivered
riscv64 ELFs under libriscv. That model carries a runtime, a sandbox,
and a delivery path, and simulation code inside the zone needs none of
the three.

`rfd/0097` decided that real-time pubsub runs in userspace, and it
measured why. It did not say how a guest subscribes, or which event
loop owns a subscriber. A fan-out that copies once per subscriber, or
that wakes a thread once per message, does not hold at h2o's rate.

## Decision

A simulation guest is a local shared object, `.so` or `.dylib`, loaded
over the plain C ABI. This is local mode. h2o routes to it, and the
call carries no network hop, because the guest shares the zone process.

The CDN keeps one job, which is bulk asset delivery. It no longer
delivers guest programs for simulation.

Fan-out runs inside the tick:

- One publish ring per zone. One writer, which is the tick. Many
  readers, each with its own cursor and sequence number.
- Serialize once into the 100-byte packet of `rfd/0053`, then fan out a
  pointer and a refcount. Never serialize per subscriber.
- Bind a subscriber to the event loop that owns its connection. Deliver
  across loops with one batched wakeup per tick, not one per message.
- A local guest registers a callback and receives the fan-out as a
  call, with no copy and no syscall.
- Gate a guest once at subscribe time, with the ReBAC actions of
  `rfd/0092`. Do not gate per message.

FoundationDB stays off the fan-out path. The tick owns the `libfdb_c`
callback chain of `rfd/0073`, and it appends the durable log off-tick.
Watches are not used.

## References

- The measurements, the back-pressure rule, and the sandbox trade:
  `DETAILS.md`
- `rfd/2097-pubsub-belongs-in-userspace`, `fdbpub.c`

## Related

- `rfd/2107-janet-scripting-over-a-c-taskweft-core`: the tier this
  fills in.
- `rfd/2049-fabric-channels-as-reliability-classes`: the vocabulary the
  back-pressure rule uses.
- `rfd/2094-minimum-ugc-game-loop-guest-composition`: the UGC loop this
  record does not serve.

## Detail

{{< include DETAILS.md >}}
