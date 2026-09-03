# RFD 2017: Compiling godot engine

**State:** prediscussion

## Decision

See `DETAILS.md` for the full argument.

## Problem

Developers build the V-Sekai multiplayer-fabric Godot engine on two
hosts from one workstation: **Windows (PowerShell + MinGW)** and **WSL
/ Linux (`linuxbsd`)**. Without a shared, persistent compiler cache,
each host rebuilds from scratch and cache hits are lost whenever a
checkout is moved or renamed.

## Related

See `DETAILS.md` for the full argument.

This RFD was drafted by an AI and read by a human before it shipped.
