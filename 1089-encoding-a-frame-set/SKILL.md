---
name: cineform-encode-a-frame-set
description: Build the CineForm pair, stand the bus up, and encode frames into one .mkv with a .cff beside it, including a held-segment sequence that shows corpus generation for one subject-pose. Use when a render sweep needs reviewing or delivering, and whenever somebody reaches for ffmpeg.
---

# Encoding a frame set

The result is one clip with a citation file, not a directory of images.
If the procedure ends with somebody scrolling a folder of PNGs, it was
not this procedure.

## Order

1. **Sync from the workspace manifest.** `repo sync` at the workspace
   root. The four dependencies live under
   `7-service/service-cineform/thirdparty/`: iceoryx2, cineform-sdk,
   libwebm and ftxui.
2. **Build the encoder**, from `3-interactor/interactor-cineform`:

       cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
         -DHARNESS_DIR=../../2-contract/bus \
         -DCINEFORM_DIR=../../7-service/service-cineform/thirdparty/cineform-sdk \
         -DLIBWEBM_DIR=../../7-service/service-cineform/thirdparty/libwebm
       cmake --build build --parallel

   `CMAKE_POLICY_VERSION_MINIMUM` is needed because cineform-sdk asks
   for CMake 3.5.1 and CMake 4 refuses below 3.10 without it.
3. **Build the display**, from `1-transport/transport-cineform-tui`,
   with `HARNESS_DIR`, `INTERACTOR_DIR` and `FTXUI_DIR` pointed at the
   same checkouts. One contract-bus, never two.
4. **Build the bus library once.** `python scripts/up.py` in
   `7-service/service-cineform` builds `iceoryx2-ffi-c` with
   `IOX2_TEMP_DIRECTORY` compiled in, which is why it cannot be
   installed from a package.
5. **Start the encoder yourself**, with the working directory set to the
   runtime directory and `WEFT_ICEORYX2_PATH` set to the library. Wait
   for it to say `listening`.
6. **Look at one frame of the subject before rendering ninety-six.**
   `--limit 1` renders a single pose and costs under a second. A subject
   that is wrong is wrong in every view, and the loop that produced it
   will not say so.
7. **Pack the frames as raw RGBA**, one frame after another, in the
   order the labels are numbered. Width times height times four bytes
   per frame, and check the file size against that product.
8. **Send the job.** `-s WxH`, `-frames N`, `-alpha`, and a frame rate
   chosen for review rather than for playback.
9. **Put the citation in the clip as a card**, opening and closing it:
   cff-version, title, authors, licence and the abstract. A frame that
   travels alone still says what it is and under what licence, which a
   file sitting beside the clip cannot do once they are separated.
10. **Name both files after the citation's title.** The `.cff` states a
   title; that title, lowercased with every run of non-word characters
   made a hyphen, is the filename stem for the clip and for the citation
   itself. `ANNY camera grid: 96 poses of one subject` gives
   `anny-camera-grid-96-poses-of-one-subject.mkv` beside
   `anny-camera-grid-96-poses-of-one-subject.cff`. Not `CITATION.cff`,
   and not a working name.

## Ordering a sequence, when the clip has to explain something

A sweep is one segment. A clip that shows how a corpus row is made is a
sequence of them, and the order is not a preference: each stage consumes
the one above it.

1. the photograph, or the rest pose when no fit is trustworthy
2. the keypoints detected in it
3. the pose definition, which is the numbers rather than a picture
4. the pose as a stick, joints joined to their parents
5. the pose labels, in the scheme's own colours
6. the cameras from `sphere_hammersley_sequence`, the measurement
7. the cameras from the 96-pose grid, the label
8. the PBR material
9. the style, which edits everything above and so comes last

**A residual cannot see a broken skeleton, and that is a claim about
the fit rather than about the frames.** The fit reported a median of
0.14 px on a 626 px stature, 0.022%, with bones passing through each
other. Seventeen detected points against 104 unconstrained rotations is
underdetermined: many poses project to the same pixels and the solver
has no reason to prefer an anatomical one. The referee cannot see it
either, because it measures the same reprojection.

WHAT IS NOT WRONG IS THE DATA. The rig was posed, the renderer put the
vertices where the rig said, and every joint label is exact whatever the
pose looks like. Those frames are ground truth by construction, and for
training a decoder or an autoencoder a folded limb is geometry the
reconstruction has to handle rather than a defect. That is the whole
reason a constructed corpus is worth rendering.

The bound matters for two narrower things, and saying which keeps this
rule from growing teeth it has not earned:

- **A pose prior.** A corpus whose poses a body cannot hold teaches a
  distribution the world does not have, which hurts anything learning
  what a pose usually is.
- **A correspondence claim.** "This render is that photograph's pose" is
  false when the solve folded a limb to reach the pixels, and that claim
  is what the loop scores.

So a fitted pose is not a corpus subject until something bounds the
joints, and the bound has two forms rather than one.

`2-contract/swing-twist-kusudama` is the authoring form: a Lean 4 and
Plausible simulation of `SwingTwistIK3D` with `JointLimitationKusudama3D`,
carrying the live humanoid rig as five chains, seventeen kusudama joints
and sixty-five cones. A cone is what a person can see and edit, which is
why the limits are authored there.

`3-interactor/physics` is the enforcing form: MuJoCo, with MJCF scenes
and the `mj_physics` wiring. Converted into that, the same limits stop
being an overlay and become physical, so a pose that folds a bone
through a body is refused by the simulation rather than by somebody
looking at a render.

The conversion is lossy: sixty-five cones over seventeen joints is more
expressive than a MuJoCo ball joint's single cone range, so a faithful
conversion needs more than one constraint per joint. That loss is
measurable rather than merely open, and EditScore is the judge: render
the same pose under the authored limits and under the converted ones,
from the same camera, and ask whether they are the same pose.

**EditScore needs its own noise floor before it judges anything.**
Measured here, three rounds scoring the same view of nearly the same
pose returned 2.53, 0.0 and 0.0. At NF4 it samples, so a difference
smaller than that swing is the instrument rather than the conversion.
Score one image k times, report the spread, and only then read a
comparison.

Pair it with the physical quantity, which is the rule this workspace
already keeps: millimetres of surface deviation between the two posed
meshes, and degrees at each joint. EditScore answers whether a viewer
would call it the same pose; the millimetres answer by how much it is
not. Neither substitutes for the other.

The range-of-motion data there is AddBiomechanics ROM, which is a
different use from the `.b3d` identity source CLAUDE.md blocklists.

Until that path exists, **start from the ANNY rest pose** when the clip
is about the pipeline itself, because it is clean and nothing was solved
to get it, and say in the clip why. When the corpus is for a decoder, a
rig-representable pose is already ground truth and needs no defence.

**A label plate takes the scheme's colours, never a palette of yours.**
`rfd107a-rule1-labels/anny-keypoint-colours.json` carries an sRGB triple
per joint and an `encoding` block that says what the colour MEANS: OKHSL
at s = 0.95, hue is the see-through layer the joint drives, lightness is
its position along the chain within that layer, 12 degree jitter, and
filled against hollow is unoccluded against occluded. Read the file and
index it by joint name.

A golden-ratio hue sweep looks similar and carries none of it: two
joints of one limb land on opposite sides of the wheel, and the plate
stops being evidence for anything. The stick takes the same colours, so
a bone group is one hue in both plates. If occlusion is not computed,
draw everything filled and say so on the plate rather than implying a
test that did not run.

**One subject and one pose, all the way down.** Every plate is drawn
through that fit's own camera. Borrowing another pose's label plate
because it is already rendered produces a clip that looks right and
shows a chain that never happened.

**Hold a still for about three seconds and a card for two and a half.**
At 8 frames per second that is 24 and 20 frames. A sweep is the
exception: it is played one frame per view, because a sweep is motion.

**A stage with nothing behind it gets a card saying so.** Two of the
nine here are absent: no textured render exists for the subject, and no
style edit was run on that pose. A Monet transfer of some other subject
dropped into slot 9 would imply a chain that does not exist. Name the
script that would produce it and say it has not been run.

## Run it as a plan, not as a list you follow

`domain.ex` and `problem.ex` beside this file are a taskweft domain for
the whole delivery. Use them rather than working the Order by hand,
because the Order is a list somebody can stop halfway through and then
report as done, which happened three times in one session: the frames
rendered, the encode never ran, and the word used was "re-rendered".

The domain makes that impossible to report by accident. `delivered` is
the goal and only `verify_delivery` sets it, after reading four earlier
results rather than trusting the steps ran: conventions complete, frame
count equal to the count asked for, a clip, and a citation. A run that
stops after rendering leaves `delivered` false and names the step that
did not run.

    plan(domain: "cineform_delivery", problem: "…/problem.ex")

taskweft is at github.com/taskweft/taskweft and serves `plan` and
`validate` over MCP. RFD 1025 gives the DSL and the type rules: there
is no `:string`, so a subject, a rig and a file handle are each `:ref`.
Both files are real Elixir, so `Code.string_to_quoted/1` checks them
with no planner, which is the check to run before asking for a plan.

Write the solved plan to `plan.ex` beside the domain and regenerate it
when the domain changes. A hand-written plan is allowed: RFD 1025 said
never, and retracted that on 2026-08-25, because the planner serves over
MCP and a desk that cannot reach it was left with a domain it could not
run. Say in the file which way it was made. The guards still hold at run
time, so a hand-written plan that violates one fails there.

## Traps

**Do not run `repo init` inside a project.** It walks up, finds the
workspace client and re-points the goal manifest at that project,
reporting only that it initialised somewhere else. Recover with the
manifests reflog.

**Do not background `up.py` and expect an encoder.** It starts the
encoder as its child, so the encoder dies with the wrapper and the next
command waits on a service that is not there, silently. Build with it,
then start the binary yourself.

**iceoryx2 prints Win32 warnings on Windows and keeps working.**
`FindNextFileA ... there are no more files` and `RemoveDirectoryA ...
the directory is not empty` are directory-scan noise from the PAL, not
failures. Judge by whether the encoder says `listening`.

**60 frames per second is not a review rate.** Choose it from the
structure of the set: a 96-pose grid of 8 azimuths reviews well at 8,
where each second is one sweep.

**The clip is visually lossless and is not bit-exact.** A per-frame
sha256 in a sidecar names the PNG, not a decoded frame. Say so in the
`.cff` rather than letting a reader assume the hash survives.

**A title built from a count collides.** `ANNY camera grid: 96 poses of
one subject` names the grid and not the subject, so a second subject
through the same grid writes the same filename and overwrites the first
in any directory holding both. The title carries what varies.

**Frames are not a delivery, and "re-rendered" is not a status.** A
render is the expensive step, so it is the one that gets reported, and
the cheap steps after it are the ones that get skipped: pack, encode,
citation. Check the clip's own timestamp against the frames' before
saying a set is current. In this session the clip was 28 minutes older
than the frames it claimed to show.

**A working name outlives the work.** `grid96-anny.mkv` says what the
directory was called on the afternoon it was made. The citation already
carries a title written for a reader, so the file takes it, and a
deliverable whose filename and whose stated title disagree makes a
reader ask which one is the asset.

**ffmpeg is not in this stack.** It is LGPL, and the pair above is
Apache-2.0 or MIT end to end.
