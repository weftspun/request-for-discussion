# RFD 1013: Strangler fig for the studio core

**State:** discussion
**Scope:** `weftspun_studio/`

## Problem

The browser client holds the studio logic: the model catalog, the
job lifecycle, and the pipeline graph. A browser tab owns state that
outlives the tab, and a page refresh drops that state. The client
calls the DGX API with no server between them, and each new task
type adds more client code.

A full rewrite carries risk. The client works today, and a rewrite
would stop the work for a long time.

## Decision

Grow an Elixir application beside the client, an API server the
browser client becomes one consumer of. RFD 1010's model inventory
is the first responsibility it takes. Phase 1 changes no behavior:
the Elixir application holds the inventory as data, reads the
JavaScript catalog, and reports each difference. The JavaScript
catalog stays authoritative, as RFD 1010 states.

See `DETAILS.md` for the end shape, the later phases, the compute
backend, the port shape, the packaging, and known risks.

## Related

RFD 1010 records the inventory that phase 1 mirrors. RFD 1006
records the See-Through stage, and RFD 1003 and RFD 1002 name the
later phases.
