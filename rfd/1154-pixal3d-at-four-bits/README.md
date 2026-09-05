# RFD 1154: Pixal3D fits only at four bits, as a whole

Abandoned at 10 of 25 and it stays abandoned, and the reason is now
measured. Complex RoPE blocked the export, an encoding rather than
arithmetic: rewritten in reals it is bit-identical and the graph
exports at 544 nodes, carrying none of the refused operators.

**THAT IS THE WRONG UNIT, AND THE ABANDONMENT WAS DECIDED ON IT.**
Pixal3D is four stages. The sparse structure stage is
`ss_flow_img_dit_1_3B_*` at **1.3 B**: 2.6 GB at bf16, 0.72 GB at
four, fitting at every precision and never meeting RFD 1128. It is
also the only stage that runs here, its two configs being the only
ones without `use_naf_upsample`, so they never reach NATTEN.

**State:** abandoned

This RFD was drafted by an AI and read by a human before it shipped.
