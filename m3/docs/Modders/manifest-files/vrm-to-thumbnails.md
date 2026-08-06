---
sidebar_position: 6
---

# VRM to thumbnails

The thumbnail generator renders one image per asset in a trait
group, and writes each to a subdirectory named for that group. Use
the output to fill in a character's `manifest.json` thumbnails.

Defaults: `backgroundColor` `[1,1,1,0]` (white, transparent),
`thumbnailsWidth`/`thumbnailsHeight` 128, `topFrameOffset`/
`bottomFrameOffset` 0.1, `cameraPosition` `"front"`.
`thumbnailsCollection` skips a `traitGroup` not present in the
character's own manifest.

```json
{
    "poseAnimation": "/Idle.fbx",
    "animationTime": 0,
    "backgroundColor": [0, 0, 0, 0],
    "screenshotOffset": [0, 0],
    "topFrameOffset": 0.1,
    "bottomFrameOffset": 0.1,
    "thumbnailsWidth": 512,
    "thumbnailsHeight": 512,
    "thumbnailsCollection": [
        {
            "traitGroup": "CLOTHING",
            "cameraPosition": "front-left",
            "cameraFrame": "mediumShot",
            "groupTopOffset": 0.1,
            "groupBotomOffset": 0.1
        },
        {
            "traitGroup": "HAIR",
            "cameraPosition": "front-left",
            "cameraFrame": "mediumShot",
            "groupTopOffset": 0.1,
            "groupBotomOffset": 0.1
        }
    ]
}
```
