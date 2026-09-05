# RFD 2205: Taskweft in Bao — database plugin, cgo-linked

**State:** discussion
**Feature:** the RECTGTN planner lives inside weftspun-bao as a
database-plugin-type Bao plugin (Go binary, cgo-linked C++ from
`taskweft_nif/standalone/`); the same C++ compiles via emcc to a
`taskweft.wasm` blob callable from the browser
**Scope:** the plugin binary itself; the weftspun-bao deploy that
loads it; the git-tracked fleet.jsonld → fleet.sqlite mirror pipeline;
the browser-side WASM parity target

## Decision

Ship one C++ planner (`taskweft_nif/standalone/*.hpp`, unchanged),
one thin `extern "C"` shim mirroring its 23-function NIF surface,
and two hosts that call the shim:

1. **Bao plugin** — Go binary at `7-service/service-taskweft-bao/`,
   registered against weftspun-bao as `bao plugin register database
   taskweft`. Every peer resolves "what is my next task?" as
   `bao read taskweft/creds/<goal_id>`. Bao stamps the response
   `lease_id` on the server clock — every peer sees the same
   `expires_at`, so global time for durations is satisfied by
   construction. `may-use--<device>` ReBAC tuples become ENFORCED
   at read-time via Bao's own capability check (fills the compute-
   lease broker gap RFD 2202 named as future work).
2. **CDN + WASM** — emcc-built `taskweft.wasm` loaded from GitHub
   Pages, reading a static `fleet.sqlite` via HTTP `Range: bytes=0-`
   the same way `service-sqlar-cas/docs/`'s persona demo already
   loads `persona.sqlite`. No server, no toolchain — reviewers see
   the planner's output client-side against the same fixture the
   Bao plugin runs.

The same `.sqlite` fixture ships under `docs/fixtures/` on GitHub
Pages and is the file the Bao plugin reads from
`secret/taskweft/db/fleet` after CI's mirror step. **One file, two
hosts, one planner.**

## Problem

RFD 2204 named the fleet-coordination shape; the plan-mode session
of 2026-09-05 iterated three approaches before landing here. Two
earlier shapes are retracted, deliberately — retraction pointers
below.

Peer sessions today coordinate through Bao rows + free-form
`SendMessage` + operator-typed un-park signals. There is no shared
representation of *why* a peer is doing what it is doing, no
programmatic assignment surface, no compute-lease enforcement, and
no clock the whole fleet can agree on for lease `expires_at`. This
RFD is the answer.

## Retractions

- **coordinator.ex Elixir adapter as primary:** retracted
  2026-09-05, superseded by the Go plugin in this RFD. The Elixir
  standalone adapter had no answer for global time or ReBAC
  enforcement.
- **thin-HTTPS bridge to taskweft-mcp.fly.dev:** retracted
  2026-09-05, superseded by cgo-linked C++. The bridge shape added
  an external service dependency the plugin doesn't need; embedding
  the planner satisfies operator's constraint that the plugin
  requires only REST commands and no other service.
- **`router.ex` mTLS auth extension:** retracted with the bridge —
  nothing calls MCP any more.

## Non-goals

Not a pure-Go port of the planner (RFD 0006 sized it at ~7000 LOC
and 8–12 weeks; cgo is 3–5 days). Not a rewrite of the RECTGTN
schema. Not a scheduler; not a hook. The plugin does not extend
Bao's storage surface — plan and skip state live in a SQLite blob
served by the sibling sqlite-fdb secrets engine, not in KV rows
under a separate mount.

## Related

- RFD 2204 (RECTGTN fleet coordination) — the domain document
  shape the plugin queries. This RFD supersedes its "coordinator
  adapter" section with a one-line pointer, per CLAUDE.md doctrine.
- RFD 2140 (OpenBao on FoundationDB) — the storage backend the
  plugin's SQLite fixture sits on top of.
- RFD 2142 (Bao PKI zerotrust) — the cert-auth path peers use.
- RFD 2146 (Bao is the secret store) — the policy discipline any
  new mount inherits.
- RFD 2147 (Bao is critical infrastructure) — the blast-radius bar
  a new plugin must meet.
- RFD 2195 (weftspun-bao Tailscale sidecar) — the deploy shape
  this plugin ships alongside.
- RFD 2202 (ReBAC Bao enforcement) — this RFD fills the
  compute-lease broker gap RFD 2202 named as future work.
- Sibling plugin scaffold: `7-service/service-bao-sqlite-fdb/` —
  the layout the new plugin copies verbatim.

This RFD was drafted by an AI and read by a human before it shipped.
