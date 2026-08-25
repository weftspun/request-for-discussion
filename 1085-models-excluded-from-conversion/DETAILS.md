# RFD 1085 details: the three kinds of exclusion

Ten model ids were carried under one heading in RFD 1084, and the heading was
`blocklisted`. Reading each row back against what excludes it splits the ten
three ways, and only the first three rows are what the word says.

## Blocklisted by the agreements

CLAUDE.md's blocklist names all three, and `BLOCKLIST.md` carries the argument
under each. This table restates neither, it points at them.

| model id                  | goal         | entry                        | RFD      |
| ------------------------- | ------------ | ---------------------------- | -------- |
| qwen_q4_k_m_image_edit    | -            | Qwen-Image-Edit (2509/2511)  | RFD 102b |
| p3sam_mesh_segmentation   | mesh-latents | P3-SAM / Hunyuan3D-Part      | RFD 1029 |
| krea2_turbo_text_to_image | -            | Krea 2 / krea2-turbo         | RFD 102a |

Qwen-Image-Edit is 20.4B and runs here only quantised, and quantised it
corrupts. P3-SAM carries a territory-restricted licence that excludes the EU,
the UK and South Korea. Krea 2 is revenue-gated and the restriction propagates.

The identifier `qwen_q4_k_m_image_edit` names the Q4_K_M build directly, so the
catalog identifier and the reason for exclusion are the same fact. That is the
one row where the id alone is the evidence.

Ranking these would send somebody to work the agreements have already closed. A
blocklist row reopens when the agreements change, and nothing in the conversion
work can reopen it.

## Abandoned with the world-building scope

These four are not blocklisted anywhere. Each has an RFD in state `abandoned`,
and each names the same cause: RFD 1040 turned the roadmap toward character
concepts.

| model id                     | RFD      | scope it left      |
| ---------------------------- | -------- | ------------------ |
| weftspun_image_to_world      | RFD 1031 | explorable worlds  |
| lingbot_map_environment_scan | RFD 1032 | environment scan   |
| worldmirror2_reconstruct     | RFD 1033 | multi-photo splat  |
| triposplat_image_to_splat    | RFD 1034 | single-photo splat |

RFD 1031 is the caller and RFD 1033 and RFD 1034 are two of its halves, so the
four are one pivot rather than four decisions.

Calling them blocklisted was wrong in a direction that costs something. A
blocklisted model stays out whatever the roadmap does. An abandoned one returns
with its scope, and RFD 1031 says so in its own words: package this entry again
only if the world-building scope returns. A reader who saw `blocklisted` would
not go looking for that sentence.

None of the four is licence-dirty, and none was measured and rejected. They are
out of scope, which is the cheapest exclusion to reverse.

## Named in RFD 1084 and nowhere else, RETRACTED

**The three are placed, and this section said they were not.** It is kept rather
than rewritten, because the way it was wrong is the more useful half.

| model id                 | path                                | revision                              |
| ------------------------ | ----------------------------------- | ------------------------------------- |
| multimodal_semantic_ids  | 3-interactor/multimodal-semantic-ids | refs/tags/mesh-latents/v0.1.0-dev.1  |
| residual_fsq_recommender | 3-interactor/residual-fsq-recommender | refs/tags/mesh-latents/v0.1.0-dev.1 |
| unified_modal_embedder   | 3-interactor/unified-modal-embedder | refs/tags/mesh-latents/v0.1.0-dev.1   |

`default.xml` carries all three as `<project>` entries, pinned to the
mesh-latents tag, and all three are checked out at 3-interactor. Placement is
what a live goal manifest says, and it says these are placed.

What the first version searched was the RFD corpus: no directory, no README, no
ALIASES.md row, no citation. That search was accurate and its bound was stated.
The bound was then read as a result anyway, which is the failure. An absence
measured over one tree was written up under a heading that claimed the workspace,
and the file that would have settled it in one grep is the same `default.xml`
this document already cites for the `goal` column of RFD 1084's table.

So the correct finding is smaller and worse. These three are not unfound, and
they are not excluded either. They are placed projects on 3-interactor that RFD
1084 listed as blocklisted, and nothing in this repository records a reason. The
RFD corpus still has no entry for any of them, which is now a documentation gap
rather than evidence of absence.

Two ways to close it. Read the three checkouts and record what they are, or
delete the rows from RFD 1084 and say the blocklisted mark was never supported.
The first is the one that leaves a reader better off.

## What this leaves for RFD 1084

RFD 1084 keeps every convertible model, the measured rank, and the census that
orders the rest. It cites this document instead of carrying a second table, so
one ranking and one exclusion list do not have to agree by hand.
