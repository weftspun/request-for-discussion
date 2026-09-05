# RFD 2207: Nord palette (or peer) for shipped demos

**State:** discussion
**Feature:** shipped demos and artifacts pick a named FOSS design
palette (Nord as the default, Solarized / Catppuccin / Tokyo Night
/ Rose Pine / Gruvbox as acceptable peers) rather than the warm
amber-on-panel look that Claude artifacts default to
**Scope:** every shipped browser demo under `7-service/*/docs/` and
every Artifact this workspace publishes as a deliverable; the same
rule does not bind private one-shot artifacts an operator uses to
inspect an intermediate

## Decision

A demo or artifact that ships as a reviewable surface picks one of
the following six FOSS-licensed palettes verbatim and sources its
tokens from that palette's published spec:

| palette | licence | source |
|---|---|---|
| Nord | MIT | nordtheme.com |
| Solarized | MIT | ethanschoonover.com/solarized |
| Catppuccin | MIT | catppuccin.com |
| Tokyo Night | MIT | github.com/enkia/tokyo-night-vscode-theme |
| Rose Pine | MIT | rosepinetheme.com |
| Gruvbox | MIT | github.com/morhetz/gruvbox |

Nord is the default this session's Starforged surface adopted and
what a new demo picks in the absence of a reason to pick otherwise.
The five peers are named so the choice is not hardcoded to one
system — a demo whose subject matter reads better in warm tones can
pick Gruvbox; a demo tuned for a night-shift reader can pick Tokyo
Night. What is banned is the un-tokenised amber-on-panel default
that a first-draft artifact carries when nothing was picked.

Both light and dark variants are declared. `data-theme="dark"` and
`data-theme="light"` on the root, plus a `prefers-color-scheme`
media query, per the artifact-design contract.

## Problem

The mid-session operator redirect that produced the Starforged
demo's Nord palette was blunt: the warm-terminal look that
Claude artifacts default to reads as an AI intermediate, not as a
deliverable. A reviewer who opens a shipped demo and sees the
default Claude look concludes, correctly, that nobody picked a
palette. Picking one — any of the six above — closes that reading.

The rule is about *picking* rather than about *which one*. What the
existing default fails at is being un-considered; the six peers all
pass by virtue of being considered and readable.

## Non-goals

Not a component library or a spacing/typography spec. Not a
mandate to reskin dot-claude, existing internal tooling, or
operator-private artifacts. Not a mandate that every demo pick
Nord specifically — the peers exist for cases where a different
palette reads better on the subject.

## Related

- RFD 2206 (video-call VRM portrait) — the shipped surface this
  palette was first applied to.
- Codebase: `7-service/service-sqlar-cas/docs/index.html` — the
  reference Nord application in this workspace.
- CLAUDE.md's "Trademarks Stay Out of Shipping Artifacts" clause —
  the six palettes are all trademark-clean and named by their own
  project names.

This RFD was drafted by an AI and read by a human before it shipped.
