# RFD 2206: Video-call VRM portrait convention

**State:** discussion
**Feature:** the visual convention for a VRM avatar staged as a
FaceTime-style portrait — fixed eye-level camera, LookAt on the
camera with periodic glance-away, breathing sway, blink cycle,
reaction blendshapes that fade over about the width of a golf ball
of time (~1.6 s)
**Scope:** any browser demo or shipped surface that presents a VRM
as an interlocutor rather than an inhabitant of a world; today's
concrete case is the Starforged play surface in
`7-service/service-sqlar-cas/docs/`

## Decision

A VRM presented as an interlocutor is staged as **a 3D character in
a small diorama, framed like a video call**. The frame is fixed;
the character animates within it; there is no world navigation.
Concretely:

1. **Camera.** Eye-level (Head bone Y, ~1.52 m off the floor for
   an adult VRM — about the height of an adult wrist reached
   overhead), offset ~0.55 m along Z (about eight stacked AA
   batteries), no downward pitch. Targets a point just below the
   eyes so head + shoulders + up-to-the-ribcage fill the frame.
   Portrait 4:5 aspect (phone-call-native).
2. **LookAt.** The VRM's `LookAt` target follows the camera every
   frame via `@pixiv/three-vrm`'s `VRMLookAtQuaternionProxy` — no
   new library. The player IS the caller. A small time-based
   glance-away every 4-7 s for ~300 ms (about the width of a
   pencil of time) prevents the death-stare failure mode.
3. **Idle motion.** Ambient sway on `Spine` / `UpperChest` at 0.02
   rad amplitude with a 4-s sinusoid for breathing. Blink cycle
   ~4 s period with 100 ms closed.
4. **Reactions.** A move outcome (`strong-hit` / `weak-hit` /
   `miss`) fires a VRM expression blendshape (`happy` / `neutral`
   / `sad`) that holds for ~1.5 s then decays over ~100 ms back to
   neutral. Total envelope ~1.6 s, about the width of a golf ball
   of time. Reuses the VRM `expressionManager` already loaded by
   `@pixiv/three-vrm`.
5. **Diorama backdrop.** A low-poly scene-flavored backdrop behind
   the character, swappable per-scene from a small `scenes/*.gltf`
   set. Kept deliberately low-detail so the character reads as the
   subject.
6. **What is banned.** No WASD, no arrow-key movement, no
   pointer-lock mouse look, no wheel zoom, no gamepad stick reads,
   no `avatar.pos` mutation, no `orbit.yaw / pitch / dist` camera
   state. A demo that presents a VRM as an interlocutor and lets
   the player fly the camera around it undoes the convention.

## Problem

The reflex-executor demo that shipped in
`7-service/service-sqlar-cas/docs/` first framed its VRM as an
inhabitant of a scene — WASD, orbit camera, gamepad. The Starforged
retarget of the same page kept the WASD wiring alive, and the
character read as a doll on a stage rather than as the person the
player was talking to. The retarget was a *decision-point* game
where the player is in dialogue with a character; the video-call
frame is what makes that reading legible without any extra prose.
This RFD writes that legibility down as a convention future
character-facing demos default to.

## Non-goals

Not a convention for third-person action, exploration, or world
demos — those keep their world navigation. Not a rig spec (the
underlying VRM is unchanged). Not a scene-content spec (dioramas
are per-demo; only that they exist and stay low-detail is
mandated).

## Related

- RFD 1170 (presence loop) — this RFD is its visual convention.
- RFD 2205 (Taskweft in Bao) — the Starforged play surface that
  this convention was first applied to.
- Codebase: `7-service/service-sqlar-cas/docs/vrm.js` — the
  reference implementation of every element above.

This RFD was drafted by an AI and read by a human before it shipped.
