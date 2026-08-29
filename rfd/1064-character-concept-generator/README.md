# RFD 1064: Character Concept Generator

**State:** prediscussion
**Scope:** To be determined

## Problem

Gall's law asks for the smallest working piece of character
authoring, with appearance traits, animation, and export to an
OpenUSD intermediate format.

## Decision

Encode useful combinations of character concepts into taskweft, and
run it on Fly.io with Nx, with no GPU acceleration.

1. Claude inspects each dataset row by vision, and writes the
   character as a taskweft `problem.ex`. One shared `domain.ex`
   holds the actions and guards, per RFD 1037. This is the Gall's
   law step.
2. Postpone RFD 1042 (Krea 2 Turbo) for image generation.
3. Postpone RFD 1043 (Qwen image edit) to match a T-pose character
   pose.
4. Postpone RFD 1044 (See-Through layer decomposition) to remove
   eyes, eyebrows, irises, and eye whites from the face.
5. Postpone RFD 1040 (Pixal3D) to generate a mesh.
6. Postpone RFD 1046 (SkinTokens) to auto-rig the mesh.
7. Postpone Godot Engine 4.7's humanoid skeleton silhouette
   retargeting.
8. Postpone research into RFD 1045 (Kimodo) to generate a body, if
   clothing, accessories, and objects need separation from the
   Soma-X body.

## Related

RFD 1037 gives the domain/problem split. RFD 1065 gives the schema
this step's `domain.ex` and `problem.ex` files follow. RFD 1042, RFD
1043, RFD 1044, RFD 1040, RFD 1045, and RFD 1046 give the postponed
stages. `DETAILS.md` holds the reference links and the critical-path
diagram.
