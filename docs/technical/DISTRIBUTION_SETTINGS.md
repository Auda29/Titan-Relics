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
An absent file uses Discoveries / Entdeckungen, the highest-frequency preset,
without writing a file automatically. This factory default was selected on
4 November 2026. Existing installation choices and saved world settings retain
their values. Save keeps
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
| Expedition | 5,000 | 2,000 | 15,000 | 6,000 | 15,000 |
| Balanced / Ausgewogen | 3,000 | 1,200 | 9,000 | 3,600 | 8,000 |
| Discoveries / Entdeckungen | 2,000 | 800 | 6,000 | 2,400 | 4,000 |

These are the revision-2 presets for newly created worlds. Existing installation
files keep their saved values until a preset is explicitly selected and saved.
Presets also select Matching landscapes for all families. Applying a preset
replaces its geometry, shares and biome modes together.

All distances are blocks. Search spacing controls the side length of the shared
opportunity grid. Each cell has one family ticket and up to 64 nearby terrain
probes for that same family. Smaller spacing creates more opportunities per
area; biome, terrain and spacing checks still reject unsuitable sites. These
values are neither a guaranteed walking distance nor independent rolls for
every relic. Dense settings also increase planning and locate-search work.

Both skull families receive 15% each outside Obelisk regions and 25% each near
Obelisks. Other family shares remain unchanged. Smaller grids provide more
opportunities per area, while each preset still enforces its minimum separation.
The ordinary minimum distance includes the reserved large-Colossus location.

Revision 2, shipped in Beta 3, checks up to 64 deterministic positions per intersecting 5,000-block
Colossus cell, orders positions by distance, and tests them in expanding rings.
The first ring is 4,000–8,000 blocks for Discoveries, 8,000–16,000 for Balanced,
and 15,000–30,000 for Expedition. These are search aims, not hard maximum travel
distances. The search expands if no valid site exists. There is still one
unique Colossus per supported enabled world, and no unsuitable terrain is forced
to accept a model.

New presets now select revision 3. Its Colossus search uses separate 1,000 × 1,000
block search cells and 1,000-block radial bands, starting at the chosen minimum.
It checks 16 spread-out, seed-jittered chunk centers per cell in the current band.
Cells with a compatible center biome and a valid model envelope receive up to
48 additional probes before the search advances to the next band. The combined
passes cover one position in each 125 × 125 block tile. Positions in each pass
are ordered by distance. Refinement may return to a closer position in the same
band; this is a bounded sample, not an exhaustive nearest-site proof.

For Discoveries, the bands from 4,000 through 8,000 blocks are therefore searched
before any more distant band. This is a preferred area, not a guaranteed maximum.
No height, water, biome or model-fit requirements are relaxed. The ordinary
relic grid, ticket shares and spacing algorithm are unchanged. A different
Colossus destination can still change which nearby repeatable sites pass its
reserved clearance.

Revision 3 journals include `colossusSearch`: the coarse/refinement pass,
refinement-cell set, checked-position totals, completed bands and first-failure
counts for `BIOME_CENTER`, `BIOME_FOOTPRINT`, `BOUNDS`, `TERRAIN` and `DISTANCE`.
The state is committed with the cursor and is exposed by
`/relicsdistribution status`; the final totals also appear in the server log.
`TERRAIN` groups the existing native slope, height, dry-land and river/ocean
conditions. The counters do not claim a separate reason for every condition
that a rejected position might fail.

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
| Crowned Skull | 15% | 25% |
| Sword Skull | 15% | 25% |
| Ruined Tower | 2% | 2% |
| Small Colossus | 2% | 2% |
| World Tree | 2% | 2% |
| Empty | 34% | 14% |

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
    "colossusMinDistance": 4000,
    "generationRevision": 3,
    "outside": [3000, 1500, 1500, 200, 200, 200],
    "inside": [3000, 2500, 2500, 200, 200, 200],
    "biomes": {
      "families": {
        "colossus": {"mode": "LANDSCAPES", "selected": []},
        "obelisk": {"mode": "LANDSCAPES", "selected": []},
        "titan_skull": {"mode": "LANDSCAPES", "selected": []},
        "titan_skull_2": {"mode": "LANDSCAPES", "selected": []},
        "ruined_tower": {"mode": "LANDSCAPES", "selected": []},
        "small_colossus": {"mode": "LANDSCAPES", "selected": []},
        "world_tree": {"mode": "LANDSCAPES", "selected": []}
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
under `relics-distribution-v5-colossus-search`; old policies retain their historical
settings and fingerprint protection. Revision 1 preserves the released v2
ticket layout and coordinates exactly. Generator, biome, asset and world-border
changes remain subject to the existing fingerprint guard.

Validation and reproduction: [initial settings report](../testing/DISTRIBUTION_SETTINGS_20261030.md)
and [world-creation/biome revision](../testing/DISTRIBUTION_WORLD_MENU_20261101.md).

## Generation revisions and existing worlds

`generationRevision` is stored inside settings. Missing values mean revision 1.
Revision 2 uses the `relics-distribution-v4-discoveries` journal policy, so
released binaries reject these worlds instead of silently applying older rules.
Unknown revisions and mismatched policy/revision pairs are rejected. Revision 1 retains the released ticket layout,
biome footprint checks, Sword Skull slope and Colossus candidate order, including
unfinished search cursors. Existing checksummed plans, destinations, maps and
rewards are not migrated by this change. All pinned structure assets stay intact.

Revision 2 introduced the skull-focused presets and effective terrain rules. Matching landscapes
and Custom biome selections apply across the sampled footprint, with one coherent
skull palette. Legacy fixed palette tags no longer veto these explicit selections.
Standard mode retains its fixed palette tags. Ocean, river, dry-ground, vertical
bounds and spacing checks remain. Only the Sword Skull's relative height
tolerance changes from ±4 to ±8 blocks; crowned skull slope limits are unchanged.

Revision 3 uses `relics-distribution-v5-colossus-search` and changes only the
Colossus search strategy. Its terrain predicates are identical to revision 2.
Revision 2 destinations and unfinished search cursors retain their previous
candidate order and start gates. Older binaries reject the revision 3 policy.

The settings screen preserves an existing revision when editing individual values;
selecting a new preset opts future worlds into revision 3. Existing worlds remain
read-only in that screen. There is no retrogen or automatic world migration.

See the [balance verification report](../testing/SKULL_DISTRIBUTION_BALANCE_20261110.md)
for measured native-generator results and their limits. Ticket shares alone are
not treated as evidence of actual discovery density.
The [Colossus search report](../testing/COLOSSUS_SEARCH_20261110.md) records the
separate revision-3 search checks and compatibility evidence.

## Simple and advanced menu views

The screen opens with three play-style choices and a schematic opportunity
diagram. It does not query the generator, read a world seed or locate structures.
Exact preset matching determines the selection; previously saved custom or legacy
settings are labelled Custom settings and are not silently replaced.

Advanced settings exposes named sections for distances, relic shares, biomes and
diagnostics. Both views edit the same cancellable draft. View changes and window
resizing do not save settings. Selecting a preset explicitly replaces the draft
with that preset. Existing worlds open in view-only mode and have no preset or
save actions. The screen supports German and English and narrates the current
style or advanced section.
