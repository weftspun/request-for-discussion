# RFD 1018: M3 documentation removal

**State:** discussion
**Scope:** `m3/`

## Problem

`m3/` holds a fork of the M3 Character Studio site. M3 holds the
copyright for that content. The file `m3/LICENSE` records the M3
copyright. The MIT terms require the repository to keep that notice
while the M3 content stays. This tree moved here from
weftspun-3d-studio's own `docs/`; the paths below read `m3/docs/`
and `m3/static/`, the current location.

The site costs more than it returns. No pipeline builds the site. The
site keeps a separate package file and two lock files. The site
caused seven dependency security commits. Its config and its API
reference both drift from the current code, per `DETAILS.md`.

## Decision

Delete the M3 API reference. Do not rewrite it. A code map replaces
it, naming each module and pointing at the source file.

Delete the Docusaurus site machinery. This step removes the M3 site
identity and the dependency cost. The markdown files stay, because
the README links to them.

Rewrite each remaining M3 guide in Weftspun words. Then delete the M3
original. A rewrite must describe the current code, not the M3 code.

Keep `m3/LICENSE` until the last M3 file goes. A deletion before
that step would drop a notice the MIT terms require.

Keep an `m3/static/` image only while a surviving markdown file names
it under `/img/`. Delete the rest now. See `DETAILS.md` for the list.

## Related

RFD 1017 records the rebrand.
