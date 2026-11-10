# Your first relic expedition

This guide describes Beta 3. Its revision-2 generation settings apply when a new
preset is selected for a new world. Existing Beta 1 and Beta 2 worlds keep
their saved rules. Start with the [installation guide](INSTALLATION.md) for
files and dependencies.

## Before creating the world

Open **Create World → World → Relic generation**. Start with one of the three
play styles. The simple view shows short descriptions and an illustrative
distribution diagram. This is not a seed preview or a promise of fixed find
locations. **Advanced settings** contains distances, family shares, biomes and
diagnostics; **Back to simple settings** keeps unsaved edits.

Expedition leaves more space
between opportunities; Balanced and Discoveries offer progressively more.
Discoveries is the factory default when no saved choice exists. Existing installation defaults and world plans keep their values.

The large Colossus has its own minimum distance from the original world spawn:
15,000 blocks for Expedition, 8,000 for Balanced and 4,000 for Discoveries.
These are lower bounds, not maximum travel distances. Terrain and biome checks
can push a valid site much farther away. Search spacing does not mean a relic
is guaranteed every few thousand blocks.

New presets favor skulls: each skull family receives 15% of opportunities away
from Obelisks and 25% near them. Matching landscapes includes suitable classified
modpack biomes. These remain chances before terrain and spacing checks.

Apply a preset or your own distances, family shares and biome selections before
creating the world. The world keeps that selection, even for later unexplored
chunks. The mod-list configuration edits future-world defaults outside a world;
the loaded local world's settings are read-only. A dedicated server uses its own
configuration. Details are in [distribution settings](../technical/DISTRIBUTION_SETTINGS.md).

## Explore and investigate

Relics appear in the Overworld. Carry supplies for a journey, look at the shape
of the landscape and investigate accessible openings. Not every large landmark
has a chest or a scripted fight. Ordinary Minecraft building and mining remain
part of exploration.

Bring a brush when investigating an Obelisk. Look for suspicious sand and gravel
around its archaeological remains and brush them rather than breaking them.
Finds can include an expedition map and a smithing template. Archaeology and
ordinary containers are shared, finite finds; returning later does not refill
them for another player.

## Follow an expedition map

Hold the map, use its player marker to orient yourself and travel toward the
marked destination as with other Minecraft exploration maps. The target may
still be a long journey away. Recovered maps lead to the same unique large
Colossus in a supported world; another map does not create another Colossus.
Maps can be copied and shared using normal map-copying behavior.

A map whose destination is not yet confirmed can resolve later. If the planner
establishes that no valid destination exists, the special map find compensates
with emeralds. If you already hold an unavailable map, use it to claim the
compensation. Do not assume an unconfirmed destination means your save needs
repair. If it remains unresolved, report it with the information in the
[reporting guide](INSTALLATION.md#reporting-a-problem).

The large site's encounter has personal participation and reward tracking.
Successful Vault use consumes its key immediately and drops the reward into
the world, so collect it. Shared archaeology and ordinary chest contents follow
different rules from the personal Vault reward.

## Use and recharge the Machine Core

Put a charged Machine Core into the fuel slot of a furnace, blast furnace or
smoker. It keeps the appliance's normal processing speed and spends charge on
completed operations. Idle time does not drain it. The tooltip reports remaining
charge; the current full capacity is 256 operations.

The depleted core stays intact. Recharge it at a crafting table with an amethyst
shard directly above it and a coal block on either side. All other slots are empty.
Recharging requires a fully depleted core and returns that core fully charged.
The recipe also appears in the recipe book.

## Use and repair the Salvage Magnet

Hold a working magnet in your selected main hand or offhand while playing
Survival. It attracts nearby dropped items with a clear path and available
inventory space. Leaving it in an ordinary inventory slot keeps it inactive.
It does not collect through solid walls or bypass another player's pickup claim.

The tooltip shows the remaining item budget. Wear counts actual collected
items, not just stacks; current full capacity is 1,000 items. Broken magnets
remain as items. A found magnet may already need repair.

Repair a worn or broken magnet in a crafting table: amethyst shard above the
magnet, iron ingots immediately left and right, and another iron ingot in each
bottom corner. Leave the other slots empty. Four iron ingots and one shard
restore its full budget; a full magnet cannot be repaired again.

## Find a place to rest

The World Tree's aura grants Regeneration II and Resistance II within 80 blocks
in all directions, with a five-minute tail after leaving. Its surroundings can
support extra natural animal spawning under normal habitat and population caps.
Neither effect makes it an unlimited resource farm.

The capacities and effect values above describe the current implementation.
Longer Survival feedback may lead to later balance changes. For known modpack,
LOD and existing-world limits, read [installation and support](INSTALLATION.md).
