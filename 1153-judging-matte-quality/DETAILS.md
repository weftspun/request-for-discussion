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

## It failed at what it is built for

EditScore's stated applications are best-of-N reranking and supplying a reward
signal for RL fine-tuning. Both were tested on this task and both failed.

*Ranking.* Mean gradient came out 4.50 for the plain segmenter, 4.23 for
HR-matting and 2.65 for the 1024px matting model -- an ordering that is
suspicious on its face, since a dichotomous segmenter should score *worse* on a
rule whose stated fault includes false hard edges. A later ground-truth run on
the alphamatting.com training set confirmed the inversion: the segmenter is
roughly 3x worse on gradient error, not better. The likely cause is that the
judge rewards crisp edges as "detail preserved" and reads a correctly soft matte
as blur, which the rubric wording asks it not to do and cannot enforce.

*Pairwise reranking.* Judged on matched crops in both orders, 37 of 52 pairings
were position-driven -- the same answer whichever image came first -- against 15
content-consistent. A reranker that reads slot rather than content cannot select
best-of-N.

Both were scored without ground truth, so the judge could not know what fine
structure ought to be present.

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
