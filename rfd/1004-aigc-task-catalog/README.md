# RFD 1004: AIGC task catalog

**State:** abandoned
**Feature:** task catalog

## Decision

Abandoned 2026-09-03. RFD 1102 (supported atelier modules) is the
current task catalog and source-of-truth for models, tasks, and
runtime footprints. RFD 1102's DETAILS.md carries the live table
and its gacha critical path. This RFD is kept for the retraction
record.

Historical decision, as published: one model catalog stayed the
source of truth, mapping task type to API feature and feature to
default model. Live model list filtered the catalog when the API
connected; licence-blocked models stayed out of the UI catalog.

## Problem

The app exposed many AI tasks, each mapping to an API feature and
a model. The catalog needed to stay in sync with the backend model
list.

## Related

RFD 1102 (task catalog, current source of truth), RFD 2174
(open-to-abandoned citation index), RFD 1016 (deep learning model
inventory, also abandoned).

This RFD was drafted by an AI and read by a human before it shipped.
