# RFD 1134 details: Running loop 1 in the browser

The apparatus, the failure text, and the defects that the first run found.

## The server

The command in the project README does not start the server on this desk.
`mix run --no-halt` runs in the dev environment. Livebook's endpoint is
compiled there with code reloading on, and `phoenix_live_reload` is a
dev-only dependency of Livebook that this project never fetches. The boot
ends with this:

    ERROR!!! [Livebook] shutdown: failed to start child: LivebookWeb.Endpoint
        ** (EXIT) an exception was raised:
            ** (UndefinedFunctionError) function
            Phoenix.LiveReloader.Socket.child_spec/1 is undefined

`MIX_ENV=prod mix run --no-halt -e 'IO.puts ServiceLivebook.start()'`
serves. It printed
`http://localhost:8080/?token=pzodiirf3iumgvvni2fculpsmf2mx4kb`, and
`/public/health` returned 200.

## The browser

Playwright 1.62.1, Chromium 151, headed, on the desk display. The launch
script holds the window open and opens a debug port:

    chromium.launch({headless: false,
                     args: ['--remote-debugging-port=9222']})

Each later step calls `chromium.connectOverCDP('http://localhost:9222')`
and takes the open page. The window stays under the person's hand.

The open route needs an absolute path. A path written as a string literal
loses its backslashes to escape sequences, and `7-service` becomes a bell
character. Livebook then redirects to the open dialog and reports nothing.
Join the parts instead:

    ['C:', 'weftspun-keypoint', '7-service', 'service-livebook',
     'notebooks', '1-keypoints-to-anny.livemd'].join(sep)

## The run

Loop 1 holds 20 cells, 11 of them code. Escape, then `e`, then `a` ran
them. The states after the run:

| cell | content                        | state                    |
| ---- | ------------------------------ | ------------------------ |
| 0    | `Mix.install`                  | Evaluated, 1.0 s         |
| 1    | `pyproject.toml`               | Evaluated, CPython 3.11  |
| 4    | paths and `weft_loop` import   | Evaluated                |
| 5    | `PHOTO`, `WORK`                | Evaluated                |
| 7    | `detect`                       | Evaluated                |
| 9    | `propose`, `score`             | Evaluated                |
| 12   | the fit                        | Evaluated, traceback     |
| 14   | `residuals_by_region`          | never ran                |
| 16   | `report`                       | never ran                |
| 18   | `run(propose, score, ...)`     | never ran                |
| 19   | provenance                     | never ran                |

Cell 12 reported this:

    Traceback (most recent call last):
      File "<string>", line 3, in <module>
      File "priv/python/loop1_fit.py", line 38, in <module>
        import torch
    ModuleNotFoundError: No module named 'torch'

## The defect this exposes

The notebook states that every cell which touches the card is a
subprocess into a pixi environment. Cell 12 is not. It imports
`loop1_fit` into the notebook's own Python process, and `loop1_fit`
imports torch at module level. The setup cell declares pillow, numpy and
matplotlib. So the fit cannot run in the notebook as written, and the
reason is not the missing detector.

Two repairs are open, and this document records both rather than picking
one.

- Run the fit as a subprocess into the `anny` pixi environment, which
  holds torch. This keeps the rule the notebook already states, and it
  moves the fit result across a file.
- Declare torch and roma in the setup `pyproject.toml`. This keeps the
  fit in process, and it makes the notebook boot download a large wheel
  set that the pixi environments already hold.

## A second defect, found by reading

The prose in loop 1 reports a round trip median of 1.19 px on a 591 px
stature, which is 0.202% of stature. The provenance cell in the same
notebook records 1.56 px and 0.263%. One of the two is stale. The run
above could not settle it, because the cell that would recompute it never
ran.

## The repair, and the second run

The repair chosen is the pythonx one. The setup `pyproject.toml` cell now
declares `torch>=2.6`, `anny` and `roma` beside the three packages it
already held. CLAUDE.md blocklists `uv` for project environments and
exempts an embedded interpreter that pins its dependencies in source.
This cell is that exemption. The pins travel with the notebook, and a
reader rebuilds the environment from the file.

The server was restarted so the session read the new file. Livebook holds
the notebook in memory and shows no notice when the file changes on disk.

The second run reached further. `build_model` and `bone_names` ran in the
notebook's own interpreter, and the fit cell stopped 22.9 s later at line
7 with the refusal the code already carried:

    weft_loop.PreconditionFailed: no environment here carries rfdetr

So the torch defect is closed and the detector gap is now the first
blocker, which is the state the notebook prose already describes. Cells
14, 16, 18 and 19 stayed queued a second time. They are NOT_RUN, and no
number is reported for them.

## The round trip, re-measured

`test_loop1_fit.py` ran in the `anny` pixi environment on 2026-08-25:
median 1.193 px on a 591.1 px stature, 0.202% of stature, 3.44 mm on a
1.7 m body, about two stacked pennies. It took 2.3 s on CPU at 60 LBFGS
iterations over 104 points. Shuffled targets reach 233.039 px. All five
referee regions fill: 31 body, 30 feet, 20 per hand and 3 face.

The prose figure was right and the provenance figure was stale. The
notebook now carries 1.193 px in both places, and the retracted 1.56 px
stays beside it in the provenance record.

## The detector, and a retraction of the paragraph above

Installing `rfdetr` in the setup cell closed the import error and showed
what it had been hiding. `RFDETRKeypointPreviewConfig` in rfdetr 1.9.4
carries `num_keypoints_per_class = [17]`. The published preview model is
COCO-17. No fullbody checkpoint ships, so the notebook's own claim that
the detector is the fullbody one is retracted, in the notebook and in
`loop1_fit.py`.

A 17-row target cannot use the 104 bone names, and `fit_2d` refuses that
pairing by design. It goes through the 23-point regressor instead.
`coco_regressor` returns the regressor and its first 17 labels, and it
checks those labels against COCO's order rather than trusting them. A
reordered `coco.pth` would otherwise fit each point to the wrong joint
and still report a small residual.

## The 1.56 px figure was not stale, and this retracts that call

The section above says the provenance cell held a stale number. That was
wrong. The two figures measure two vocabularies:

| vocabulary            | median   | of stature | on a 1.7 m body     |
| --------------------- | -------- | ---------- | ------------------- |
| ANNY bone joints, 104 | 1.193 px | 0.202%     | 3.44 mm, two pennies |
| COCO-17, regressor    | 1.555 px | 0.263%     | 4.48 mm, one pencil  |

The prose recorded the first and the provenance cell recorded the second.
`test_loop1_fit.py` now runs both round trips, so neither figure can be
mistaken for the other again. Shuffled targets reach 233.039 px and
111.844 px. The notebook carries both, each named by its vocabulary.

## A wrist is not a hand

The 17-point control found a defect in `region_of`. `HAND_MARKERS` held
`wrist`, so a COCO-17 target filled `left_hand` and `right_hand` with one
point each. The referee would then judge a hand from a single boundary
joint and report a region rather than NOT_RUN. That is the pass a missing
region exists to prevent.

`wrist` is out of `HAND_MARKERS`. The fullbody vocabulary loses nothing,
because it carries 19 further points per hand. The counts move from 31
body and 20 per hand to 33 body and 19 per hand. A 17-point target now
fills body, face and feet, and both hands stay NOT_RUN.

The control that found it is a negative control and it stays: the test
fails if either hand region fills from 17 points.

## The third run, and the two gaps it reached

`rfdetr` in the setup cell reaches the checkpoint, and the notebook then
found a data defect before a code one. At threshold 0.4 the detector
returns nothing for `hv_0.png`, which was the notebook's default photo.
Measured over the three renders at 1024 by 1024: `hv_0` gives 0
detections at 0.4 and 2 at 0.2, while `hv_1` and `hv_2` give one person
at 0.999 and 1.000. The default is now `hv_1.png`.

The fit then ran in the browser and printed a median of 0.34 px on a 508
px stature, 0.07%, over 17 of 104 points. That number is not evidence of
a correct pose. Seventeen points constrain 104 bones loosely, so the
solve is underdetermined and a small reprojection error is what an
underdetermined fit gives. The referee answers NOT_RUN, which is the
honest verdict.

Cells 12, 14 and 16 evaluated. Cell 18 stopped, and it names the next
gap: `propose` shells into the `anny` pixi environment to run
`render_view.py`, and that environment reports

    ModuleNotFoundError: No module named 'drjit'

`mitsuba` is a dependency of the corpus repository's default feature, and
the `anny` environment sets `no-default-feature = true`, so the renderer
is not in the environment the loop calls. Behind that sits a second gap
already recorded above: `propose` reads `fit_{i}.npz` and nothing writes
one. Neither is repaired here, because closing them is a design step
rather than a test step.

## The document completes, and the score is zero for a nameable reason

Every cell evaluates. The referee reports `NOT_RUN`, which is correct on 17
points. The three rounds report this:

    baseline 0.000 on hv_1.png
      round=1  iters=80   score=0.0  delta=0.0  35.2 s  scorer 28.0 s  6.74 GiB
      round=2  iters=120  score=0.0  delta=0.0  42.7 s  scorer 33.5 s  6.74 GiB
      round=3  iters=160  score=0.0  delta=0.0  40.4 s  scorer 25.9 s  6.74 GiB

Zero three times is not a converged loop. It is the loop measuring the
wrong thing, and the camera vocabulary says which thing in one line.

`propose` returns `rendered[0]`, and view 0 of the sequence is azimuth 0
with elevation -90: a camera directly underneath the body. In fal's
vocabulary that camera has no phrase at all, because the elevation bands
stop at -45. The scorer's own words for it were "the edited image shows
the person lying down".

So each round handed EditScore a view from beneath a standing figure and
asked whether it matched an upright photograph. The answer is 0.0, and it
is the right answer to the question that was asked.

Two things follow, and neither is repaired here.

- The scored view must be the one the fit claims. The fit solves a
  weak-perspective camera facing the subject, so the comparison belongs at
  that camera, not at whichever index the sequence happens to start on.
- Rendering the whole sequence stays. The rule is about what is rendered,
  never about which render is scored, and the two were conflated.

`describe_camera` in `weft_loop.py` names every view of the sequence, and
five of the eight have no phrase because they sit between the
vocabulary's elevation steps. That is a fact about
`sphere_hammersley_sequence` rather than a fault in either.

## The render found the defect the residual hid

Rendering the fitted mesh through 96 poses showed a body sprawled in every
frame. The cause is one interface, and it retracts every percent-of-stature
figure above.

ANNY's rest mesh measures X 1.046, Y 0.434, Z 1.660, so the rig is Z-up, and
`render_view` agrees with `up=[0,0,1]`. `fit_2d` projected `points3d[:, :2]`,
which feeds the body's DEPTH axis to image-vertical. Against an upright
target the solver's only way to match was to rotate the whole figure about
ninety degrees. `stature` read component 1 for the same reason, so residuals
were normalised by a depth of 0.434 where a height of 1.660 belonged.

The known-answer round trip could not catch it. It built its targets through
the same two axes, so it was wrong and self-consistent together, and reported
1.19 px while the pose it recovered was lying down. That is the sampled-check
failure in a different costume: a control that shares an assumption with the
thing it checks tests everything except that assumption.

`image_axes` now measures the axes off the rest pose and raises when the
longest extent is not clearly longest, and `to_image` negates the up axis
because image rows count downward and a positive scale cannot absorb a flip.

Re-measured, and these supersede the figures above:

| vocabulary            | median   | of stature | on a 1.7 m body      |
| --------------------- | -------- | ---------- | -------------------- |
| ANNY bone joints, 104 | 3.131 px | 0.212%     | 3.60 mm, 2.4 pennies |
| COCO-17, regressor    | 0.947 px | 0.064%     | 1.09 mm, one penny   |

The fitted mesh now measures X 0.526, Y 0.813, Z 1.544 against a rest height
of 1.660. It stands.

## The scorer is the next thing that needs a baseline

With the axes fixed and the comparison view chosen, the three rounds report:

    round 1  iters 80   score 2.530  view 16, 12.9 deg from a front view
    round 2  iters 120  score 0.000  view 16, 12.9 deg from a front view
    round 3  iters 160  score 0.000  view 16, 12.9 deg from a front view

Every round scored the same view of nearly the same pose, and the score moved
by 2.53 and back. That is not the extra LBFGS iterations. EditScore runs at
NF4 and samples, so the loop is currently measuring the scorer's variance.

Nothing here knows how large that variance is, because it has never been
measured: score one image k times and report the spread. Until that number
exists, a round-to-round delta from this loop is not a measurement, and
CLAUDE.md's rule is the one that applies -- a number without a baseline is
not a measurement, and the baseline for a noisy instrument is its own noise.

## The bound on a pose has two forms, and neither is wired in

The fitted pose that opened this work folds bones through each other at
0.022% of stature, so the residual does not see it and neither does the
referee. What would see it exists in this workspace, in two halves.

`2-contract/swing-twist-kusudama` authors the limits. It is a Lean 4 and
Plausible simulation of `SwingTwistIK3D` with `JointLimitationKusudama3D`,
holding the live humanoid rig as five chains, seventeen kusudama joints
and sixty-five cones, checked against Godot's own output. A cone is a
thing a person can see and edit, which is why the limits live there.

`3-interactor/physics` enforces them. It is MuJoCo with MJCF scenes and
the `mj_physics` wiring. Converted into that, a limit stops being an
overlay on a solver and becomes physical: the simulation refuses the
pose rather than a person noticing it in a render.

Two things are open, and both are numbers rather than opinions.

- **The conversion is lossy, and the loss is measurable.** Sixty-five
  cones across seventeen joints is more expressive than a MuJoCo ball
  joint's single cone range, so one constraint per joint cannot carry
  it. EditScore judges it: render one pose under the authored limits and
  under the converted ones, from the same camera, and ask whether they
  are the same pose. That is the loop this project already runs, pointed
  at the conversion instead of at a fit.

  It cannot be read until EditScore has a noise floor. Three rounds of
  this notebook scored the same view of nearly the same pose and
  returned 2.53, 0.0 and 0.0, so a difference smaller than that swing is
  the scorer and not the conversion. Score one image k times and report
  the spread first.

  Pair it with the physical quantity rather than replacing one with the
  other: millimetres of surface deviation between the two posed meshes,
  and degrees at each joint. EditScore says whether a viewer would call
  it the same pose. The millimetres say by how much it is not.
- **Neither half is wired into `loop1_fit`.** The solver runs
  unconstrained today, which is why the rest pose is the corpus subject.

The range-of-motion dataset in the kusudama project is AddBiomechanics
ROM. CLAUDE.md blocklists AddBiomechanics `.b3d` as an IDENTITY source,
for a narrow and inequitable population, and bounding a joint angle is
not that use. Worth stating so the row is not read as wider than it is.

## A correction: the frames were never the wrong part

The section above calls the fitted pose broken and says so plainly. It
is worth separating what that does and does not condemn, because the
first version of this record blurred them.

The renders are ground truth. ANNY was posed, the renderer put the
vertices where the rig said, and every joint label is exact whatever the
pose looks like. For training a decoder or an autoencoder, a folded limb
is geometry the reconstruction has to handle, not a defect in the data,
and that is the reason to render a constructed corpus at all: the label
is true by construction rather than annotated.

What was wrong was narrower, and it was a claim rather than a frame.

- **The correspondence.** "This render is that photograph's pose" is
  false when the solve folded a limb to reach the pixels, and that is
  precisely the claim the loop scores.
- **The prior.** A corpus whose poses a body cannot hold teaches a
  distribution the world does not have, which matters to anything
  learning what a pose usually is and not at all to a reconstruction.

So the rest pose is the right subject for a clip that explains the
pipeline, and a rig-representable pose needs no defence when the corpus
is for a decoder. Both were true at once and the earlier text implied
only the first.

## The two fitted subjects were deleted

`grid96-anny` and `grid96-anny-hv2` are gone, deleted on 2026-08-25 as
invalid poses. Between them they held 397 files and 115 MB: two posed
meshes, 192 rendered frames with sidecars, two citations and one clip.

The measurements they produced stay in this record because they are what
the runs measured, and the reader should know the sets behind them no
longer exist:

| subject  | median      | of stature | chest facing | why it went                       |
| -------- | ----------- | ---------- | ------------ | --------------------------------- |
| hv_1 fit | 0.17 px     | 0.033%     | 345.9 deg    | `.L` joints at +0.009, limbs cross |
| hv_2 fit | 0.14 px     | 0.022%     | 72.7 deg     | same class of fit                  |

Both are what an unconstrained 17-point solve produces, and both report
a residual small enough to look converged. The rest pose is the only
corpus subject until a joint bound exists, which is the state RFD 1137's
skill already describes and RFD 1138's question has to be answered
before it changes.

Nothing in the argument depends on the files. The conventions check
still refuses that class of rig, and `check_conventions.py` carries the
hv_1 numbers as the reason the feet are not the forward witness.
