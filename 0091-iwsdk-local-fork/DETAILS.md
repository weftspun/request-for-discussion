# RFD 0091 details: the layout, the commands, and the package table

## Sibling-clone layout

```
/home/sifr/
  immersive-web-sdk/     git clone AlfaOmegaGrafx/immersive-web-sdk
  Weftspun3DStudio/      file:../immersive-web-sdk/packages/*/iwsdk-*.tgz
```

On a second machine, clone `immersive-web-sdk` next to this
project's own checkout the same way.

## Link or refresh

```bash
cd Weftspun3DStudio
npm run iwsdk:link-local              # build tgz if missing, then npm install
npm run iwsdk:link-local:rebuild      # force rebuild the fork, then reinstall
```

Or by hand:

```bash
cd ../immersive-web-sdk
pnpm install && npm run build:tgz:skip-reference-assets
cd ../Weftspun3DStudio && npm install
```

## Packages this project wires in

| Package | Role |
| --- | --- |
| `@iwsdk/core` | World, ECS, grab, locomotion |
| `@iwsdk/locomotor` | `EnvironmentType`, locomotion |
| `@iwsdk/xr-input` | Galaxy XR controllers and hands |
| `@iwsdk/vite-plugin-dev` | XR emulation inside Vite |
| `@iwsdk/cli` | `dev:iwsdk`, adapter sync |
| `@iwsdk/reference` | Reference assets for the CLI |

## Reverting to the npm release

In `package.json`, restore the `^0.4.2` ranges, then run `npm
install`.
