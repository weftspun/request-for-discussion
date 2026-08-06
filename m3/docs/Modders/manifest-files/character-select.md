---
sidebar_position: 2
---

# Character select

`public/manifest.json`, under the `characters` array, drives the
character select screen. Each entry is a character template, the
way a class works in an MMO, or a fighter in a fighting game.

![image](/img/B1DdAF3oa.png)

Each entry names `name`, `description`, `portrait`, `manifest` (the
path or URL to that character's own trait manifest), and `format`:

```json
{
  "characters": [
    {
      "name": "Feminine",
      "description": "Anata Female",
      "portrait": "./assets/portraitImages/anata.png",
      "manifest": "./anata-vrm/female/manifest.json",
      "format": "vrm"
    },
    {
      "name": "Masculine",
      "description": "Anata Male",
      "portrait": "./assets/portraitImages/anata_male.png",
      "manifest": "./anata-vrm/male/manifest.json",
      "format": "vrm"
    }
  ]
}
```

The character's own `manifest.json`, named in the `manifest` field
above, defines its traits. [Getting started](../getting-started.md)
walks through that file.
