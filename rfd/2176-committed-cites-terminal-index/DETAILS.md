# RFD 2176 details: per-pair annotations for the 39 pairs

Full list from the Lean 4 audit (`Report.lean` output). Three classes:
retraction chain (keep), historical framing (keep, weakly stale), real
drift (successor annotated).

## Retraction chains (14, keep as-is)

The citer IS the retraction; citation is by design.

  2168 → 1122     RFD 2168 abandons 1122
  2169 → 1019     RFD 2169 abandons 1019
  2169 → 1067     RFD 2169 references abandoned CockroachDB
  2173 → 1019     Qwen3-VL migration index references studio-core
  2174 → 1019     Abandoned-citation index references itself
  2174 → 1122     "
  2174 → 1166     "
  2175 → 1132     Rented-compute retraction lists what it abandons
  2175 → 1140     "
  2175 → 1163     "
  2175 → 2133     "
  2175 → 2138     "
  2159 → 2158     RFD 2159 supersedes 2158 (self-hosted RISC-V compiler)
  (5 rented-compute rows already appear in 2175's own list)

## Historical framing (14, keep as-is, weakly stale)

Published loop-RFDs and moat-narrative RFDs cite the framing the
workspace used at the time. Rewriting risks losing the story.

  1005 → 1012     Avatar pipeline history
  1020 → 1019     CockroachDB persistence over the abandoned Elixir core
  1021 → 1019     Shared HRR library history
  1030 → 1019     See-Through component models history
  1030 → 1166     "
  1054 → 1019     Planner history
  1057 → 1062     Open work history
  1058 → 1019     Zero-trust networking history
  1060 → 1019     Thirdparty reset history
  1106 → 1012     Moat overview
  1106 → 1015     "
  1106 → 1109     "
  1143 → 1122     Keypoints-to-ANNY loop cites the wholebody framing
  1145 → 1122     Stylized-to-OmniGen2 loop, same framing
  1147 → 1122     EditScore cost, same framing

## Real drift (11, per-pair successor annotated)

Citations that should migrate on next edit. Each names a specific
successor.

  1080 → 1062     Fly deploy cost cites Fly.io toplevel (abandoned).
                  Successor: none; drop on next edit.
  1086 → 1101     Dev machine topology cites SSH host names (aband).
                  Successor: none; drop.
  1095 → 1100     NVIDIA XR AI cites spatial fabric integration
                  (abandoned). Successor: RFD 1107 (world package).
  1099 → 1100     Scripts cheatsheet, same abandoned RFD 1100.
                  Successor: RFD 1107.
  1102 → 1100     3DAIGC modules, same. Successor: RFD 1107.
  1103 → 1098     Vercel loot cites public deploy (aband). Drop.
  1107 → 1100     World package cites spatial fabric integration.
                  Self-successor; keep or drop.
  1108 → 1090     XR mode cites IWSDK integration (aband). Drop.
  1111 → 1100     3DAIGC-API reference cites 1100. Successor: 1107.
  1146 → 1132     Latent-to-Pixal3D cites priority list (abandoned
                  by RFD 2175). Successor: RFD 2175.
  1057 → 1062     Open work also drops abandoned Fly.io toplevel.

## Verification

Lean 4 (v4.33.1) audit:
  ` cd scratchpad/rfd_check && lake build rfdReport && ./.lake/build/bin/rfdReport`

Four metatheorems typecheck:
  `unknown_not_open`, `abandoned_not_open`, `moved_not_open`,
  `classification_complete`.

Counterexamples are extensional (a real inhabitant of the pair list,
not a missing proof); the classification above cites the full 39.
