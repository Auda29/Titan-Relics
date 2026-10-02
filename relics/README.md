# Relic design and gameplay index

Each relic has its own folder. Keep shared workflows in [docs/](../docs/README.md)
and implementation code in `src/`, `tools/`, and `tests/`.

| Relic | Current status |
| --- | --- |
| [Colossus](colossus/README.md) | V3 selected in Alpha 3; core, magnet, and head-trial gameplay not implemented |
| [Obelisk](obelisk/README.md) | V3 selected in Alpha 3; archaeology, collectibles, and Colossus maps not implemented |
| [Titan Skull](titan-skull/README.md) | V3 selected in Alpha 3 with worldgen; authored ordinary-mob exploration not implemented |
| [Ruined Tower](ruined-tower/README.md) | Concept only |
| [World Tree](world-tree/README.md) | Concept only |

## In-game demos

- [Colossus V3 shader demo](colossus/demo/README.md): three actual Minecraft
  screenshots in normal terrain, separate from generated Blender previews.

## V4 studies from in-game inspection

The V3 models remain selected in Alpha 3. The following documents record the
agreed visual findings and revision direction. Colossus V4 now has two offline
[export variants](colossus/docs/COLOSSUS_V4_EXPORTS.md), with B / open machine frame
selected by the user. [Obelisk V4](obelisk/docs/OBELISK_V4_EXPORTS.md) and the four
[Titan Skull V4 variants](titan-skull/docs/TITAN_SKULL_V4_EXPORTS.md) are exported
and checked offline, awaiting visual acceptance and integration.

- [Colossus V4](colossus/docs/COLOSSUS_V4.md): preserve the overall design; focus on
  damaged rear armor, a readable hand with potentially raised fingers, and removal
  or replacement of the simple chest-interior cylinder.
- [Obelisk V4](obelisk/docs/OBELISK_V4.md): weathering, material readability and
  a naturally buried archaeological site at the foot.
- [Titan Skull V4](titan-skull/docs/TITAN_SKULL_V4.md): organic mound transitions,
  biome-compatible surfaces and clearer fossil/bone materials.

## Discovery hierarchy and lore

The intended frequency order is **Titan skulls and future bone/skull variants
(most common) -> Obelisks (clearly rarer) -> Colossi (very rare)**. Alpha 3 has
provisional candidate rates, not final discovery balance; future skull/bone
variants must share the family-level density target.

The working history connects the three: a Colossus was sent to kill the Titans,
while Obelisks served as wayfinders or marked destroyed Titans. Details remain
open in the [lore bible](../docs/project/LORE-BIBLE.md).

## Folder convention

```text
<relic>/
  README.md             # Entry point, status, and links
  docs/                 # Design decisions and version history
  design/
    <asset>.json        # Export/material/preview configuration
    generated/<asset>/  # Blender models, exports, reviews, and provenance
  gameplay/             # Items, loot, encounters, and other gameplay decisions
  demo/                 # Optional in-game screenshots and presentation gallery
```

Future hand-edited sources can live in `<relic>/design/blender/`, separate from
generator outputs. Run pipeline commands from the repository root: config paths
inside JSON remain **repository-root-relative**, not relative to the config file.

Generated folders retain their existing version names, including the Colossus's
original `ots/` experiment. Git includes selected source models, whole exports,
review sheets, and provenance; intermediate files and tile exports stay local.
Do not regenerate assets just to move them.

The playable Alpha 3 explicitly selects the three V3 exports using
`tools/integrate_v3.py`; see [V3 integration](../docs/technical/V3_INTEGRATION.md).
Organizing an asset here alone does not select it or implement proposed gameplay.
