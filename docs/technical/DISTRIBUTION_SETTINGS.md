# Relic distribution settings

Available since Alpha 5.0.4 for Fabric and NeoForge, Minecraft 1.21.1 and 26.2.
Alpha 5.0.5 adds the preset-dependent, editable large Colossus minimum distance.

## Menu and scope

In **Create World → World / Neue Welt → Welt**, open **Relic generation /
Relikt-Generierung** below the existing generation switches. Choose a preset,
edit distances, shares and biome rules, then apply. These choices belong to
this creation screen and survive returning from the editor. Cancel and Escape
discard the current editor draft. Hover a field for its meaning and limits.

The editor also opens through the configuration button in **Fabric Mod Menu**
(optional, no hard dependency) or the **NeoForge mod list**. Outside a world,
this edits personal defaults for future worlds. Loading the actual datapack
biome registry can take a moment. There are no extra title/general-options
buttons. While a local gameplay world is loaded, the mod-list entry shows its
saved settings and diagnostics read-only. A remote server or legacy world with
no available journal gets an explicit unavailable message, never assumed values.

Every new gameplay world saves a
validated copy in its checksummed planning journal. Existing worlds retain their
own plan, even in unexplored chunks, and ignore subsequent changes to the
installation defaults. This includes pre-menu v1/v2 worlds. No retroactive
placement or world migration is performed. In-world editing is disabled.

Dedicated servers use their own `config/relics-distribution.json`; a client's
menu cannot change a server. Set the file before creating the server world.
An absent file uses Expedition without writing a file automatically. Save keeps
the previous file as `.bak` and replaces the config atomically. Invalid files
are preserved and rejected; the menu offers an explicit save of replacement
defaults, with the same backup behavior.

Creation writes a validated, world-scoped `data/relics_creation_settings.json`
inside the actual newly created save directory before its server starts. Fresh
world initialization consumes that selection ahead of installation defaults;
the normal frozen journal then becomes authoritative. Existing worlds ignore
both files when loading their saved plan. No process-global world selection,
temporary change to the installation config or server-bound settings packet is used.

## Biomes and diagnostics

Each of the seven relic families has an independent mode:

- **Standard:** the existing exact biome tags, including approved mod mappings.
- **Matching landscapes:** retain Standard and add biomes classified by common
  `minecraft`, `c` and legacy `forge` landscape tags plus explicit known mappings.
  Obelisks match desert/badlands; the large Colossus and Sword Skull open/dry
  landscapes; the Crowned Skull also desert/rocky; Tree open/forest; Tower and
  Small Colossus open/forest/dry. Common tags may overlap; an explicitly dry
  desert may therefore match a dry-land family as well.
- **Custom:** exactly the selected IDs. Switching to Custom initially copies
  the currently permitted set; checkboxes then add/remove individual biomes.

The searchable list comes from the actual loaded datapack registry. Search by
biome ID, mod ID or installed mod display name; tooltips show the mod name,
registry ID and mapped landscape groups. Unclassified entries remain visible
and selectable manually. Missing IDs retained from a saved configuration are
reported rather than silently removed. Loaded-biome counts are not land-area
percentages or estimated find rates; the registry can include biomes absent
from this generator. Biome selection never disables terrain, bounds or spacing
checks. Skull palettes are selected deterministically with no extra ticket roll.
If no biome in the generator's possible-biome set permits the large Colossus
(for example an empty Custom list), the unique resolver commits an unavailable
destination immediately instead of continuing an impossible search.

The final settings page shows rejected biome probes, unsuitable-terrain probes,
world-bounds rejections and spacing rejections since the current server load.
These are diagnostic attempts (including unique-site resolution), not distinct
sites or lifetime totals. New-world/default editors have no measurements yet.
The same counters appear under `diagnostics` in `/relicsdistribution status`.

## Presets

| Preset | Search spacing | Relic minimum distance | Obelisk minimum distance | Obelisk-region radius | Colossus minimum from world spawn |
|---|---:|---:|---:|---:|---:|
| Expedition | 5,000 | 2,000 | 15,000 | 6,000 | 30,000 |
| Balanced / Ausgewogen | 3,000 | 1,200 | 9,000 | 3,600 | 15,000 |
| Discoveries / Entdeckungen | 2,000 | 800 | 6,000 | 2,400 | 8,000 |

All distances are blocks. Search spacing controls the side length of the shared
opportunity grid. Each cell has one family ticket and up to 64 nearby terrain
probes for that same family. Smaller spacing creates more opportunities per
area; biome, terrain and spacing checks still reject unsuitable sites. These
values are neither a guaranteed walking distance nor independent rolls for
every relic. Dense settings also increase planning and locate-search work.

Presets retain the existing family shares. The ordinary minimum distance applies
to all accepted relic centers, including the reserved large-Colossus location.
The unique Colossus uses its independent historical grid and resolver, with one
valid destination per supported enabled world. Its editable minimum distance
from the initial shared spawn now follows the selected preset. The first search
ring extends from that minimum to twice the minimum; priority and valid terrain
choose the destination, so this is not a guarantee of finding the nearest site
or a maximum travel distance. Further rings are searched when needed. Expedition
retains its historical rings and candidate order. Changing ordinary density alone
never creates more large Colossi or changes their candidate stream.

The Colossus-distance revision starts with Alpha 5.0.5; it is not in Alpha 5.0.4.
Previously saved configurations and worlds without `colossusMinDistance` retain
the historical 30,000-block minimum, even if their other values match Balanced
or Discoveries. Existing saved destinations and pending search cursors are kept.
Selecting a preset again in a future-world editor adopts its new minimum;
loading an old save does not. No valid destination still means no fabricated
destination.

## Custom values

- Search spacing: 1,500–10,000.
- Relic minimum distance: 512–4,000, at most the search spacing.
- Colossus minimum from world spawn: 4,000–100,000, at least twice the relic
  minimum distance. This remains separate from distances between relic centers.
- Obelisk-region radius: 500–12,000.
- Obelisk minimum distance: at least the relic minimum, strictly greater than
  twice the region radius and at most four times the search spacing. The last
  bound limits the planner's neighborhood work.
- Shares: 0–100% per family, up to two decimal places. Each region's sum must be
  at most 100%; the remainder stays empty. Zero disables that family in that
  region. Rejections remain empty and do not roll another family.

Shares are edited on four pages: outside Obelisk regions and near Obelisks,
split into two pages each. The Obelisk share is edited once on the first share
page and mirrored into the near-region page; anchor selection cannot depend on
its own region. The menu accepts a comma or dot decimal separator.

| Family | Outside regions | Near Obelisks |
|---|---:|---:|
| Obelisk | 30% | 30% |
| Crowned Skull | 2.5% | 15% |
| Sword Skull | 2.5% | 15% |
| Ruined Tower | 2% | 2% |
| Small Colossus | 2% | 2% |
| World Tree | 2% | 2% |
| Empty | 59% | 34% |

These are opportunity shares before rejection, not final realized frequencies.

## Server configuration example

This is the Discoveries preset. File values for shares are integer hundredths
of a percent: `250` means 2.5%, `10000` means 100%. The menu converts these to
ordinary percentages. Unknown/missing fields, non-integer file values, unsafe
distance combinations and totals above 100% fail validation.

```json
{
  "format": 1,
  "settings": {
    "cellSize": 2000,
    "minDistance": 800,
    "obeliskDistance": 6000,
    "regionRadius": 2400,
    "colossusMinDistance": 8000,
    "outside": [3000, 250, 250, 200, 200, 200],
    "inside": [3000, 1500, 1500, 200, 200, 200],
    "biomes": {
      "families": {
        "obelisk": {"mode": "LANDSCAPES", "selected": []}
      }
    }
  }
}
```

Array order is Obelisk, Crowned Skull, Sword Skull, Tower, Small Colossus, Tree.
`colossusMinDistance` is optional for older format-1 files; absence means 30,000,
not a value inferred from the other preset fields. `biomes` is optional for
older format-1 files; absence means Standard. Family
keys are `colossus`, `obelisk`, `titan_skull`, `titan_skull_2`, `ruined_tower`,
`small_colossus`, `world_tree`. Modes are `STANDARD`, `LANDSCAPES`, `CUSTOM`;
`selected` contains exact namespaced biome IDs for Custom. Old v3 journals
without biome rules also retain Standard behavior.
Do not edit the world journal to apply density changes. Its settings are frozen
under `relics-distribution-v3-settings`; old policies retain their historical
settings and fingerprint protection. Expedition preserves the released v2
ticket layout and coordinates exactly. Generator, biome, asset and world-border
changes remain subject to the existing fingerprint guard.

Validation and reproduction: [initial settings report](../testing/DISTRIBUTION_SETTINGS_20261030.md)
and [world-creation/biome revision](../testing/DISTRIBUTION_WORLD_MENU_20261101.md).
