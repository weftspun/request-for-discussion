# RFD 1080 details: the apparatus, and what each number would mean

## The instrument is the card we have, and it is enough for this

An RTX 3090: 24 GB, sm_86, 2020. It is not a 4090, and there is no
high-performance inference pipeline on this desk. The machine also
carries a Radeon 780M, which is an integrated RDNA3 part sharing
system memory with no dedicated VRAM, so it is not a second candidate.

Neither fact blocks this measurement, because tolerance is not a
throughput question. It needs enough memory to hold two forms of one
stage at once, and it needs identical inputs. 24 GB gives the first
and a deterministic renderer gives the second.

Windows reports the 3090 as 4 GB through `Win32_VideoController`. That
is the 32-bit `AdapterRAM` field overflowing; `nvidia-smi` reports
24576 MiB. The wrong number is recorded here so nobody re-derives it.

## What is compared, and against what

| run | precision                    | purpose                                 |
| --- | ---------------------------- | --------------------------------------- |
| A   | bf16                         | the baseline, on this card, not a paper |
| B   | four-bit, DFC host emulation | what the device would compute           |

Same image, same seed, same fov in radians. `render_view.py` is
bit-reproducible at one thread: two runs, identical sha256, measured.

## The quantity

Surface deviation between the two meshes, in millimetres, paired with
a household object. A penny is 1.52 mm and a credit card is 0.76 mm,
so half a penny of error is a sentence somebody can act on, and "the
mesh looks fine" is not.

Report a distribution rather than one number: median, 95th percentile
and maximum. A mean hides the case that matters, which is a hand or an
ear moving while the torso stays put.

## What would make this a failure

No threshold is set here, on purpose. The RFD that consumes the mesh
should set it. What this produces is the number a threshold can be
written against.

## Why the DFC and not bitsandbytes

A general quantiser measures a four-bit. The device runs the Dataflow
Compiler's four-bit, with its own calibration and layer rules, and the
DFC ships a host emulator that runs that graph. The emulator is slow
and exact, which is the right trade when the question is numerics
rather than speed. `weftspun-hailo-dfc:5.3.0` is the image, built and
verified importable on 2026-08-22.
