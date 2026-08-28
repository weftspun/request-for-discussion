# RFD 1153 details: what the crops found, and what they did not

## Result

72 crops, four per cutout, across three backends and six photographs chosen for
sheer fabric, specular surfaces and wispy hair.

| category | mean | below 6.0 |
|---|---|---|
| connectivity | 9.63 | **0 / 72** |
| gradient | 3.79 | **47 / 72** |

The failure mode of these background removers on this corpus is **edge fidelity,
and only edge fidelity**. Not one crop showed a connectivity fault: no floating
fragments, no holes punched through solid regions. 65% of crops showed a gradient
fault -- an edge either smeared into a blur or, more often here, hardened into an
abrupt cut where the real edge is soft.

Unlike the two whole-image formats, this produces variance: connectivity spans
8.0 to 10.0 and gradient spans 0.8 to 8.0.

## Crop selection

The study selected crops by hand for exhibiting one artefact category.
Automating that: artefacts live where the matte is uncertain, so candidate
windows are ranked by how much partial alpha they contain, taken at native
resolution and spaced apart so k crops are not k views of one artefact.

Measured concentration on a wispy-hair source: whole-image soft alpha 3.97%,
selected crops 35-75%. A 9 to 19 times enrichment, which is the mechanism that
puts artefacts inside the judge's input budget.

## Configuration, not capability

EditScore's stated applications are best-of-N reranking and supplying an RL
reward signal. Both failed on first attempt here, and the cause was how it was
configured rather than the model.

Three faults, all ours:

* `num_pass=1` at temperature 0.7 -- a single stochastic sample. Self-ensembling
  is how the paper reaches its headline numbers.
* a pairwise "is B better than A" comparator, which is not how best-of-N works:
  candidates are scored independently against the source and the best wins. That
  comparator was position-driven in 37 of 52 pairings.
* custom single-image rubrics, which bypass the SC pass entirely and are not
  EditScore at all.

Corrected -- published SC rubric, source and candidate as the pair, an edit
instruction, `num_pass=3`, judged on 100px crops -- it reproduces the
ground-truth ordering on the alphamatting.com set:

| backend | overall | following | true SAD |
|---|---:|---:|---:|
| birefnet-hr-matting | 4.07 | 5.39 | 4.00 |
| birefnet-matting | 3.81 | 4.97 | 4.90 |
| birefnet | 3.44 | 4.78 | 8.15 |

48 judgements over 8 images. Both score columns descend monotonically as true
error rises, and the ordering held when the sample was tripled from an earlier
15-judgement run. The misconfigured run had ranked the segmenter *best* on
gradient, which ground truth inverts.

**Aggregate ranking works; per-sample selection does not.** Spearman against true
SAD is -0.237 -- right sign, strengthening with sample size (-0.139 at n=15),
still weak. Best-of-N picked the true best on 6 of 16 crops, 37.5% against a 33%
chance rate: at n=15 it read 3 of 5 and that was noise.

Individual judgements are noisy and the noise averages out over sixteen per
backend, which leaves the true ordering standing. That is what self-ensembling
buys, and why `num_pass=1` inverted the ranking.

The consequence for anything built on this: EditScore can referee a comparison
between models, so it is usable for evaluating a trained keyer. It is not shown
to be a per-sample reward, which is the mode a DPO loop would need.

## What this does not establish

**The between-backend ordering**, for the reasons above. Model selection was
settled separately, against ground truth: see RFD 1152.

## No rationales

Every fault carries `reasoning: "concise"`. The Apple-silicon backbone prefills
the assistant turn as far as `{"reasoning": "concise", "score": [` so that only
the score tokens are generated, which is roughly 20 times less decoding. The
reasoning field is therefore a constant supplied by us, not model output.

Scores are unaffected. Recovering explanations means dropping the prefill and
paying full decode.

## Rubric scale hazard

EditScore builds its rubrics as `text.replace('10', str(score_range))` and
divides the answer by `score_range / 10`. A rubric injected without the same
replace is answered on a 0-10 scale and rescaled as if it were 0-25. Full marks
then read 4.00, and the range looks compressed into three levels when it is not.
