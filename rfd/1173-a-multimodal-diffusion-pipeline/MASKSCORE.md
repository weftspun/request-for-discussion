# MaskScore: multimodal edit scoring via render-and-compare

EditScore evaluates image edits across 13 task types in 4 groups
(object, appearance, scene, advanced) and 3 dimensions
(instruction_following, consistency, overall). It ships three
datasets: EditReward-Bench (2,890 evaluation rows),
EditScore-Reward-Data (97,300 reward model training rows), and
EditScore-RL-Data (110,000 RL training rows).

MaskScore extends that structure to all eight modalities in
RFD 1173. Every modality scores through the same metric: render
the ANNY mesh via Mitsuba 3 on `sphere_hammersley_sequence` views
and compare. The mesh is the common reference frame.

## The MaskScore self-supervised training loop

**MaskScore** is the codename for this technique: mask a region of a
latent, reconstruct with the stage's denoiser, decode to the output
domain, score the decoded reconstruction against the decoded original.
It parallels EditScore (which scores image edits via a VLM) but
operates across all modalities and needs no human annotation, because
the original asset IS the ground truth.

### Stage 1: mask, then reconstruct (denoiser pretraining)

This is how diffusion and flow-matching models are already trained.
Take a clean latent, corrupt it (add noise or mask a region), predict
the clean version back. Qwen3-Omni, Pixal3D, VoxHammer, and the talker
are all trained this way. The training signal is reconstruction loss
against the original. No labels.

### Stage 2: construct reward signal (self-supervised scoring)

Mask a region of a latent from a held asset. Reconstruct. Decode
BOTH original and reconstruction to the output domain. Score on the
decoded output via render-and-compare: render both through the ANNY
mesh via Mitsuba 3 on `sphere_hammersley_sequence` views, then L1 on
depth/normals, SSIM on normals, LPIPS on normals.

The original decoded output is the reference. No human annotator.
The score is computable from the data alone.

### Stage 3: train a reward model on self-supervised scores

Collect (input, instruction, candidates, scores) tuples from stage 2.
Train a reward model to predict the score from the (input, output,
instruction) triple, where the "instruction" is a natural-language
edit using the See-Through part vocabulary ("edit the mouth to match
frame B", "repose the eyebrow"). This is supervised learning, but the
labels come from automated render-and-compare, not humans.

The reward model replaces the raw metric. EditScore did exactly this
for images. The reward model here IS Qwen3-Omni, which scores its
own generations during training (OmniScore). No separate VLM.

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

| stage                       | latent format                     | mask operation               |
| --------------------------- | --------------------------------- | ---------------------------- |
| Qwen3-Omni text             | `(B, seq)` token ids              | replace span with mask_id    |
| Qwen3-Omni image            | `(B, C, H, W)` VAE latent         | noise a spatial patch        |
| Qwen3-Omni video            | `(B, T, C, H, W)` temporal latent | noise a temporal span        |
| ANNY keypoints              | `(B, N, 3)` landmark coords       | drop a landmark subset       |
| MoGe-3 depth                | `(B, 1, H, W)` metric depth map   | noise a spatial patch        |
| Pixal3D sparse structure    | `(B, C, R, R, R)` voxel grid      | noise a 3D subvolume         |
| VoxHammer structured latent | SparseTensor (coords + feats)     | drop/noise a spatial region  |
| Talker                      | speech token sequence             | replace span with mask token |

The 3D latents are confirmed maskable: `SparseStructureFlowModel`
asserts `x.shape == [B, C, R, R, R]` (line 177 of
`sparse_structure_flow.py`), and `SLatFlowModel` operates on
SparseTensors with the same `(x, t, cond)` interface.

Scoring happens on the decoded output, not in latent space. The
masking operates on latents (where the model works); the evaluation
decodes once (the "stages pass latents; VAE decode happens once, at
final output" constraint) and scores what the user would see.

## One universal metric: render-and-compare

Every modality is a projection of the ANNY mesh. The mesh is the
common reference frame. Every metric reduces to: render the ANNY
mesh via Mitsuba 3 on `sphere_hammersley_sequence` views, compare
L1 on depth/normals, SSIM on normals, LPIPS on normals.

| modality   | what it is                        | how it reaches the mesh               |
| ---------- | --------------------------------- | ------------------------------------- |
| Mesh       | root representation               | direct                                |
| Keypoints  | surface points on the mesh        | displace vertices, re-render          |
| Pose       | bone transforms producing the mesh | FK + skin, re-render                  |
| Depth      | mesh rendered to depth buffer     | compare depth channel of render       |
| Video      | temporal sequence of mesh renders | per-frame render, activation sequence |
| Speech     | drives ANNY face activations      | face bone rotation agreement          |
| Text       | transcription of mouth motion     | mouth bone activation agreement       |
| Multimodal | cross-modal agreement             | pairwise render across paths          |

No Chamfer distance (blocklisted). No free-space Euclidean distance
for keypoints (they are surface points on the mesh). No rotation
geodesic for pose (FK + skin to mesh, then render). Lip-sync is
ANNY face bone rotation agreement between audio-derived and
video-derived activations, not a separate model.

## The undivided unit: 1 SpeakingFaces trial

Gall's Law: a complex system that works evolved from a simple system
that worked. One SpeakingFaces trial already carries image + audio +
video. The ANNY pipeline derives keypoints + pose + mesh. MoGe-3
derives depth. Ground-truth transcripts (Stanford digital assistant
+ Siri command sets) supply text. One trial in, all eight modalities
out.

**Source dataset: SpeakingFaces** (issai/Speaking_Faces, CC-BY-4.0,
142 subjects, 13,000+ instances). Synchronized visual video
(768x512), thermal video (464x348), and audio at nine camera angles.

- https://huggingface.co/datasets/issai/Speaking_Faces
- https://doi.org/10.48333/smgd-yj77

The extraction pipeline per trial:

1. Select a representative frame from the trial video
2. Fit ANNY canonical rig to the frame via AnnyInverter + LBFGS
   polish (SOMA format, 78 bones, float64)
3. Run MoGe-3 on the frame for metric depth
4. Render the fitted mesh to depth/normals via Mitsuba 3
5. Read the ground-truth transcript
6. Extract the synchronized audio clip
7. Extract video frame sequence

All derivations are deterministic from source assets we hold, labels
true by construction (the original IS the ground truth), same seed
reproduces the corpus. This is constructed synthetic, not generated
synthetic, so none of the four conditions for generated data apply.

## Edits are frame pairs, not perturbations

EditScore's format: input + edit instruction + candidate outputs +
scores. The edit instruction is a natural-language command describing
what changed.

MaskScore mirrors this. The edit is always: "edit the {See-Through
part} to match frame B." Frame A is the input, frame B is the
target, both from the same subject. The instruction describes the
change between them using the See-Through part vocabulary.

Candidates are graded executions of the edit:

| rank | candidate                                  | expected score |
| ---- | ------------------------------------------ | -------------- |
| 1    | frame B's representation for that part     | highest        |
| 2    | interpolation between A and B              | high           |
| 3    | partial edit (wrong severity)              | medium         |
| 4    | wrong part edited                          | low            |
| 5    | wrong subject entirely                     | lowest         |

The reward model must recover this ranking. If it cannot rank
frame-pair edits, it cannot rank model-generated reconstructions.
When a denoiser comes online, the candidates swap from frame pairs
to model outputs. The instruction, format, and scoring do not change.

## See-Through part taxonomy as mask vocabulary

The mask vocabulary comes from `bodytags_v3.json` (23 part
categories):

    front hair, back hair, headwear, face, irides, eyebrow,
    eyewhite, eyelash, eyewear, ears, earwear, nose, mouth,
    neck, neckwear, topwear, handwear, bottomwear, legwear,
    footwear, tail, wings, objects

For SpeakingFaces (face video), the active parts are: front hair,
back hair, face, irides, eyebrow, eyewhite, eyelash, ears, nose,
mouth, neck (11 of 23). The remaining 12 activate when the pipeline
extends beyond face data.

Each part maps to a subset of ANNY mesh vertices and SOMA bones.
The edit instruction names the part; the mask targets the
corresponding vertices/bones/pixels/audio span.

## Three datasets (mirroring EditScore)

| dataset              | rows   | purpose                               | EditScore analogue     |
| -------------------- | ------ | ------------------------------------- | ---------------------- |
| maskscore-bench      | ~2,890 | evaluates OmniScore                   | EditReward-Bench       |
| maskscore-reward-train | ~97k | trains OmniScore (the reward model)   | EditScore-Reward-Data  |
| maskscore-rl-train   | ~110k  | trains generators via RL              | EditScore-RL-Data      |

All three share the same schema and task type vocabulary. The bench
set is strictly held out from reward model training and RL training.

## 13 task types in 4 groups

Mirroring EditScore's 13 image-edit task types grouped into object,
appearance, scene, and advanced:

| group      | task types                                           | See-Through parts used                    |
| ---------- | ---------------------------------------------------- | ----------------------------------------- |
| Part       | part_add, part_remove, part_replace                  | headwear, earwear, eyewear, neckwear      |
| Surface    | expression_change, surface_edit, lighting_change, skin_tone | face, mouth, eyebrow, irides, nose  |
| Region     | depth_edit, region_extract, background_change        | front hair, back hair, ears, neck         |
| Motion     | pose_change, speech_edit, temporal_edit, cross_modal_compose | mouth, face, eyebrow, irides, neck |

**EditScore groups for reference:**

| EditScore group | task types                                                         |
| --------------- | ------------------------------------------------------------------ |
| object          | subject-add, subject-remove, subject-replace                       |
| appearance      | color_alter, material_alter, style_change, tone_transfer           |
| scene           | background_change, extract                                         |
| advanced        | ps_human, text_change, motion_change, compose                      |

## Three scoring dimensions

Same as EditScore:

- **instruction_following:** did the edit match what the instruction
  asked for? Measured by render-and-compare on the target part
  region between the candidate and frame B's render.
- **consistency:** was the rest preserved? Measured by
  render-and-compare on the non-target regions between the
  candidate and frame A's render.
- **overall:** weighted combination of instruction_following and
  consistency.

## The eight stubs

All eight score via render-and-compare through the ANNY mesh via
Mitsuba 3. All eight are constructible now from SpeakingFaces +
ANNY + MoGe-3 + Mitsuba 3 + ground-truth transcripts.

### 1. TextEditReward

**What it is:** ground-truth command transcript.
**Edit:** "change the command to {target phrase}."
**Score:** ANNY mouth bone activation agreement between the
candidate text and the video-derived face activations, plus
render-and-compare on the mouth region.

Text comes from SpeakingFaces ground-truth transcripts (Stanford
digital assistant + Siri command sets). Whisper is blocklisted.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_text         | string            | frame A's transcript                     |
| conditioning_image | string            | path to source frame                     |
| output_texts       | list[string]      | candidate transcripts                    |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 2. MeshEditReward

**What it is:** root geometric representation.
**Edit:** "edit the {part} to match frame B."
**Score:** render-and-compare via Mitsuba 3 (L1 depth/normals,
SSIM, LPIPS on `sphere_hammersley_sequence` views).

The mesh is the ANNY canonical rig fitted to the frame. All other
modalities are projections of this mesh.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_mesh         | string            | path to frame A's mesh (.glb)            |
| conditioning_image | string            | path to source frame                     |
| output_meshes      | list[string]      | paths to candidate meshes (.glb)         |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 3. SpeechEditReward

**What it is:** audio that drives ANNY face activations.
**Edit:** "resynthesize the {part} to say {phrase B}."
**Score:** SOMA face bone rotation agreement between
audio-derived and video-derived activations, plus
render-and-compare on the mouth region.

Lip-sync is face bone rotation agreement, not a separate
lip-sync model.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_audio        | string            | path to frame A's audio (.wav)           |
| conditioning_image | string            | path to source frame                     |
| output_audios      | list[string]      | paths to candidate audio (.wav)          |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 4. MultimodalEditReward

**What it is:** cross-modal agreement through the ANNY mesh.
**Edit:** "match the {part} across modalities to frame B."
**Score:** pairwise render-and-compare across all derivation
paths (image, depth, keypoints, pose, speech, text, video).

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_modality     | string            | source modality name                     |
| output_modality    | string            | target modality name                     |
| input_data         | string            | path to input                            |
| output_candidates  | list[string]      | paths to candidate outputs               |
| scores             | list[float]       | pairwise render-and-compare scores       |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 5. KeypointEditReward

**What it is:** surface points on the ANNY mesh.
**Edit:** "refit the {part} landmarks to frame B."
**Score:** displace mesh vertices at the keypoint locations,
re-render, render-and-compare.

Keypoints are not free-floating landmarks. They are vertex
positions on the mesh surface. The metric is surface distance
through the mesh render, not Euclidean distance in free space.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_keypoints    | list[float]       | frame A's surface point coordinates      |
| conditioning_image | string            | path to source frame                     |
| output_keypoints   | list[list[float]] | candidate surface points                 |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 6. DepthEditReward

**What it is:** the ANNY mesh rendered to a depth buffer.
**Edit:** "reconstruct the {part} depth to match frame B."
**Score:** render-and-compare on the depth channel of the
Mitsuba 3 render.

Two depth sources: MoGe-3 (monocular estimation from the image)
and the ANNY mesh rendered to depth via Mitsuba 3 (ground truth
from geometry). The Mitsuba render is the reference.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_depth        | string            | path to frame A's depth map (.exr)       |
| conditioning_image | string            | path to source frame                     |
| output_depths      | list[string]      | paths to candidate depth maps (.exr)     |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 7. VideoEditReward

**What it is:** temporal sequence of ANNY mesh renders.
**Edit:** "transition the {part} from frame A to frame B."
**Score:** per-frame render-and-compare plus ANNY face activation
consistency across the frame sequence.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_video        | string            | path to input frame sequence             |
| aligned_audio      | string            | path to aligned audio (.wav)             |
| output_videos      | list[string]      | paths to candidate frame sequences       |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

### 8. PoseEditReward

**What it is:** bone transforms that produce the ANNY mesh.
**Edit:** "repose the {part} to frame B's expression."
**Score:** FK + skin to mesh, then render-and-compare via
Mitsuba 3. Same metric as every other stub.

The output is SOMA-format bone poses: the same representation
Kimodo-SOMA produces, directly consumable by any downstream
that accepts Kimodo output without running Kimodo itself.

| column             | type              | description                              |
| ------------------ | ----------------- | ---------------------------------------- |
| key                | string            | trial identifier                         |
| instruction        | string            | edit described in natural language        |
| input_pose         | list[float]       | frame A's SOMA rotations [78x3] + t [3]  |
| conditioning_image | string            | path to source frame                     |
| output_poses       | list[list[float]] | candidate bone poses                     |
| scores             | list[float]       | render-and-compare scores                |
| task_type          | string            | one of the 13 task types                 |
| dimension          | string            | instruction_following, consistency, overall |

## Reward model: OmniScore

Qwen3-Omni is the reward model for all eight stubs (OmniScore).
It handles text, image, audio, and video natively. For geometric
modalities (mesh, keypoints, pose, depth), it scores multi-view
Mitsuba 3 renders. The thinker scores its own generations during
training, so the reward model and the generator share weights.

## Construction status

All eight stubs are constructible from existing tools:

| tool              | provides                              |
| ----------------- | ------------------------------------- |
| SpeakingFaces     | image, audio, video, text transcripts |
| AnnyInverter      | mesh vertices, keypoints              |
| LBFGS polish      | refined SOMA bone poses               |
| MoGe-3            | metric depth maps                     |
| Mitsuba 3         | rendered depth/normals for scoring    |
| See-Through partseg | semantic part masks                 |
| bodytags_v3.json  | part vocabulary for instructions      |

No blocked model dependencies. No Whisper (blocklisted). No
Chamfer distance (blocklisted). The pipeline evolves by swapping
frame-pair candidates for model-generated reconstructions one
modality at a time as each denoiser comes online.
