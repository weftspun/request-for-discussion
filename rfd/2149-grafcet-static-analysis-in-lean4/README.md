# RFD 2149: GRAFCET static analysis in Lean 4, from Elixir

**State:** prediscussion
**Feature:** port `Project-AGRAFE/GRAFCET-static-analysis` (Java, MIT)
to Lean 4 with a plain C ABI, called from Elixir via a C NIF
**Scope:** taskweft-grafcet-static (new repo), taskweft (NIF module)

## Decision

Port the two structural analyses to Lean 4. The port is a first-class
repository, `taskweft-grafcet-static`, placed in the workspace
manifest at `3-interactor/taskweft-grafcet-static`. Lean's `@[export]`
produces a C ABI declared in `c_src/grafcet_static.h`; a small NIF in
taskweft loads the shared library and exposes `analyse/1` to Elixir.
Abstract interpretation is staged; the SFC types carry the fields,
the analysis is a follow-on that needs either a Lean-native interval
domain or a Z3 bridge.

    char *grafcet_static_analyse(const char *sfc_json);
    void  grafcet_static_free(char *buf);

A stub in `c_src/grafcet_static_stub.c` returns `{"error":"stub"}` so
the NIF links today; swapping the stub for the Lean-produced library
closes this RFD. `DETAILS.md` carries semantics, staging, verification.

## Problem

RFD 2148 puts compact IEC 60848 GRAFCET at the front of taskweft, but
provides no verifier. AGRAFE ship a static analyser (step reachability,
pairwise concurrency, abstract interpretation of variable domains) as
an Eclipse plugin in Java, with hard build dependencies on Apron and
Z3. Not something a taskweft loader can call.

## References

1. `3-interactor/taskweft-grafcet-static/`; the port
2. Upstream: https://github.com/Project-AGRAFE/GRAFCET-static-analysis
3. RFD 2148: compact GRAFCET as taskweft's authoring surface

This RFD was drafted by an AI and read by a human before it shipped.
