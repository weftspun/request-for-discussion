# Details

## Context

The zone server binary was built by `multiplayer-fabric-baker` and
pushed to `ghcr.io/v-sekai-fire/godot-zone-double`. The zone deploy
workflow (in `multiplayer-fabric-zone`) used `--local-only` with
`docker/login-action` to pull that image, but received 403 Forbidden.

GitHub Container Registry ties package write access to the repository
whose `GITHUB_TOKEN` created it. The zone repo's token could not push to
a package owned by the baker repo, and could not pull a private package
owned by another repo without package-scoped access.

## Consequences

- Package names must reflect the owning repo to avoid confusion.
- Moving a package between repos requires deleting it (needs
  `delete:packages` API scope) and rebuilding, or renaming.
- Cross-repo GHCR access requires either a PAT with `read:packages`
  scope or making the package public.
