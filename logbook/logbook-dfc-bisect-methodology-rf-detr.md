# DFC parse-bisect methodology, from an rf-detr investigation

Recording the methodology two probes converged on today while task #64 tried
to place the DFC-vs-rf-detr failure. Journal shape rather than an RFD; the
finding is a pattern next probes can copy, not a decision.

## The two errors DFC emits, and where each localizes

When DFC's `ClientRunner.translate_onnx_model` rejects a graph, the pair of
errors that surfaces localizes different parts of the failure:

- `ValueError: channels is not in list` (from
  `onnx_translator/onnx_graph.py:444`, `update_reshape_output_format` calling
  `input_format.index(Dims.CHANNELS)`) means a Reshape node received a tensor
  with a format the tracker cannot map to NCHW. Usually fires downstream of
  an NLD-shaped (sequence) tensor being rewrapped as spatial.
- `IndexError: list index out of range` from
  `_convert_axes_to_nhwc` at `onnx_graph.py:2463` (`input_format[axis]`)
  means a LayerNormalization node's `axes` attribute references a position
  beyond what DFC's format tracker knows. Fires under the simplifier-retry
  pass. If a first-attempt `channels is not in list` and a simplifier-retry
  `IndexError` come out of the same run, they name two symptoms of the same
  LayerNormalization mishandling.

The retry pass ships `[info] Simplified ONNX model for a parsing retry
attempt (completion time: MM:SS.ss)` and saves `<model>.sim.onnx`. Many
minimal repros pass on the retry that fail on the first attempt, which is
how a small negative control can accidentally read as green while the real
model stays red.

## The bisect that actually localizes

The point is to isolate the failing site by parsing subgraphs, not the whole
model. Two techniques, one wrong-then-right one right-from-the-start:

**`start_node_names` + `end_node_names` on the full ONNX.** Cheap because
DFC does the extraction. **Takes NODE names, not tensor names.** A first
probe using `<node>_output_0` tensor names returned
`MisspellNodeError: Unable to find end node name`, silently succeeding
on the parser side while returning nothing useful. Once switched to bare
node names (`.name` attribute on `onnx.NodeProto`, drop the `_output_0`),
the partial parses land.

**`onnx.utils.extract_model(src, dst, inputs, outputs)`.** Extracts a
subgraph as a standalone ONNX file. Takes TENSOR names (which the caller
maps as new graph inputs and outputs), not node names. Then run
`translate_onnx_model` on the extracted file the same way. Slower per
probe (writes an intermediate ONNX) but sidesteps DFC's own extraction
path, so it isolates the failure from any surprise-behavior of the
partial-parse machinery.

Under `start_node_names`/`end_node_names`, DFC still walks the ancestors of
the requested end nodes. So a cut ending inside the encoder still requires
the encoder's context and can fail during output-layer construction on a
raw NLD tensor with `IndexError: list index out of range`. That error at an
encoder-internal cut is not the actual failure site; it is DFC unable to
emit a valid output on a tensor whose format is not NCHW. `extract_model`
does not have this problem because the extracted subgraph's inputs and
outputs become the new graph's boundary, so DFC has no encoder-side
context to walk.

## Prefer `extract_model` when isolating a failure site

`start_node_names`/`end_node_names` is fast and useful for the "does this
part fail" question against the whole model.
`onnx.utils.extract_model` is right for the "is the failure in this
component alone" question. Confusing the two costs a rewind: the first
finding today read `end_node_names=projector_end → ValueError: channels
is not in list` and concluded the projector was the failure site, but the
same site when extracted (with the encoder cut off entirely) parsed
green. The actual failure was the encoder outputs feeding the projector,
and the `end_node_names` cut ran the whole encoder up to the projector
boundary.

## Retry-pass changes what a probe passes

DFC's simplifier retry can transform a `Transpose → LayerNormalization →
Transpose` sequence into an atomic LN that DFC's channel tracker accepts.
A minimal PyTorch reproducer that ships with the same transpose-wrap
pattern will therefore pass on the retry, even when the whole model with
the same pattern fails. Two ways the minimal repro can miss the real
failure:

1. The simplifier reduces the minimal repro but not the whole graph
   (because the whole graph has entangled Concat/Split/residual context
   the simplifier cannot fold).
2. The minimal repro's LN operates on a tensor rank the tracker can map,
   while the whole graph's LN operates on a tensor rank that trips
   `_convert_axes_to_nhwc`.

If the goal is a controlled negative test, extract the failing subgraph
literally rather than reconstruct it in PyTorch. The extract preserves
the axes, opset, and simplifier-boundary the whole model has.

## What a partial-parse report reads as

A green partial parse always reports `PARSE OK` and saves a HAR under the
name passed to `save_har`. A red partial parse hits an exception; the
`type(exc).__name__` + `str(exc)[:400]` is enough to distinguish
`MisspellNodeError` (methodology bug), `ValueError: channels is not in
list` (format tracker on Reshape), `IndexError: list index out of range`
(format tracker on LN axes), and the shape-mismatch broadcast errors that
fire when `net_input_shapes` overrides a static ONNX input to a
resolution its position embeddings cannot span.

Rule 3 corollary: a probe that catches the exception and returns
`ok = False` without naming the error type is decoration. Log the type
and truncated message; save the traceback separately when the error class
is genuinely surprising.

## Reference

External sources touched during the investigation are in
`logbook-rfd-2199-hailo-int4-survey.md`. The prototype scripts live in
this session's scratchpad under
`AppData/Local/Temp/.../scratchpad/dfc-compat/` (`probe_seg2.py` for
resolution scan, `probe_seg3_bisect.py` for the wrong tensor-name bisect,
`probe_seg4_bisect.py` for the corrected node-name bisect,
`extract_projector.py` and `extract_encoder.py` for `extract_model`
isolation). Not shipped; the pattern is what matters.
