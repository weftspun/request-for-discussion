## What moved

| Path                                                   | Records |
| ------------------------------------------------------ | ------- |
| `_archive/decisions/`                                  | 26      |
| `_archive/decisions/attachments/`                      | 1 image |
| `rfd/200b-observability-stack-victoriatraces/`         | 1       |
| `rfd/203d-quadlets-on-fedora-44-instead-of-harvester/` | 1       |

`_archive/README.md` moves with the directory. Its text now states that
the leading underscore does no work in a repository that builds no
site, and that the path stays as it was so older links keep their
shape.

## Link repair, which a move forces

A deleted file leaves no stub. A live Markdown link to that file leaves
a 404 on the published site. So a move repairs every inbound link, and
that is not a stub.

| File                                                                    | Repair                                                                              |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `changelog/2026/20260606-deck-log.md`                                   | Four relative links into `_archive/decisions/` now point at the archive repository. |
| `rfd/2071-yagni-times-structure-to-need/index.md`                       | Two pointers to `_archive` now name the archive repository.                         |
| `rfd/2089-flyio-over-podman-quadlets/index.md`                          | The `rfd/0061` reference now links to the archive.                                  |
| `rfd/2060-org-scoped-github-app-token-for-gh-access/index.md`           | The `rfd/0061` reference now links to the archive.                                  |
| `rfd/2070-loop-slice-telemetry-to-the-observability-collector/index.md` | The `rfd/0011` reference now links to the archive.                                  |
| `rfd/2062-repository-and-capability-inventory/DETAILS.md`               | The two-org split decision path now links to the archive.                           |
| `_quarto.yml`                                                           | Drops the `decisions/attachments` resource, which no longer exists.                 |

Inline prose in `rfd/0089`'s `DETAILS.md` still names `rfd/0061` in
code spans, without links. Those read as citations of a numbered
record, so they stay.

## A broken link the move exposed

Two archived records cite the debug-orb image as
`attachments/20260606_vsekai-mpf_xr-grid-debug-orbs_0001.png`, relative
to `_archive/decisions/`. The image sat in `decisions/attachments/`,
two directories away, so the link never resolved. No rendered page
exercised it, because Quarto skips `_archive`.

The archive repository puts the image at
`_archive/decisions/attachments/`, where the existing links resolve.

## Two archive destinations now exist

`V-Sekai-archive` is a separate organization that already holds three
archived repositories: `lean-predictive-bvh`, `viser`, and
`usd-converter-for-vrchat`. `multiplayer-fabric-archive` is a
repository for archived records inside this organization.

A whole repository goes to the `V-Sekai-archive` organization. A record
inside the manuals goes to `multiplayer-fabric-archive`. A future
record that consolidates the two supersedes this one.

## Counts after the split

| Set                                   | Count |
| ------------------------------------- | ----- |
| Repos in `v-sekai-multiplayer-fabric` | 73    |
| Active                                | 49    |
| Archived                              | 24    |

## What stays

`decisions/` keeps `madr-proposal-template.md`, the live template. The
directory holds no records, because `rfd/2000-conventions` migrates
each MADR into an RFD and deletes the MADR file.

`AGENTS.md` still directs a new image to `decisions/attachments/`, and
that directory returns when the next asset arrives.
