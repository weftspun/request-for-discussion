# RFD 1164: A calibration set is training data

**State:** ideation
**Feature:** data hygiene at the compiler boundary
**Scope:** `3-interactor/rf-detr-cpp/scripts/prep_calibration.py`

## Decision

A calibration set obeys the training-data rules in full: it comes
from a training-side corpus such as `coco_images_train2017`, never
from the blinded holdout or anything derived from it.

`prep_calibration.py` already re-asserts the exclusion at read time
and hard-fails on a blinded id. That was written as belt and braces
and this is why it is load-bearing. `--calib` takes a training
corpus, so the docstring should say so rather than leave it inferred.

## Problem

"Calibration" sounds read-only: run frames through a graph, record
activation ranges, quantise. At optimization level 1 it is. At
level 2 the Dataflow Compiler runs Quantization-Aware Fine-Tuning,
and the log says plainly what that means:

    [info] Starting Quantization-Aware Fine-Tuning
    [info] Using dataset with 1024 entries for finetune
    Epoch 1/4

Four epochs of gradient steps over the frames handed in as
calibration, so the weights that reach the device were trained on
that set rather than measured against it.

CLAUDE.md holds validation and test splits out of training, tuning
and selection. A set passed to `--calib` meets all three and nothing
at the call site says so. Handing the compiler the blinded holdout
would read as a sensible choice and would train on it.

## Related

RFD 1163 places the compile. RFD 1128 asks about four bits.
