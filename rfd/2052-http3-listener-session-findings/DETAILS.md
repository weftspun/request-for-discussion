## Confirmation

The four-player smoke passes at the harness, and a multi-session
reply test starts passing per session when the module fix lands.

## More information

The fix is open as
[godot#56](https://github.com/v-sekai-multiplayer-fabric/godot/pull/56):
a mutex-guarded session list with MultiplayerPeer ids replaces the
single slot, ingress attributes its session, egress routes by target
(broadcast at zero), the drain validates session membership, and
teardown erases before delete. The pattern matches the single
pending-slot bug fixed in `fire/webtransportd@f0fc9a4`.

Post-fix, all four clients receive their own announcements and the
server survives every teardown; the one-listener-per-process limit
stands. A `FabricMultiplayerPeer` probe (ENet factories injected) also
routes four clients correctly and stays an alternative transport for
the loop.

## Consequences

- Issues stay disabled on the engine fork, so this record carries the
  findings.
- The grant-delivery path back to each client is blocked on the
  module fixes, which are queued as engine work: per-session ids on
  the MultiplayerPeer surface, teardown without the double free, and
  ideally multiple listeners per process.
