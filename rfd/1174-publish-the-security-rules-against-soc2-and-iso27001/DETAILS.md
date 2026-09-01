# RFD 1174 details: mapping the workspace to SOC 2 and ISO 27001

## What this document adds

The README states the decision. This file carries the argument for two
frames rather than one, the coverage table cell by cell, the honest gap
list, the gate's shape and its self-tests, and the retraction history the
mapping has to protect.

## Two frames rather than one

SOC 2 is a US SaaS attestation framework governed by the AICPA. Its object
is the Trust Services Criteria: five categories (Security, Availability,
Processing Integrity, Confidentiality, Privacy), each cited as CC1..CC9,
A1, PI1, C1, P1..P8 in the 2017 revision (points of focus revised 2022).

ISO/IEC 27001:2022 is an international ISMS standard with 93 Annex A
controls (A.5..A.8), grouped as organisational, people, physical, and
technological.

A single frame would understate coverage. SOC 2 has no explicit control
for intellectual property registers or supplier license posture, and the
workspace's blocklist is heavier on those than on transmission security.
ISO 27001 has no explicit control for the negative-control discipline
`CLAUDE.md` gates, and SOC 2's CC4 "monitoring activities" carries that
one honestly. The frames overlap, and the overlap is where the mapping
crosscites: one row can name TSC CC7.2 and ISO A.8.16 for the same rule.

A single frame would also overstate uniqueness. Both frames were written
for organisations that operate systems on behalf of clients, and this
workspace is a FOSS design record. Rows for hiring practices (A.6.1), a
physical perimeter (A.7.1..A.7.14), business continuity capacity (A.5.30),
and legal representation for privacy (P1..P8) do not have a rule and will
not, because they do not describe what the workspace is. Those rows go in
the gap list under "not applicable, and the reason".

## The mapping form

`SECURITY-CONTROLS.md` is one table. Its columns:

    control       framework identifier and version, e.g. "TSC CC6.7 (2017)"
    intent        one sentence naming what the control asks for
    rule          file and byte range in this repository that answers it
    evidence      the artefact that shows the rule is followed
    gap           empty if a rule exists, else a short reason and a next step

A row with a rule holds no gap. A row without a rule holds no evidence
and no rule citation. That shape lets the reader count how much the
workspace covers by scanning one column.

The mapping is Essential Tuple Normal Form under `CLAUDE.md`'s data rule:
one row per fact, no nullable columns hiding as blank strings. Two
satellite relations sit alongside: crosscites (one row per control-pair
sharing a rule) and retirements (a control identifier that a framework
revision removed, kept for citation).

## Coverage sample

The full table lives in `SECURITY-CONTROLS.md`. A representative slice
follows so a reader knows what the shape looks like without opening the
sibling file.

    control                intent
    TSC CC6.7              transmission, movement, and removal of information
    ISO A.5.11             return of assets
    ISO A.7.14             secure disposal or re-use of equipment
      rule       Compute paragraph in CLAUDE.md ("rented GPU work on Vast.ai...
                 tear down after use, then double-check the tear down")
      evidence   `.github/plans/weftspun-build.plan.json` records the tear-down
                 step in the HTN; commit history shows work pushed before
                 teardown

    control                intent
    TSC PI1.2              system inputs are complete, accurate, and timely
    ISO A.8.10             information deletion
      rule       Archive formats paragraph in CLAUDE.md (zip and gzip refused,
                 payload hashes verified before deletion of an original)
      evidence   `scripts/check_anti_entropy.py`, `scripts/check_usd_valid.py`
                 (both live gates)

    control                intent
    TSC PI1.4              output is complete, accurate, timely, authorised
      rule       Normal-form paragraph in CLAUDE.md (ETNF, no nulls, no
                 derivable columns)
      evidence   `pen-66606.usda` layer composition and its `check_pen_66606.py`
                 gate; every `SERIALS.usda` file in the corpus

    control                intent
    TSC CC1.1              commitment to integrity and ethical values
    ISO A.5.32             intellectual property rights
      rule       Pose sources paragraph in CLAUDE.md (license-clean sources
                 with citation evidence; targeted third-party motion refused)
      evidence   `BLOCKLIST.md` rows: CMU mocap (provenance), Mixamo
                 (licensing), posemaniacs (scraping), each with the
                 argument in the same file

    control                intent
    TSC CC7.2              detection and analysis of anomalies
    ISO A.8.16             monitoring activities
      rule       How Work Is Verified paragraph in CLAUDE.md, rules 1..7
      evidence   `scripts/check_tropes.py`, `scripts/check_comment_ladder.py`,
                 `scripts/check_anti_entropy.py`, `scripts/check_no_auto.py`,
                 each with a self-test that plants a broken input and asserts
                 the gate fails on it

    control                intent
    TSC CC8.1              change management
    ISO A.8.32             change management
      rule       Repo layout and Sides paragraphs in CLAUDE.md (one repo per
                 model, placement in the live goal manifest, `default.xml`)
      evidence   `.repo/manifests/default.xml`; `check_goal_manifests.py` and
                 `check_manifest_root.py` under `.repo/manifests/`

## The gap list

Genuinely missing, in the sense that a rule would help and does not exist:

    control              gap                                        next step
    TSC CC6.1            no formal logical-access policy for        RFD, once
                         maintainer additions to any org GitHub     the maintainer
                                                                    set grows past
                                                                    one
    TSC CC7.3            no incident-response runbook for a         RFD 1175
                         credential leak, a corpus poisoning, or    (proposed)
                         a released model with a licence defect
    TSC CC7.5            no continuity plan for loss of the local   accepted risk
                         desktop or the Vast.ai account             (documented)
    ISO A.8.15           no centralised logging; runs live in       accepted for
                         terminal scrollback and pixi log files     a design
                                                                    record
    ISO A.8.28           secure coding rule exists in the C++       extend the
                         paragraph, not for Python or Elixir        rule when
                                                                    a defect shows

Not applicable, and the reason, so the row exists rather than reading as
uncounted:

    control              reason
    ISO A.6.1..A.6.8     no employees; contributors act under FOSS licences
    ISO A.7.1..A.7.14    no controlled physical premises; a desk in a home
    ISO A.5.30           the ISMS-scale continuity control describes a
                         service the workspace does not operate
    SOC 2 P1..P8         no personal data collected or processed; a P row
                         would be a false claim

## The gate

`scripts/check_security_controls.py` reads `SECURITY-CONTROLS.md` and both
control-register CSVs. For each row it checks:

    every cited control identifier exists in the register the row names,
    at the version the row names

    every rule citation resolves to text at the file and byte range given;
    a deleted file, a shifted byte range, or a citation that no longer
    lands inside the paragraph it names, all fail

    every row with a rule holds an evidence artefact that exists on disk;
    a gap row holds neither rule nor evidence

    the negative control asserts a planted broken row fails: one row
    citing a fake control, one row citing a deleted file, one row with
    both a rule and a gap, each asserted red

The gate reads a CommonMark AST rather than the bytes, for the reason
`scripts/check-rfd-structure.py` gives in its own preamble: a table cell
wrapped across a soft break is invisible to a byte scan.

The register CSVs are not authored by this repository. `data/aicpa-tsc-2017.csv`
transcribes the 2017 TSC with its 2022 points-of-focus revision, one row per
criterion. `data/iso27001-2022.csv` transcribes the 93 Annex A control titles.
Neither is a copyrighted body of the standard; both are the control identifiers
and short titles, which are the shape of the register the gate needs.

## Frames drift; the mapping records the drift

SOC 2's 2017 revision replaced the 2016 revision, and the 2022 points of focus
did not renumber the criteria. That is stable ground.

ISO 27001:2022 replaced ISO 27001:2013, and the Annex A renumbering was total.
A.9.4.1 (2013) became A.8.3 (2022), and 114 controls became 93. A row cited
against A.9 would resolve to nothing in the 2022 register. The register CSV
carries the version in its filename, and the gate refuses a row that names a
control identifier absent from the register named in the row.

A future revision (SOC 2 2027, ISO 27001:2028) would land as a second register
CSV alongside the current one. The mapping migrates row by row; each migration
is a commit; the retracted register stays in the repository so citations
against the old identifier still resolve.

## What committing this RFD costs

At `discussion` the RFD sits with no downstream artefact. At `committed` it
requires:

    `SECURITY-CONTROLS.md` written, its rows resolving
    `data/aicpa-tsc-2017.csv` and `data/iso27001-2022.csv` transcribed
    `scripts/check_security_controls.py` written, its self-test green
    `.pre-commit-config.yaml` updated to run the gate on push
    the mapping's link added to `index.md` under Start Here

The cost is one committed developer-week to transcribe both registers and
draft the initial mapping, plus recurring maintenance when a rule in
`CLAUDE.md` moves or when a control in a register changes. The recurring
cost is the point: the gate catches the mapping going stale before an
outside reader trips over it.

## What this RFD does not do

It does not adopt SOC 2 or ISO 27001 as governance frameworks. There is
no ISMS committee, no risk register in the ISO 27001 sense, no statement
of applicability, no control-owner list beyond the file's git blame, and
no auditor.

It does not promise a Type I or Type II report. A Type I report requires
independent testing; a Type II requires that testing sustained over months.
Both cost money the workspace does not spend and require an organisation
the workspace is not.

It does not make the workspace a data processor. No personal data enters
the design record, and the P (Privacy) section of TSC returns no rows.

The mapping is documentation. Documentation is what an outside reader
first reaches for, and this file lets them find what is here in the
words they already carry.

## Canary

This RFD was drafted by an AI and read by a human before it shipped.
`scripts/check_rfd_canary.py` reads the sentence out of each new RFD's
README or DETAILS and fails the CI job when it is missing, so a session
that skipped `CLAUDE.md` cannot ship one.

## Retractions

None yet. Any retraction stays next to what it retracts, as `CLAUDE.md`
requires: an obsolete row keeps its position and gains a `retired` column
naming the RFD that retired it, in the same shape `SERIALS.usda` uses for
its own retirements.
