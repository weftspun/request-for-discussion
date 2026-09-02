# RFD 2174 details: per-pair annotations for open→abandoned citations

Full pair list from the 2026-09-02 audit. Format: citing RFD (state)
→ cited abandoned RFD → successor to migrate to, or note.

## Citations of RFD 1122 (abandoned by RFD 2168)

RFD 1122's bespoke wholebody detector never shipped; RFDs 1143 (published)
and 1173 (discussion) settled the pipeline differently. Every citation
below treats 1122's rendered-ANNY corpus route as authoritative when
the workspace actually uses ANNY-as-pose-primitive per RFD 1143.

  RFD 1121 (discussion) → RFD 1143 + RFD 1173
  RFD 1123 (discussion) → RFD 1143
  RFD 1126 (discussion) → RFD 1143
  RFD 1128 (discussion) → RFD 1143
  RFD 1130 (discussion) → RFD 1143
  RFD 1131 (discussion) → RFD 1143
  RFD 1132 (discussion) → RFD 1143
  RFD 1134 (discussion) → RFD 1143
  RFD 1142 (discussion) → RFD 1143
  RFD 1148 (discussion) → RFD 1143
  RFD 1170 (ideation)   → RFD 1173
  RFD 1171 (ideation)   → RFD 1173

## Citations of RFD 1166 (abandoned)

RFD 1166 was the See-Through scoring plan; RFD 1168 (segment 3D
latent with rf-detr) replaced it.

  RFD 1006 (discussion) → RFD 1168
  RFD 1044 (discussion) → RFD 1168
  RFD 1167 (ideation)   → RFD 1168
  RFD 1168 (ideation)   → self (chain, keep)
  RFD 1169 (ideation)   → RFD 1168
  RFD 1170 (ideation)   → RFD 1168
  RFD 1171 (ideation)   → RFD 1168
  RFD 1173 (discussion) → RFD 1168

## Citations of RFDs 1049-1052 (abandoned model images)

Weftspun-image-to-world, LingBot map, WorldMirror2, TripoSplat --
all abandoned in the 2026-09-01 catalog prune.

  RFD 1038 (discussion) → drop (RFD 1038 mesh model is the same shape)
  RFD 1133 (discussion) → self (chain, keep)
  RFD 1171 (ideation)   → drop

## Citations of RFD 1019 (abandoned by RFD 2169)

The Elixir strangler-fig studio core.

  RFD 1022 (discussion) → RFD 2169
  RFD 1023 (discussion) → RFD 2169
  RFD 1055 (discussion) → RFD 2169
  RFD 1056 (discussion) → RFD 2169

## Citations of RFD 1155 (abandoned)

RFD 1155 abandoned Gemma 4 as an accelerator target; ironic given
the reasoning-core swap in RFD 2169. Cite path chain intentional.

  RFD 1157 (ideation)   → self (chain, keep)
  RFD 1169 (ideation)   → self (chain, keep)
  RFD 1170 (ideation)   → self (chain, keep)
  RFD 1171 (ideation)   → self (chain, keep)

## Citations of other abandoned RFDs

  RFD 1018 (discussion) → RFD 1012 (Phygital passport, abandoned)  → drop
  RFD 1073 (prediscussion) → RFD 1062 (Fly.io toplevel, abandoned) → drop
  RFD 1075 (prediscussion) → RFD 1062                              → drop
  RFD 1076 (prediscussion) → RFD 1062 + RFD 1074 (moved)           → drop
  RFD 1077 (prediscussion) → RFD 1067 (CockroachDB rerank, aband.) → RFD 2140 (OpenBao on FDB)
  RFD 1112 (discussion) → RFDs 1090, 1100 (IWSDK + moat abandoned) → drop
  RFD 2150 (prediscussion) → RFD 2151 (CoAP+OSCORE NIF, abandoned) → drop
  RFD 2173 (committed)  → RFD 2139 (MaskScore QAFT budget, aband.) → self (chain, keep)

## Categories

  chain, keep    -- retraction chain; the citation IS the walk-back
  successor RFD  -- migrate the citation on next edit
  drop           -- reference is stale, no successor, remove on next edit

Roughly 60% of the 32 pairs are legitimate retraction chains. The
remaining ~13 pairs (marked with a successor or drop) are real drift.
