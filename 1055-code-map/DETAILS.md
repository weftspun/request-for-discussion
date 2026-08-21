# RFD 1055 details: the module table, by group

## React contexts

Path: `src/context/`

| Context | Role |
| --- | --- |
| `SceneContext.jsx` | Scene state and the loaded avatar |
| `Core3DContext.jsx` | Renderer, camera, and viewport state |
| `TaskContext.jsx` | Task list state for the Task Manager |
| `AccountContext.jsx` | Wallet account state |
| `AudioContext.jsx` | Audio graph and lip-sync input |
| `SoundContext.jsx` | Interface sound effects |
| `ViewContext.jsx` | Active page and view state |
| `LanguageContext.jsx` | Interface language |

## Scene and rendering

Path: `src/library/`

| Module | Role |
| --- | --- |
| `sceneManager.js` | Three.js scene, camera, and render loop |
| `effectManager.js` | Post effects and transitions |
| `sharedHDRManager.js` | Shared environment lighting |
| `viewportLighting.js` | Viewport light and exposure state |
| `cameraFrameManager.js` | Camera framing for avatars |
| `vrmManager.js` | VRM load and unload |
| `sparkSplatManager.js` | Gaussian splat view, through Spark.js |

## WebXR

Path: `src/library/sceneManagerXr*.js`

The XR code splits by concern, one concern per file: input,
locomotion, teleport, grab, interaction, menus, axes, controller
visuals, gamepad buttons, measure, mouse emulation, and the avatar
view. RFD 100a (weftspun-3d-studio's own `decisions/`) gives the
WebXR design.

## Avatar and traits

| Module | Role |
| --- | --- |
| `characterManager.js` | Avatar assembly and trait swap |
| `manifestDataManager.js` | Manifest load and trait lookup |
| `animationManager.js` | Animation load and playback |
| `blinkManager.js` | Eye blink timing |
| `lookatManager.js` | Head and eye aim |
| `EmotionManager.js` | Expression state |
| `assetManager.js` | Asset fetch and cache |

RFD 1005 records the avatar and VRM pipeline.

## Export and generation

| Module | Role |
| --- | --- |
| `screenshotManager.js` | Viewport capture |
| `thumbnailsGenerator.js` | Trait thumbnail sheets |
| `spriteAtlasGenerator.js` | Sprite atlas output |
| `loraDataGenerator.js` | LoRA training image sets |
| `OverlayTextureManager.js` | Texture overlay composition |
| `zipManager.js` | Archive output |
| `VRMExporter.js` | VRM write |

## Tasks

| Module | Role |
| --- | --- |
| `taskManager.js` | Job submit and poll, against `3DAIGC-API` |
| `taskPersistence.js` | Task storage in the browser |
| `aiModelsCatalog.js` | Task types and model names |

RFD 1003 records the job lifecycle. RFD 1004 records the task
catalog.

## Wallet and payments

| Module | Role |
| --- | --- |
| `solanaManager.js` | Solana wallet calls |
| `baseX402Manager.js` | Base chain x402 calls |
| `thirdwebX402Manager.js` | Thirdweb x402 calls |
| `vanaDataManager.js` | Vana data calls |
| `mint-utils.js` | Mint helpers |

RFD 100c records the wallet decision. That RFD's own state is
abandoned.

## Hardware bridges

| Module | Role |
| --- | --- |
| `mbientLabsManager.js` | MbientLab sensor input |
| `tapStrapManager.js` | Tap Strap input |
| `nativeFaceBridge.js` | Android face-bridge interface |
| `nativeFaceRelay.js` | Face data relay to the browser |

## Pages

Path: `src/pages/`

Each page file holds one route. `src/App.jsx` maps the routes. RFD
0001 records the app shell and the routing.
