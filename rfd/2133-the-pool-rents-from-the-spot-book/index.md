---
rfd: 2133
title: "RFD 2133: The pool rents from the spot book, gated on requirements first"
state: "discussion"
feature: "where pool generation runs, and how a card is chosen"
scope: "the gacha demo pool activity; scratchpad tooling pending a home"
---

Pool generation wants days of GPU the desk 3090 should not give up:
that card is the interactive seat, and RFD 1163 already keeps it for
the loops. Rented RTX 4090s carry the batch instead, chosen from the
vast.ai book with requirements applied before price -- CUDA 12.8 or
newer, 100 GB of disk, 32 GB of RAM, 200 Mbit/s down -- because the
cheap listings that fail those gates convert their discount into paid
idle: a 52 GB disk cannot hold the model set, and over a starved link
the two-hour model pull is paid idle time.

Measured on 2026-08-30 and recorded in DETAILS.md: the qualified
on-demand book floors near 21 cents with a median near 39; qualified
interruptible floors at 7.3 cents globally and 16 within US/CA, so the
latency gate costs about two-to-one at the floor and is a per-job
choice, not a standing one. Sub-floor outliers lived minutes in every
observation, which is why catching one is a watcher's job and not a
person's. Pool work checkpoints per seed, so the interruptible tier's
failure mode costs one pull.

The RunPod discipline transfers whole: push results when produced,
destroy the instance after use, double-check the destruction. The API
key stays in the user environment, sourced from the password manager,
absent from repositories and transcripts. The first rental under this
rule is contract 49287440, a Texas host at 21.63 cents per hour whose
$46 of credit covers the pool activity roughly four times over.
