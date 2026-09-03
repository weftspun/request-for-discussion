# RFD 1028: Model license gate

**State:** published
**Feature:** model licensing

## Decision

Any model shipped to paying users must clear commercial use. The gate
is the hard prerequisite in MODEL_LICENSES.md. The repository keeps a
FOSS blocklist for permissive licenses only.

See `DETAILS.md` for the deleted models and the blocklisted models,
each with its license and its replacement.

## Problem

Some model weights permit non-commercial use only. Some carry
territory rules and user-count rules. The catalog must not ship them
to paying users.

## Related

RFD 1016 lists the active models. RFD 1029 gives the FOSS
replacements. RFD 1035 lists the legacy models. The license audit is
docs/MODEL_LICENSES.md in AlfaOmegaGrafx/3DAIGC-API.
