# RFD 2143: Close-out gates — red control, green, scout

**State:** prediscussion
**Feature:** three gates every piece of work records at close-out
**Scope:** logbook entries, all projects

## Problem

A gate recorded only passing is decoration: it has never shown it
can detect the broken state, and a pass without its command cannot
be re-run. Sessions also shed side effects — stray processes, /tmp
files, caches, credentials — that no gate inspects, and a defect can
hide inside them. The first inventory run found a stale server
holding a port behind a probe that reported the same identity for
the broken and the fixed build.

## Decision

Work closes with three gates in the logbook, each with runnable
apparatus. Backfilling any of them is permitted: the record is the
requirement, not the timing.

1. **Red control gate.** The exact command shown failing on the
   broken state. Verification rule 2 in the working agreements.
2. **Green gate.** The same check shown passing on the fixed state.
   The probe must distinguish the two states it separates; an
   identity-blind probe (one that answers alike for both) does not
   qualify.
3. **Scout gate.** The place left better than we arrived: an
   inventory of the session's side effects shown non-empty before
   cleanup and empty after, plus what was improved beyond the task.

`DETAILS.md` carries the reference case with its measurements.
