# RFD 1082 details: the rig, and the confounds that will spoil it

## The device

ASUS UGen300: Hailo-10H, 8 GB LPDDR4, USB 3.1 Gen2 at 10 Gbps.
Frameworks accepted are Keras, TensorFlow, TensorFlow Lite, PyTorch
and ONNX, which in practice means a graph the Dataflow Compiler maps.

8 GB is the number that decides everything else. At bf16 the Pixal3D
checkpoints are 24.045 GB and nothing fits. At four bits they are
about 6 GB and the weights can stay resident, which turns the bus from
a per-inference cost into a one-off.

## The three quantities

| quantity                  | why it is not the others                     |
| ------------------------- | -------------------------------------------- |
| time to first output      | includes transfer, and is what a user feels   |
| steady-state rate         | excludes it, and is what a batch job gets     |
| transferred bytes         | predicts behaviour on a different bus         |

A single "frames per second" hides which of the three it came from,
and the three diverge by more than an order of magnitude on a USB
device.

## Confounds worth naming before they are discovered

**Thermal.** A USB stick has a small thermal budget. A rate measured
over ten seconds and a rate measured over ten minutes are different
numbers, and the second is the one that matters.

**Host contention.** USB 3.1 Gen2 is shared. A measurement taken while
the same controller carries anything else is not a measurement of the
device.

**Cold caches.** The first inference includes compilation, allocation
and transfer. Report it separately rather than averaging it away.

## What the comparison is for

The 3090 will win on rate and lose on power, and neither fact is
interesting on its own. The comparison exists so somebody can decide
where a stage runs, which needs the cost of moving data to it stated
beside the rate.

## What is not measured here

Accuracy. RFD 1080 owns that, and mixing the two produces a table
where a fast wrong answer looks good.
