---
title: "RFD 2126: Two see-through interactors, and the check that keeps the A/B one question"
rfd: "2126"
state: discussion
scope: the see-through interactor pair, and what holds them to the same command
---

## Problem

See-through decomposes one anime illustration into semantic layers. The reference
implementation is PyTorch; a port to ggml exists for machines where CUDA does not. Both are
worth running, and the interesting question is which is faster and whether they agree.

A comparison between two implementations is only a comparison if both answer the same question.
Nothing enforces that. Two programs drift apart in the settings they accept, the errors they
refuse, and the shape of what they return, and every one of those differences turns a timing
comparison into a comparison of two different jobs. RFD 2123 makes this argument for a second
WebTransport implementation and gets the benefit from the disagreement; the same benefit needs
the same discipline here.

## Decision

**Two interactors, and neither takes the unqualified name.**
`interactor-see-through-cpp` and `interactor-see-through-python`, for the reason RFD 2123 takes
the unqualified names from the gateway pair: a name that says which of two it is beats a name
that implies the other is a variant.

**They share the wire and nothing else.** The C++ half reaches the bus through the harness's
dlsym table over the iceoryx2 C ABI. The Python half reaches it through iceoryx2's own Python
binding. Each parses the command itself and encodes its own reply. An implementation that
shared a parser could not disagree with the other about a command, and disagreeing is the job.

**A check reads one half's constants out of the other's source.** The production settings are
two numbers, and if the pair ever disagree about them the comparison is void.
`proof/test_agreement.py` reads `ST_MIN_RES`, `ST_MIN_STEPS` and the weight path out of the C++
header and fails when they differ from the Python values. It prints how many comparisons it
made, because a check that found nothing because the other half was not checked out reads
exactly like agreement.

**A run below the production settings is refused, not served.** 1280 pixels and 30 steps. Low
step counts produce degenerate layers that look plausible in a viewer and say nothing about
quality, and MADR 0009 in the see-through project records a 512-pixel artefact that vanished at
full settings. An interactor that answered a cheap request with a cheap result would invite
exactly that comparison. The refusal names the number it saw, because a refusal that does not is
one the caller retries unchanged.

**The engine is a seam, and the absent one fails.** It does not return a plausible layer set.
This pipeline is judged by compositing its layers and looking at them, so a fabricated result is
not caught by checking that a result arrived, and a missing model must stay distinguishable from
a bad one.

## What this does not decide

**Which is faster.** Nothing here has measured a decomposition through either interactor. RFD
0129 holds the budgets and they are empty on purpose.

## References

- RFD 2123: the same argument for a second WebTransport implementation
- See-through: <https://doi.org/10.1145/3799902.3811209>
- Upstream implementation: <https://github.com/shitagaki-lab/see-through>, Apache-2.0
