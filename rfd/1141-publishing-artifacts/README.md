# RFD 1141: Publishing artifacts

**State:** discussion
**Feature:** where results go
**Scope:** anything produced that outlives the machine that made it

## Decision

Artifacts go to Hugging Face. Code stays on GitHub, and each names the
other. A dataset repository holds corpora; a model repository holds
weights, in safetensors, carrying only the tensors that were trained.

Every artifact repository carries a `CITATION.cff` naming its title,
its licence, and every source it derives from. An artifact without one
cannot answer what it is made of, which is condition 1.

The name matches the source repository, and the README names the side
it sits on, so a reader who finds the artifact first reaches the code.

## Problem

Code goes to GitHub, and the goal manifest places every repository on a
side of the hexagon. Artifacts had no such rule. A trained adapter, a
rendered corpus and a set of vertex weights are not code: too large for
a source repository, regenerated rather than edited, and carrying the
licence of whatever they derive from as well as our own. Left on a desk
they go with the desk. Pushed into a source repository they bloat a
history nobody can shrink again.

A checkpoint also lies about its own size: the trainer writes the whole
model, so a 19.5 MiB adapter arrives as 14.8 GiB of mostly somebody
else's Apache-2.0 base weights.

## References

- `SKILL.md` is the procedure. `DETAILS.md` says what is not published.

## Related

RFD 1140 rents the machines. RFD 1000 gives placement.
