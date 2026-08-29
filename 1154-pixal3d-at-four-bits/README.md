# RFD 1154: Pixal3D fits only at four bits, as a whole

**State:** abandoned
**Feature:** edge acceleration candidate
**Scope:** `3-interactor/pixal3d-image-to-textured-mesh`

## Problem

Pixal3D is 12.02 B parameters: 24.05 GB at bf16 and 12.02 GB at eight
bits against 8 GB of device memory, fitting only at four bits and
6.61 GB. One precision reaches it, so RFD 1128 was a precondition.

**THAT IS THE WRONG UNIT, AND THE ABANDONMENT WAS DECIDED ON IT.**
Pixal3D is four stages. The sparse structure stage is
`ss_flow_img_dit_1_3B_*` at **1.3 B**: 2.6 GB at bf16, 0.72 GB at
four, fitting at every precision and never meeting RFD 1128. It is
also the only stage that runs here, its two configs being the only
ones without `use_naf_upsample`, so they never reach NATTEN.

## Decision

**THE PREDICTION THAT REPLACED IT WAS ALSO WRONG.** This RFD said
sparse convolution would supply RFD 1131's gather and scatter.
`sparse_structure_flow.py` imports nothing from `modules.sparse`: it
is a dense DiT, named for what it emits, not how it computes.

Abandoned at 10 of 25 and it stays abandoned, and the reason is now
measured. Complex RoPE blocked the export, an encoding rather than
arithmetic: rewritten in reals it is bit-identical and the graph
exports at 544 nodes, carrying none of the refused operators.

The compiler refuses it anyway, and not for arithmetic. Every attempt
dies in `_add_input_layers`: the parser wants each input image-shaped,
and this stage takes a voxel grid, a timestep and two conditioning
tensors. `Cos`, `Sin` and `ReduceL2` stay unjudged; `DETAILS.md` has
the ladder.

## Related

RFD 1131 names the refused operators; RFD 1140, the kernel wall.
