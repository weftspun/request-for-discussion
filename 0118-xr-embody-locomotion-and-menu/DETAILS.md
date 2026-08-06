# RFD 0118 details: forbidden changes

Sourced from `xr-avatar-view-locomotion-protected.mdc`
(user-locked 2026-07-26).

Without an explicit user request, a change must not:

- Teleport the avatar back to its pre-embody spot on disembody,
  instead of the exit spot the user actually stood at.
- Shift the rig's Y position on embody.
- Leave Move set to Avatar after the user switches to third person;
  Move must follow the view switch to Viewpoint.
- Require the in-headset menu to be open before Left X or the stick
  click can toggle view or Move.
- Float the menu roughly 0.5 m ahead of the controller grip; the
  panel's bottom edge belongs on the grip itself.
