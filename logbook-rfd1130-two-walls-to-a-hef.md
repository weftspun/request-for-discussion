# Logbook: two walls between a translated graph and a HEF

RETRACTED IN THIS ENTRY, ALL THREE MINE. That the Dataflow Compiler
found "no suitable GPU" was a container started without `--gpus all`,
not a machine without a card. That fine-tune batch size was the lever
for the video-memory wall: it is not, and `batch_size=1` fails the same
way. That NATTEN has no sm_86 kernel and a rebuild cannot fix it:
the failing run installed a prebuilt wheel, and Pixal3D's README
step 3 builds NATTEN for the architecture you name.

Question: what stands between `backbone_576.hailo10h.har`, which the
compiler already accepts, and a HEF the UGen300 can run.

## The apparatus

The device is an ASUS UGen300, `usb/004:013`, HAILO10H, firmware
5.3.2 after `hailo_usb_loader fw-update`. HailoRT-CLI 5.3.2 at
`C:\Program Files\HailoRT\bin`. It is a USB gadget on
`VID_0B05&PID_1D6F`, so no rented machine can see it and no
compile needs it -- `gate_dfc_parse.py` says as much in its docstring.

The desk is Windows 11 on a Framework Laptop 13, Ryzen 7 7840U, 16
logical cores, 64 GB, with an RTX 3090 (24 GiB, sm_86) attached.
Docker Desktop and WSL2 share one virtual machine and one memory
ceiling.

The compiler is `weftspun-hailo-dfc:cuda`, DFC 5.3.0 on Ubuntu 22.04
and Python 3.10, built from
`3-interactor/rf-detr-cpp/deploy/hailo-dfc/Dockerfile`. The wheel is
`py3-none-linux_x86_64` and gated, so the container is not optional
on this desk.

    docker run --rm --gpus all -v <scratch>:/mnt -v <scripts>:/ws:ro \
      weftspun-hailo-dfc:cuda /opt/dfc/bin/python /ws/compile_hef.py \
      /mnt/backbone_576.hailo10h.har --calib /mnt/calib_576_1024.npy \
      --opt-level 2 --finetune-batch 1 --out /mnt/backbone_576.hef

Inputs: the graph exported by `gate_onnx_device.py --num-windows 1
--resolution 576` at 825 nodes and 22 operators, `max|diff|`
3.099e-06 against PyTorch; the HAR from `gate_dfc_parse.py`, parse OK
with no operator outside `DEVICE_OPS`; and calibration from
`prep_calibration.py` over `coco_images_train2017`, 1024 frames of
576x576x3 uint8, 1019 MB, the blinded holdout re-asserted at read.

## The device, before any of this

`hailortcli run` is refused on a USB device -- it says to use `run2`.
Latency and rate cannot be measured in one pass, because
`--measure-latency` sends frames singly and says so.

    efficientnet_lite0, zoo v5.3.0, 224x224x3
    hw latency          2.272 ms
    overall latency     4.452 ms
    steady state        1274.68 fps, 982 GOPS
    chip temperature    35.1 C to 38.9 C over two 10 s runs

Derived: 2.180 ms of that round trip is host and bus, 49 per cent,
and it is paid per inference whatever the model. At 151.5 KB a frame
the bus sits at 16 per cent of its 1.2 GB/s, so nothing here is
bandwidth-bound. A v5.4.0 HEF also runs on the 5.3.2 runtime, at
1276.40 fps, so a newer compiler does not require a newer runtime.

## Wall one: system memory

`Statistics Collector` took SIGKILL at Docker's 30.26 GiB. WSL2
showed the same 30 GiB, both being one VM under an absent
`.wslconfig`, so moving to WSL would not have helped.

    [wsl2]
    memory=48GB
    processors=16

then `wsl --shutdown` and a Docker Desktop restart. Docker reported
47.04 GiB afterwards. The stage then completed in 14:58 and the run
peaked at **39.87 GiB**, above the old ceiling, so the lift was
load-bearing rather than precautionary.

Measured with `docker stats --no-stream --format '{{.MemUsage}}'` on
a 4-second loop. The first sampler ran a fixed 900 iterations and
stopped after an hour, reporting 22.55 GiB; that was a lower bound on
a run still going, and reporting it as the peak was wrong.

## Wall two: video memory

    AccelerasResourceError: GPU memory has been exhausted. Please try
    to use Quantization-Aware Fine-Tuning with lower batch size.

Quantization-aware fine-tuning is training: four epochs of gradient
steps over the calibration set, which is why RFD 1164 says a
calibration set is training data. It exhausted the 3090's 24 GiB at
the default batch after about thirty minutes of epoch 1 of 4.

The directive `post_quantization_optimization(finetune,
policy=enabled, batch_size=1, epochs=1)` over 64 frames raised the
same error after 44 minutes, with the directive verified in the
loaded model script. So batch size is not the lever at the bottom of
its range, and this desk cannot fine-tune a 25.245 M device half in
24 GiB.

`optimization_level=1` skips fine-tuning and also drops compression
to 0, which the compiler says out loud. That is a different artifact,
not a cheaper one.

## The rented card

RunPod, REST at `rest.runpod.io/v1`, per RFD 1140. Requested 48 GiB;
received an A40 with 46068 MiB, 503 GB of system memory and 96 vCPU,
at 0.44 US dollars an hour. Ubuntu 22.04, Python 3.10.12, which
matches the container's own pair.

Two setup costs, both paid once. A bare `nvidia/cuda` image runs no
sshd, so `dockerStartCmd` installs and starts one. And revoked
account SSH keys leave `$PUBLIC_KEY` empty, which reads as a refused
key; injecting the public key through the pod's `env` and restarting
fixes it without touching the account.

Transfer was 1.64 GB over scp in 2m24s: the 522 MB wheel, the 102 MB
HAR, the 1019 MB calibration array and the script.

## Two gates, each with a control that fails

`tensorflow[and-cuda]==2.19.1` was needed on top of the DFC's own
pin: the base image's cuDNN is not the one TF loads, and the symptom
is `No DNN in stream executor` on the first convolution while
`list_physical_devices` still reports the card.

So the gate asserts on the device a tensor lands on, with soft
placement OFF, because soft placement makes a `/GPU:0` scope fall
back to CPU and pass on a machine with no GPU at all.

    positive  gpus=1 ran=True device=/GPU:0        ok
    negative  CUDA_VISIBLE_DEVICES=""  raised      ok
    PASS      the check works in both directions

osquery 5.23.1 runs as `osqueryd` on the pod and supplies process and
memory state. `memory_info` exists on Linux and not on Windows, which
is why the same query failed on the desk. Its own gate is five checks
of which three are negative controls, and the third is the one worth
keeping: a query against a nonexistent table must be REJECTED rather
than return zero rows, because a row-counting check cannot otherwise
tell a typo from an empty result.

## Stage times, desk against pod

    stage                     desk 3090      pod A40
    Mixed Precision              2.43 s       1.72 s
    LayerNorm Decomposition      2:14         2:41
    Statistics Collector        14:58         7:09
    Translate Parameters        11:29         running

The pod is not uniformly faster. LayerNorm Decomposition is slower on
96 slower cores than on 16 quicker ones, and over a 90-second sample
during it the A40 peaked at 1 per cent utilisation holding 4389 MiB.
Most of this pipeline is CPU work. The card is rented for one stage.
