# RFD 2181: Drop the allosaurus-rus phone-inventory control

**State:** published
**Feature:** documentation retraction
**Scope:** RFDs 2164, 2170; `emit_10track_panel.py`;
`add_allosaurus_control.py`; `CITATION.cff`

## Problem

RFD 2164 shipped allosaurus at three inventories: `universal`,
`eng`, `rus`. The `rus` inventory was picked as a plausible L1
transfer partner for the first SpeakingFaces subject (Kazakh L2
English speaker), then RFD 2170 generalised the set. The panel's
implementation still carries `rus` as a per-clip inventory and
runs it on every clip regardless of the speaker's L1.

## Decision

Drop `allosaurus-rus`. Panel drops from 8 tracks (post-2180) to 7:

  text-track   Parakeet TDT 0.6B v3, Voxtral Mini 3B, wav2vec2
  IPA-track    Voxtral-IPA, Gemma-4-12B GBNF-IPA
  phone-track  allosaurus universal + eng

Universal stays as the language-inventory-free default; `eng` stays
as the English control. Per-clip language inventories can be added
back keyed to the speaker's L1 if a future corpus documents it, rather
than one hard-coded language for everyone.

Follow-ups: `emit_10track_panel.py` and `add_allosaurus_control.py`
drop the `rus` inventory; downstream RFDs lose their `rus` mentions;
`CITATION.cff` unaffected (allosaurus itself stays).

## Related

Extends RFD 2179 (drop Whisper) and RFD 2180 (drop gemma-auto).
Amends the panel row in RFD 2170's decision that named `universal
+ eng + rus`.

This RFD was drafted by an AI and read by a human before it shipped.
