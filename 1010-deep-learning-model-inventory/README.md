# RFD 1010: Deep learning model inventory

**State:** published
**Feature:** model inventory

## Problem

The repository references many model identifiers. The catalog records
no type and no runtime location. A reader cannot tell a neural model
from a geometric algorithm.

## Decision

src/library/aiModelsCatalog.js stays the source of truth for the
identifiers. This RFD records the type, the task, and the runtime
location. The live list filters the catalog when the API connects.

Fifteen models form the inventory, each a deep learning model
packaged as its own model image, per RFD 1024. See `DETAILS.md`
for the full table, plus the client and external models the table
excludes.

## Related

RFD 1004 catalogs the tasks. RFD 101a gives the memory per model. RFD
0028 records the license gate. RFD 101e records the See-Through
components. RFD 1021 lists the geometric algorithms. RFD 1023 lists
the legacy identifiers.
