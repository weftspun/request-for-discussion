# Logbook: the comment ladder

CLAUDE.md gained a rule for how much a comment carries, and for one commit it had
nothing behind it. `check_comment_density.py` sat in the tree looking like the gate for
it and is not: it reads C and C++ only, draws peers from the repository being edited, and
exists for the diffs we send to other people. Our own Python and Elixir were unmeasured.

## The proxy lied, by more than three times

The first measurement counted lines beginning with `#`. That is the convenient proxy, and
rule 1 says to expect it to lie.

Across the 31 tracked Python and Elixir files with 100 or more non-blank lines:

| counting                 | median | p90   | max   |
| ------------------------ | ------ | ----- | ----- |
| `#` lines only           | 7.4%   | 26.6% | 38.2% |
| `#` lines and docstrings | 25.1%  | 31.4% | 39.9% |

A Python module docstring is not a `#` comment and it is where every narrative in this
repository actually lives — `check_comment_density.py`'s own 24-line docstring counted as
code under the first method. So does an Elixir `@moduledoc` heredoc. A gate blind to them
is satisfied by moving a paragraph into one, which is not a change to anything.

The second row is the number the gate uses. The first is recorded because it was reported
first, and a reader who re-derives it should find out here that it was withdrawn rather
than conclude the corpus is three times leaner than it is.

## Rungs, and why it is not a ratchet on the exact number

    rung  5%   0 files
    rung 10%   1     <- new files enter here
    rung 15%   6
    rung 20%   4
    rung 25%   4
    rung 30%   8
    rung 35%   7
    rung 40%   1
    floor      9.7%, scripts/mi_bench.py
    max       39.9%, scripts/check_double_join.exs

A changed file may not leave the rung it sits on. Every rung from 10 to 40 is occupied, so
the ladder describes the corpus rather than imposing a shape on it.

**The first draft of this gate let the problem get worse, and the ladder is why.** With
the ceiling set to the rung alone, `scripts/check_anti_entropy.py` at 30.2% could have
climbed to 35% and passed, because that is where its rung ends. Every file in the corpus
carried between 0 and 5 points of headroom to grow into, handed out on the day the gate
was written. A gate that legalises the next 5 points is not a gate against the thing it
was written for.

So the ceiling depends on what moved:

| what changed               | ceiling                    |
| -------------------------- | -------------------------- |
| comment lines went up      | the density it already had |
| comment lines held or fell | the rung                   |
| new file                   | the entry rung, 10%        |

Adding a comment cannot raise density, full stop. The rung is slack for the other case,
which is real: density is comments over non-blank lines, so **deleting code raises it
without a comment being added**. 40 comment lines over 180 code lines is 18.2%; delete 60
lines of code and the same file is 25.0%. An exact ratchet fails that commit, and the next
commit goes out with `--no-verify`. The slack is bounded by the third and fifth controls:
the same deletion carried past the rung boundary is rejected.

New files enter at 10%, the rung `scripts/mi_bench.py` already occupies — a floor
somebody has already met rather than a number chosen for the shape of it.

`scripts/check_comment_ladder.py` is 9.2% and passes its own entry rung.

## Apparatus

    python scripts/check_comment_ladder.py --baseline    # the table above, re-derived
    python scripts/check_comment_ladder.py --self-test   # the seven controls
    python scripts/check_comment_ladder.py --base origin/main

Seven controls, four of which must reject known-broken input:

| control                                                           | must |
| ----------------------------------------------------------------- | ---- |
| a file padded past its rung                                       | FAIL |
| a comment added inside the rung, density up from 18.2% to 19.3%   | FAIL |
| code added, comments untouched, density falls                     | pass |
| code deleted inside the rung, comments untouched                  | pass |
| code deleted until the ratio crosses the rung, comments untouched | FAIL |
| a new file above the entry rung                                   | FAIL |
| a new file under the entry rung                                   | pass |

The second is the one the first draft would have failed.

They build a throwaway git repository in a temporary directory. `check_comment_density.py`
proves itself by writing 400 comment lines into a real file in the working tree and
restoring it in a `finally`, which is a control that damages the thing it measures if the
process dies between the two. Not copied.

Files under 100 non-blank lines are not measured, and that is a gap rather than a
convention: at 60 lines a single comment moves the ratio by 1.7 points, so the number
would be noise. `scripts/comment_density.py` itself falls under the floor and is therefore
unmeasured by the gate it implements.
