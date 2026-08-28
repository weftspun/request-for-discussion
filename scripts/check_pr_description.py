"""Gate: a pull request description explains itself to someone who was not there.

A reference is not an explanation. "RFD 1137 steps 9 and 10." names a decision without
saying what it decided, and a reader who has not opened that document learns nothing.

Structure only. `--self-test` prints the detection floor.

Usage:
    python check_pr_description.py <pr-number> [--repo owner/name]
    python check_pr_description.py --file body.md
    python check_pr_description.py --self-test
"""

import json
import re
import subprocess
import sys

CITATION = re.compile(
    r"""(RFD\s*\d{3,4}
        |PITFALLS\s*\#?\s*\d+
        |\brules?\s+\d+
        |\bsteps?\s+\d+(\s*(and|,|-|through)\s*\d+)*
        |\#\d+)""",
    re.X | re.I)

WHY_HEADING = re.compile(r"^\s{0,3}#+\s*(why|problem|context|motivation|background)\b", re.I)
HEADING = re.compile(r"^\s{0,3}#+\s+(.*)$")
MIN_OPENING_WORDS = 5
MIN_SUBJECT_WORDS = 8


def strip_code(text):
    """Fenced blocks are not prose. An inline span is a word: it is often the subject."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", "CODE", text)


def prose_lines(text):
    return [ln for ln in strip_code(text).splitlines() if not HEADING.match(ln)]


def sentences(text):
    out = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = " ".join(chunk.split())
        if not chunk:
            continue
        out.extend(s.strip() for s in re.split(r"(?<=[.!?])\s+", chunk) if s.strip())
    return out


def bare_words(sentence):
    """The sentence with every citation removed, as a word count."""
    return len([w for w in CITATION.sub(" ", sentence).split() if re.search(r"\w", w)])


def first_prose_sentence(body):
    got = sentences("\n".join(prose_lines(body)))
    return got[0] if got else ""


def cited_documents(body):
    return sorted({" ".join(m.group(0).split()).lower()
                   for m in CITATION.finditer(strip_code(body))
                   if re.match(r"RFD", m.group(0), re.I)})


def headings(body):
    return [m.group(1).strip() for m in
            (HEADING.match(ln) for ln in strip_code(body).splitlines()) if m]


def check_opening(body):
    """The first prose sentence must say something once its references are removed."""
    first = first_prose_sentence(body)
    if not first:
        return False, "no prose before the first heading"
    n = bare_words(first)
    if n >= MIN_OPENING_WORDS:
        return True, "%d words beyond its references" % n
    return False, "opens with a bare reference: %r" % first[:60]


def check_no_lone_citations(body):
    """A sentence made only of a reference asserts that the reader has already read it."""
    bad = [s for s in sentences("\n".join(prose_lines(body)))
           if CITATION.search(s) and bare_words(s) == 0]
    if bad:
        return False, "reference stands as a whole sentence: %r" % bad[0][:60]
    return True, "none"


def check_documents_have_subjects(body):
    """Every RFD cited must appear once in a sentence that says what it is about."""
    docs = cited_documents(body)
    if not docs:
        return True, "no documents cited"
    said = sentences("\n".join(prose_lines(body)))
    unexplained = []
    for doc in docs:
        pat = re.compile(re.escape(doc).replace(r"\ ", r"\s*"), re.I)
        if not any(pat.search(s) and bare_words(s) >= MIN_SUBJECT_WORDS for s in said):
            unexplained.append(doc)
    if unexplained:
        return False, "cited without a subject: %s" % ", ".join(unexplained)
    return True, "%d document(s), each with a subject" % len(docs)


def check_reason_precedes_mechanism(body):
    """A why-section first, or prose that carries the reason before any section does."""
    heads = headings(body)
    if heads and WHY_HEADING.match("# " + heads[0]):
        return True, "opens with %r" % heads[0]
    lead = strip_code(body).split("\n#", 1)[0]
    n = sum(bare_words(s) for s in sentences(lead))
    if n >= MIN_SUBJECT_WORDS * 2:
        return True, "%d words of prose before the first section" % n
    return False, ("first section is %r with no reason before it"
                   % (heads[0] if heads else "(none)"))


CHECKS = (
    ("the opening says something beyond its references", check_opening),
    ("no reference stands alone as a sentence", check_no_lone_citations),
    ("every document cited is given a subject", check_documents_have_subjects),
    ("a reason comes before the mechanism", check_reason_precedes_mechanism),
)

# anny-render-corpus PR #14, as first written and as rewritten after review.
BROKEN = """RFD 1137 steps 9 and 10. The clip now opens and closes with a citation
card, and the card is read from the `.cff` rather than typed a second time -- step 10
derives the filename from the title, so `citation_cff` globs for it instead of naming it.

## The .cff is the one beside the code

The first cut of this pointed `CITATION` at a Desktop path on one desk, where there is
no `.cff` at all. That is worth spelling out because of what it hid.

## Verification

    13 of 13 controls fired
"""

FIXED = """## Why

A 96-pose render sweep leaves ~192 loose files in a directory. Nobody reviews 96 PNGs,
and a directory has no title, no licence, and no statement of what made it. RFD 1137
settles that a sweep ships as one CineForm clip with a `.cff` beside it.

A file beside the clip stops working the moment the two are separated, which is what
happens to a video once someone shares it. So step 9 of that RFD puts the citation
inside the clip, as the first and last thing you see.

## What changed

The clip opens and closes with a citation card, read from the `.cff` rather than typed
a second time.

## Verification

    13 of 13 controls fired
"""


# Well-formed, empty, and NOT CAUGHT. Asserted as passing so the floor is a fixture
# rather than a paragraph: strengthen the gate and these flip, forcing it to be restated.
BLIND_SPOTS = (
    ("a why-section that only restates the patch", """## Why

This change updates the renderer to use the new API surface.

## What changed

The call sites now pass a context object instead of the previous arguments.
"""),
    ("a citation padded out to look explained", """## Why

RFD 1137 steps 9 and 10 are implemented by this change in the manner described.

## What changed

The clip now opens and closes with a citation card as specified in that document.
"""),
    ("fluent jargon with no problem in it", """Refactor the frame pipeline to align
the encoder boundary with the downstream consumer contract, ensuring the latent
handoff remains consistent across stages.

## Implementation

The sequencer now emits normalized descriptors and the adapter reconciles them.
"""),
)


def run(body, verbose=True):
    bad = 0
    for name, fn in CHECKS:
        ok, detail = fn(body)
        bad += 0 if ok else 1
        if verbose:
            print("  %-4s %-46s %s" % ("ok" if ok else "FAIL", name, detail))
    return bad


def self_test():
    r = []
    print("  the rewritten body:")
    r.append(("a comprehensible description passes", run(FIXED) == 0))
    print("  the body that was called incomprehensible:")
    broke = run(BROKEN)
    r.append(("the description that failed review is rejected", broke > 0))
    r.append(("it is rejected for more than one reason", broke >= 2))
    r.append(("an empty description is rejected", run("", verbose=False) > 0))
    r.append(("a description of only references is rejected",
              run("RFD 1137 steps 9 and 10. See rule 3.", verbose=False) > 0))
    for label, body in BLIND_SPOTS:
        r.append(("BLIND SPOT, passes: %s" % label, run(body, verbose=False) == 0))

    print()
    for name, ok in r:
        print("  %-4s control: %s" % ("ok" if ok else "FAIL", name))
    bad = sum(1 for _, ok in r if not ok)
    print("  %d of %d controls fired." % (len(r) - bad, len(r)))
    print("\n  Detection floor. This counts citation structure. It does not read for")
    print("  meaning, and a fluent description with no reason in it passes every check")
    print("  -- the three blind spots above are that, asserted rather than described.")
    print("  Judging whether prose explains anything wants a parser or a model, and")
    print("  neither belongs in a blocking gate; `prose-detrope` is where that lives.")
    return 1 if bad else 0


def body_of(pr, repo=None):
    cmd = ["gh", "pr", "view", str(pr), "--json", "body"]
    if repo:
        cmd += ["--repo", repo]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise SystemExit("FAIL  gh: %s" % out.stderr.strip().splitlines()[-1:])
    return json.loads(out.stdout)["body"]


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if "--file" in argv:
        body = open(argv[argv.index("--file") + 1], encoding="utf-8").read()
    elif argv:
        repo = argv[argv.index("--repo") + 1] if "--repo" in argv else None
        body = body_of(argv[0], repo)
    else:
        body = sys.stdin.read()
    bad = run(body)
    print()
    if bad:
        print("%d check(s) failed. The description does not carry its own reason;" % bad)
        print("a reader who has not opened the documents it cites learns nothing.")
    else:
        print("the description states a reason and does not lean on its references.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
