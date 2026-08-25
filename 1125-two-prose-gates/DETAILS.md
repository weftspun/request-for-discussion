# RFD 1125 details: what already exists, and the three detectors that cannot fire

Every section below names its gate in an HTML comment under its heading. That
mark is the mechanism this RFD adds, so this file is also its first example.

## Why the rule was split

<!-- gate: tropes -->

The blanket rule was not wrong when it was written. It was written for one kind
of document, and the repository then grew a second kind without anyone noticing
that the rule had stopped fitting.

ASD-STE100 exists so a maintenance technician reading in their second language
can take a procedure and act on it correctly the first time. Every constraint it
carries serves that: bounded sentences, one approved term per referent, no
contractions, no ambiguity about what a pronoun points at. Applied to a schema
table or an install step, those constraints are exactly right.

Applied to an argument they remove what makes it an argument. A decision
persuades through how its reasons sit against each other, and a controlled
vocabulary flattens that into a list of assertions. The reader loses the ability
to tell a load-bearing claim from an incidental one.

The failure an essay actually has is one ASD-STE100 says nothing about. An essay
fails by reading as though nobody wrote it. The tropes.fyi catalog names that
failure, which is why a second gate buys something instead of duplicating the
first.

The per-section mark follows from a fact about this repository rather than a
preference. A `DETAILS.md` is where a measurement lands, and it is also where
the reasoning that motivates the measurement lands. Those are two kinds of
writing in one file, and any file-level rule has to be wrong about one of them.

## What already exists

<!-- gate: ste100 -->

This RFD proposes less than it first appears. The `tropes-removal-model` project
holds most of the parts:

| part                       | state                                                    |
| -------------------------- | -------------------------------------------------------- |
| `seeds/trope.parquet`      | 28 ASD-STE100 violation categories                       |
| `seeds/ai_trope.parquet`   | 20 AI-writing tropes, seeded from tropes.fyi             |
| `runtime/prose_nodes.py`   | CommonMark prose extraction, so a gate reads no syntax   |
| `gate.py`                  | the ASD-STE100 gate; it runs the STE table only          |
| a runner for the AI tropes | **absent**                                               |

`scripts/seed_ai_tropes.py` reached the same conclusion as this RFD before this
RFD did. Its own docstring states that ASD-STE100 "gates the wrong things" in an
essay. Two facts remain to settle, and this RFD settles them.

`gate.py` does not import `prose_nodes`, and nothing reads `ai_trope.parquet`.
The catalog and the parser exist and are not connected.

`runtime/prose_nodes.py` imports `markdown_it`. `pixi.toml` does not declare it.
The RFD gates pin `markdown-it-py==3.0.0`, so the two projects must agree on a
version once both depend on it.

## The measurement

<!-- gate: ste100 -->

`scripts/measure_ai_tropes.py` in `tropes-removal-model` reads
`seeds/ai_trope.parquet` and `runtime/prose_nodes.py`. It owns no patterns and
no parser, because a second copy of either would drift from the first.

It reads all 119 RFD `README.md` files. The counts are exact: the population is
fixed and the script reads every member, which is what CLAUDE.md rule 5 asks for.

The table holds 20 tropes: 15 regex, 3 classifier, 2 manual. Three of the 15
find anything:

| trope               | documents | share | hits |
| ------------------- | --------- | ----- | ---- |
| Compulsive Counting | 6         | 5%    | 7    |
| Overused Adverb     | 2         | 2%    | 2    |
| Em-Dash Addiction   | 2         | 2%    | 2    |

## Three detectors cannot fire

<!-- gate: ste100 -->

Twelve detectors report zero. Nine of those zeros are real. Three are not.

`--audit` feeds each pattern its own recorded `example_phrase`, passes it through
`prose_nodes`, and asserts the pattern still matches. A detector that cannot
match its own example is BROKEN, and its zero on a corpus means nothing.

| detector              | fault                                                |
| --------------------- | ---------------------------------------------------- |
| Bolded Lead Clause    | matches `**...**`; `prose_nodes` removes the markers |
| Where/What/Why Header | matches `#{1,6}`; `prose_nodes` removes the hashes   |
| Negative Parallelism  | spells `it'?s`; its own example says "it is"         |

The first two are one fault twice. Both patterns were written against raw
markdown, and the extractor hands over the text a reader sees. Measured on one
file: `Bolded Lead Clause` finds 5 in the source and 0 after extraction.

Each repair is small. Move the two formatting rules to run before extraction, or
rewrite them against the extracted text. Add `it is` to the third alternation.

A zero from a broken detector reads exactly like a clean corpus. That is the
failure CLAUDE.md rule 3 names, and it is why `--audit` runs first.

## Every hit is a false positive

<!-- gate: ste100 -->

Run `--inspect` to see each hit in context. The inspection changes the result,
so the count alone is not the measurement.

| trope               | what the hits are                                      |
| ------------------- | ------------------------------------------------------ |
| Compulsive Counting | exact counts of items the document then enumerates     |
| Overused Adverb     | "silently", describing a check that skipped in silence |
| Em-Dash Addiction   | two parenthetical dashes across 119 documents          |

`seed_ai_tropes.py` predicted this. Its docstring records that a regex is "a
screen, not a verdict", and that Compulsive Counting "fires on the phrase 'three
things', which is sometimes just three things". The corpus agrees: all seven hits
count things the document goes on to list.

No hit in the corpus is a true positive. Against the mechanical subset, the
corpus is clean, and every firing rule needs narrowing before it gates anything.

## What no mechanical detector reaches

<!-- gate: ste100 -->

tropes.fyi lists 49 tropes. The table seeds 20, and records that limit per row in
its `coverage` column rather than in a README.

Five of the 20 have no regex. `Invented Concept Label`, `Premise Stacking` and
`Enumeration As Prose` need the classifier. `Circular Fractal` and
`Symmetric Paragraph Length` have no automatic detector at all.

The ASD-STE100 half splits the same way: about 18 mechanical rules as regular
expressions, about 8 semantic rules through a SetFit classifier, and 2 more
through a whole-document pass in `runtime/cross_sentence.py`. An essay gate needs
the same second half, and this RFD does not build it.

## The conflict this RFD resolves

<!-- gate: tropes -->

`seed_ai_tropes.py` already assigns work to each table, and it puts READMEs on
the ASD-STE100 side:

    trope.parquet      ASD-STE100        READMEs, procedures, reference, rules
    ai_trope.parquet   AI-writing tells  essays, design notes, logbook entries

This RFD moves READMEs to the other column. The disagreement belongs in the open
rather than under a silent overwrite.

That assignment is defensible on its own terms. A README in most repositories is
reference material, and reference material belongs under a controlled language.
It is wrong here because an RFD README is not that kind of README. RFD 1000 asks
it to state a problem and a decision in forty lines, which makes it the most
compressed argument in the repository rather than the most procedural document.

The measurement decides it rather than merely permitting it. Both tables were run
over the same 119 READMEs, through the same extractor:

| table                    | documents flagged | hits  |
| ------------------------ | ----------------- | ----- |
| `ai_trope.parquet`       | 10 of 119         | 11    |
| `trope.parquet` patterns | 119 of 119        | 4,397 |

Three orders of magnitude apart, on identical input. `Three+ Nouns in a Row`
alone flags every document in the corpus. `Contraction Used` flags roughly two
thirds of them, and `Semicolon Used` about a quarter.

Neither number is a verdict, and the trope side is not flattered by the
comparison: its 11 hits are all false positives, as the section above records.
These are weak-label screens from `scripts/seed_labels.py` rather than the
shipped classifier, which applies thresholds these patterns do not. Read them as
direction and magnitude, not as counts of real defects.

The direction is the whole argument. A gate that fails 119 documents out of 119
is not holding a standard, it is producing noise, and people stop running it.
`prose_nodes.py` was written to avoid the same outcome, which arrives here
through the choice of table rather than through the choice of parser.

## How to re-run

<!-- gate: ste100 -->

```
cd .tropes_removal_model
python3 scripts/measure_ai_tropes.py --audit    # check each detector can fire
python3 scripts/measure_ai_tropes.py            # the AI-trope table
python3 scripts/measure_ai_tropes.py --inspect  # every hit, in context
python3 scripts/measure_ai_tropes.py --compare  # both tables, same extractor
```

`--audit` exits non-zero while any detector is broken. Run it before you trust a
zero from the other modes.

The default path is `../.request_for_discussion`, which holds when both projects
sit at the workspace root. `default.xml` places them there.
