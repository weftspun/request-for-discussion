# RFD 2138: interactor-shuttle merges spot-broker and uro

They merge as **interactor-shuttle** at `3-interactor/interactor-shuttle`. Interactor
because the primary role is user-facing (GitHub sign-in, landing page, roll button, VRM
download); spot-broker's keeper policy, the TigerBeetle accounting on ecto_sqlite3, and
the FoundationDB event ledger become internal modules rather than peers. `shuttle` fits
the weaving vocabulary the workspace already uses (weftspun, sinew, taskweft).
spot-broker's Fly URL and repo become redirects; RFDs 2133-2137 stay as written, naming
the predecessor service, per the retractions-stay-in-place rule.

**State:** abandoned

This RFD was drafted by an AI and read by a human before it shipped.
