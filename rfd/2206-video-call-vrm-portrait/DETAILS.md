# RFD 2206: Video-call VRM portrait — details

## Amendment 2026-09-05: runtime swap to Godot `platform=web`

The portrait originally shipped as `@pixiv/three-vrm` in
`7-service/service-sqlar-cas/docs/vrm.js`. Per [RFD 2210](../2210-atelier-godot-web-shipping-surface/)
(L3) and [RFD 2216](../2216-threejs-blocklist/) (three.js blocklist),
the three-vrm path is retired. VRM 1.0 loading now happens via
[RFD 2213](../2213-vrm-via-godot-sandbox-elf/) — `V-Sekai/godot-vrm`
compiled to a RISC-V ELF loaded by `modules/sandbox` (libriscv)
inside a Godot `platform=web` export.

The convention this RFD carries (video-call framing, LookAt on
camera, breathing/blink idle, reaction blendshapes, no world
navigation) stays the same. The runtime that renders the portrait
moves from three-vrm-in-a-browser-canvas to Godot-in-a-browser-
canvas. VRM asset (`SK_VRM1_Constraint_Twist_Sample`) unchanged.

The retracted-shape section below still holds — it retracted the
world-navigation input handlers regardless of runtime. Everything
below that references three-vrm specifically applies to how the
convention was implemented, not how it's implemented today; treat
those references as historical.

## The retracted shape

Before this convention landed, `docs/vrm.js` carried:

- WASD / arrow-key handlers driving `avatar.pos.x, z`.
- Pointer-lock mouse look driving `orbit.yaw, pitch`.
- Mouse-wheel zoom driving `orbit.dist`.
- Gamepad L-stick / R-stick reads for the same three targets.
- A camera pose derived per frame from `orbit.*` around a target
  parented to the avatar's chest.

That shape reads naturally for a *scene* (a character walking a
world), and it read wrong for a *dialogue* (a character talking
to the player through a phone-shaped frame). Nothing about the
handlers was buggy — they applied inputs faithfully. The
convention is a signal to the character (the player is holding
still and listening) not a limitation on the inputs.

## The reference implementation

`docs/vrm.js` after the retarget:

- Camera constructed once at boot; parent is `null` (world-space
  pinned) rather than the avatar's head bone. Head-bone-parenting
  was tried and rejected: it slid on breathing sway and read as
  the room shaking, not the character breathing.
- `applyLookAt(now)` reads the head-bone world position each
  frame, offsets +0.55 m along the character's forward axis at
  +0.02 m Y (eye height offset), and writes the camera position.
  Cheap; runs before the render call.
- `applyGlanceAway(now)` maintains one piece of state — the epoch
  of the next glance — and briefly targets a point offset from the
  camera by ~0.25 m along the character's right or up axis (uniform
  random each cycle). Duration 300 ms. Next glance scheduled 4-7 s
  out.
- `applyBreathing(now)` writes a small rotation on `Spine` and
  `UpperChest` — 0.02 rad amplitude, 4 s period. Amplitude and
  period were picked by eye; larger read as swaying, smaller
  wasn't visible.
- `applyBlink(now)` fires the expressionManager `blink` at ~4 s
  period with a 100 ms held-closed window. `@pixiv/three-vrm`'s
  built-in blink cycler was declined because it uses the same
  hook and adding two blinkers is hard to debug.
- `fireReaction(kind)` sets `expressionManager` `happy` /
  `neutral` / `sad` to 1.0, then a per-frame decay drops it back
  to 0 over the next ~1.6 s. The window is deliberately short:
  Starforged play surfaces a menu after each reaction, and a
  facial expression that holds past the next menu confuses the
  next beat.

## Diorama backdrops

Loaded once at scene start via three.js `GLTFLoader`. Static; no
animation. Swap per-scene by unloading the current backdrop and
loading a new one. Small target: any single backdrop under ~500 KB.
The Starforged demo ships `scenes/{cockpit,station-bar,deckplate}.gltf`
as reference set.

## Verification

- The Playwright script at `7-service/service-sqlar-cas/scripts/qa_demo.mjs`
  asserts:
  - `vrm.expressionManager.getValue('happy') > 0` within 200 ms of
    a strong-hit;
  - `vrm.expressionManager.getValue('happy') < 0.05` at 2000 ms
    after (reaction has decayed);
  - the camera position is unchanged across 10 s of idle (no
    world-navigation input reaches the camera).
- **Negative control** (rule 2): the test suite includes a
  scripted keyboard event dispatching WASD; the camera position
  MUST remain unchanged. A revision that reintroduces the WASD
  handler fails this assertion loudly.

## Trademark note

The convention is inspired by a genre of consumer video-calling
apps that share the same framing (eye-level, portrait 4:5,
head-and-shoulders composition). The RFD describes the shape by
its generic vocabulary and does not name any specific app or
platform. See CLAUDE.md's "Trademarks Stay Out of Shipping
Artifacts" clause.

This RFD was drafted by an AI and read by a human before it shipped.
