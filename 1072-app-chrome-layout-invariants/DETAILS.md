# RFD 1072 details: tokens, forbidden changes, checklist

Sourced from `app-chrome-layout-protected.mdc`,
`collapsed-rail-icons.mdc`, and `sidebar-z-index.mdc`
(user-confirmed good state, 2026-06-18).

## Tokens

| Token                                          | Purpose                                                          | Owner                                 |
| ---------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------- |
| `--app-content-top`                            | Measured top offset, read by the right rail                      | `:root`, from `App.jsx`; never `.app` |
| `--collapsed-rail-width`                       | Collapsed rail width, both sides                                 | `.app`                                |
| `--collapsed-rail-icon-width` / `-icon-height` | Icon button size, matches the scene-controls hamburgers at 40x40 | `.app`                                |
| `--collapsed-rail-icon-gap`                    | Vertical gap between icons                                       | `.app`                                |
| `--collapsed-rail-icon-padding`                | Icon column padding                                              | `.app`                                |
| `--z-side-panel`                               | Side panel z-index, 998                                          | `.app`                                |
| `--z-app-header`                               | Header z-index, 1001                                             | `.app`                                |
| `--z-scene-controls`                           | Scene controls row z-index, 1002                                 | `.app`                                |

## Shared selectors, styled together

Containers: `.collapsed-sidebar-icons`, `.collapsed-weftspun-icons`.
Buttons: `.sidebar-icon`, `.weftspun-sidebar-icon`. Collapsed width:
`.sidebar.collapsed`, `.weftspun-sidebar.collapsed`.

In-panel hamburgers (`.hamburger-menu`, `.weftspun-sticky-hamburger`)
set `display: none` when collapsed. The scene-controls row hamburgers
stay the active controls in that state.

## Forbidden without an explicit user request

- A fixed task bar with a hardcoded `top` (for example `52px`), or a
  z-index above the header band.
- The right rail's `top` set from `--app-chrome-top-height` alone,
  without `--app-content-top`.
- An asymmetric `padding-top` on one collapsed rail only.
- Removing the `TaskAdvancedOptions` import from `TaskManager.jsx`.
- A side panel z-index raised past 998 to fix an overlap; fix `top`
  instead.

## Protected files

`App.jsx`, `App.css`, `TaskProgressBar.jsx`, `TaskProgressBar.css`,
`TaskManager.jsx` (the `TaskAdvancedOptions` import),
`src/pages/Appearance*.{css,jsx}`, `BottomDisplayMenu.jsx`.

## Visual check, before merging a layout touch

Both rails collapsed: icon rows align, row for row, left to right.
A running task: the progress bar sits below the scene-controls row,
the header stays clickable, and both rails stay aligned.
