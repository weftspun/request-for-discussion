# Why RFD 2199 picked the Hailo vit_base_bn recipe

Records the concrete diagnosis that drove the pick, so a later retract-if-
below-keypoint-bar has provenance to reference. Sits alongside
`logbook-rfd-2199-hailo-int4-survey.md` and
`logbook-dfc-bisect-methodology-rf-detr.md`.

## The three candidate paths at the pick point

After the DFC compat bisect converged, three fix-paths were live:

1. **fork-encoder-LN emission**: patch rf-detr's PyTorch export to emit
   LayerNormalization in the shape DFC's parser accepts (opset tweak,
   manual decomposition, or a decoder-specific export flag). Days if the
   pattern is small, unknown until the fork lands.
2. **Hailo vit_base_bn recipe**: replace LN with BN across the encoder
   and retrain. Weeks-scale wall from zero epochs; the LN→BN arch
   amendment lands as a single edit inside a QAT-4bit + expanded-
   keypoints retrain HERO will run once the recipe pull + ANNY-SOMA
   corpus render + BN placement cross-check are in place. A "folds into
   an already-in-flight retrain" framing bounced through the coordinator
   thread here and was retracted; HERO had zero epochs run this session
   at pick time.
3. **zoo pivot**: pick a CNN detection/keypoint model already validated
   in `hailo_model_zoo` and abandon rf-detr for the first spike.

## The diagnosis that named the pick

Extracted subgraph tests (`extract_model` boundary at the encoder's four
`Transpose_1/3/5/7` outputs) reproduced the DFC failure inside the encoder,
not the projector. Full traceback in `logbook-dfc-bisect-methodology-rf-detr.md`.
Two errors surface in one pass:

```
onnx_graph.py:444, update_reshape_output_format
  ValueError: channels is not in list

onnx_translator.py:967, _create_layer_normalization_layer
  → onnx_graph.py:2463, _convert_axes_to_nhwc
  IndexError: list index out of range
```

DFC's LayerNorm handler asks `nchw_to_nhwc_axis_mapping[input_format[axis]]`
where `axis` comes from the ONNX LayerNormalization node's `axes` attribute
and `input_format` is DFC's own NHWC-shaped format tracker. For rf-detr's
encoder LNs, the axes reference positions the tracker cannot map. Hailo's
own `vit_base` (LayerNorm variant) parses cleanly through the same DFC
5.3.0, so the failure is specific to rf-detr's LN emission pattern, not
LayerNormalization in general.

## Why the pick is vit_base_bn rather than fork-encoder-LN

The fork-encoder-LN path would fix rf-detr's LN emission to match the
pattern DFC accepts (probably matching what `vit_base` emits). Cheaper
than a full retrain in isolation, and reversible if it doesn't take.

The vit_base_bn path replaces LN with BN outright, sidestepping the
DFC-vs-LN interaction entirely.

The pick came down to how the two options compose with the training
work HERO was scoped for regardless:

- HERO's task #65 was queued for a QAT 4-bit + expanded-keypoints
  retrain (not yet running at pick time).
- vit_base_bn's arch amendment (LN → BN in the encoder) lands as a
  single edit inside that retrain; one weeks-scale wall carries both
  the arch swap and the QAT loop.
- fork-encoder-LN would still need HERO to run the same retrain, then
  either export with the fork or retrain again if the fork requires
  weight-shape changes. Same or longer wall.

vit_base_bn also has stronger prior: Hailo ships the recipe as a
supported path in `hailo_model_zoo` (`vit_base_bn.yaml` + its `.alls`),
so DFC handles it by construction. fork-encoder-LN is an rf-detr-specific
export tweak with no equivalent precedent.

## What triggers the retract

The vit_base_bn recipe carries an accuracy cost (BN vs LN in a
transformer typically loses 1-3 mAP points on classification; unknown
delta on detection / keypoints). If the retrained BN-encoder rf-detr
lands below the keypoint accuracy bar RFD 2199 needs, the
fork-encoder-LN path is still available as a follow-up. The
zoo-pivot is the second fallback if fork-encoder-LN also misses.

Retract shape when it triggers: this entry stays (the reasoning is what
gets retracted-around, per CLAUDE.md's "retractions stay in place next
to what they retract" rule), a follow-up logbook entry names the
observed accuracy gap and the switch, and RFD 2199's body carries the
one-line pointer to the follow-up per RFD 2201 doctrine.

## Compat probe expectation

`dot-claude#19` (hailo-dfc-compat-probe skill) will exercise on the
incoming ONNX once HERO's retrain hands it over. Beyond the plain
`PARSE OK`, the probe now also implicitly validates BN placement: if
any encoder LayerNormalization survives the arch amendment (retrain
kept old checkpoint LN shapes somewhere), the probe's error signature
will still be the `IndexError` at `_convert_axes_to_nhwc` and we catch
it before the compile+measure spec fires. Green parse plus
`onnx.load(...).graph.node` showing zero LayerNormalization inside the
encoder subgraph is the double-check.

## References

- `logbook-rfd-2199-hailo-int4-survey.md`, original DFC + hardware
  survey.
- `logbook-dfc-bisect-methodology-rf-detr.md`, bisect methodology +
  full traceback of the two DFC error signatures.
- `logbook-rfd-2199-compile-measure-spec.md`, compile pipeline +
  metric matrix that fires once the retrained ONNX lands.
- `hailo_model_zoo` `cfg/networks/vit_base_bn.yaml` + `training/vit/README.rst`
  in `5-repository/hailo-model-zoo`, the reference recipe.
