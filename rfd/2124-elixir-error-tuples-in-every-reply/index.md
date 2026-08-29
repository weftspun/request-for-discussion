---
title: "RFD 2124: Elixir error tuples in every reply"
rfd: "2124"
state: discussion
scope: what an interactor replies, and how a caller on the BEAM reads it
---

## Problem

An interactor replies with CBOR. `contract-command` chose that, and `weft/cbor.h` writes it.
Today every failure is a CBOR map with one text value:

    {"error": "--res 512 is below the production setting 1280; a smaller run is not evidence"}

A person can read that sentence. A program cannot act on it. To tell one failure from another,
a caller must match the text, and the text changes when somebody improves the wording.

This matters because the callers are Elixir. `interactor-weft`, `entities-assembly`,
`fabric-platform-central` and `zone-backend` run on the BEAM. Elixir code selects a branch with
a pattern, and the pattern it wants is `{:error, :some_reason}`. CBOR has no atom type and no
tuple type, so a CBOR reply cannot be that pattern. It arrives as a map with binary keys, and
the caller writes string comparisons instead of clauses.

## Decision

**A reply is an Erlang term, encoded in the External Term Format.** Three shapes only:

- `:ok` when there is nothing to report.
- `{:ok, value}` when there is.
- `{:error, reason}` when the command failed.

A `reason` is an atom, or a tuple of an atom and a map: `{:error, :no_engine}` or
`{:error, {:res_below_minimum, %{got: 512, minimum: 1280}}}`. The atom says what went wrong and
the map carries the numbers. Prose does not appear in the reason. Where a message helps a
person, it goes in the map under `:detail`, and no program reads it.

**The encoding is CBOR, and the mapping is closed.** An atom is CBOR tag 39, which IANA
registers as "identifier" and which Ruby symbols and Erlang atoms already travel under. A tuple
is an array. A map is a map, a binary is a text string, an integer is an integer. A reply
carries no lists, so an array is always a tuple and the mapping needs no second rule.

The External Term Format was written first and measured against this. Both reach the identical
term on the BEAM; `DETAILS.md` has both runs. ETF is exact and needs no adapter, which is a real
advantage, and three things outweigh it:

- This stack already writes CBOR. `weft/cbor.h` exists, the fan-out path uses it, and
  `transport-bus-cli` reads it. Adding ETF puts two encodings in one tree, and the second copy
  of a decision is the one that drifts.
- Not every caller is a BEAM process. The command-line transport layer, the RunPod job output,
  and anything reading the volume decode CBOR with a library they already have. ETF would need
  an ETF reader written into each.
- The C++ interactor already has a CBOR writer. Under ETF it would have needed a hand-rolled
  term encoder; under CBOR it needs one tag.

**The adapter is written once, in the contract.** The objection to CBOR is that it needs a
decoder that knows the mapping. It does, and there is one: `Weft.Reply.decode!/1`. The objection
is to _every caller_ writing one, and shipping it answers that rather than dismissing it.

**An atom is decoded with `String.to_existing_atom/1`.** That refuses an atom the virtual
machine does not already have, so a reply cannot grow the atom table of the process that reads
it. It is the same guarantee `:erlang.binary_to_term/2`'s `[:safe]` gives, written down instead
of relied upon.

The rule that makes it work is worth stating, because it looks like a problem and is not. An
atom exists in the receiving virtual machine when some module names it. A caller that matches
`{:error, :res_below_minimum}` has that atom compiled into it. So the set of reasons a caller
can decode is exactly the set it has a clause for, and the guarantee is supplied by the caller's
own source. `DETAILS.md` records the test that established this, including the reading of
`[:safe]` that was wrong.

**The reason set is closed and shared.** `contract-command` lists every atom an interactor may
send. A new reason is a change to that list, in the same commit that first sends it. Three
implementations already write replies: `interactor-see-through-cpp` in C,
`interactor-see-through-python` in Python, and `transport-runpod` for its own transport
failures. One list keeps them in agreement, and the A/B between the two interactors depends on
it: two implementations that report different reasons for the same refusal are not answering
the same question.

**A transport layer's own failures use the same shape.** A worker that cannot reach the bus
replies `{:error, :bus_unavailable}`, and one whose deadline passes replies
`{:error, {:timeout, %{waited_ms: 900000}}}`. The caller cannot tell, and does not need to tell,
whether the interactor or the transport layer produced a failure. Both are failures of the
command it sent.

**C++ that writes a term uses Fine.** [Fine](https://github.com/elixir-nx/fine) (Apache-2.0) is
already the answer in this organisation: `taskweft/nif` vendors it, and `interactor-ward` and
`datasource-queen` carry it as `thirdparty/taskweft/fine.hpp`. Erlang's C API is large, and
every project that touches it grows the same set of helpers copied from the last project. Fine
is that set, written once.

Two of its properties decide this rather than taste. It encodes and decodes from the function
signature, so the shape of a reply is stated in the type and not in a sequence of
`enif_make_*` calls that no compiler checks against each other. And it creates all static atoms
at load time, which is the same closed set this decision needs: an atom that exists at load
cannot be created later by a message, and a reason the module does not name is a reason it
cannot emit.

A gate holds this. A repository that handles Erlang terms in C++ and shows no Fine fails, and
so does a first-party source that calls `enif_make_*` or `enif_get_*` directly. Vendored trees
are skipped, or Fine itself would be reported as the defect. It is green today over 39
children, which is the reason to add it now: a convention is cheapest to hold before a second
way of doing the same thing exists.

**Fine does not reach a worker that is not a NIF.** This is the limit worth stating. Fine
operates on `ERL_NIF_TERM` inside an `ErlNifEnv`, and a standalone worker has neither: it is an
operating-system process that writes bytes to shared memory, not a library the virtual machine
loaded. So an interactor that answers over the bus writes the External Term Format itself, and
Fine governs the NIF boundary where the BEAM calls into C++ directly. Both produce the same
term. Only one of them has a virtual machine to produce it in.

## What this does not decide

**The bus payload stays bytes.** `weft/command.hpp` sends a request id and a body. ETF is what
the body holds, and the envelope does not change.

**The entity path is untouched.** `weft/cbor.h` still writes the fixed entity rows the fan-out
path carries, where no BEAM process reads them and the receiver is C. This decides the reply to
a command, which is the surface an Elixir caller touches. Both are CBOR, which is the point:
one encoding.

**A RunPod job result is still JSON.** The queue carries JSON, so the reply bytes stay base64 in
`{"output": {"cbor": "..."}}`. The field name does not change, because the encoding did not.

## References

- `contract-command`, `weft/interactor.h`: a command in, reply bytes out
- `weftspun/logbook` holds no entry for this yet
- Erlang External Term Format: https://www.erlang.org/doc/apps/erts/erl_ext_dist.html
- `:erlang.binary_to_term/2`: https://www.erlang.org/doc/apps/erts/erlang#binary_to_term/2
- `DETAILS.md` in this folder: the encoder subset, and the test against a real virtual machine

{{< include DETAILS.md >}}
