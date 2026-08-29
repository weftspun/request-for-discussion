---
title: "RFD 2112: Lexical for the slash command interface"
rfd: "2112"
state: abandoned
scope: the Queen of the Gyre, and what serves her
---

## Status

The slash command field is not being built. The client the Gyre is
getting has hands in it rather than a caret: RFD 2119 puts salvage in a
headset under distributed physics authority, and RFD 2118 takes the
pipeline to a Godot release template driven by sandboxed guests. A
Lexical editor serves neither.

The argument that chose Lexical over ProseMirror was about the caret --
that a parameter must be one thing to it, and that a decorator node
crosses in one key press where an atom node can trap. That argument was
correct and it no longer has a subject.

What survives is the boundary the RFD drew rather than the widget it
chose. Commands still arrive as a command in and reply bytes out,
`thirdparty/interactor` still carries that contract, and the server
still checks on receipt whatever a client chose to show, because a
filtered menu is a convenience and never an authorization. The browser
client in `fabric-store-domain/client/` reached a working editor and a
passing caret suite, and it never opened a live session outside its own
test.

## Problem

`fabric-store-domain/src/queen.c` has no client. Its `main()` founds a ward, runs the
cycles, prints, and exits, with no socket and no instance that outlives the run. A slash
command interface needs a live game and a field to type into, and neither exists.

The field is the harder half. When a player types `/commission`, it must show the parameter
as an inline block that the player cannot edit, with editable space around it. An HTML form
control holds plain text only. A `contenteditable` element can show a block, and written by
hand it fails on the caret, on mobile autocorrect, on IME composition, and on paste.

## Decision

Use Lexical, from Meta. Its decorator node is one block to the caret, which therefore
crosses a parameter in one key press, and Meta tests the mobile and IME paths at Facebook
scale. ProseMirror is rejected, because its atom node can hold the caret and needs a plugin
to correct it. The cost is developer speed, so the version is pinned.

The Queen's rows are entities and they take coordinates. A Spark, a venue, and a contract
each become an entity in the zone model, so the interest filter in `fabric-fanout-edge`
decides who sees a change. A Spark moving to a contract is local by intent and reaches every
box it enters. `/restart` reaches everyone, because one ward serves all players.

The ward is served the way a stream is served. One primary holds the fence and writes.
Secondaries read the same pages out of FoundationDB, and one is hosted when the primary
goes, which `check_fence` makes safe by refusing the old writer. A player may hold a
secondary as a fallback, and a background tab holds its seat with a keepalive.

The menu shows a command only when the caller's rebac relations permit it. The server checks
again on receipt. `fabric-asset-edge` serves the built client on Fly as a transport layer,
and `queen` gains a transport layer of its own.

## References

- Lexical: <https://lexical.dev>. ProseMirror: <https://prosemirror.net>
- RFD 2111 sets the words transport layer and service. RFD 2085 holds the setting.
- RFD 2049 holds the channel classes the ward scalars need. RFD 2050 sets the keepalive.
- The comparison, the entity mapping, and three hazards: `DETAILS.md`

## Detail

{{< include DETAILS.md >}}
