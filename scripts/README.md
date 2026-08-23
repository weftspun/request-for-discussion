# Apparatus and gates

Two kinds of script share this directory, and the difference is what they are for.

A **gate** rejects a change. Each one carries its own negative controls, reachable
with `--self-test`, because a check that cannot fail on known-broken input certifies
the defect instead of catching it. The RFD gates check numbering, structure and the
model images; the migrated logbook gates check comment density against a host
project's own p90, that a README indexes no files, that USD layers validate and
round-trip, and that `rfd107a-plan.usda` agrees with RFD 107a. `.pre-commit-config.yaml`
wires them and is the index of which gate runs on which files.

An **apparatus** script re-runs a measurement. Each is kept so a number in an entry can
be re-run rather than believed, which is the whole reason an entry clips its apparatus.
The table below is a map from measurement to entry, not an index of this directory:

| script               | entry                     | what it measures                                                  |
| -------------------- | ------------------------- | ----------------------------------------------------------------- |
| `cfhd_probe.py`      | cineform-movie-writer     | what CineForm costs a depth map, in millimetres, at 10 and 12 bit |
| `bench1024.py`       | soft-renderer-and-mitsuba | the soft renderer at 256, 512 and 1024, with peak memory          |
| `bench_cull.py`      | soft-renderer-and-mitsuba | the bounding-box cull against the unculled reference              |
| `sweep.py`           | soft-renderer-and-mitsuba | block size against work and wall time                             |
| `mi_bench.py`        | soft-renderer-and-mitsuba | first Mitsuba pass, and the three ways it flattered itself        |
| `mi_bench2.py`       | soft-renderer-and-mitsuba | Mitsuba against an exact z-buffer, with Dr.Jit actually synced    |
| `samples.py`         | soft-renderer-and-mitsuba | ANNY depth and silhouette renders, written to disk for inspection |
| `keypoint_render.py` | soft-renderer-and-mitsuba | 104 keypoints coloured by See-Through layer in OKHSL              |

These import from `3-interactor/pose-consensus/python` and expect `anny` installed. They were
run against a local 4090 and name that in their output, because a timing without the machine
is not a measurement.

Two naming conventions are in use here. The RFD gates are `kebab-case.py` and the migrated
logbook scripts are `snake_case.py`. The names were kept through the migration because
CLAUDE.md, PITFALLS.md and several entries cite them; CLAUDE.md records that deferral under
"Why the logbook moved here".
