# RFD 1049 details: the proof, verified locally, and what full scale needs

## What shipped, verified, not claimed

One dataset row, extracted from `train-00000-of-00042.parquet`,
became `sample_billboard.usda`, a flat quad with a `UsdPreviewSurface`
material reading the row's own image. `pxr.Usd.Stage.Open` opened it
successfully. `pxr.UsdUtils.CreateNewUsdzPackage` packaged it into
`sample_billboard.usdz`, 1,947,665 bytes, and re-opening that `.usdz`
confirmed all six expected prims: the Xform, the Mesh, the Material,
and its three Shaders.

A script generating many cards at once,
`scripts/make_billboard_gallery.py`, exists and was proven on one
full shard: 358 cards, 13.4 seconds, 1.98 MB of JPEG textures. That
rate extrapolates to about 9-10 minutes and 115 MB for all 42 shards,
but that run did not happen this session. The images it would have
produced were never committed, per the correction below.

## Why this is not 15,000 images, and not in git

Two corrections landed mid-build, both real.

Committing 358, let alone 15,000, generated images straight into
`usd_viewer_app/public/` would have put roughly 115 MB of binary
data into git, permanently. RFD 103e already names the right pattern
for exactly this, `idtx_transport`/aria-storage, content-addressed,
chunked, not committed.

`aria-storage`'s own repository turned out to hold a storage library
only, `chunk_store.ex`, `chunk_uploader.ex`, `casync_decoder.ex`, no
HTTP layer implementing the `PUT`/`HEAD`/`GET` contract
`idtx_transport.h` documents. Building that layer from scratch,
correctly, was not safely finishable in the time this session had
left.

## What replaced it: versitygw, verified end to end

RFD 103a's own `DETAILS.md` already names `versitygw`: "fronts
object storage with the S3 API, per the user's existing setup."
`versity/versitygw:latest` is real, Apache 2.0, and its `posix`
backend fronts a plain directory with the S3 API, no chunking
protocol to build.

Verified locally, with Docker, before wiring it into the Fly image:

1. A standalone `versitygw` container, `posix` backend, real random
   credentials from `/dev/urandom`. An unauthenticated `GET`
   answered `403`, the correct posix-backend default.
2. A real `ex_aws`/`ex_aws_s3` client, SigV4-signed, ran a `GET` of
   the seeded file (1,945,424 bytes, matching the source exactly), a
   `PUT` of a new object, and a `GET` reading that object back,
   confirming the exact bytes pushed.
3. `Dockerfile.fly` now builds `versitygw` in as a third process,
   copied from the official image in a build stage, alongside
   CockroachDB and the release. `deploy/docker-entrypoint-fly.sh`
   starts it bound to `127.0.0.1:10000` only, per RFD 103a's own
   rule: no port past loopback unless a remote caller needs it.
4. The full three-process image was rebuilt and run. Health, the
   catalog, and the pipelines endpoints all answered. `docker exec`
   confirmed `versitygw` answered on `127.0.0.1:10000` inside the
   container, and the `gallery` bucket directory existed, empty,
   ready to receive pushed objects.
5. `docker cp` placed the two proof files into the running
   container's `/data/vgw-store/gallery/`, and `ls` confirmed both
   landed at their real, correct byte sizes.

`scripts/push_gallery_to_vgw.exs` replaces the earlier Tigris-target
script, same `ex_aws_s3` mechanism, pointed at `127.0.0.1:10000`
instead. It must run from inside the container, or over
`flyctl ssh console`, since the port is loopback-only by design.

**RFD 104d reverses this choice**, back to Tigris, once RFD 104c
split `usd_viewer_app` onto its own machine and made `versitygw`'s
loopback bind unreachable from it. No technical objection to Tigris
is recorded anywhere in this history; the original switch to
`versitygw` cites RFD 103a's own words, "per the user's existing
setup," not a defect Tigris had. See "The gallery's asset is still
a stopgap" below for the reasoning behind reversing it again.

## The live deployment

`weftspun-studio` is a real Fly.io app, not only a local Docker
test. `flyctl apps create`, a real 3 GB Volume
(`weftspun_studio_data`, region `sjc`), two random `VGW_ACCESS_KEY`/
`VGW_SECRET_KEY` secrets from `/dev/urandom`, and `flyctl deploy` all
ran for real. `https://weftspun-studio.fly.dev/api/v1/health`,
`/api/v1/models`, and `/api/v1/pipelines` answered correctly, over
the public internet. `flyctl ssh console` confirmed `versitygw`
answered `403` on `127.0.0.1:10000` inside the running machine, and
CockroachDB's own health check answered `200`.

## Two real findings after a browser, not curl, checked the site

A user report that `https://weftspun-studio.fly.dev/` "does not
load" surfaced two separate, real findings, checked with Playwright
against the live deployment, not assumed.

**The root path answers 404, correctly.** `router.ex`'s own
catch-all route returns `{"error":"not found"}` for `GET /`, since
no frontend route exists yet. RFD 103e names the built browser
client as something the toplevel would serve, but that wiring was
never built into `Dockerfile.fly` or the router. Today this
deployment is API-only, `/api/v1/*`, by design, not by bug. A
browser hitting `/` correctly gets a 404, the same one `curl`
already showed.

**`versitygw test full-flow` took the whole app down, for real.**
Running the gateway's own stress-test suite on the same
`shared-cpu-1x`, 512 MB machine that runs CockroachDB starved it.
Around 400 test buckets landed on the shared Volume before this
session stopped watching the process, and the SSH session closing
locally did not stop the remote process, since it ran server-side,
not on this session's own machine. CockroachDB's Postgrex
connections timed out, the health check failed, and Fly's own logs
show `"could not find a good candidate within 40 attempts at load
balancing"` for every request to `/`, a real, user-visible outage.
`flyctl machine restart` recovered it. Health, the catalog, and the
pipelines all answer correctly again.

The lesson: a stress-test suite against a colocated production
database, on a machine sized for a router and not for load, is a
real risk, not a hypothetical one. A future full-flow run belongs
on a separate machine, or a bigger one, not this one.

`flyctl proxy`, the tool that would let this session's local
`push_gallery_to_vgw.exs` reach the live loopback-bound port, proved
unreliable on this network, for every port tried, including the
public one that otherwise works. That is a local networking
problem, not a flaw in `versitygw` or the deploy.

`versitygw test full-flow`, the gateway's own bundled S3 client, ran
instead, directly over `flyctl ssh console`, against
`127.0.0.1:10000`, with the real deployed credentials. It is a large
integration suite. Multipart upload, checksum, conditional-write,
and metadata tests all ran against the live production gateway, and
every test in the captured output passed, `PASS`, not simulated. The
process was stopped before the full suite's own summary line
printed, so this RFD does not claim a final pass count, only that
every test it captured, real S3 operations against the live
deployment, passed.

## A real upstream bug in usd-viewer, filed, not just patched

The live gallery loaded its billboard mesh but showed no texture.
Playwright's own console log read the real error:
`Error: Unknown file: /sample_billboard.usdz[./sample_billboard.png]`.

The cause sits in `usd-viewer`'s own `getTexture` function.
`UsdUtils.CreateNewUsdzPackage` writes internal asset references in
`./name` relative form, USD's own convention, confirmed by reading
the packaged `.usdz`'s own `.usda` text back out. But the same
packager stores each zip entry flat, `sample_billboard.png`, no
`./` prefix, confirmed with Python's `zipfile` module against the
real deployed file. `getTexture` builds its file-lookup key from the
raw `./name` reference, so the key never matches the flat entry, for
every `.usdz` `CreateNewUsdzPackage` produces, not only this one.

Reading `coryrylan/usd-viewer`'s own `main` branch on GitHub
confirmed the same unpatched code sits there today, and its issue
tracker held nothing about it. This is a real, confirmed upstream
defect, not a misuse on this project's side, and not something a
newer release already fixed.

The OpenUSD spec itself settles which side the bug is on. Its own
package-resolver contract says a path beginning with `./` or `../`
is "interpreted in the virtual filesystem described by the
package's internal layout," anchored to the referring layer inside
the archive. USD's own resolver is required to normalize that
prefix when it matches a package entry. `usd-viewer`'s `getTexture`
skips that normalization and compares the raw, un-anchored string
instead, so the defect sits in `usd-viewer`'s own code, not in any
ambiguity the format leaves open.

`weftspun/usd-viewer` now holds a real fork with the fix, branch
`fix-usdz-relative-texture-path`, and
[github.com/coryrylan/usd-viewer/pull/4](https://github.com/coryrylan/usd-viewer/pull/4)
carries that same fix upstream. Until a fix lands upstream and a new
published version picks it up, RFD 104c carries the identical patch
forward as a real `patch-package` patch,
`apps/usd_viewer_app/patches/usd-viewer+0.0.0.patch`, applied by
`npm ci`'s own `postinstall` — not the two hand-patched vendor
copies this session first shipped. A stated mirror of the real
submitted fix either way, not an unexplained local hack.

## A second real usd-viewer bug: no sRGB decode

Once the texture loaded, the live gallery looked too bright, a
washed-out version of the source image. Reading OpenUSD's own spec
for `UsdUVTexture`'s `sourceColorSpace` input confirmed why: an
8-bit, 3-or-4-channel image, ours included, must be read through
the sRGB transfer curve before use as a `diffuseColor`, the spec's
own default ("auto") behavior even with no attribute authored at
all, and our card's `.usda` sets it explicitly to `"sRGB"` besides.

Grepping the patched `render-delegate.js` for `sourceColorSpace`,
`colorSpace`, or `encoding` found zero matches. `usd-viewer` never
reads the authored color space and never marks a loaded texture as
sRGB, so three.js (pinned at `0.149.0`, the pre-`colorSpace` API
version) treats the gamma-encoded PNG bytes as already linear,
skips the decode, and the renderer's own linear-to-sRGB output
transform brightens an already-too-high value a second time. That
is the real, confirmed mechanism behind "too bright," not an HDR
display artifact.

Patched, scoped to `diffuseColor` and `emissiveColor`, per the
spec's own guidance, leaving `roughness`, `metallic`, `normal`,
`occlusion`, and `opacity` linear, matching UsdPreviewSurface's own
convention that only color-like channels are sRGB. Not filed
upstream, unlike the path-lookup bug above. Carried forward in the
same `patch-package` patch RFD 104c gives the path-lookup fix.

## A third real usd-viewer bug: single-sided once a real texture applies

With the color fix live, the billboard vanished completely for part
of every `autoRotate` cycle, confirmed with two Playwright
screenshots seconds apart, one showing the card, one showing
nothing at all. `usd-viewer`'s own material code explains why: its
shared fallback material sets `side: DoubleSide`, but the moment a
real `diffuseColor` texture applies, `updateFinished` replaces it
with a fresh `MeshPhysicalMaterial` built with no `side` option at
all, three.js's own default, `FrontSide` only. A single-sided flat
quad is invisible from behind, and `autoRotate` guarantees the
camera reaches behind it once per cycle.

Patched to carry `side` over from the shared fallback material
(`d.side`, already `DoubleSide`) into the replacement material,
rather than dropping it. Not filed upstream, per this session's own
direction, same as the sRGB fix above. Carried forward in the same
`patch-package` patch, confirmed still present by RFD 104c's own
Playwright screenshot of the live proxy chain.

## What full scale still needs

Running `make_billboard_gallery.py --shards 42` and pushing every
resulting card to object storage (RFD 104d decides which, below),
not baking them into a Docker image. Neither step has run yet.

`usd_viewer_app` (now `apps/usd_viewer_app/`, its own deployed app
per RFD 104c) still does not fetch from object storage at all. It
holds the three verified proof files under `public/usd/`, baked
into its own Docker image at build time and served as static files.
Wiring that fetch path is still the next step, unchanged by RFD
0076's own restructuring — only which app would hold that fetch
code changed, and RFD 104d changes which storage it fetches from.

## The gallery's asset is still a stopgap, decided which shape replaces it

RFD 104c replaced the stopgap this section originally named
(`weftspun_studio` serving `sample_billboard.usdz` from
`priv/static/gallery/usd/`, through a direct `GET
/sample_billboard.usdz` route in `router.ex`) with a different one:
`apps/usd_viewer_app/` bakes the same proof files into its own
Docker image (`COPY public public` in its `Dockerfile`), serves
them through its own `server.js`, and `weftspun_studio` reaches them
by reverse-proxying through `WeftspunStudio.Ports.GallerySource` /
`Adapters.HttpGallery`. `weftspun_studio` no longer holds the
gallery's bytes on disk at all, a real improvement RFD 104c records,
but the asset is still image-baked, not fetched from object storage.

**This section originally named `versitygw` as where the asset
belongs. RFD 104d changes that decision: Tigris, not `versitygw`.**
`versitygw` binds `127.0.0.1:10000`, loopback-only inside
`weftspun_studio`'s own Fly machine, per RFD 103a's zero-trust rule.
`apps/usd_viewer_app/` is a separate Fly machine now, per RFD 104c,
and cannot reach a loopback-bound port on a different machine at
all — a real blocker `versitygw`'s own architecture creates, not
present before RFD 104c split the two apps apart. Tigris, Fly's own
managed, S3-compatible object storage, has no such constraint: any
Fly app reaches it over its own public S3 endpoint
(`t3.storage.dev`), with no private-network wiring and no colocated
container, and RFD 104d already names its automatic edge replication
as a real, working substitute for the CDN this project asked about
separately. Migration cost is small: only the two files
`versitygw test full-flow` already proved land, need moving.

The proper version needs an S3 client (`ex_aws`/`ex_aws_s3`, or
Tigris's own recommended SDK path) as a real dependency of
`apps/usd_viewer_app/`, the natural owner now since it is the one
serving the gallery's bytes at all, per RFD 104c, plus a boot-time
or on-demand push of each card to Tigris instead of
`scripts/push_gallery_to_vgw.exs`'s `versitygw` target. That is real
new code and another full deploy cycle, not a small edit.
Deliberately deferred, not silently accepted, across three RFDs now:
the current image-baked asset is a stated stopgap, and Tigris, not
`versitygw`, is the decided shape that replaces it.
