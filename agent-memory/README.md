# agent-memory

Facts an AI agent should know when starting a session in this
workspace, dumped from Claude Code's per-folder memory
(`~/.claude/projects/<hash>/memory/`) so they survive folder
deletes and machine moves.

Each file follows Claude Code's memory format: yaml frontmatter
(`name`, `description`, `metadata.type` = user / feedback / project
/ reference), then a fact in the body. Cross-links between memories
use `[[name]]` where `name` is the other memory's `name:` slug.

`INDEX.md` is the one-line-per-memory index the harness auto-loads
on session start.

## Restoring into a new machine's Claude Code memory

Claude Code keys its memory by the absolute workspace path. On a
fresh checkout on a different machine, the memory directory the
harness reads is empty. Restore with:

    # POSIX
    dst="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')/memory"
    mkdir -p "$dst"
    cp 2-contract/manuals-weftspun/agent-memory/*.md "$dst/"
    mv "$dst/INDEX.md" "$dst/MEMORY.md"

    # PowerShell
    $slug = (Get-Location).Path.Replace(':','').Replace('\','-')
    $dst = "$env:USERPROFILE\.claude\projects\$slug\memory"
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Copy-Item 2-contract/manuals-weftspun/agent-memory/*.md $dst
    Rename-Item "$dst\INDEX.md" "$dst\MEMORY.md"

Subsequent Claude Code sessions in this workspace auto-load
`MEMORY.md` and any memory files it references, on session start.

## Editing rule

The dump here is the source of truth. Local
`~/.claude/.../memory/*.md` edits are drifty. When a session records
a new persistent fact worth surviving, it should land here in one
commit rather than only in its per-folder memory dir.
