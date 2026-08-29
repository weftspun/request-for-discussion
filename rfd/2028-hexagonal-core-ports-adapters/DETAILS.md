## Context and problem statement

Components in the stack span several languages (C, C++, Python,
Elixir, GDScript), run as separate processes, and each binds to
hardware, a GPU, the network, or an engine runtime. A component has to
stay testable without its device, replaceable without a rewrite of its
callers, and composable with components written in another language.
A shared monolith or a single in-memory object model does not hold
across those boundaries.

## Decision drivers

- Real-time and pipeline paths cross process and language boundaries
  with no shared object model.
- Hardware, OS, GPU, network, and engine concerns have to stay out of
  the entities and the interactors, or they become untestable away
  from the live system.
- CI runs the interactors against recorded data, without the device or
  the runtime.
- One computed result often feeds several outputs from a single pass.

## Decision outcome

Each component takes a uniform `entities/` + `repositories/` +
`datasources/` layout, in the Netflix formulation of the pattern.
Components compose into a service, as RFD 2111 defines a service.

### entities/ — the objects, and the interactors that act on them

An entity is an object the component works on, and it knows nothing
about where it is stored. An interactor performs the actions on
entities. Together they open no socket, read no device, and link no
framework. They carry their own `entities/spec/` of tests that run in
isolation against recorded data. A transport layer never reaches
inside them.

### repositories/ — interfaces to the entities

A repository is an interface that gets, creates, and changes entities.
The interactor declares it and a data source implements it.

A repository stays at the lowest common denominator every binding
language can implement: a C-ABI struct of function pointers where a
service crosses languages, a language-native interface where it does
not. One header then binds C, C++, and Python data sources alike.

### datasources/ — the implementations, outside the interactor

A data source implements a repository against the real world: a serial
device, a UDP socket, a recorded fixture for CI, a GPU compute host, a
renderer, an engine runtime. One repository admits many data sources,
so one pass of an interactor reaches several destinations, and a
recorded fixture stands in for live hardware under CI.

### The transport layer, and composition across the seam

A transport layer is the input that triggers an interactor. All
dependencies point inward, so the transport layer depends on the
interactor and never the reverse.

Components compose when a data source of one component is the
transport layer of another. An in-process dependency links the sibling
directly. A cross-process dependency meets on a wire, which is a
protocol the two ends share. The wire is the integration contract, so
a producer in one language and a consumer in another share no code,
only the message format. Each component declares its sibling wiring
beside its repositories.

## Consequences

- Entities and interactors with no dependencies let CI replay recorded
  data through them with no device and no runtime.
- The wire seam decouples languages and processes, so any component is
  rewritable or replaceable as long as it keeps the message contract.
- A new output is a new data source, with no change to the interactor
  that produced the data.
- All dependencies point inward, so a data source depends on the
  interactor through a repository, and the interactor depends on
  nothing.
- The convention costs interface boilerplate, and across a process
  boundary it adds a serialize and parse step the in-process link
  avoids. That cost buys cross-language, cross-process composition.

## More information

The `sinew-mocap` components apply the pattern end to end. Each git
repository (`driver`, `mount_drift`, `solve`, `viewer`, `vr_bridge`)
carries the triad. The interfaces are header-only C struct vtables
(FrameSource, TrackerSink, PoseSink, HmdSource). The data sources bind
the serial dongle, a recorded `.rawlog`, UDP, polyscope, SteamVR,
OpenVR, and Vulkan. The components compose over the `/sinew` OSC wire
(UDP 39539), and each `sibling-repos.txt` declares the wiring. The
synthetic-data branch in `sinew-vrdance/pose_distill` applies the same
triad in Python: geometry and label cleaning inside, interfaces for the
teacher pose model, the renderer, and the dataset, and data sources for
the model, the Godot renderer, and the COCO output.

Those files still carry the older names on disk, and the `*_source.h` /
`*_sink.h` spelling with them. RFD 2111 holds the rename list.
