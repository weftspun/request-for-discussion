# Gacha ladder end-to-end, RFD 2136 stack, 2026-09-02

Requested by a peer session (MPS-side, no CUDA), routed to the desk with the
3090. **The stack the peer listed does not match RFD 2136's ladder** —
Wan-VACE 14B, Qwen3-TTS and the 7-track ASR panel are not on the ladder; the
ladder is OmniGen2 → Pixal3D → EditScore → VoxHammer → SkinTokens →
See-Through partition → seed-to-VRM. This entry measures the actual ladder.

**End-to-end did not run.** Four rungs (1, 3, 5, 6) have no runnable
environment on this desk today. Two more (7-9) depend on the spot-broker,
which is blocked (rented compute, RunPod/Vast.ai, blocklisted this session per
CLAUDE.md's Retracted Condition 5 paragraph). One rung (4) has a pixi env but
its `_run_upstream` raises `NotImplementedError` — scaffold, not
implementation. Rungs 0 and 2 are the only ones with working stacks.

This is rule 3 written out: a silent skip reads exactly like a pass, so every
absent rung is named and counted with the reason.

## Per-rung state

Numbers below in the household-object frame CLAUDE.md asks for where a
physical anchor makes it read faster.

### Rung 0 — text → image (OmniGen2)

**State:** RUNNABLE. Executed once earlier this session (LLaDA-o smoke test);
numbers below are that run, not a fresh fire (there was no rung 1 to consume
another image, so firing again would spend 10 min producing an artefact
nothing reads).

- Wall-clock: **12.06 s per denoising step × 50 steps = ~10 min per 1024²
  image** on the 3090 with `enable_sequential_cpu_offload()`. Ten minutes is
  about a coffee-and-a-half.
- VRAM peak: **~7 GB on-device** (weights streamed via offload); Python RSS
  spilled to **24.85 GB** in system RAM holding the offloaded blocks.
- Artefact: no persisted PNG (the smoke test computed but did not save the
  edit-mode output; the harness saved only the sha256).
- **Baseline:** without offload the 15.9 GB DiT does not fit; the "no
  measurement" case is compared to the 10-min figure here.
- **Extrapolation (unmeasured, sanity-check math):** n=100 × 10 min = 16.6 h.
- **Reproduction:** the exact env is
  `3-interactor/omnigen2/pixi.toml` (torch 2.6.0 cu124, transformers 4.51.3,
  flash-attn 2.8.3 via bdashore3 wheel). See memory note
  `windows-torch-2.6-dep-matrix` for the dep pins that survive this stack on
  Windows.

### Rung 1 — image → mesh (Pixal3D)

**State:** COULD NOT RUN. `3-interactor/pixal3d-image-to-textured-mesh/`
carries no `pixi.toml`; no environment materialised on this desk.
`3-interactor/pixal3d-upstream/` is checked out at commit
`cdbb2bbffbf4e6f298b5f2af3d1d76a8d823d2af` per manifest but likewise has no
declared env.

- Owed: author a `pixi.toml` (upstream requirements + Windows CUDA pin
  matrix), pull weights (unknown HF path), run one image through — reference
  images are widely available in the OmniGen2 outputs, so once the env is up
  Rung 0 + Rung 1 land together.
- Setup estimate: 30-60 min env, 15-30 min weight download, 30-60 min first
  inference debug (Windows CUDA env parity is where LLaDA-o and OmniGen2
  each spent 1-2 hours this session, per memory notes).
- **No fresh measurement possible.** Skip counted as one.

### Rung 2 — mesh + prompt → EditScore judgment

**State:** RUNNABLE, verified this session by loading the scorer end-to-end
(smoke test at `3-interactor/editscore/examples/llada-o-vs-omnigen2/`, output
in the earlier session's persisted transcript).

- Wall-clock per `evaluate([source, edited], instruction)`:
  **~30-60 s** (two `.generate()` calls at Qwen2.5-VL-7B, one SC + one PQ,
  each producing ~50-90 tokens). About the time to microwave leftovers.
- VRAM peak: **~15.5 GB with device_map="auto"** (bf16 weights + activations;
  no offload used).
- Artefact: dict with `prompt_following`, `consistency`, `perceptual_quality`,
  `overall` — the paired-t-testable scalar is `overall = sqrt(SC * PQ)`.
- **Baseline:** the fp32 EditScore-7B doesn't ship; there is no fp32
  reference to compare against, so the bf16 numbers ARE the baseline. If the
  QAFT-nf4 build in `3-interactor/editscore/examples/qaft-4bit/` lands, the
  paired comparison against these bf16 numbers becomes the gate for shipping
  int4.
- **Blocker for feeding Rung 1 output:** we can only score
  (source_image, edited_image, instruction) triples. Rung 2 in the ladder
  wants to score a mesh — that requires a rendered projection of the mesh
  before EditScore sees it, which the ladder doesn't call out. Owed: a
  mesh-to-image projector between rungs 1 and 2, or a direct
  mesh-scorer variant. Either is real work.
- API note: `EditScore(backbone="qwen25vl", ...)` — not `.from_pretrained`.
  Full surface in memory note `editscore-api-surface`.

### Rung 3 — VoxHammer repair loop

**State:** COULD NOT RUN. `3-interactor/voxhammer-image-mesh-editing/` and
`3-interactor/voxhammer-upstream/` both lack `pixi.toml`. Active branches on
the repo (`export-the-dinov2-device-half`) target Hailo compile work, not
end-to-end runtime.

- Owed: same class as Rung 1 — env setup + weights pull + first-inference
  debug. Skip counted as one.

### Rung 4 — mesh → skinned rig (SkinTokens on ANNY)

**State:** COULD NOT RUN. The pixi env exists at
`3-interactor/skintokens-auto-rig/` and materialised on disk. But its
`README.md` states verbatim, and grep confirms in `server.py`:

> Scaffolded from the RFD, not yet built or run. `_run_upstream()` and
> `_write_joint_map()` raise `NotImplementedError` outside stub mode —
> SkinTokens' real forward pass and the VRM humanoid joint-map write are not
> yet ported from the upstream repo.

So the rung looks half-ready (env present) but is not runnable end-to-end.
This is exactly the class of thing rule 3 exists to catch — an env with a
successful `pixi install` is not evidence the code inside works.

- Owed: port `_run_upstream()` from `VAST-AI-Research/SkinTokens` upstream;
  wire the humanoid joint-map write for VRM output. RFD 0046 already
  identifies the joint-name-order trap. Skip counted as one.

### Rung 5 — mesh → tagged with See-Through partition

**State:** COULD NOT RUN. `3-interactor/seethrough-partseg/` has no
`pixi.toml`. See-Through's partition v3 spec (RFD 1121) is authored, but the
part-segmentation worker isn't stood up on this desk.

- Owed: env, weights, then the VoxHammer-mediated loop the ladder specifies
  (VoxHammer proposes tag corrections toward canonical partition, EditScore
  judges each proposal, bounded to N attempts). That's Rungs 3+5 depending
  on each other; both need to land together. Skip counted as one.

### Rung 6 — tagged rig → VRM (one-command assembly)

**State:** COULD NOT RUN. No single-command wrapper is committed on the
manifest projects examined here (`skintokens-auto-rig`,
`voxhammer-image-mesh-editing`, nor a `seed-to-vrm` project). The RFD
describes the rung as "the seed-to-VRM assembly runs end to end from a
single command" — the command does not exist yet.

- Owed: an assembler that takes (skinned-mesh USD, part-tag primvar,
  humanoid joint map) and writes a portable VRM per the CLAUDE.md deliverable
  rule (pure data, no runtime modifiers/drivers/extensions). Skip counted
  as one.

### Rungs 7, 8, 9 — pool / roll button / public

**State:** BLOCKED. Rung 7 leans on the spot-broker (RunPod / Vast.ai) for
rented GPU capacity to generate ~50 VRMs in a batch. Rented compute is on
CLAUDE.md's blocklist this session — the Retracted Condition 5 paragraph
records the funding retraction (2026-09-02, this session). Rungs 8-9 sit
downstream of the pool rung 7 would produce.

- Skips counted: 3 (all blocklist-blocked, not env-blocked).

## Summary

| Rung | State | Wall-clock | VRAM peak | Skip reason |
|---|---|---|---|---|
| 0 OmniGen2 text→image | RUNNABLE | 10 min/img | 7 GB (offload; 24.85 GB RSS) | — |
| 1 Pixal3D image→mesh | SKIP | — | — | no env |
| 2 EditScore judge | RUNNABLE | 30-60 s/eval | ~15.5 GB | — |
| 3 VoxHammer repair | SKIP | — | — | no env |
| 4 SkinTokens skin | SKIP | — | — | scaffold, NotImplementedError |
| 5 See-Through tag | SKIP | — | — | no env |
| 6 seed→VRM | SKIP | — | — | no wrapper |
| 7 pool | BLOCKED | — | — | spot-broker (RunPod/Vast) blocklisted |
| 8 roll button | BLOCKED | — | — | downstream of 7 |
| 9 public | BLOCKED | — | — | downstream of 7 |

**Skips: 6 (four env-owed, one scaffold-owed, three blocklist-blocked).**
Working rungs: 2 of 10.

**Bottleneck for end-to-end:** the interface between rungs 1 and 2. The
ladder writes "prompt → mesh → judged" but EditScore takes images not meshes.
A mesh-to-projection step or a mesh-scorer variant is missing from the RFD
and from the code. This is a design decision to resolve before the ladder
can actually run rungs 1 and 2 in sequence, independent of whether the
Pixal3D env is standing.

**Recommended next actions, in order:**

1. Author `pixi.toml` for `pixal3d-image-to-textured-mesh` and
   `voxhammer-image-mesh-editing`. Same dep matrix as
   `omnigen2/pixi.toml` (torch 2.6 cu124 + windows wheels), documented in
   memory note `windows-torch-2.6-dep-matrix`. Each 30-60 min setup.
2. Decide the rung 1 → rung 2 handoff (mesh-to-image projector, or teach
   EditScore to score meshes). This is an RFD-level question, not code.
3. Implement `SkinTokens._run_upstream()` per RFD 0046 to close the rung 4
   scaffold. Half-day of porting; the upstream repo is MIT-clean.
4. Stand up `seethrough-partseg` and write the seed-to-VRM assembler
   (rungs 5 and 6 together — they share the tag-primvar contract).
5. Rungs 7-9 wait for either the rented-compute constraint to be relaxed
   (a separate decision the CLAUDE.md paragraph is careful to leave to whoever
   funds it) or a re-scoping of "pool" to what the desk 3090 can produce
   overnight (~5 VRMs at rung 0's rate, assuming rungs 1-6 average faster
   than rung 0).

## Cross-session note

The peer session's stack list (Wan-VACE 14B video, Qwen3-TTS voice, 7-track
ASR panel) is not RFD 2136 material. Those items describe a *different*
pipeline — likely a talking-avatar generation loop rather than the VRM
gacha. If the peer wants that pipeline measured, that's a separate RFD and a
separate logbook entry; this one is the ladder RFD 2136 defines.

## Follow-up RFD

The bottleneck at the rung 1 → rung 2 interface (mesh vs image domain) is a
real design gap in RFD 2136 itself, not an implementation gap. That warrants
a follow-up RFD or an amendment to 2136 spelling out the projector /
mesh-scorer choice.

This logbook was drafted by an AI and read by a human before it shipped.
