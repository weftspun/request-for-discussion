# RFD 2133: The pool rents from the spot book, gated on requirements first

**State:** abandoned
**Feature:** where pool generation runs, and how a card is chosen
**Scope:** the gacha demo's pool activity; `scratchpad` tooling pending a home

## Decision

Rent single RTX 4090s from the vast.ai book, requirements before
price. A qualifying host carries CUDA at 12.8 or newer, 100 GB of
allocatable disk, 32 GB of RAM, and 200 Mbit/s down; the measurements
behind each gate are in DETAILS.md, with the price distributions that
show what the gates cost. The gates exist for the cheap unqualified
boxes: the sub-15-cent listings that flicker through the
book bought their price with 52 GB disks and 16 GB hosts, and a model
pull over a starved link is paid idle time.

Interruptible is the planning tier, near 20 cents per hour at the
qualified p25; on-demand is bought when a qualified outlier dips, and
sub-floor outliers were measured living minutes, not hours. Pool work
is seed-checkpointed, so an interruption costs one pull.

The RunPod teardown rule applies unchanged: results are pushed when
produced, the instance is destroyed after use, and the destruction is
double-checked. The API key lives in the user environment, read from
the password manager, never in a repository or a transcript.

## Problem

Pool generation wants days of GPU that the desk card should not give
up: the 3090 is the interactive seat for rigging and judging, and a
batch that owns it for two days stalls the critical path it feeds.

## Related

RFD 1163 keeps the desk card for the loops this rule protects. The
demo plan this feeds is charted in the Gacha Critical Path artifact;
pool generation is its activity E.
