# MaskScore: dataset stubs for modalities EditScore does not cover

EditReward-Bench covers 13 image-editing subtasks (background_change,
subject-remove, subject-add, text_change, ps_human, style_change,
motion_change, tone_transfer, color_alter, compose, subject-replace,
material_alter, extract) across 3 dimensions (overall, prompt_following,
consistency). All are image→image edits scored by a VLM reward model.

The pipeline in RFD 1173 has seven modalities beyond image.
Each stub names the gap, the format the dataset would take, and why the
pipeline cannot close the loop without it.

## The MaskScore self-supervised training loop

**MaskScore** is the codename for this technique: mask a region of a
latent, reconstruct with the stage's denoiser, decode to the output
domain, score the decoded reconstruction against the decoded original.
It parallels EditScore (which scores image edits via a VLM) but
operates across all modalities and needs no human annotation — the
original asset IS the ground truth.

### Stage 1: mask → reconstruct (denoiser pretraining)

This is how diffusion and flow-matching models are already trained.
Take a clean latent, corrupt it (add noise or mask a region), predict
the clean version back. Qwen3-Omni, Pixal3D, VoxHammer, and the talker
are all trained this way. The training signal is reconstruction loss
against the original. No labels.

### Stage 2: construct reward signal (self-supervised scoring)

Mask a region of a latent from a held asset. Reconstruct. Decode
BOTH original and reconstruction to the output domain. Score on the
decoded output:

- **Preservation:** perceptual distance on the decoded unmasked region
  (LPIPS for images, render-and-compare via Mitsuba 3 for meshes,
  mel distance for audio, BLEU/ROUGE for text)
- **Edit quality:** perceptual quality on the decoded masked region
  (FID/CLIP-score for images, render-and-compare via Mitsuba 3 for
  meshes, UTMOS for audio, perplexity for text)

The original decoded output is the reference. No human annotator.
The score is computable from the data alone.

### Stage 3: train a reward model on self-supervised scores

Collect (mask, reconstruction, score) triples from stage 2. Train a
reward model (a VLM for images, an LLM for text, a domain model for
meshes/audio) to predict the score from the (input, output,
instruction) triple — where the "instruction" is the mask described
in natural language ("fill the bottom-left quadrant", "complete the
masked sentence"). This is supervised learning, but the labels come
from automated metrics, not humans.

The reward model replaces the raw metric. EditScore did exactly this
for images. The reward model here IS Qwen3-Omni — the same model
that serves deployment scores its own generations during training
(OmniScore). No separate VLM.

### Stage 4: RL fine-tuning with the reward model

Use the trained reward model as the reward signal for online RL
(PPO, GRPO, or similar). The denoiser generates, the reward model
scores, the policy updates. Same loop EditScore uses for OmniGen2.
No human in the loop.

The quality ceiling of this loop is bounded by the automated metrics
in stage 2. A metric that lies (latent L2 instead of decoded
perceptual distance) propagates through every stage. Scoring on the
decoded output rather than in latent space is the guard: the decoded
image, mesh, or waveform is what the user sees.

## All stages operate on maskable latents

Every stage in the pipeline is either a 1D token sequence or a 3D
spatial grid, and the generation model is a flow-matching or
diffusion denoiser that takes `(x, t, cond)`:

| stage | latent format | mask operation |
|---|---|---|
| Qwen3-Omni text | `(B, seq)` token ids | replace span with mask_id |
| Qwen3-Omni image | `(B, C, H, W)` VAE latent | noise a spatial patch |
| Qwen3-Omni video | `(B, T, C, H, W)` temporal latent | noise a temporal span |
| ANNY keypoints | `(B, N, 3)` landmark coords | drop a landmark subset |
| Thermal frame | `(B, C, H, W)` thermal latent | noise a spatial patch |
| Pixal3D sparse structure | `(B, C, R, R, R)` voxel grid | noise a 3D subvolume |
| VoxHammer structured latent | SparseTensor (coords + feats) | drop/noise a spatial region |
| Talker | speech token sequence | replace span with mask token |

The 3D latents are confirmed maskable: `SparseStructureFlowModel`
asserts `x.shape == [B, C, R, R, R]` (line 177 of
`sparse_structure_flow.py`), and `SLatFlowModel` operates on
SparseTensors with the same `(x, t, cond)` interface.

Scoring happens on the decoded output, not in latent space. The
masking operates on latents (where the model works); the evaluation
decodes once (the "stages pass latents; VAE decode happens once, at
final output" constraint) and scores what the user would see.

## Construction via masking corruption

The masking corruption technique applies to any denoiser: mask a span,
reconstruct, score. This is the StyleGAN corruption/reconstruction
technique applied to discrete tokens and latents. A masked span IS
an edit instruction, and the (original, mask, reconstruction) triple
is a scored edit by construction. The technique was prototyped on
LLaDA-o (now blocklisted for latency) and transfers to Qwen3-Omni's
generation stages without change.

This makes all seven datasets **constructed synthetic**: deterministic
from source assets we hold, labels true by construction (the original
IS the ground truth), same seed reproduces the corpus. No generative
model in the scoring loop, so none of the four conditions for
generated synthetic apply.

## 1. TextEditReward-Bench

**Modality:** text→text edit
**Why required:** Qwen3-Omni generates and revises text. Without a
text-edit reward signal, the thinker's text output has no RL training
signal and no automated quality gate.

**Self-supervised construction:**
1. Take a source text from held assets
2. Encode to token ids
3. Mask a span (vary position and length for task diversity)
4. Let the denoiser reconstruct
5. Decode both to text
6. Score: BLEU/ROUGE on unmasked tokens (preservation), perplexity
   on masked span (edit quality)
7. Record (text, mask, reconstruction, scores)

Mask length determines task_type: word-level = grammar_fix,
sentence-level = rephrase, paragraph-level = summarize. No human
annotation — the original text is the reference.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | mask described as edit ("rephrase the second sentence") |
| input_text | string | original text |
| output_texts | list[string] | candidate reconstructions |
| scores | list[float] | automated (preservation, edit_quality) |
| task_type | string | one of: tone_change, grammar_fix, summarize, expand, rephrase, factual_correction, style_transfer |
| dimension | string | one of: overall, instruction_following, fluency, preservation |

**Reward model (stage 3):** Qwen3-Omni scores (input_text, instruction,
output_text) directly — the thinker IS the reward model for its own
text output (OmniScore).

## 2. MeshEditReward-Bench

**Modality:** image→3D mesh and 3D→3D edit
**Why required:** Pixal3D and VoxHammer produce meshes from images.
Without a reward signal, mesh quality is manual inspection only and
the 3D stage cannot participate in RL training.

**Self-supervised construction:**
1. Take a mesh from Objaverse (held, Apache 2.0 subset)
2. Encode to voxel grid `(B, C, R, R, R)` via the sparse structure VAE
3. Mask a 3D subvolume (vary position, size, shape)
4. Let the flow model reconstruct
5. Decode both to meshes via FlexiCubes
6. Score via render-and-compare: render both meshes from matched
   viewpoints (Mitsuba 3, sphere_hammersley_sequence), then L1 on
   mask/depth/normals, SSIM on normals, LPIPS on normals for the
   unmasked region (preservation) and the masked region (edit
   quality). For textured meshes: SSIM and LPIPS on rendered base
   color and material attributes
7. Record (voxel latent, mask, reconstruction, scores)

Mask shape determines task_type: a limb-sized subvolume = part_edit,
a thin shell = texture_transfer, the full interior = mesh_refinement.
No human annotation — the original mesh is the reference.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | mask described as edit ("refine the hand region") |
| input_mesh | string | path to input mesh (.glb) |
| input_image | image | conditioning image (for image→mesh tasks) |
| output_meshes | list[string] | paths to candidate meshes (.glb) |
| scores | list[float] | automated (preservation, edit_quality) |
| task_type | string | one of: image_to_mesh, mesh_refinement, part_edit, texture_transfer, pose_change |
| dimension | string | one of: overall, geometric_fidelity, image_alignment, topology_quality, preservation |

**Reward model (stage 3):** Qwen3-Omni scores multi-view Mitsuba 3
renders of (input mesh, output mesh, instruction) directly — it
judges geometric and visual quality from the rendered views, learning
to weight the dimensions rather than averaging them (OmniScore).

## 3. SpeechEditReward-Bench

**Modality:** text→speech and speech→speech edit
**Why required:** The Qwen3-Omni talker produces speech with voice
cloning. Without a reward signal, the audio head cannot participate
in RL training.

**Self-supervised construction:**
1. Take audio from held assets (license-clean speech corpora)
2. Encode to speech token sequence
3. Mask a time span (vary position, duration)
4. Let the talker/vocoder reconstruct
5. Decode both to waveforms
6. Score: mel spectrogram distance on unmasked region (preservation),
   UTMOS on masked region (naturalness/quality), speaker embedding
   cosine similarity (voice identity preservation)
7. Record (audio tokens, mask, reconstruction, scores)

Mask duration determines task_type: a phoneme = pronunciation_fix,
a word = prosody_edit, a sentence = full resynthesis. For voice
cloning: mask the speaker conditioning and score identity
preservation via speaker verification. No human annotation — the
original waveform is the reference.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | mask described as edit ("resynthesize from 2.0s to 3.5s") |
| input_audio | string | path to input audio (.wav) |
| reference_voice | string | path to voice reference (.wav) for cloning |
| output_audios | list[string] | paths to candidate audio (.wav) |
| scores | list[float] | automated (preservation, quality, identity) |
| task_type | string | one of: tts_generation, voice_cloning, prosody_edit, speed_change, emotion_transfer, pronunciation_fix |
| dimension | string | one of: overall, instruction_following, voice_identity, naturalness, preservation |

**Reward model (stage 3):** Qwen3-Omni scores (input audio, instruction,
output audio) directly — the thinker handles audio natively, so it
IS the reward model for the talker's speech output (OmniScore).

## 4. MultimodalEditReward-Bench

**Modality:** cross-modal edits (text↔image, image↔mesh, text↔speech)
**Why required:** The pipeline is a chain: text→image→mesh, with audio
parallel. Edits cross modality boundaries. Within-modality scoring
does not cover the seam.

**Self-supervised construction:**
1. Take a (text, image, mesh, audio) tuple from held assets
2. Mask in one modality's latent space
3. Reconstruct
4. Decode to the output modality
5. Score cross-modal alignment: CLIP-score (text↔image), rendered
   LPIPS (image↔mesh), CLAP/UTMOS (text↔audio)
6. Record (input modality latent, mask, output modality decoded, scores)

The cross-modal score is the distance between the decoded
reconstruction and the paired asset in the other modality. The
paired assets provide the ground truth without annotation.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | edit instruction |
| input_modality | string | one of: text, image, mesh, audio |
| output_modality | string | one of: text, image, mesh, audio |
| input_data | varies | the input in its modality |
| output_candidates | list[varies] | candidate outputs |
| scores | list[float] | automated cross-modal alignment |
| task_type | string | one of: text_to_image_edit, image_to_mesh_edit, text_to_speech_edit, mesh_to_image_edit |
| dimension | string | one of: overall, cross_modal_fidelity, instruction_following, preservation |

**Source dataset: SpeakingFaces** (issai/Speaking_Faces, CC-BY-4.0,
142 subjects, 13,000+ instances). Synchronized visual video
(768×512), thermal video (464×348), and audio at nine camera angles.
The synchronization IS the cross-modal ground truth:

- audio → face image: mask audio tokens, score reconstruction
  against the synchronized video frame
- face image → audio: mask visual regions, score voice identity
  against the paired audio
- thermal ↔ visual: mask one spectrum, score against the paired
  spectrum (domain transfer edit)

The canonical ANNY rig can be fitted to the face video frames to
recover keypoints and encode the 3D latent via the sparse structure
VAE. This gives a (face image, ANNY keypoints, ANNY 3D latent,
audio) tuple per synchronized frame — the full pipeline ground
truth from visual through 3D through audio, all paired. The
keypoint fit is deterministic from the video frames and the
canonical mesh, so the derived latents are constructed synthetic.

No annotation needed — the synchronized streams plus the ANNY fit
are the paired assets. CC-BY-4.0 clears the license bar.

- https://huggingface.co/datasets/issai/Speaking_Faces
- https://doi.org/10.48333/smgd-yj77

**Reward model (stage 3):** Qwen3-Omni scores cross-modal alignment
directly — it handles text, image, audio, and video natively, so
it IS the reward model for cross-modal edits (OmniScore). The
training signal is self-supervised (SpeakingFaces' synchronized
streams are the ground truth).

## 5. KeypointEditReward-Bench

**Modality:** image→keypoints and keypoints→keypoints edit
**Why required:** Keypoints and the canonical ANNY representation are
interchangeable — the keypoints ARE the rig state expressed as sparse
landmarks, and the canonical ANNY mesh IS the dense surface they
parameterise. Fitting the canonical rig to a SpeakingFaces frame
produces both: the landmarks locate the face, and the rig state
reconstructs the mesh. Without a reward signal on this representation,
the fit step is unscored and the downstream 3D latent inherits any
drift silently.

**Self-supervised construction:**
1. Fit ANNY canonical rig to a SpeakingFaces video frame → keypoints
2. Represent as a structured sequence (landmark index, x, y, z, confidence)
3. Mask a subset of landmarks (vary count, region — face, jaw, brow)
4. Reconstruct the masked landmarks from the unmasked ones and the
   conditioning image
5. Score: Euclidean distance on masked landmarks against the fit
   (geometric accuracy), reprojection error against the source frame
   (image alignment)
6. Record (keypoints, mask, reconstruction, scores)

Mask region determines task_type: jaw landmarks = expression_edit,
brow landmarks = micro_expression, full-face = pose_refit. The ANNY
fit is deterministic from the frame and the canonical mesh, so the
derived keypoints are constructed synthetic.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | mask described as edit ("refit the jaw landmarks") |
| input_keypoints | list[float] | ANNY landmark coordinates |
| conditioning_image | string | path to source frame |
| output_keypoints | list[list[float]] | candidate reconstructions |
| scores | list[float] | automated (geometric_accuracy, reprojection_error) |
| task_type | string | one of: expression_edit, micro_expression, pose_refit, landmark_interpolation, symmetry_correction |
| dimension | string | one of: overall, geometric_fidelity, image_alignment, anatomical_plausibility |

**Reward model (stage 3):** Qwen3-Omni scores (image, input keypoints,
instruction, output keypoints) directly — the thinker sees the
conditioning image and judges whether the reconstructed landmarks
are anatomically plausible (OmniScore).

## 6. ThermalEditReward-Bench

**Modality:** thermal→thermal and thermal↔visual edit
**Status:** exploratory — the signal exists but the use is not yet known.
**Why it exists:** SpeakingFaces provides synchronized thermal video
(464×348) alongside visual video (768×512). Thermal captures heat
distribution — a structural signal analogous to depth from the canonical
ANNY fit: both encode face geometry through a physical quantity rather
than appearance. The thermal→depth analogy suggests thermal could
condition or validate the ANNY fit, but how is not yet decided.
**Why it is stubbed rather than dropped:** the synchronized data is
present and CC-BY-4.0. Recording the stub costs less than rediscovering
the modality later if a use materialises.

**Self-supervised construction:**
1. Take a synchronized (visual, thermal) frame pair from SpeakingFaces
2. Encode thermal frame to image latent
3. Mask a spatial patch in the thermal latent
4. Reconstruct
5. Decode both to thermal images
6. Score: LPIPS on unmasked region (preservation), SSIM on masked
   region (reconstruction quality), cross-modal alignment against
   the paired visual frame (domain consistency)
7. Record (thermal latent, mask, reconstruction, scores)

For thermal↔visual transfer: mask the thermal latent, condition on
the visual frame, score the reconstruction against the original
thermal. The synchronized pair IS the ground truth for domain transfer.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | mask described as edit ("reconstruct the forehead thermal region") |
| input_thermal | string | path to input thermal frame |
| paired_visual | string | path to synchronized visual frame |
| output_thermals | list[string] | paths to candidate thermal frames |
| scores | list[float] | automated (preservation, quality, cross_modal_alignment) |
| task_type | string | one of: thermal_inpaint, thermal_to_visual, visual_to_thermal, thermal_enhancement, heat_region_edit |
| dimension | string | one of: overall, thermal_fidelity, cross_modal_alignment, preservation |

**Reward model (stage 3):** Qwen3-Omni scores (thermal frame, visual
frame, instruction, output thermal) directly — the synchronized
visual frame anchors the cross-modal score (OmniScore).

## 7. VideoEditReward-Bench

**Modality:** video→video edit and video↔audio edit
**Why required:** Qwen3-Omni handles video natively. SpeakingFaces video
can be converted to CineForm with aligned audio, giving temporally
coherent video+audio pairs. Without a video reward signal, the temporal
dimension is unscored — frame-level image scoring misses motion
coherence, lip sync, and temporal consistency.

**Self-supervised construction:**
1. Take a SpeakingFaces video clip (converted to CineForm with aligned
   audio)
2. Encode video frames to a temporal latent sequence
3. Mask a temporal span (vary position, duration — a few frames to a
   full segment)
4. Reconstruct the masked frames conditioned on unmasked context
5. Decode both to video
6. Score: per-frame LPIPS on unmasked frames (preservation), FVD on
   masked span (temporal coherence), lip-sync score against aligned
   audio (audio-visual alignment), optical flow consistency between
   reconstructed and original (motion coherence)
7. Record (video latent sequence, mask, reconstruction, scores)

Mask duration determines task_type: 1–3 frames = frame_interpolation,
a segment = video_inpaint, the audio track = audio_driven_generation.
The aligned audio is the temporal anchor: lip sync and audio-visual
coherence are scored against the original audio track, not inferred.

**Format:**

| column | type | description |
|---|---|---|
| key | string | unique identifier |
| instruction | string | mask described as edit ("interpolate frames 30–45") |
| input_video | string | path to input video (CineForm .mov) |
| aligned_audio | string | path to aligned audio (.wav) |
| output_videos | list[string] | paths to candidate videos |
| scores | list[float] | automated (preservation, temporal_coherence, lip_sync, motion) |
| task_type | string | one of: frame_interpolation, video_inpaint, audio_driven_generation, speed_change, expression_transfer, temporal_super_resolution |
| dimension | string | one of: overall, temporal_coherence, audio_visual_sync, motion_fidelity, preservation |

**Reward model (stage 3):** Qwen3-Omni scores (video clip, aligned
audio, instruction, output video) directly — it handles video
natively, so it judges temporal coherence and audio-visual alignment
that frame-level image scoring cannot reach (OmniScore).
