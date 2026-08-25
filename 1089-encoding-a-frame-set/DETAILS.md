# RFD 1089 details: What the encode measured

## Throughput

Measured on this desk, 16-thread CPU, one job:

| stage           | quantity                                    |
| --------------- | ------------------------------------------- |
| input           | 96 frames, 1024 by 1024, packed 8-bit RGBA  |
| raw size        | 402.7 MB, which is 96 x 1024 x 1024 x 4     |
| output          | 23.4 MiB, CineForm RGBA_4444, quality 3     |
| ratio           | 16.8 to 1                                   |
| encoder time    | 554 ms                                      |
| rate            | about 173 frames per second                 |
| playback        | 8 fps, so 12 seconds of clip                |

The clip is 12 seconds and took 0.554 s to make, which is 21 times
realtime. `interactor-cineform` publishes 112 fps at 1920 by 1080 for
RGB; this is a smaller frame with an alpha channel, and the two figures
sit either side of the pixel-count scaling as expected.

Against the render the encode disappears. The same 96 frames took 32.3 s
on the card and would take 2 h 5 min at llvm's 78 s a frame.

## What the clip does to a frame hash

Every render writes a sidecar carrying a sha256 of its PNG. CineForm is
visually lossless and is not bit-exact, so a frame decoded from the clip
will not reproduce that digest. Nothing is wrong with either, and the
`.cff` says which artefact the hash names.

Two ways to keep a check, and neither is chosen here:

- Hash the container. One digest for the sweep, which answers "is this
  the clip we made" and not "is this frame the frame we rendered".
- Keep the PNGs as the archival form and treat the clip as the viewing
  copy. Costs the storage the clip was meant to save.

## The build, and what it cost to find

Four traps, each of which produced a wrong answer rather than an error.

`repo init` inside `3-interactor/interactor-cineform` re-pointed the
WORKSPACE manifest at that project. It reports only "repo has been
initialized in C:\weftspun-keypoint". Recovery: the manifests git keeps
its history, `git -C .repo/manifests reflog` names the branch, and
`repo init -u .../weftspun-keypoint -b <branch> -m default.xml` restores
it. `repo list | wc -l` is the check.

`up.py` under `nohup` builds the library and then starts the encoder as
its own child, so both exit together. The next command then waits on a
service that is not there and prints nothing at all.

iceoryx2's Windows PAL prints `FindNextFileA ... there are no more
files` and `RemoveDirectoryA ... the directory is not empty` during
normal startup. They look like failures and are not.

The composing manifest was incomplete. `service-cineform/default.xml`
listed the two programs and the bus, but a manifest root's own list is
not read when the project is one of ninety-four, so a workspace sync
gave the programs and nothing they link. The root manifest now carries
iceoryx2, cineform-sdk, libwebm and FTXUI under the service, and both
builds take them through the cache paths the CMakeLists expose.
