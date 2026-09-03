# RFD 2179 details: WER pass across the 5 text tracks on 15 clips

Per-clip WER against SpeakingFaces canonical text. Lower is better.
Zero = exact match on the canonical wording (case-insensitive, whitespace-
split, Levenshtein / reference word count).

## Per-clip

| clip                     | parakeet | whisper | voxtral | wav2vec2 | gemma-auto |
| ------------------------ | -------: | ------: | ------: | -------: | ---------: |
| 100_1_2_1_1134_1         | 0.000    | 0.000   | 0.000   | 0.500    | 1.000      |
| 100_1_2_1_1293_1         | 1.000    | 1.000   | 0.000   | 0.500    | 1.000      |
| 100_1_2_1_574_1          | 1.000    | 1.000   | 0.000   | 1.000    | 1.000      |
| 100_1_2_1_594_1          | 1.000    | 0.200   | 0.000   | 0.400    | 1.000      |
| 100_1_2_1_856_1          | 0.000    | 1.000   | 0.000   | 0.200    | 1.000      |
| 100_1_2_1_97_1           | 0.125    | 0.000   | 0.000   | 0.500    | 1.000      |
| 100_1_2_2_1170_1         | 0.286    | 0.286   | 0.000   | 1.000    | 1.000      |
| 100_1_2_2_1202_1         | 0.200    | 0.400   | 0.000   | 0.400    | 1.000      |
| 100_1_2_2_288_1          | 1.000    | 0.000   | 0.000   | 0.500    | 1.000      |
| 100_1_2_2_323_1          | 0.111    | 0.000   | 0.000   | 0.333    | 1.000      |
| 100_1_2_2_846_1          | 1.000    | 1.000   | 0.000   | 0.500    | 1.000      |
| 100_1_2_3_1070_1         | 0.600    | 0.000   | 0.000   | 0.400    | 1.000      |
| 100_1_2_3_1098_1         | 0.000    | 0.000   | 0.000   | 0.400    | 1.000      |
| 100_1_2_3_351_1          | 0.200    | 0.200   | 0.000   | 0.600    | 1.000      |
| 100_1_2_3_380_1          | 1.000    | 0.000   | 0.000   | 1.333    | 1.000      |
| **MEAN**                 | **0.501**| **0.339**| **0.000**| **0.571**| **1.000**  |

Method: hypothesis is the concatenated cue text from each track's
`.vtt` (WEBVTT header + timing lines stripped, remaining text
whitespace-joined). Reference is the SpeakingFaces canonical text
from `maskscore_speech.parquet`.

## What the numbers say

**Voxtral is the accuracy leader (0.000 mean WER, all 15 clips
exact).** Same track also returns sub-second per clip on MPS.
Whichever axis dominates the decision (speed or accuracy), Voxtral
wins.

**Whisper-large-v3 is not the worst on accuracy (0.339 mean).** It
beats Parakeet (0.501) and wav2vec2 (0.571) but takes several
seconds per clip on MPS. The reason to drop it is latency, not
accuracy. The operator's initial "bad accuracy" observation was
partially wrong; Whisper's problem is speed.

**Parakeet is the workspace's stated CC-BY-4.0 canonical (RFD 2164)
but sits at 0.501 mean WER**, worse than Whisper. Kept because the
canonical-judge choice was made on license grounds, not accuracy
alone; Voxtral is the accuracy-first alternate.

**Gemma-auto shipped empty transcripts across all 15 clips**
(WER 1.000 because the vtt files carry only the WEBVTT header, no
cues). Separate bug: either the llama-mtmd-cli invocation failed or
the output-parsing step drops the response. Follow-up separate from
this RFD.

## The 15-clip subset

Sub_100 speaking English into a Kazakh L1 accent. Not a general-purpose
benchmark. The three tracks Whisper family loses to (Voxtral wins,
Parakeet loses, wav2vec2 loses) do not necessarily generalise to
other accents. If a wider corpus lands (Rung 2, more SpeakingFaces
subjects), rerun.
