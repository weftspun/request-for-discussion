# RFD 1141 details: what is not published, and the numbers behind the rules

## The size measurement that drives the weights rule

Measured 2026-08-25 on `experiments/anny_camera_lora_1gpu/checkpoint-200`:

| | |
| --- | ---: |
| checkpoint on disk | **14.8 GiB** |
| tensors in it | 886 |
| tensors carrying LoRA | **304** |
| extracted adapter | **19.52 MiB** |
| ratio | **776x** |

`docs/FINETUNE.md:80-81` records why: under FSDP the trainer cannot easily separate the
adapter parameters, so it writes all of them. Two checkpoints at `checkpoints_total_limit: 2`
is already 30 GB for 39 MB of trained weight.

## The rename that fails silently

The trainer writes `context_refiner.0.attn.to_k.lora_A.default.weight`. PEFT reads
`base_model.model.context_refiner.0.attn.to_k.lora_A.weight`. Two differences: the `.default.`
segment carrying the adapter's PEFT name, and the `base_model.model.` prefix.

A loader that finds nothing under its expected keys does not raise. It adds a freshly
initialised adapter and generates from the base model, so the output is ordinary rather than
broken, and the run reads as a model that learned nothing. `extract_lora_adapter.py` counts
both rewrites and exits non-zero on a partial, because a rewrite that hits some keys and not
others is the same failure wearing a smaller mask.

## What must not be published

**Quantised output.** CLAUDE.md's condition 5. NF4 outputs are device evidence. Measured
here, four bits also bought no speed on this card -- 133 s against 131 s -- so there is
nothing to trade.

**Blinded-holdout derivatives.** `coco_person_commercial_val2017` is 523 licence-filtered
COCO person images and is not inspected during development at all. Anything derived from it
inherits that: `6-datasource/coco-ood-eval` is evaluation-only twice over, being both
val2017-derived and generated.

**`weftspun/rf-detr-keypoint-data`.** Its own README says the licence file is wrong: it claims
CC BY 4.0 for the whole set, and **1,823 of 2,346** images carry NC, ND or share-alike terms.
The file names look like a training split and are not one.

**`alfredplpl/anime-with-caption-cc0` images.** Blocklisted for hand quality; the captions are
permitted. An artifact using the captions says so and does not imply the images.

**Anything from a set behind a registration form.** Terms that cannot be read without
accepting them cannot be gated on, so the set is not licence-clean whatever it says after you
accept.

## Naming, worked through

`weftspun/anny-render-corpus` on GitHub sits on `6-datasource`. Its artifacts publish under
the same name, and the dataset card's first line links back to the GitHub repository and
names the side.

Where one source repository produces both a corpus and a weight, they are two Hugging Face
repositories, one dataset and one model, sharing the name and differing in type. A model
repository holding a corpus is the mistake this rule prevents, and it is easy to make because
the run that produced both is one run.

## What is not measured here

Hugging Face upload throughput, LFS behaviour on files above 5 GB, and whether the hub's own
licence detector agrees with a dual `Apache-2.0 OR MIT` pair. The last of those has a known
answer on GitHub -- two `LICENSE-*` files at the root read as "Other" until one is on the
default branch -- and nothing here has checked the hub.
