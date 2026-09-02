# RFD 2170: allosaurus runs universal + Squad's game-localization language set

**State:** committed
**Feature:** phone-inventory controls for the ASR panel
**Scope:** `6-datasource/anny-render-corpus/emit_10track_panel.py`,
`6-datasource/anny-render-corpus/add_allosaurus_control.py`

## Problem

RFD 2164's panel shipped allosaurus at three inventories (`universal`,
`eng`, `rus`, picked because the first speaker was Kazakh L2 English).
That does not generalize; per-corpus priors make runs incomparable.

## Decision

allosaurus runs at **universal + Squad's full Steam-page language
set** (27 languages, verbatim as of 2018-12-15 and preserved into
the 2026 store page):

  universal, eng, fra, ita, deu, pol, rus, cmn, cmn-Hant, tur, spa,
  ara, ces, kor, bul, dan, nld, fin, ell, hun, jpn, nor, por, por-BR,
  ron, swe, tha, ukr

28 tracks. Codes ISO 639-3 with a script/region suffix where Squad
distinguishes (cmn/cmn-Hant, por/por-BR). Squad's Steam page drives
the standard as the tightest actively-maintained AAA-game
localization set spanning every top game market.

Clip whose L1 is out-of-set scores under `universal` alone;
language-specific rows return empty (real signal, not silent skip).
Where allosaurus shares one phone inventory across a pair
(cmn/cmn-Hant, por/por-BR), rows share weights; labels survive.

## Related

Spine: urn:oid:1.3.6.1.4.1.66606.1.1.1173 (MaskScore).
Applies to: urn:oid:1.3.6.1.4.1.66606.1.2.2164 (Speech stub).
Squad Steam page: https://store.steampowered.com/app/393380/Squad/
Squad Wiki translation portal: https://squad.fandom.com/wiki/Squad_Wiki:Translation_portal

This RFD was drafted by an AI and read by a human before it shipped.
