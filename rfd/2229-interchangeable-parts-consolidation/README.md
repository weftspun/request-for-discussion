# RFD 2229: interchangeable-parts consolidation as workspace policy

**State:** discussion
**Flight level:** L3 (strategy — sets a policy that touches
every future part-adding decision)
**Feature:** codify the interchangeable-parts directive from
2026-09-05 as workspace policy plus name the concrete candidates
already visible in the goal manifest
**Scope:** `weftspun-keypoint/default.xml` (goal manifest), all
future RFDs that add a new module / fork / build fragment /
loader path, memory `consolidate-interchangeable-parts`

## The policy

Operator directive 2026-09-05, verbatim: *"like ford's factories
we have to conslidate our interchagable parts. we have too many
parts"* + trademark-scrub follow-up *"please avoid using the
company name ford as a trademark for inventing the interchable
parts process"*.

**Historical note.** Interchangeable parts predate the company
that got named in the first draft by a century — Whitney's musket
contract 1798, the Springfield Armory / American System of
manufactures through the 1820s–1850s. That company scaled
assembly-line production using interchangeable parts; it did not
invent them. Neutral vocabulary is **interchangeable parts**,
**standardized interfaces**, **the American System of
manufactures** if a historical anchor is wanted.

**The workspace rule (goes into CLAUDE.md next):**

Before landing a new part — a module, a fork, a build fragment,
a loader path, a bundle format, a C API extension — check whether
an existing part covers the interface. If yes, extend the
existing part rather than land a parallel one. Every RFD that
names a new component carries a sentence naming the existing
part it substitutes for and why substituting doesn't work.
"Doesn't work" is a measurement, not a preference.

Two mechanisms already carry the rule for specific interfaces:

- `2-contract/ggml/` (RFD 2188) as the single ggml source every
  consumer links.
- `2-contract/manuals-weftspun/` (this repo) as the single
  workspace-doctrine mount, reached from `weftspun-keypoint` via
  linkfile.

## Live candidates in the manifest (2026-09-05 as of writing)

Enumerated from `weftspun-keypoint/default.xml` at 112 project
entries.

### Three `ggml` checkouts

    3-interactor/trellis2cpp/ggml       remote=weftspun  rev=331b9cba
    3-interactor/ggml-seethrough        remote=weftspun  rev=3404c951
    2-contract/ggml                     remote=weftspun  rev=weftspun-consolidated

**RFD 2188 named `2-contract/ggml` as the single ggml source
workspace-wide.** The manifest still ships three checkouts. Two
of them (`trellis2cpp/ggml`, `ggml-seethrough`) are consumers
still pinned to their own ggml revisions rather than reading
through the shared source.

**Verification needed before trimming.** Whether each consumer
has actually migrated to `2-contract/ggml`'s API, or whether the
pinned revision holds something the consolidated source doesn't
yet cover. A CI green on `trellis2-ex` and `seethrough` against
`2-contract/ggml` is the measurement.

Follow-up L1 RFDs (planned in the 22xx range): one per consumer
scoping the migration + trim per project.

### `entities-godot-main` (trimmed 2026-09-05)

Same repo as `entities-godot-sandbox` at revision `main` instead
of `feat/vsk-sandbox-4.7`. Trimmed as `weftspun-keypoint#101`.
Recorded here as the reference case that proves the pattern
lands cleanly.

### `motion-bricks-cpp` + `kimodo` + `skin-tokens-cpp`

Three ggml-graph-in-C++ shapes with three separate build
systems. All target the same interface: a C API that Godot's
`modules/motionbricks/` (RFD 2212) wraps for scene-graph access.
Consolidation candidate: one `ggml-godot-module-kit` that all
three link, replacing three per-project CMake `if(NATIVE_WEBGPU)`
branches with one shared fragment.

Not urgent; the three projects are early enough that their build
systems haven't diverged much. RFD 2188 shared source + a small
build-fragment consolidation covers most of it. Concrete work is
a follow-up L2 once RFD 2212's `modules/motionbricks` lands.

### Manifests-of-manifests

**Not a candidate.** `weftspun-keypoint` is the single live goal
manifest per CLAUDE.md's "Sides" rule; the archived
`weftspun-mesh-latents` is placement history, not a parallel
manifest.

## Verification

The policy is measured by:

1. **RFD-add gate.** A new RFD that adds a component but does
   not name an existing part it substitutes for is asking for a
   parallel part. Add a section to `check_rfd_structure.py`
   requiring an "Alternatives considered" or "Substitutes for"
   paragraph when the RFD's frontmatter is tagged as adding a
   module/fork/bundle-format. Draft in a follow-up PR; RFD 1000
   carries the structure list this gate reads from.
2. **Manifest-scan gate.** `scripts/check_manifest_dupes.py`
   (new) reads the live goal manifest, groups by name/path/
   remote+rev, and reports groups of size > 1 as candidates
   needing a doctrine pointer (an RFD saying why both stay) or
   a trim PR (like `weftspun-keypoint#101`). Silent-skip case:
   the two-manifest state that exists during a manifest cutover
   — the gate reports both, doesn't fail on the presence.

## Related

- RFD 2188 (one ggml across workspace) — the reference
  consolidation this RFD generalises.
- RFD 2210 (L3 atelier shipping surface) — the arc that
  produced the directive.
- RFD 2211 (base tree entities-godot-sandbox) — picked the tree
  the trim in `weftspun-keypoint#101` acted on.
- RFD 2228 (WebGPU native, drop platform=web) — the reversal
  that made post-hoc consolidation cheap because it dropped one
  build target.
- Memory `consolidate-interchangeable-parts` — the operator
  directive + how-to-apply, kept as the working memory next to
  this policy.
- Memory `coordinator-verify-before-relay` — records the earlier
  trademark violation this RFD's naming was scrubbed against.

## Operator context 2026-09-05

Two verbatim directives (paired):

> like ford's factories we have to conslidate our interchagable
> parts. we have too many parts

> please avoid using the company name ford as a trademark for
> inventing the interchable parts process

Both applied. The first is the policy; the second is the naming.
The RFD carries neutral vocabulary from here on.

This RFD was drafted by an AI and read by a human before it shipped.
