# Weftspun 3D Studio: design notes, moved from `thirdparty/`

These 28 files (this README makes 29) came from
[weftspun/weftspun-3d-studio](https://github.com/weftspun/weftspun-3d-studio)'s
`thirdparty/` directory root, per the user's own direction. They
are not vendored third-party content — several reference `../README.md`
and `../docs/...` paths, confirming they are this project's own
design and planning notes, left at the `thirdparty/` root by an
earlier reorganization (RFD 0060's `thirdparty/` reset) rather than
their own directory.

Unlike the numbered `NNNN-slug/` RFDs elsewhere in this repository,
these do not follow the Oxide RFD format (a scoped `README.md` under
40 lines, a `State:`, a `DETAILS.md`) or ASD-STE100 Simplified
Technical English. They moved here as-is, unedited, to get them out
of a vendored-code directory and into a documentation repository
where they belong. Three PDFs that sat alongside them at the same
`thirdparty/` root did not move, per the user's own direction.

Some content here may be stale (`activeContext.md` and `progress.md`
read as point-in-time working notes, not living documents) or may
duplicate a file that also exists inside a genuinely vendored
subtree (`thirdparty/m3/docs/`, for instance) — that duplication was
not resolved as part of this move, only the loose, orphaned copies
at the `thirdparty/` root were relocated.
