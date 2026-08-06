# RFD 0119 details: the affected-RFD queue

35 RFDs name DGX Spark, Android XR, or Galaxy XR. Each falls into
one of three groups.

## Group A: built around that one machine or headset

Rewriting these replaces the specific name with the general
requirement, keeping the specific name as one example.

| RFD | What it assumes | Status |
| --- | --- | --- |
| 0086 | Dev machine topology names the DGX Spark and a Surface PC as the two machines | Generalized this session |
| 0095 | "A voice XR path... on the DGX Spark" | Generalized this session |
| 0099 | Scripts cheatsheet, 77 DGX-path references, a real runbook for one deployment | Pointer note added; full rewrite still open |
| 0090 | Galaxy XR named in the title; state is abandoned | Deferred; abandoned RFDs are not this decision's priority |

## Group B: Android-specific by real technical necessity, not choice

These do not generalize away. The feature itself is an Android-only
OS or OpenXR extension. The fix is to state that boundary clearly,
not to pretend the feature runs elsewhere.

| RFD | The real boundary | Status |
| --- | --- | --- |
| 0082 | The companion APK is an Android app; native face relay needs Android | Clarified this session |
| 0096 | `XR_ANDROID_face_tracking` is an Android OpenXR extension by name | Clarified this session |
| 0108 | Floor-anchor code path is headset-agnostic already; `Galaxy XR AR` in one heading names the test device, not a requirement | Open |
| 0105 | Webcam driver defers to the Android native bridge only when present | Open |

## Group C: one incidental mention

A path example, a log sample, or a related-RFD pointer names DGX or
Galaxy XR once, with no structural dependency. Lower priority; a
pass can fix wording without changing any decision.

0009, 0013, 0018, 0019, 0027, 0030, 0034, 0036, 0040, 0052, 0060,
0083, 0084, 0085, 0088, 0089, 0091, 0092, 0093, 0094, 0098, 0100,
0101, 0102, 0107, 0110, 0111.

RFD 0027 was already GPU-agnostic; the DGX Spark line in its own
Problem section is a corrected historical artifact, kept as
context, not a live dependency. Gained one line this session naming
the RTX 4090 as a real, supported 24 GB tier.
