# Logbook: two DFC emulation contexts disagree by six orders of magnitude

Apparatus: `weftspun-hailo-dfc:cuda`, Dataflow Compiler **5.3.0**, on the local 3090 through
`docker run --gpus all`. Graph: two 1x1 convolutions and a ReLU, 256 -> 256 -> 64, authored
with `onnx.helper` at opset 17, `onnx.checker` clean, translated with
`translate_onnx_model(hw_arch="hailo10h")` and optimised against 1024 random calibration
samples at full optimisation level. Probe scripts under
`scratchpad/mezo/probe{1..6}.py`. **No inference in this entry ran on the Hailo-10H itself.**

Chasing whether MeZO -- zeroth-order optimisation, which estimates a gradient from
`[L(t+ez) - L(t-ez)] / 2e` and needs no backward pass -- can adapt a LoRA while the frozen
base sits on an inference-only accelerator. The device cannot compute a gradient; the
question is whether it needs to.

## The result that matters is that the instrument contradicts itself

Same graph, same precision `a16_w16`, same script, same 48 perturbation draws. Only the
inference context differs.

    SDK_QUANTIZED                          SDK_BIT_EXACT

    eps      sign      r     ratio         eps      sign      r         ratio
    3e-02   95.8%  +0.993     1.0x         3e-02   43.8%  -0.258      75,134x
    1e-02   95.8%  +0.988     1.1x         1e-02   39.6%  -0.033     200,035x
    1e-03   79.2%  +0.669     1.2x         1e-03   45.8%  -0.180   4,156,505x

`sign` is agreement between the quantised zeroth-order estimate and the float one on the
same `z`; `r` is Pearson correlation over the 48 draws; `ratio` is median `|g_quant|` over
median `|g_float|`.

**Correlation +0.99 becomes approximately zero. Sign agreement 96% falls below chance. The
estimate's magnitude is wrong by five to six orders of magnitude** -- `|g_quant|` reaches
89.6 where the true gradient is 2.16e-05.

**The two contexts agree exactly on the unperturbed output.** Both report
`start loss = 1.7700e-03`, identical to five figures. They diverge only under perturbation,
which is the regime the whole method depends on.

## Two of three precisions cannot run bit-exact at all

    a16_w16   ran
    a16_w4    FAILED  AttributeError: 'function' object has no attribute 'set_wraparound_loss'
    a8_w8     FAILED  InferenceError, graph execution error at conv2_1/act_op_1/pow

The first is a missing attribute inside the DFC, nothing to do with the graph submitted. The
second reproduced across two separate runs and lands at the **default** precision, on the
`pow` inside an activation op.

So the context whose name claims agreement with hardware is the one that crashes on two of
three configurations, including the one a deployment would use.

## What this does and does not establish

**It does not establish that MeZO fails on Hailo.** `SDK_BIT_EXACT` producing a gradient
magnitude of 89.6 against a true 2e-05, while crashing elsewhere, reads as a broken path
rather than a measurement.

**It does not establish that MeZO works on Hailo.** The +0.99 correlation came from
`SDK_QUANTIZED`, which the other context contradicts.

**It establishes that DFC 5.3.0's two emulation contexts disagree by six orders of magnitude
on one graph at one precision**, and that neither can be used as an oracle for the other.
CLAUDE.md's three-oracle principle is exactly the shape of the problem: two disagree and
there is no third.

The third oracle is the device. `SDK_HAILO_HW` needs `hailo_platform`, which is not on PyPI,
is not shipped with the HailoRT 5.3.2 install -- `lib/` holds `libhailort.lib` and cmake
files only -- and lives behind Hailo's developer-zone login. `hailortcli` cannot substitute:
`run2` generates its own random inputs and offers no input file or output dump, only
`--json` statistics.

## Retractions, in order, because three conclusions were drawn and two were wrong

**"The quantised graph is locally flat."** Withdrawn. Probe 1 measured `max|d output|` on 64
outputs from one sample and found a staircase: the response pinned at 1.134e-02 for three
different epsilons, then exactly zero below 1e-03. True, and the wrong quantity. MeZO
consumes a scalar loss summed over a batch, where individual quantisation steps partly
cancel. Probe 2 measured that: at eps=1e-05 only **17 of 16,384** outputs moved, and the mean
over them still moved. Aggregation rescues what a single output cannot show.

**"MeZO fails at a16_w16."** Withdrawn. Probe 3 set the target to the model's own output,
placing it at an exact minimum where the true gradient is ~0 -- `|g_float|` was 6.1e-11, near
fp32 noise -- and no estimator wins there. That is harsher than MeZO's regime, which is
low-but-nonzero loss on a pretrained model. Probe 5 offset the target to a real loss of
1.85e-03 and the correlation appeared.

**"MeZO works at a16_w16."** Withdrawn by this entry. It was measured under `SDK_QUANTIZED`
only.

## Facts collected along the way that outlive the question

**The Hailo-10H has no floating-point mode.** The DFC's `PrecisionMode` enum is
`a8_w8, a8_w4, a16_w16, a16_w8, a16_w4, a8_w4_exp, a16_w16_non_zero, native, a8_w8_a8,
a8_w8_a16, a8_w4_a8, a8_w4_a16, a16_w16_a8, a16_w16_a16, a16_w8_a8, a16_w8_a16, a16_w4_a16,
a16_w4_a8`. Every deployable entry is integer; `native` is the emulator's float reference and
does not compile to a HEF. So `a16_w16` is the ceiling and bf16 is not a setting to find.

**The DFC runs quantisation-aware finetuning during full optimisation.** At lower precisions
the log prints `_distill_loss_tiny/conv2: 0.0291` over 128 steps -- a distillation pass
teaching the quantised graph to match the float one. That is QAFT, inside the vendor's
compile step, for work this workspace was separately planning to do by hand.

**`conv_a16_w4` and `llm_modifications` are pre-quantisation features.** Hailo ships
LLM-specific handling in the optimiser and a 16-bit-activation / 4-bit-weight convolution
path, which is the shape a quantised decoder deploys in.

## The device, measured while it was to hand

`efficientnet_lite0.hef`, single context, compiled by DFC 5.3.0, on the UGen300 over USB
after moving it off a 1.5A port to a USB4 dock:

    steady-state throughput   ~1168 FPS   (1177.4 / 1174.0 / 1153.9, spread 2%)
    HW latency, NN core       2.27 ms
    overall latency           3.95 ms
    USB crossing cost         1.68 ms, 43% of end-to-end
    chip temperature          38.7 - 41.7 C

The crossing cost is RFD 1130's central quantity. It amortises under pipelining -- 1168 FPS
is 0.86 ms per frame against 3.95 ms for a lone frame -- so throughput is not the constraint
at video rate, and the two-device question turns on whether two HEFs fit 8 GB resident
rather than on speed.

`measure-power` and `measure-current` both report "not supported" on this device and
`monitor` does not run on Windows, so temperature is the only proxy available and RFD 1130
should not promise a power figure.

## THE DEVICE RUNS WHOLE LLMs AND VLMs, AND THIS ENTRY SAID OTHERWISE

Everything above treats the Hailo as able to serve a vision encoder and not a decoder, on
the reasoning that an autoregressive decoder carries dynamic shapes and a KV cache and an
HEF is a static forward graph. **That is wrong, and it was wrong on the evidence used to
support it.**

`C:\Program Files\HailoRT\include\hailo/genai/` ships three headers -- `llm/llm.hpp`,
`vlm/vlm.hpp`, `speech2text/speech2text.hpp` -- and the surface is a complete generation
stack:

    LLMParams::set_model(const std::string &hef_path, const std::string &lora_name = "")
    LLMGeneratorParams   temperature, top_p, top_k, frequency_penalty,
                         max_generated_tokens, do_sample, seed
    LLMGenerator::write(const std::string &prompt)
    LLMGeneratorCompletion::read()          incremental token streaming
    VLMParams(hef_path, optimize_memory_on_device)
    VLMGenerator                            prompt plus input_frames

**A LoRA is a named parameter on the model, not something merged before compilation.**
`genai/common.hpp` defines `BUILTIN = "<builtin>"`, so a HEF carries model and adapter
metadata and an adapter is selected at load time.

**The evidence that produced the wrong claim was `hailortcli --help`.** Its nine verbs --
`run run2 scan benchmark measure-power monitor parse-hef fw-control logs` -- are all
inference or diagnostics, and the argument went from there to a claim about the silicon. The
CLI exposes **no genai verbs at all**, so it was the wrong instrument: `libhailort.dll`
carries 285 mangled genai symbols the command line never mentions. Reading a library's
capability off its bundled CLI is rule 1 -- the convenient proxy, and it lied.

**What survives.** No training. There is no backward pass, no gradient and no optimizer
anywhere in the API, so `adapt` still has no path onto this device and the CPU blocklist
row's closing paragraph stands. What does not survive is every statement in this entry and
in that row's neighbours about `ask` being limited to an encoder.

**What it costs to use.** GenAI is C++ classes; the DLL exports no `extern "C"` entry points
for it, so ctypes cannot reach it. Three ways in: Hailo's `hailo_platform` wheel, which needs
a developer-zone login; a small `extern "C"` shim over `LLM` and `VLM` compiled against
`include/` and `libhailort.lib`; or C++ directly. The plain C API -- `hailo_create_vdevice`,
`hailo_create_hef_file`, the vstream calls and `hailo_infer` -- **is** `extern "C"` and
reachable from ctypes today, which is enough to put the MeZO probe on real hardware and not
enough for the generation path.

## Worth reporting upstream

`set_wraparound_loss` is an outright missing attribute on a function object, reached through
`load_model_script("quantization_param({*}, precision_mode=a16_w4)")` followed by `optimize`.
It is not a misuse of the API by the caller.
