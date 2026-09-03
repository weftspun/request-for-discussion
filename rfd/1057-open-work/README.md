# RFD 1057: Open work

**State:** published
**Scope:** the repository

## Decision

Keep one list of open work, in `DETAILS.md`. Each entry names the
RFD that owns it, and what closing it needs. Delete an entry when it
closes, so that file shrinks and never grows a history section.

`DETAILS.md` holds five sections: verified and running, written and
never run, measured and not built, unknown and blocking a number, and
decided but waiting.

## Problem

This branch changed the host, the packaging, the backend, and the
planner. Some of that work is complete, some is measured but not
built, and some is written but never run.

A reader who returns to this cannot tell those apart from the RFDs
alone. Each RFD records its own decision, and none records what is
still owed.

## Related

RFD 1055 selects the host. RFD 1056 selects the development system.
RFD 1036 packages the models. RFD 1026 holds the memory numbers.

RFD 1058 gives the Quadlet deployment. RFD 1059 gives the one-step
build. RFD 1061 gives the `idtx_core` upload-prep decision. RFD 1062
gives the Fly.io / 4090 split.
