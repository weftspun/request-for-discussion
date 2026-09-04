# RFD 2199 rf-detr INT4 compile + measure spec

Precedes the compile step. Names the DFC command sequence, the metric
matrix, the acceptance floors, and the HF result-dataset shape. Written
under task #64 while blocked-passive on the DFC install (operator
Hailo Developer Zone download) and on HERO's task #65 (rf-detr QAT
training). Consumes HERO's output when it lands; drives the compile +
measure on-device work when the USB firmware recovery lands.

## Inputs from upstream

From HERO (task #65): HF **model repo** `chibifire/rf-detr-int4-qat-<yyyymmdd>`
per the test-to-HF standing rule (coordinator ruling 2026-09-04: model
repo for the weights + metrics hand-off, dataset repo shape reserved
for the measurement results downstream), carrying:

- `checkpoint.pt` (or `.safetensors`), the QAT-trained rf-detr weights at
  bf16-storage with int4 fake-quant applied during training via STE
  backward, per RFD 2199's real-QAT stance.
- `training_metrics.parquet`: loss curve, calibration set, held-out
  accuracy at bf16 and at simulated int4 (from the fake-quant forward
  pass). One row per step, ETNF-shaped per RFD 2196 rule 1.
- `qat_config.json`: quantizer choice (`torchao Int4WeightOnlyQuantizer`
  or workspace substitute), group size, calibration set identity, seed.
  This is the config the compile step must match exactly.

`qat_config.json` is the contract. If DFC's QAT-import path cannot honour
the group size or per-channel choice HERO used, the whole compile fails
loudly at import rather than silently re-quantizing to a nearby scheme.
That's the negative control on the pipeline.

## Compile pipeline

DFC runs in Fedora WSL. The reference tutorial is `DFC_6_QAT_Tutorial.ipynb`,
which imports a pre-QAT-trained checkpoint into DFC's Model Optimization
stage under a `qat_import` flow. If that flow rejects the checkpoint (the
community-thread parser gotcha from the survey), the fallback is a smaller
rf-detr variant or an operator escalation to a Model-Optimization bypass.

Pipeline shape:

1. `hailo parser` on the ONNX export of the QAT checkpoint. Confirms the
   graph is DFC-parseable; blocks on any op the parser refuses.
2. `hailo optimize --qat-import` (or the DFC 6 QAT tutorial equivalent).
   Loads the int4 weights + quantizer config from `qat_config.json`.
   Emits a `<variant>.har` in the WSL working dir.
3. `hailo compiler <variant>.har --hw-arch hailo10h`. Produces
   `<variant>.hef`. Failing here means the arch does not have a kernel
   for one of the layers at int4; report the layer name back to HERO so
   the training loop can substitute.
4. `hailortcli fw-control identify` on the USB device. Un-park
   precondition, checks the device is out of bootloader before the
   measure step runs.
5. `hailortcli benchmark <variant>.hef` for a first synthetic-latency
   number. Not the accuracy measurement, just a smoke test.

Each step's exit code and stdout gets captured to a file named by the
step number, per RFD 2196's "don't lose the apparatus" logbook shape.

## Metric matrix

The measurement, on real inputs, is a table one row per
`(variant, precision)`:

| column           | meaning                                                                    |
| ---------------- | -------------------------------------------------------------------------- |
| `variant`        | rf-detr variant (nano / small / base) as HERO picked                        |
| `precision`      | one of `bf16-baseline`, `int4-qat-fake` (from HERO), `int4-hef-hailo10h`    |
| `map_50`         | COCO-style mAP at IoU 0.50 on the eval set                                  |
| `map_50_95`      | COCO-style mAP averaged over IoU 0.50 to 0.95                               |
| `latency_p50_ms` | median per-image latency on Hailo-10H (int4-hef only; else null-as-value -1) |
| `latency_p95_ms` | 95th-percentile latency same way                                            |
| `throughput_fps` | steady-state throughput after warm-up                                        |
| `hef_bytes`      | size of the HEF (int4-hef only; else -1)                                     |
| `notes`          | free text, blocklisted-op fallbacks or measurement caveats                  |

`-1` sits where "no value" would be if this were nullable, per CLAUDE.md's
ETNF rule.

## Acceptance floors

For the first spike, floors that are also RFD 2199's success criteria:

- `int4-hef-hailo10h` mAP within Hailo's blog-claimed 1-2 points of
  `bf16-baseline`. A larger drop is a genuine finding worth surfacing
  before ship, since the blog claim is against LLMs and this is vision.
- `latency_p50_ms` on Hailo-10H under 20 ms per image for rf-detr-nano
  scale. Placeholder floor; refine against the vendor's INT4 TOPS
  claim (40 TOPS at INT4) once a real measurement lands.
- No layer falls back to CPU during compile. A silent fallback is a
  failure per rule 3 (silent skip reads as pass).

## Eval set

The eval set is the held-out portion of whatever HERO trained on. `qat_config.json`
names the calibration set; the held-out is its non-overlapping complement.
No use of `coco_person_commercial_val2017` (blinded holdout) or anything
derived from `val2017`.

## HF result dataset

`chibifire/hailo-rf-detr-int4-measure-<yyyymmdd>`, per RFD 2196 rule 5
upload recipe with `hf upload-large-folder --repo-type=dataset`. Shape:

```
data/measurements/train-*.parquet    # the metric-matrix table above
raw/step_1_parser.log                  # exit code + stdout for each pipeline step
raw/step_2_optimize.log
raw/step_3_compiler.log
raw/step_4_fw_control.log
raw/step_5_benchmark.log
artifacts/rf_detr_<variant>_int4.hef   # the compiled HEF, referenced from the parquet by content-hash path per RFD 2196 rule 4
inputs/qat_config.json                 # copy of HERO's config, for reproducer
CITATION.cff                           # per Deliverables rule in CLAUDE.md
```

`data/measurements/train-*.parquet` follows the wide-row-per-example
shape from RFD 2196 rule 1: each row is one `(variant, precision)`
combination, no satellite tables for a metric-only dataset this small.

## What this spec does not cover

- Whether the DFC `qat_import` path accepts a torchao-QAT checkpoint. It
  needs a first attempt against a fabricated tiny checkpoint before
  HERO burns training compute on rf-detr proper. Task-order suggestion:
  I install DFC (once the wheel lands), fabricate a two-layer int4 dummy
  net, run steps 1-3, and report back before HERO starts task #65.
- The MoGe-3 second-spike (only relevant if rf-detr's int4 result is
  surprising).
- LLM INT4 case (deferred per the survey, pending operator override on
  the PTQ blocklist).

## Reproducer

None yet. This spec is drafted before the compile step runs. The
reproducer lands in a follow-up logbook entry after the first
end-to-end compile succeeds, and re-lands (with retraction notes) if
early measurements force spec revisions.
