# Relic distribution settings

Implemented on the feature branch for Fabric and NeoForge, Minecraft 1.21.1 and
26.2. This feature is not part of the published Alpha 5.0.3 artifacts.

## Menu and scope

Open **Relic distribution / Relikt-Verteilung** at the upper left of the title
screen or Options screen. Choose a preset, edit values if desired, then save.
Cancel and Escape discard edits. Hover a field for its limits and meaning.

These are defaults for **new local worlds**. Every new gameplay world saves a
validated copy in its checksummed planning journal. Existing worlds retain their
own plan, even in unexplored chunks, and ignore subsequent changes to the
installation defaults. This includes pre-menu v1/v2 worlds. No retroactive
placement or world migration is performed. The options button while connected
to a server still edits only future local-world defaults.

Dedicated servers use their own `config/relics-distribution.json`; a client's
menu cannot change a server. Set the file before creating the server world.
An absent file uses Expedition without writing a file automatically. Save keeps
the previous file as `.bak` and replaces the config atomically. Invalid files
are preserved and rejected; the menu offers an explicit save of replacement
defaults, with the same backup behavior.

## Presets

| Preset | Search spacing | Relic minimum distance | Obelisk minimum distance | Obelisk-region radius |
|---|---:|---:|---:|---:|
| Expedition | 5,000 | 2,000 | 15,000 | 6,000 |
| Balanced / Ausgewogen | 3,000 | 1,200 | 9,000 | 3,600 |
| Discoveries / Entdeckungen | 2,000 | 800 | 6,000 | 2,400 |

All distances are blocks. Search spacing controls the side length of the shared
opportunity grid. Each cell has one family ticket and up to 64 nearby terrain
probes for that same family. Smaller spacing creates more opportunities per
area; biome, terrain and spacing checks still reject unsuitable sites. These
values are neither a guaranteed walking distance nor independent rolls for
every relic. Dense settings also increase planning and locate-search work.

Presets retain the existing family shares. The ordinary minimum distance applies
to all accepted relic centers, including the reserved large-Colossus location.
The unique Colossus still uses its independent historical grid and resolver:
one valid destination per supported enabled world, at least 30,000 blocks from
the initial shared spawn. Changing ordinary density never creates more large
Colossi or moves their candidate stream. No valid destination still means no
fabricated destination.

## Custom values

- Search spacing: 1,500–10,000.
- Relic minimum distance: 512–4,000, at most the search spacing.
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
    "outside": [3000, 250, 250, 200, 200, 200],
    "inside": [3000, 1500, 1500, 200, 200, 200]
  }
}
```

Array order is Obelisk, Crowned Skull, Sword Skull, Tower, Small Colossus, Tree.
Do not edit the world journal to apply density changes. Its settings are frozen
under `relics-distribution-v3-settings`; old policies retain their historical
settings and fingerprint protection. Expedition preserves the released v2
ticket layout and coordinates exactly. Generator, biome, asset and world-border
changes remain subject to the existing fingerprint guard.

Validation and reproduction: [settings test report](../testing/DISTRIBUTION_SETTINGS_20261030.md).
