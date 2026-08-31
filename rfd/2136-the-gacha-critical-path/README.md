# RFD 2136: The gacha critical path, as a ladder

**State:** discussion
**Feature:** the plan of record for the public roll button, as a ladder of small working systems
**Scope:** the gacha demo; `page.qmd` beside this file carries the figure

## Problem

The prior draft of this RFD ran a PERT network with a chain
A → I → D → E → G, and I → D skipped every step that turns a text prompt
into a mesh good enough to skin: no image-to-3D via Pixal3D, no
EditScore judge, no repair loop. A pull is not a gacha item without
those, so the network was drawing a schedule around a pipeline that
did not yet exist end to end.

## Decision

Rebuild the plan as a ladder, in Gall's Law's sense: each rung is a
small working system that the next one extends, and no rung is added
until the one below it demonstrably runs. That replaces the parallel
tracks with a sequence where every step shows something, and it
puts Pixal3D and EditScore on the spine where they belong.

The ladder, bottom to top:

0. **Language prompt → image.** OmniGen2 renders a reference image
   from a text prompt. Pixal3D takes an image, not text, so this rung
   is the ground the rest stands on. An image comes out.
1. **Image → mesh.** Pixal3D renders one mesh from the reference
   image on the desk 3090. A mesh comes out. Whether it is good is
   the next rung's problem.
2. **Prompt → mesh → judged.** EditScore scores the mesh against
   the prompt. A number comes out. Whether the number is trusted is
   the next rung's problem.
3. **Prompt → mesh → judged → repaired.** VoxHammer runs the repair
   pass on below-threshold meshes; they are rejudged and the loop
   bounds to N attempts. Every prompt yields a mesh with a passing
   score, or a recorded refusal.
4. **Prompt → passing mesh → skinned.** SkinTokens runs in skin-mode
   against the canonical ANNY skeleton and produces a rig that bends
   without collapsing (EditScore on posed frames is the QA gate).
5. **Prompt → skinned mesh → tagged.** The canonical See-Through
   partition (VALID_BODY_PARTS_V3, 23 tags; RFD 1121 audited) is
   recovered on the mesh by treating the mesh's partition as
   corruption: VoxHammer proposes repairs toward the canonical
   partition, EditScore judges each proposal, the loop bounds to N
   attempts. Written to the mesh as a per-vertex tag primvar. Parts
   are addressable.
6. **Prompt → tagged rig → VRM.** The seed-to-VRM assembly runs end
   to end from a single command: a portable, editable character file.
7. **Prompt list → pool.** The seed-to-VRM command runs against a
   list of prompts, gated by rent from the spot-broker when the desk
   is not enough. About 50 VRMs, judged and reproducible by seed.
8. **Pool → roll button.** A page with a roll button dispenses one
   VRM per pull, downloadable.
9. **Public.** The page is hosted with a sponsor link and an
   automation-disclosure page.

Each rung is a demo you can show. A rung is "done" when it produces
its output from the previous rung's output, and a control run on a
known-broken input fails. The order stays fixed: skipping a rung is
the failure mode this RFD replaces.

## Verification

`page.qmd` beside this file draws the ladder and pairs each rung with
its inputs, its output, and the negative control that certifies it.
The spend infrastructure the higher rungs lean on is live (RFDs
2133–2135); the two operator-side blockers (vast.ai key, broker
token) bite at rung 7, not before.
