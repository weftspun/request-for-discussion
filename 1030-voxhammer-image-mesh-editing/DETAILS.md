# RFD 1030 details: the mode branch, the model, the interface, the guard

## The mode branch

```elixir
mode: %{type: :ref, init: %{conditioning: "image"}}
```

`apply_edit` holds one alternative per conditioning. Each one checks
`/mode/conditioning`, thus the planner takes exactly one.

This folder holds `problem.ex` only. RFD 1000 keeps one source per
design, and the domain is that source.

## The model

| Property   | Value                             |
| ---------- | ---------------------------------- |
| Parameters | 0. It shares the RFD 1026 weights |
| bf16       | 8.0 GB, the RFD 1026 cost         |
| License    | MIT                               |

## The interface

| Input     | Type | Default |
| --------- | ---- | ------- |
| mesh      | Path | none    |
| reference | Path | none    |
| region    | Path | none    |
| seed      | int  | -1      |

`reference` is an image of what the region should become. It is not a
texture, and the model does not paste it.

## The same guard applies

`a_decode` requires `/have/preserved_outside`, exactly as in RFD 102f.
The conditioning changed, and the loss in the inversion did not.
