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

## Named in RFD 1084 and nowhere else

| model id                 | goal         | what was found |
| ------------------------ | ------------ | -------------- |
| multimodal_semantic_ids  | mesh-latents | nothing        |
| residual_fsq_recommender | mesh-latents | nothing        |
| unified_modal_embedder   | mesh-latents | nothing        |

Each was searched for across the RFD corpus: no directory, no README, no
ALIASES.md row, and no citation. RFD 1084's own table is the only file in this
repository that names any of the three.

The search is bounded and the bound is stated, because an absence measured over
one tree is not an absence. It covers this repository. It does not cover
`src/library/aiModelsCatalog.js`, which is the studio's catalog and the source
RFD 1010 drew from, and it does not cover the mesh-latents checkouts pinned at
`refs/tags/mesh-latents/v0.1.0-dev.1`. A grep across the whole workspace was
started for this and did not finish inside two minutes, so it is not reported as
a result. What is reported is the smaller claim the search supports.

So these three are not excluded. Their status is unknown, and it was written
down as an exclusion, which is the failure mode this RFD exists to separate. The
three carry the `mesh-latents` goal in RFD 1084's table, and a goal comes from
`default.xml`, so something placed them once.

Two ways to close it, and either is cheap: read the catalog and confirm the ids
are live entries, or delete the rows and record that RFD 1084 carried three ids
nothing supports. Neither has been done.

## What this leaves for RFD 1084

RFD 1084 keeps every convertible model, the measured rank, and the census that
orders the rest. It cites this document instead of carrying a second table, so
one ranking and one exclusion list do not have to agree by hand.
