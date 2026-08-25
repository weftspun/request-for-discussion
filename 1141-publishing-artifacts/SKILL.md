---
name: publishing-artifacts
description: Publish a corpus or a trained weight to Hugging Face with a CITATION.cff and a name that reaches back to its code. Use when a run produces something worth keeping, when a checkpoint is far larger than what it trained, or when deciding whether an artifact may be published at all.
---

# Publishing an artifact

RFD 1141 says where artifacts go. This is the order to do it in.

Code goes to GitHub, artifacts go to Hugging Face, and each names the other. An artifact
nobody can trace back to the code that made it is a file, not a result.

## Decide first whether it may be published

Four things stop publication, and they are checked before anything is uploaded:

- **Quantised output.** CLAUDE.md's generated-synthetic condition 5 keeps quantised weights
  out of a corpus. An NF4 run is device evidence and never corpus data.
- **Anything derived from the blinded holdout.** `coco_person_commercial_val2017` and every
  set built from it inherit its status. `6-datasource/coco-ood-eval` is evaluation-only
  twice over, being both val2017-derived and generated.
- **Licence-dirty sources.** The bar is commercial use *and* derivatives. A set behind a
  registration form is not licence-clean, because terms that cannot be read without
  accepting them cannot be gated on.
- **Someone else's weights wearing our name.** See the size check below.

## Name it after the code, and name the side

The artifact repository takes the **same name as the source repository** it came from, so
`weftspun/anny-render-corpus` on GitHub publishes to a Hugging Face repository of the same
name. A different name means a reader holding one cannot find the other.

The README's first section names the **side of the hexagon** the source repository sits on
and links it. Sides are `1-transport`, `2-contract`, `3-interactor`, `4-entities`,
`5-repository`, `6-datasource` and `7-service`, and the live goal manifest decides which.
A corpus comes from `6-datasource`; a definition other repositories agree on comes from
`2-contract`; a model comes from `3-interactor`.

Dataset repositories hold corpora. Model repositories hold weights. Do not put a corpus in a
model repository because it happened to be produced by one.

## `CITATION.cff` is required, and it is the whole point

No artifact is published without one. It carries, at minimum:

- `title`, matching the repository name rather than describing it;
- `license`, ours;
- `references`, one entry per source the artifact derives from, each with **its own** licence
  and URL.

The references are what condition 1 actually asks for. An adapter trained on a corpus
rendered from a rig cites three things: the base model, the rig, and the corpus. Writing only
our own licence claims the derived work and says nothing about what it was derived from,
which is the failure this file exists to prevent.

Where a number appears in the card, it appears as measured. "Improves camera control" is a
claim; "azimuth 90 moved from 97.6 degrees wrong to 13.3" is a measurement, and the second
one tells a reader whether to bother.

## Weights: publish the adapter, not the checkpoint

A trainer that saves under FSDP writes the **whole model** every time, base weights included.
Measured here: a checkpoint is **14.8 GiB** and the tensors that were actually trained are
**19.52 MiB**, 304 of 886. Publishing the checkpoint ships Apache-2.0 base weights as though
they were ours, at 776 times the size, with no way to tell which tensors changed.

So extract first. Two things break quietly and both are asserted rather than hoped for:

- **The tensor count.** Rank 8 over `to_k`, `to_q`, `to_v`, `to_out.0` gives 304. A different
  number means different target modules or a different rank, and the card must say so.
- **The key names.** The trainer writes `...to_q.lora_A.default.weight`; PEFT reads
  `base_model.model....to_q.lora_A.weight`. A loader that finds nothing under its expected
  keys **adds a fresh adapter and generates from the base model**. Nothing raises. The output
  looks like a model that learned nothing rather than one that was never loaded, so the
  rewrite counts what it matched and fails on a partial.

Safetensors, always. `adapter_config.json` records the real `lora_alpha`, which in this
trainer always equals the rank because `train.py:267` sets it and ignores the config.

## Corpora: parquet, zstd, and the manifest beside it

Bulk storage is **ZStandard parquet**. Zip and gzip are both refused. Compress and verify
payload hashes before deleting an original.

Split hygiene travels with the data. If a corpus has train and validation parts, the split is
assigned at identity level and stated in the card, so a consumer cannot leak one into the
other by resampling.

## Publishing, and checking it landed

Create the repository, upload, then **read it back**. A push that reported success and a
repository that serves the files are different claims, and the second is the one that matters.
Confirm the visibility is what was intended, that the `CITATION.cff` is present at the root,
and that the size on the hub is the size that was uploaded.

Then link it from the source repository's README, so the two are reachable in both
directions rather than one.
