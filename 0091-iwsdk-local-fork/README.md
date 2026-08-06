# RFD 0091: A local IWSDK fork, linked, not published

**State:** published
**Scope:** `AlfaOmegaGrafx/immersive-web-sdk`, this project's own `package.json`

## Problem

The upstream `@iwsdk/*` npm packages, pinned at `^0.4.2`, do not
carry a fix this project needs. Publishing a patched fork to npm, or
vendoring its source directly into this repository, are both real
options, and both are heavier than the gap needs.

## Decision

Consume local builds from a sibling clone of
`AlfaOmegaGrafx/immersive-web-sdk` instead, cloned next to this
project's own checkout, not published anywhere. `npm run
iwsdk:link-local` builds the fork's packages into `.tgz` files and
installs them; `iwsdk:link-local:rebuild` forces a clean rebuild.
Reverting to the npm release needs only restoring the `^0.4.2` range
in `package.json` and reinstalling.

See `DETAILS.md` for the sibling-clone layout and the package table.

## Related

Upstream: `iwsdk.dev`. The fork: `github.com/AlfaOmegaGrafx/immersive-web-sdk`.
