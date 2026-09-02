# RFD 2170: allosaurus runs universal + Squad's localization language set

**State:** committed
**Feature:** phone-inventory controls for the ASR panel
**Scope:** `6-datasource/anny-render-corpus/emit_10track_panel.py`,
`6-datasource/anny-render-corpus/add_allosaurus_control.py`

## Problem

RFD 2164's panel shipped allosaurus at three inventories: `universal`,
`eng`, `rus`. The eng/rus pair was ad-hoc (Kazakh L2 English speaker,
Russian as plausible L1). That reasoning does not generalize, and
picking language priors per corpus makes runs incomparable.

## Decision

allosaurus runs at **universal + Squad's localization language set**,
verbatim from the Squad Steam store page (a proxy for the industry
standard game-localization language set):

  universal, eng, cmn, fra, deu, spa, jpn, por, rus, ukr

Ten tracks total. Language codes are ISO 639-3. Squad's list drives
the standard because it is the tightest actively-maintained AAA-game
localization set that still covers the top-five game markets by
revenue plus the operational languages of Weftspun's own contributors.

An audio clip whose speaker's L1 is not in the set is scored under
`universal` alone; the language-specific rows return empty rather than
mislead. That is a real signal, not a silent skip.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1173 (MaskScore).
Applies to: urn:oid:1.3.6.1.4.1.66606.1.2.2164 (Speech stub).
Squad supported-languages page: https://store.steampowered.com/app/393380/Squad/

This RFD was drafted by an AI and read by a human before it shipped.
