# RFD 1000 details: numbering

## The problem this rule answers

Two repositories allocated RFD numbers from what each treated as a private
space. The spaces were the same space. This repository held 116 RFDs numbered
0000 to 0123. `v-sekai-fabric/multiplayer-fabric-manuals` held 129 RFDs
numbered 0000 to 0132. 113 numbers named a document in both places.

The old rule in this file did not cause the collision on its own. It said
nothing about numbering at all. The root README said the repository used "one
shared numbering space", and it meant shared across weftspun projects. The
fabric repository told its writers to check its own listing and, in its own
words, "not any other repo's own numbering". Each rule was correct inside its
repository. Together they guaranteed the collision.

## The rule

An RFD number has four hexadecimal digits, in lower case.

The first digit names the organization. This repository uses digit 1. The
fabric manuals use digit 2. `v-sekai/manuals` reserves digit 3 and has no RFDs
yet.

The last three digits are the serial number. A new RFD takes the next unused
serial under its own organization digit. A writer no longer checks another
repository, because another organization cannot reach this digit.

    RFD 1015    this repository, serial 0x015
    RFD 2015    the fabric manuals, serial 0x015

Three hexadecimal digits give 4096 serials for each organization. This
repository uses 116 of them.

## Where the organization digit comes from

The digit is a short name for an arc under an IANA Private Enterprise Number.
The full identifier is an object identifier:

    1.3.6.1.4.1.<PEN>.<organization>.<serial>

One owner holds all three organizations, so one PEN carries three sub-arcs.
The PEN is not assigned yet. Until it is, the number is 32473. RFC 5612
reserves 32473 for use in examples, so IANA cannot assign it to a real
organization. A provisional identifier therefore cannot collide with a real
one later.

When IANA assigns the real number, only the table below changes. The document
numbers do not change.

    32473.1    weftspun
    32473.2    v-sekai-fabric
    32473.3    v-sekai

## A third sibling: SKILL.md

The README states the problem and the decision. DETAILS.md holds the
measurement. Neither says what to do, in what order, and both are the
wrong shape for it: a procedure is not a decision, and it is not a
result either.

So an RFD may carry a `SKILL.md`, in the same folder, with the
frontmatter a skill takes:

    ---
    name: <kebab-case, matching the RFD folder's subject>
    description: <when to reach for it, not what it contains>
    ---

It holds the order to do things in and the errors that name the wrong
cause. RFD 1028 is the first: eighteen packaging gaps, each found by
running the thing rather than by reading the file, and every one of
them reporting either success or a cause that is not the cause. That
knowledge fits nowhere in a README bounded at 40 lines, and putting it
in DETAILS.md would mix a procedure into a measurement.

The test for whether something belongs here: a reader following it in
order should not need to have read either sibling. A skill that only
makes sense after the DETAILS is a section of the DETAILS.

## What this rule does not repair

Git history and pull request titles hold the old numbers. 66 commit subjects
in this repository cite an RFD by its decimal number. Git history does not
change. `ALIASES.md` maps every old number to its new one. It is a lookup and
not a repair.
