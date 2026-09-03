# Logbook: RFD 2183 baseline against See-Through public test images

Question: how well does the out-of-the-box three-step pipeline
(SAM2 or rf-detr-Seg -> OmniGen2 pretrained -> MoGe-3) reconstruct
the five See-Through test images and their depth, measured against
See-Through's own outputs on the same inputs. This is the pre-training
baseline the RFD 2183 retrain is graded against.

## The apparatus

Inputs: `test_image.png`, `test_image2.png`, `test_image3.png`,
`test_image4.png`, `representative.jpg` from the See-Through public
`common/assets/`. These are public generated images, evaluation only;
they do not enter any training corpus (RFD 2183 uses ANNY renders
from `render_layer_decomp_corpus.py` and VRMs from the atelier
pipeline for training).

Runner: CUDA on the RTX 3090, `pixi run -e omnigen2` for the
inference legs. Scoring on either desk via
`6-datasource/anny-render-corpus/eval_layer_decomp.py`.

Baseline outputs: See-Through's own masks, layer reconstructions and
depth for the same five inputs.

Metric floors: recorded in `logs/rfd2183-baseline-floors.json`,
computed as the mean pairwise score between different layers of the
same image (IoU/SSIM), the mean random-pair LPIPS ceiling, and the
abs-rel of a constant depth map at the baseline's mean.

## Command

    cd 6-datasource/anny-render-corpus
    pixi run -e omnigen2 python eval_layer_decomp.py \
        --candidate build/rfd2183/baseline/omnigen2-oob \
        --baseline  build/rfd2183/baseline/see-through \
        --floors    logs/rfd2183-baseline-floors.json \
        --out       ../2-contract/manuals-weftspun/logbook/logbook-rfd2183-baseline-see-through-assets.md

## Result table

<!-- Fill from eval_layer_decomp.py output. Do not hand-edit numbers;
     re-run the eval and paste. Household-object anchors on the mm
     depth span come from the script per CLAUDE.md. -->

| layer      | n | IoU | IoU floor | SSIM | SSIM floor | LPIPS | LPIPS ceiling |
|------------|---|-----|-----------|------|------------|-------|---------------|
| body       | ? |  ?  |     ?     |   ?  |      ?     |   ?   |       ?       |
| face       | ? |  ?  |     ?     |   ?  |      ?     |   ?   |       ?       |
| hair_front | ? |  ?  |     ?     |   ?  |      ?     |   ?   |       ?       |
| hair_back  | ? |  ?  |     ?     |   ?  |      ?     |   ?   |       ?       |
| clothing   | ? |  ?  |     ?     |   ?  |      ?     |   ?   |       ?       |

| n | abs-rel | abs-rel floor | Pearson | Pearson floor | mean scene span |
|---|---------|---------------|---------|---------------|-----------------|
| 5 |    ?    |       ?       |    ?    |       ?       |    ? mm (?)     |

## Verdict

<!-- Fill: does out-of-the-box OmniGen2 clear the floor on any layer,
     and by how much. This is what the RFD 2183 retrain has to beat. -->

## What did not go as planned

<!-- Anything that ran differently from what the apparatus says.
     Missing images, dropped layers, LPIPS install failure, depth
     scale mismatch, mask registration offset. Rule 3: an unmet
     precondition is a FAIL, not a skip. -->

## Retraction shelf

<!-- Reserved for a subsequent entry that withdraws a number above.
     CLAUDE.md: retractions stay in place next to what they retract. -->
