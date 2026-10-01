# Relic design and gameplay index

Each relic has its own folder. Keep shared workflows in [docs/](../docs/README.md)
and implementation code in `src/`, `tools/`, and `tests/`.

| Relic | Current status |
| --- | --- |
| [Colossus](colossus/README.md) | V3 asset exported; core, magnet, and head-trial gameplay specified but not implemented |
| [Obelisk](obelisk/README.md) | V3 asset exported; gameplay planning remains open |
| [Titan Skull](titan-skull/README.md) | V3 asset exported; worldgen and gameplay remain open |
| [Ruined Tower](ruined-tower/README.md) | Concept only |
| [World Tree](world-tree/README.md) | Concept only |

## Folder convention

```text
<relic>/
  README.md             # Entry point, status, and links
  docs/                 # Design decisions and version history
  design/
    <asset>.json        # Export/material/preview configuration
    generated/<asset>/  # Blender models, exports, reviews, and provenance
  gameplay/             # Items, loot, encounters, and other gameplay decisions
```

Future hand-edited sources can live in `<relic>/design/blender/`, separate from
generator outputs. Run pipeline commands from the repository root: config paths
inside JSON remain **repository-root-relative**, not relative to the config file.

Generated folders retain their existing version names, including the Colossus's
original `ots/` experiment. Git includes selected source models, whole exports,
review sheets, and provenance; intermediate files and tile exports stay local.
Do not regenerate assets just to move them.

The playable alpha still uses the separate generators and resources described
in the [main README](../README.md). Organizing an asset here does not integrate
it into the mod build or imply that proposed gameplay is implemented.
