# RFD 2070: Loop slice telemetry to the observability collector

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

The loop-slice server emits OpenTelemetry through the `OpenTelemetry`
C++ engine module: spans for the loop's phases, counters and gauges
for grants and ticks, and log lines. Export is opt-in. The server
reads `OTEL_EXPORTER_OTLP_ENDPOINT`, and with no endpoint set it stays
idle — it records signals in process but exports nothing, which keeps
a server that has no collector from retrying against one that is not
there. The observability stack
(`rfd/200b-observability-stack-victoriatraces`) runs an OTEL collector

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
