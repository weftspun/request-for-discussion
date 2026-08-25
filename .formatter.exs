# Formats every RFD's taskweft RECTGTN domain/problem/plan file.
# Moved here from weftspun-3d-studio's own root .formatter.exs when
# decisions/ itself moved to this repository.
# `*/*` reached scripts/ when the logbook merged in, and its .exs files were
# never mix-formatted. Each half keeps the convention it arrived with.
[
  inputs: ["[0-9][0-9][0-9][0-9]-*/*.{ex,exs}"],
  line_length: 98
]
