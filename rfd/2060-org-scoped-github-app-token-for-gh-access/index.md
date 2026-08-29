---
title: "RFD 2060: Org-scoped GitHub App installation token for gh access instead of a personal OAuth token"
rfd: "2060"
state: published
scope: gh CLI authentication for v-sekai-multiplayer-fabric
---

## Problem

`gh` ran on a personal OAuth token with the `repo` scope. That scope
grants read, write, admin, and delete access on every repository the
personal account can reach, across every org. A leaked personal token
could then reach far more than the one org's repositories this
project needs.

## Decision

`gh` used to run on a personal OAuth token with the `repo` scope. That
scope grants read, write, admin, and delete on every repository the
personal account can reach, across every org. A GitHub App installed
on `v-sekai-multiplayer-fabric` now mints the token instead. A helper
script reads the App id and private key from 1Password, signs a JWT,
and exchanges it for an installation access token, which `gh` uses
directly. The installation token is org-scoped by construction: it
cannot read or write any private repo outside the org, and it expires
about one hour after minting, so a leak dies on its own. The
installation is granted `administration: write`, `contents: write`,
`workflows: write`, `actions: read`, and `metadata: read` on every
repository in the org — the set the repo work needs. The GitHub App's
private key is itself high-value and stays guarded in 1Password.

## References

- Full drivers, considered options, consequences, and confirmation
  probe against the live API: `DETAILS.md`
- Original record:
  `decisions/20260613-org-scoped-github-app-token-for-gh-access.md`
- Helper script: `~/bin/gh-fabric-token.sh`

## Related

- [`rfd/203d-quadlets-on-fedora-44-instead-of-harvester`](https://github.com/v-sekai-multiplayer-fabric/multiplayer-fabric-archive/tree/main/rfd/203d-quadlets-on-fedora-44-instead-of-harvester):
  the same org's repos carry the quadlet sources this token drives. It
  now lives in `multiplayer-fabric-archive`, per `rfd/0106`.

## Detail

{{< include DETAILS.md >}}
