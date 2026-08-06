# RFD 0018 details: background, plan, risk, references

## Background

The site config still names the M3 origin. The rebrand changed only
the title, so the config now claims the Weftspun name over the M3
identity.

The API reference under `Developers` copies the source. RFD 0000
forbids a copy of the source. The reference has also drifted. The
animation manager source holds 47 methods, and the document lists
26 and misses the viewport and XR work.

## Plan

The work follows this order:

1. Delete the template blog and the template page.
2. Delete the `Developers` reference. Add the code map.
3. Rewrite the `Modders` manifest guides. Delete the originals.
4. Rewrite the `General` guides and the quickstart.
5. Rewrite the history page as a short lineage note.
6. Delete the site config, the sidebars, and the package files.
7. Delete `docs/LICENSE`.

Steps 1 and 2 are complete. Steps 3 to 7 remain open.

## Risk

The image folder holds 29 MB. The history page uses many of those
images. A rewrite of the history page must drop the unused images.

The GitHub Pages workflow named an M3 host. The workflow now runs as
a check only. It builds the app and runs the animation tests. It no
longer publishes to any host. RFD 0013 keeps Vercel as the deploy
path for the public demo.

## Static assets

`m3/static/img/` holds 40 files. Ten markdown files under `m3/docs/`
name 37 of them, under `/img/`. Three go unnamed anywhere in the
repository: `charstudio.jpg`, `overview-app.jpg`,
`overview-schema.jpg`. Delete those three now. Delete each remaining
image only when the guide rewrite that named it either drops the
image or moves to a source the reader can reach on their own.

## References

- M3 notice: `m3/LICENSE`
- Site config: `m3/docs/docusaurus.config.js` (if still present)
- Code map: `m3/docs/CODE_MAP.md` (to add)
- DRY policy: RFD 0000
- Attribution: `README.md`, section Third-Party Trademarks
