# RFD 1163 details: what the accelerator can take, and what bounds it

## The division, and why it is forced

    RunPod, rented, Linux x86_64        the desk, Windows
    ----------------------------        -----------------
    OmniGen2 + anny-camera-lora
    EditScore, Qwen3-VL-8B at NF4
    RF-DETR keypoints, soma_referee
    Dataflow Compiler -> HEF     ---->  hailortcli run2, usb/004:013

Not a preference. The DFC wheel is `py3-none-linux_x86_64`, so it
never ran on this desk except in a container. A pod exposes no USB,
so the HEF cannot run there. Each half goes where it can go.

## What a round costs today

From `logbook-fourloops-first-runs.md`, on the desk card:

    stage                       memory        wall clock
    OmniGen2 bf16               14.75 GiB     131 s
    OmniGen2 NF4                 4.33 GiB     133 s
    EditScore NF4                6.75 GiB     28-36 s

A round is one propose and one score, so roughly 163 s, and scoring
is under a quarter of it. That quarter is the whole envelope the
accelerator could touch in Loop 2, and the vision encoder is a
fraction of the quarter again. RFD 1157 scores EditScore `value` 2
of 25 for exactly this reason, and this table is the reason.

Four bits bought memory and not speed here: 133 s against 131 s,
because dequantisation costs about what the narrower reads save.

## Why the card is rented rather than the desk endured

Input count, not resolution, is what the ladder costs.
`ladder_camera_obedience.py` measures A at 105 s, B at 182 s and C
at 529 s a view, so the eight-azimuth three-condition factorial is
about 3.6 hours. That is the shape RFD 1140 calls a sweep, and a
sweep wants batch rather than a pod that bills while it waits.

The desk fails this in the way RFD 1140 warns about rather than by
erroring. Two bf16 OmniGen2 pipelines want 29.5 GiB on a 24 GiB
card; both then run about fifteen times slower, and the only
symptom was a benchmark row taking 27 minutes instead of 131
seconds. `ladder_camera_obedience.py` refuses to start when
`nvidia-smi` reports more than 2000 MiB already in use, which is a
guard against that and not a preference.

## The first candidate, and where it already runs per image

`test_pose_survives_restyle.py` is the clearest place the detector
earns a HEF: it restyles each render with OmniGen2 and then re-runs
`RFDETRKeypointPreview` on the result to measure joint drift, so the
detector fires once per generated image rather than once per run.
`fit_ladder_azimuth.py` calls `loop1_fit.detect_keypoints` the same
way, per view.

That the two are separate executables is a rule rather than an
accident, stated in three files: a generator scoring its own output
is not a measurement. Moving the detector onto the accelerator does
not disturb that separation, because it changes where the check runs
and not who runs it.

Loop 1's `detect_keypoints` in `loop1_fit.py` wraps
`RFDETRKeypointPreview` at `num_windows=1`, which is the
configuration that clears `DEVICE_OPS` and costs a measured 1.35x
wall-clock against the checkpoint default of 2. Measured 2026-08-28:

    export      825 nodes, 22 operators, max|diff| 3.099e-06
    translate   parse OK, arch hailo10h, operators outside
                the allowlist: none
    compile     not reached; SIGKILL at 30.26 GiB
                ceiling lifted 2026-08-28: .wslconfig memory=48GB, WSL reports 47 GiB

The device half is 25.245 M parameters against the full model's
40.852 M, both counted rather than estimated. At bf16 that is
0.050 GB, about 0.6 per cent of the part's 8 GB, so memory was never
what stopped it.

## The EditScore correction

RFD 1157 was written against `Qwen3-VL-4B-Instruct`. `weft_score.py`
loads the **8B**, with adapter `EditScore/EditScore-Qwen3-VL-8B-
Instruct` and `score_range=25`:

    precision       size        against 8 GB
    16-bit          16.0 GB     no
    8-bit            8.0 GB     exactly on the ceiling
    4-bit            4.40 GB    fits
    NF4, measured    6.75 GiB   fits

So the deployed EditScore is four-bit-only in practice, and inherits
RFD 1128's open question that the 4B avoided.

What does not change is the finding. The 8B adapter carries the same
516 tensors as the 4B: 504 language-model layers and 12 at
`visual.deepstack_merger_list.{0,1,2}.linear_fc{1,2}`, with no
`visual.blocks.*`. `tools/mtmd/clip.cpp:3850` still puts the
projector inside the HEF, so a stock encoder is still silently wrong
for either size.

## The measurement this RFD does not have

Encode against decode, timed separately. Until that number exists,
the 28-36 s above bounds the score stage but not the encoder inside
it, and the case for compiling an EditScore encoder rests on a
fraction nobody has measured.

## Two things this does not fix

The detector is COCO-17. `loop1_fit.py` carries the retraction:
`RFDETRKeypointPreviewConfig` in rfdetr 1.9.4 has
`num_keypoints_per_class = [17]`, so there is no wholebody
checkpoint to read and the referee reports `NOT_RUN` for three of
five regions. A HEF compiles the same 17 points faster; it does not
widen them.

`publish_artifacts.py` refuses any name containing `nf4`, `int4` or
`int8`. A quantised HEF is an artifact under RFD 1141 and will meet
that list, so it needs a name that says what it is without saying a
precision, or that gate needs to learn the difference between a
quantised corpus and a quantised deliverable.

## Teardown

RFD 1140's rule is a verification step here rather than housekeeping.
Push before renting, tear down after, and check the tear down: the
HEF is the artifact, and a HEF that existed only on a pod did not
happen.
