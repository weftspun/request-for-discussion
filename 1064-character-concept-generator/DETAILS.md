# RFD 1064 details: reference links, the critical path

## The critical path

Step 1 is the only active step. Everything below it runs today.
Everything to its side does not run yet.

```
RFD 1064 (root, step 1 active)
 |- RFD 1037  (domain/problem split, step 1 uses this)
 |- RFD 1065  (ETNF schema, step 1's problem.ex follows this)
 |   `- RFD 1021  (HRR library, RFD 1065's resolve step runs on this)
 `- RFD 1000  (conventions, universal)
```

Steps 2 through 8 postpone RFD 1042, RFD 1043, RFD 1044, RFD 1040,
RFD 1046, and RFD 1045. Each is sequenced future work, already
justified by its own step, and not a candidate for deletion under
RFD 1070's rule. A postponed step waits on order. It does not wait
on a guess.

A new RFD earns a place on the critical path only when a step above
names it. RFD 1069, RFD 1071, and RFD 1072 did not clear that bar.
RFD 1070 records the rule they failed.

## Reference links

- https://github.com/taskweft/taskweft
- https://github.com/0b5vr/khr-character-testbed/blob/main/README.md
- https://github.com/Kjakubzak/glTF/tree/kjakubzak/avatar_ext/extensions/2.0/Khronos/KHR_character
- https://huggingface.co/datasets/alfredplpl/anime-with-caption-cc0
