## Status

Done for the smallest loop (`zone-server-h2o` PR #5). Not verified end
to end.

## Wire protocol

The `domain` field flows through the same chain the `objective` field
already used: `mud_cbor_encode_boot_config()`, then
`mud_session_get_or_create()`, then `on_mud_command()`'s
`POST /api/mud/command` handler. That handler now reads `domain` from
the request body and picks a matching default objective
(`explore_gyre` for The Gyre, `gain_watch_trust` for Middleham). The
handler's own prior comment already flagged an objective/domain picker
as website-UI scope, not its own. This work fills that gap rather than
inventing a new extension point.

## Verification

Real, not assumed:

- `mud/guest/test/gyre_smoke_test.cpp`: a native (non-riscv64) link of
  `mud_guest.cpp` that drives `mud_boot()` and `mud_step()` through the
  whole Gyre loop (look, go east, look). Built and run locally against
  QCBOR (`laurencelundblade/QCBOR`). It produces real narration text
  and real `post_room` transitions, and `objective_complete()` returns
  true after the player visits both rooms. A native Middleham boot, run
  the same way with the same seed `DIFFERENTIAL_TEST.md` uses, produced
  byte-identical "Middleham City Gate" narration to before this
  change. The default path did not regress.
- The client change (mode selector, per-domain session ID, `domain`
  field on the wire) went through real end-to-end tests. The team used
  Playwright, in both Chromium and Camoufox (a Firefox-family browser),
  against a throwaway local Node stub that matched the real API shape.
  The team did not commit that stub. The team threw it away once it
  confirmed the client logic was correct.
- `mud/web/test/gyre.spec.ts` is the real, committed spec. It is
  Camoufox-driven, and it follows `mud.spec.ts`'s own house rule:
  `MUD_BASE_URL` must point at a real reachable instance, with no
  mock. It has not run against one yet. It stays red until a real
  deployment with the Gyre domain exists — the same state
  `mud.spec.ts` itself documented before its own first real deploy.

The team did not verify a `riscv64-musl` and `libriscv` build and run
of the changed guest code. The team's own environment had no cross
toolchain for that. The team did not attempt an FDB or H2O real build
or deploy either.

## Revisit when

A real `-z` deploy exists with the Gyre domain reachable. At that
point, run `gyre.spec.ts` for real. Also run a real riscv64
differential test, matching `DIFFERENTIAL_TEST.md`'s own Middleham
precedent. Only then treat this as more than a reviewed, natively
tested diff.

`rfd/0085`'s fuller room graph, contract catalog, and item set stay
design only. Porting them past the two-room smallest loop is a
separate, larger task. This RFD does not claim the team finished that
larger task.
