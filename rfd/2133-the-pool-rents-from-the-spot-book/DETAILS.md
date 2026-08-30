# Details: the measurements behind the gates

All prices in dollars per hour, single RTX 4090, measured 2026-08-30
between 10:30 and 11:00 PDT via the public bundles endpoint. The book
moves in minutes; these are snapshots with their time attached, not a
menu.

## The requirement gates, each with its reason

| gate | value | reason |
| --- | --- | --- |
| CUDA | >= 12.8 | torch cu128 wheels; one floor host offered 12.6 |
| disk | >= 100 GB | Pixal3D ~25 + OmniGen2 ~12 + EditScore ~9 + SkinTokens ~2 + envs ~15 + workdir; a live 12.15-cent host carried 52 GB total |
| RAM | >= 32 GB | USD authoring and exports; a 14.81-cent host carried 16 GB |
| down | >= 200 Mbit/s | ~60 GB of model pulls; at a measured 59 Mbit/s that is 2.3 hours of paid idle |

## Qualified price distributions

    tier                     n   min   p10   p25   med   p75   p90   max   <=.12  <=.14  <=.20
    on-demand, global       61  .216  .322  .361  .394  .536  .697  4.002    0      0      0
    on-demand, US/CA        38  .216  .336  .362  .484  .607  .710  4.002    0      0      0
    interruptible, global   49  .073  .160  .188  .267  .400  .600   .667    2      3     18
    interruptible, US/CA    32  .160  .175  .200  .333  .467  .613   .733    0      0     10

The latency gate (US/CA) costs about two-to-one at the interruptible
floor, 0.160 against 0.073, and nothing at the on-demand floor.

## Outlier lifetimes, observed

- A 0.121 on-demand listing appeared and was taken inside twenty
  minutes; the five-minute watcher caught only its disappearance.
- A 0.1215 listing that followed failed the disk gate at 52 GB.
- A 0.120 qualified interruptible (Virginia, 99.7%, 1.45 TB) was
  present in one scan and gone in the next, minutes later.

Sixty-second polling is the correction the first observation forced.

## The first rental

Contract 49287440: host 48234252, Texas, on-demand at 0.2163 -- 126 GB
RAM, 748 GB disk, 909/643 Mbit/s, CUDA 13.2, reliability 98.0%. Chosen
at roughly 60% of the qualified p25; nothing at or under the p25 beat
it on any axis without costing half again more. The pool activity at
two GPU-days costs about $10 on it.

## Key handling

`VAST_API_KEY` at user scope in the Windows environment, written by
`setx` from a 1Password read (`op item get ... --fields credential`),
value never echoed into a transcript. The snipe tooling reads it from
the registry so fresh shells inherit it without the session snapshot.
