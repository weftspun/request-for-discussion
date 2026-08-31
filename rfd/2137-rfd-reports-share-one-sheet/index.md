---
rfd: 2137
title: "RFD 2137: RFD reports share one sheet"
state: "discussion"
feature: "the page template an RFD report is published from"
scope: "any RFD published as a page; the PERT sheet's design system"
---

RFD reports published as pages share one template, `template.html` in
this directory, carrying the PERT sheet's design system: Libre
Franklin over IBM Plex Mono, the paper/ink/critical/done/steel tokens,
light and dark themes resolved at the token level. The layout encodes
the working agreements rather than describing them: measurement tables
carry their baseline row, the retraction block sits in place next to
what it retracts, the controls card lists each planted defect the gate
caught, figures are labelled inline SVG with one claim apiece, and the
provenance foot pairs physical measurements with a household-object
equivalent. To publish a report, copy the file and replace every
bracketed slot; the worked example filling them is RFD 2134, a report
that shipped.
