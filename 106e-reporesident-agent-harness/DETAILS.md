# RFD 106e details: file map, context layers, workflows, and carried-over decisions

## File map

| File | Role | Loaded |
| --- | --- | --- |
| `CLAUDE.md` | Operating rules, protocol, routing, and project facts | Every session |
| `AGENTS.md` | Entry point for tools using the `AGENTS.md` convention | Tool dependent |
| `.agent/STATE.md` | Current project state and inter-session handoff | Every session |
| `.agent/MAP.md` | Compact module and directory map | When locating code |
| `.agent/PROJECT.md` | Architecture, constraints, glossary, and project-wide risks | Feature work or confusion |
| `.agent/DECISIONS.md` | Binding technical choices with reasons | Before design work |
| `.agent/ISSUES.md` | Bounded backlog for bugs, debt, and deferred work | Before design or work selection |
| `.agent/workflows/*.md` | Procedures for task categories | One per task |
| `.agent/designs/` | Active and archived feature designs | Active design only |
| `.agent/areas/` | Optional deep documentation for complex modules | When working in that area |
| `.agent/journal/` | Append-only session outcomes | Written at session close |
| `.agent/scratch/` | Ignored temporary investigation notes | Only while active |

## Context layers

| Layer | Content |
| --- | --- |
| L0 | `CLAUDE.md`, the operating manual |
| L1 | `STATE.md`, the current project state |
| L2 | One workflow for the current request |
| L3 | Map, project facts, decisions, issues, area docs, and active design |
| L4 | Targeted source code |

## Working roles

Rules for a phase, not conversational personas.

- **Architect:** scopes and designs without writing implementation code.
- **Builder:** implements an approved design without changing its structure silently.
- **Fixer:** makes the smallest complete correction and avoids unrelated refactoring.
- **Reviewer:** reports verified findings and does not rewrite unless asked.
- **Curator:** maintains the harness and its bounded knowledge files.

## Workflow selection

| Workflow | For |
| --- | --- |
| `bootstrap.md` | First session on a new or adopted project; `CLAUDE.md` still has `<fill>` placeholders, or `STATE.md` Session is 0 |
| `patch.md` | Small fix, cause known or trivially findable, no interface change, at most two files |
| `debug.md` | A defect whose cause is unknown; output is a named root cause with evidence, then `patch.md` or `feature.md` |
| `feature.md` | New capability, or any change touching more than two files or any interface/schema/dependency |
| `refactor.md` | Structure improvement with zero behavior change; a bug found mid-refactor gets parked, not bundled |
| `review.md` | Reviewing a diff, PR, or branch; best run fresh, from a session that did not write the code |
| `maintain.md` | Every tenth session, or when a size budget is blown, or the user asks; checks the harness against the repository |

`feature.md`'s exit test: if a change has a single known site, no
interface change, and obvious verification, it downgrades to
`patch.md`. `patch.md` escalates to `feature.md` the moment an
interface or schema must change, or the fix wants more than two
files; it escalates to `debug.md` the moment five files are read and
the cause still cannot be named with evidence.

## Technical decisions not covered by another RFD

From `.agent/DECISIONS.md`, append-only, project-specific choices
this repository's own numbered RFDs do not yet record:

- **2026-07-26, XR disembody:** the avatar exits at the exit spot
  facing the headset, the viewer stands one meter behind, and
  Move-to-Viewpoint, X, and the stick-click all work without opening
  a menu. Embody never shifts the rig's Y position. Reason:
  user-confirmed on the Galaxy XR editing flow.
- **2026-07-26, LingBot Gaussian-splat worlds:** these use Spark with
  `orientationMode: none`, never an XYZRGB point stride, since the
  wrong stride scatters points. Gravity-aligned point clouds must not
  receive TripoSplat's X-flip.
- **2026-06-26, API↔client contracts:** must land together, since
  `models.yaml` and `aiModelsCatalog.js`/`taskManager.js` describe
  the same models from two sides.

Decisions already carried by other RFDs, not repeated here: UI on
the Surface, API on the DGX (RFD 1056); scp-based sync with no agent
git push (RFD 1056, RFD 1063); RepoResident's own adoption,
replacing MindLink (this RFD's README).
