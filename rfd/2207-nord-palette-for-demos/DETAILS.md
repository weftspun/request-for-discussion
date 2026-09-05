# RFD 2207: Nord palette for demos — details

## Applying Nord

Nord defines 16 tokens across four groups (Polar Night, Snow
Storm, Frost, Aurora). A shipped demo declares them as CSS custom
properties on `:root` with dark values, then overrides them under
`:root[data-theme="light"]` with the Snow Storm-anchored light
variant. `prefers-color-scheme: dark` is a media query on top of
the `:root` defaults so a viewer that never picked gets the dark
values by default when their system prefers dark.

`docs/index.html` is the reference application. Structure:

    :root {
      --nord0: #2E3440;   /* Polar Night — bg */
      --nord1: #3B4252;   /* Polar Night — panel */
      --nord4: #D8DEE9;   /* Snow Storm — fg */
      --nord7: #8FBCBB;   /* Frost — accent 1 */
      --nord8: #88C0D0;   /* Frost — accent 2 */
      --nord11: #BF616A;  /* Aurora — danger */
      --nord14: #A3BE8C;  /* Aurora — success */
      /* … */
    }
    :root[data-theme="light"] {
      --nord0: #ECEFF4;
      --nord4: #2E3440;
      /* … */
    }

Every surface pulls from these tokens; no hex literal appears
outside `:root`.

## Why not name a single palette

Two failure modes, both cheaper to close with a peer list than
with a rewrite later:

1. **Subject-matter mismatch.** A demo whose subject is a
   parchment interface reads uncanny in Nord's cool blues; Gruvbox's
   warm palette reads correctly. A palette-of-one rule would force
   the demo author to choose between the rule and the demo reading
   right.
2. **Reader accessibility.** Different palettes carry different
   contrast profiles; a reader with a specific accessibility
   preference is better served by *some* named palette than by any
   one particular one.

Both close by naming the shape of the choice ("pick a named FOSS
design palette") rather than the choice itself.

## Verification

The QA runner at `7-service/service-sqlar-cas/scripts/qa_demo.mjs`
extends to grep the shipped `docs/*.html` and `docs/*.css` for
raw hex-color literals outside the `:root` declaration. Every
match is either a token definition or a defect. Negative control:
a planted `color: #ff0000` in a rule body fails the grep.

## Related retractions

None. Prior demos in `7-service/service-sqlar-cas/docs/` shipped
under the un-tokenised default; this RFD retires that default
prospectively for new work and any material redraft.

This RFD was drafted by an AI and read by a human before it shipped.
