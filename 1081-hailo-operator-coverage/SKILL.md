---
name: hailo-operator-parse
description: Find out which operators the Hailo Dataflow Compiler rejects, by compiling a small export rather than reading documentation. Use before promising any model to the UGen300, and when an allowlist and a compiler disagree.
---

# Asking the compiler

The compiler is the authority. A support matrix in documentation is a
description of it, and the two are allowed to differ.

## Order

1. **Export the smallest graph that carries the question.** One block,
   one attention layer. A rejection names an operator at any size, and
   a small graph fails in seconds rather than minutes.
2. **Run the pair.** `gate_onnx_device.py` on the host, then
   `gate_dfc_parse.py` inside `weftspun-hailo-dfc:5.3.0`. The DFC wheel
   is `py3-none-linux_x86_64`, so the container is not optional.
3. **Read a disagreement as the finding.** If the gate passes and the
   compiler rejects an operator, `DEVICE_OPS` is too generous and the
   operator moves to `KNOWN_BLOCKERS`. If the gate fails and the
   compiler parses, the allowlist is too strict and the operator moves
   in. Both are results.
4. **Record the rejected operators by name**, not as a count. The next
   person needs to know whether it was one exotic op or the whole
   attention pattern.

## Traps

A silent skip reads exactly like a pass. If a precondition is unmet --
no export, no image, no weights -- that is a FAIL, and the run says
which.

Do not substitute an operator to make a graph parse. A graph that
compiles because somebody replaced neighborhood attention with dense
attention answers a question nobody asked.

`natten` and `flex_gemm` are CUDA libraries, not ONNX operators. What
gets exported is whatever the tracer emits in their place, so read the
export before reading the rejection: the operators in the graph may
already be a poor rendering of the intent.
