# RFD 1070: Keep options open

**State:** published
**Scope:** `decisions/`

## Decision

Do not open an RFD for a build this project has not committed to.

Kent Beck's price-theory reading of YAGNI names the cost: an
unexercised option costs twice if the guess is wrong, so a thing not
yet committed to is worth more left unbuilt. Waiting holds an asset.
It does not delay work.

The rule stops a new RFD from opening before commitment. It does not
reach back into one already running.

See `DETAILS.md` for the three RFDs this rule removed, what made each
speculative, and what the rule left in place.

## Problem

This repository wrote down three RFDs for a build nobody started.
Each carried a reading cost, a cross-reference to keep current, and
an index row, for an option nobody had exercised.

## References

- Kent Beck, "The Cost YAGNI Was Never About":
  https://newsletter.kentbeck.com/p/the-cost-yagni-was-never-about

## Related

RFD 1000 gives the state ladder a speculative RFD would otherwise
sit on. RFD 1031 keeps the fallback RFD 1032 would have replaced.
