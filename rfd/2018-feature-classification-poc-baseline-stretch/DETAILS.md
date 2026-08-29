# Details

## Context and Problem Statement

The capabilities table lists features with a free-text status ("working",
"loses about 90%"). Free text does not say whether a feature is a
throwaway experiment, a committed part of the product, or a
nice-to-have. The team needs one shared vocabulary for how far along and
how committed a feature is, so planning and the docs agree on what
"done" means for each one.

## Decision Drivers

- One vocabulary shared between planning and the manuals.
- A reader should know at a glance whether a feature is committed or
  exploratory.
- Cheap to apply and to move as a feature matures.

## Considered Options

- Keep free-text status only.
- A maturity ladder (alpha / beta / stable).
- A three-tier commitment classification: proof of concept, baseline,
  stretch.

## Consequences

- Good: planning and docs share one word per feature for its commitment
  level.
- Good: the tier is a small, reversible edit as features move.
- Bad: a tier is a judgement call and can drift from reality if the
  table is not kept current.

## Confirmation

The capabilities table has a Tier column, and every row carries one of
the three tiers. New capabilities are added with a tier.

- consulted: lyuma
