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

An RFD number has four decimal digits.

The first digit names the organization. This repository uses digit 1. The
fabric manuals use digit 2. `v-sekai/manuals` reserves digit 3 and `fire/manuals`
reserves digit 4. Neither has an RFD yet.

The last three digits are the serial number. A new RFD takes the next unused
serial under its own organization digit. A writer no longer checks another
repository, because another organization cannot reach this digit.

    RFD 1015    this repository, serial 015
    RFD 2015    the fabric manuals, serial 015

Three decimal digits give 1000 serials for each organization. This repository
uses 131 of them.

## Where the organization digit comes from

The digit is a short name for an arc under an IANA Private Enterprise Number.
PEN 66606 is assigned to iFire. RFC 9371 gives the
registration procedure, and the assignment is itself the delegation. No arc
below 66606 is registered with anybody.

That is also the hazard. RFC 9371 section 1.1 says plainly that no one controls
how an assignee uses its PEN. Nothing outside this workspace will stop two of
our own namespaces from minting the same arc. Only a table we keep will.

So one arc under the PEN names a namespace, and no namespace mints a sibling of
another:

    66606.1    documents, one arc for each manual site

The category arc is not decoration. Without it, a manual site and anything else
this PEN ever identifies allocate from one space. A fifth site would take arc
5, and whatever else had picked 5 would already hold it.

No second category is allocated. This document allocates one when something
needs one, under RFD 1070's rule.

66606.1 carries the sites, and the site arc is the organization digit:

    66606.1.1    weftspun
    66606.1.2    v-sekai-fabric
    66606.1.3    v-sekai
    66606.1.4    fire

`v-sekai/manuals` and `fire/manuals` both name a decision by its date rather
than by a serial, so digits 3 and 4 are reserved and hold nothing. A reserved
digit costs one line here. An unreserved one costs what the collision above
cost, which was 113 numbers meaning two documents at once.

The full identifier of an RFD is:

    1.3.6.1.4.1.66606.1.<site>.<number>

RFD 1015 is `urn:oid:1.3.6.1.4.1.66606.1.1.1015`. The last arc is the four
digits the folder name already writes. Its first digit repeats the site arc
above it, and the repetition is worth its cost. The mapping from a document
number to its arc is the identity, so a reader who can read one can read the
other. That is what the decimal rule below was for.

Two rules carry to whatever takes the next category. It keeps a register of
what it allocates, in the way `SERIALS.usda` does. A kind of thing gets an arc of
its own rather than a neighbouring parent number, because `<thing>.1.<id>` and
`<thing>.2.<id>` say which kind they are and `<thing>` beside `<thing+1>` does
not.

## Why the digits are decimal

The first version of this rule made the digits hexadecimal. It shipped. 131
RFDs carried hex numbers for the life of it, and this section withdraws it.

An OID arc is decimal. A hex document number therefore needed a conversion at
each crossing between the folder name and the identifier. Serial 100a was arc
4106, and nothing in the name said so. That put two representations of one
number in service at once, which is the condition the rule above exists to
remove.

Hexadecimal offered 4096 serials to each organization and decimal offers 1000.
This repository uses 131. The ceiling was never the constraint the rule was
written against.

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
cause. RFD 1040 is the first: eighteen packaging gaps, each found by
running the thing rather than by reading the file, and every one of
them reporting either success or a cause that is not the cause. That
knowledge fits nowhere in a README bounded at 40 lines, and putting it
in DETAILS.md would mix a procedure into a measurement.

The test for whether something belongs here: a reader following it in
order should not need to have read either sibling. A skill that only
makes sense after the DETAILS is a section of the DETAILS.

## The serial register

`SERIALS.usda` lists every serial this site has allocated. It carries the live
ones and the deleted ones, because a deleted number stays cited.

It is USD rather than a table, and in Essential Tuple Normal Form: one prim
per tuple, the primary key in the prim name, the remaining columns as typed
attributes on that prim. A row count is the number of children. A packed row
was rejected early, because a value with a space in it splits into two columns
without saying so.

**It held parallel arrays until this revision, one per column, indexed
together.** Two arrays that correspond by position can stop corresponding, and
nothing in the layer says so: `[1, 1, 2]` is a legal `int[]` carrying a
duplicate key, and a reader that walks the columns with `zip` stops at the
shorter one, so a register missing a slug reports one fewer serial and no
error. That failure was gated rather than prevented. Under the row form USD
refuses two siblings of one name, so a duplicate key cannot be authored, and
a missing value belongs to one row rather than shifting every row after it.

Other sites still author the array form, and the readers take both. A reader
that understood only the new shape would compose their registers to nothing,
which reads exactly like a site with no serials.

It holds this site's serials and no other site's. A copy of another site's
rows would be a second record of one fact, and the first copy edited would win
by accident. `pen-66606.usda` composes the sites with sublayers, so the whole
PEN reads as one stage and no site restates another.

The published page holds no copies either. `multiplayer-fabric-manuals`
renders `pages/serials.qmd` from these registers at build time, reading each
site's over HTTPS, so the identifiers exist once and a reader sees what the
registers say rather than what a generator last wrote.

There was a generator, and it wrote that page into the site. It needed a gate
to catch the page drifting from the registers, and that gate went red twice in
a week, correctly both times. The page reading the registers itself removes
the copy rather than watching it, and the generator and its gate are deleted.

A serial is appended once. It is never removed and never reused. A slug
follows its directory, because a retitle renames a document and does not
renumber it. The two look alike in a diff and are not alike. A renumbering
takes serials out of the register, so `scripts/check-rfd-serials.py` fails on
what went missing rather than on what arrived. RFD 1124's gate borrows that
script's reader, so the two gates cannot disagree about which numbers exist.

This entry is the reason the register exists. Renumbering 131 RFDs took 121
directory renames and 295 file rewrites, and nothing in the repository would
have objected if the mapping had been wrong.

## What this rule does not repair

Git history and pull request titles hold two older forms. 67 commit subjects
cite an RFD by its first number. 48 more cite a hex one. Git history does not
change.

`ALIASES.md` held 122 rows mapping the first numbers to hex. It is deleted
rather than extended, because the first form now resolves by a rule instead of
a table. The decimal serial equals the first number in all 122 rows. The
document that opened as 0123 is RFD 1123, and the lookup is "prepend the
organization digit". Hexadecimal
was the detour, and leaving it returned every document to the number it
started with.

A hex number resolves no such way. A reader who finds one in a commit subject
converts it or reads the commit. 48 subjects carry that cost, and it is the
price of deleting the table rather than adding a third column to it.
