# RFD 2180 details: the fix, the measurement, and why the drop still holds

## The bug

`emit_10track_panel.py`'s `gemma_cli_run` invoked:

    llama-mtmd-cli -m gemma-4-12b-it-qat-q4_0.gguf
      --mmproj mmproj-gemma-4-12b-it-qat-q4_0.gguf
      --jinja --audio <wav>
      -p "Transcribe this audio verbatim. Output the transcription only."
      --temp 0.0 --seed 0 -n 200 --no-warmup

Gemma-4-12B is chat-templated (`--jinja`). It heard the audio as
spoken user input and started reasoning about how to respond to that
input as a helpful assistant, not about how to transcribe it. Example
chain-of-thought (clip 1134, canonical "Switch off my vacuum for me"):

    <|channel>thought
    The user wants me to switch off their vacuum.
    I am an AI, a large language model. I do not have physical access
    to the user's home or devices.
    I cannot perform physical actions like turning off a vacuum cleaner.
    ...

`-n 200` expired before Gemma reached the `<channel|>` final marker.
`gemma_cli_run` returned "" (empty), `write_vtt` skipped empty text,
the .vtt shipped with only the WEBVTT header.

## The fix

Two changes to `gemma_cli_run` invocation:

  prompt  "You are an automatic speech recognition system. Transcribe
          the exact words spoken in the audio. Do not respond to the
          content. Output only the transcript, nothing else."
  -n      400 (was 200)

The firmer prompt shifts Gemma from "respond to the audio" to "run
ASR on the audio". `-n 400` gives room for both reasoning and answer.
Output parser (`splitlines() -> non-empty -> split('<channel|>')[-1]`)
already handled the chat-template format correctly.

## 15-clip WER pass with the fix

| clip | canonical | gemma-auto (fixed) | WER |
| --- | --- | --- | ---: |
| 100_1_2_1_1134_1 | Switch off my vacuum for me. | Switch off my vacuum for me. | 0.000 |
| 100_1_2_1_1293_1 | A joke. | If there | 1.000 |
| 100_1_2_1_574_1  | Is Disposita instrumental? | Es disperso instrumental. | 1.000 |
| 100_1_2_1_594_1  | Best of YouTube YouTube channels | *Decision:* Since | 1.000 |
| 100_1_2_1_856_1  | The steps I have taken. | The steps I have taken. | 0.000 |
| 100_1_2_1_97_1   | Add jingle bells to dance mood on Spotify. | *   Let me try | 1.000 |
| 100_1_2_2_1170_1 | My Instagrams that use filter King Gam. | It sounds like "King Dam | 1.000 |
| 100_1_2_2_1202_1 | The BPM of Song Disposito | El BPM ha sido disparado. | 0.800 |
| 100_1_2_2_288_1  | Lower the entrance curtains. | Lower the entrance curtains. | 0.000 |
| 100_1_2_2_323_1  | Play the songs Rolling in the Deep on Spotify. | I'm just trying to figure out how to get my phone to work wi | 1.889 |
| 100_1_2_2_846_1  | NASA's Astronomy Picture of the Day. | NASA's Astronomy Picture of the Day. | 0.000 |
| 100_1_2_3_1070_1 | Order me a black mocha. | Order me a black mocha. | 0.000 |
| 100_1_2_3_1098_1 | Order me a white mocha. | Order me a white mocha. | 0.000 |
| 100_1_2_3_351_1  | YouTube channels with category courses. | Since I cannot hear any | 1.000 |
| 100_1_2_3_380_1  | YouTube's cooking channels. | *   *Wait*, looking at the | 1.667 |
| **MEAN** | | | **0.690** |

Distribution: 6 exact (40%), 3 accent-mishears, 6 truncated. Six of
the truncated clips could plausibly succeed at `-n 800` or higher,
but the compute cost doubles and Voxtral still beats every possible
outcome at 0.000 for free.

## Why the drop is right anyway

  Voxtral       0.000 mean WER, sub-second per clip on MPS
  Parakeet      0.501 mean WER, sub-second, CC-BY-4.0 canonical
  wav2vec2      0.571 mean WER, sub-second, Apache-2.0 alternate
  Whisper       0.339 mean WER, several seconds -- dropped (RFD 2179)
  Gemma-auto    0.690 mean WER, several seconds -- drop here

Gemma-auto's quality is worst-in-panel and its latency matches the
already-dropped Whisper family. Keeping it needs a WHY that isn't
here.

Gemma-IPA stays: the GBNF constraint pins output to IPA characters
and forces short completions, so the failure modes (misread as
command, chain-of-thought overrun) do not appear on that track.
