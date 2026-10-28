# Relic Mod Alpha 5.0 for Fabric 1.21.1

The 1.21.1 port now includes Alpha 5 gameplay: persistent relic distribution,
one natural large Colossus, expedition maps to the same saved target, defense
golem encounters, personal physical Trial/Vault drops and immediate Vault key
payment. Machine Cores have 256 operations. Salvage Magnets work in either held
hand and charge wear per inserted item. Maintenance recipes appear in the book.

The approved large Colossus V7, small Colossus V11, Tower V10, Obelisk V6,
World Tree V5 and corrected Skull 2 are selected for new worlds. Obelisk
archaeology provides the Monolith trim and maps. Trees apply Regeneration II
and Resistance II within 80 blocks, with five minutes after departure. Nearby
selected farm animals receive bounded extra natural attempts under vanilla caps.

## Installation

- Minecraft 1.21.1 and Java 21 or newer.
- Fabric Loader 0.19.5+, Fabric API 0.116.17+1.21.1.
- Lithostitched 1.8.0 for Fabric 1.21/1.21.1.
- Install `relics-0.1.0-alpha.5.0+mc1.21.1.jar`, replacing the previous Relic JAR.

Create a new native 1.21.1 world for all Alpha 5 features. Existing visual-alpha
worlds keep their generation selection. Do not open a 26.2 save in 1.21.1.

## Version differences and checks

1.21.1 uses ferns in place of unavailable firefly bushes and ordinary chests in
the approved reward frames. Positions, loot and access remain the same. Charge
icons, recipe-book data and Monolith trim assets use native 1.21.1 formats.

The artifact is checked on Java 21 with actual Fabric server starts/restarts,
native core/recipe/smithing/menu checks, two simulated-player reward/magnet
tests, Tree aura/cap checks, natural generation, exact footprint/protection
comparison and consumed-loot non-refill. The build is reproducible. These are
server and asset checks; they do not claim a new graphical two-client or arbitrary
modpack/shader acceptance on 1.21.1.

See the [profile and reproduction commands](../../compat/alpha5-fabric-1.21.1/README.md).
Exact hashes and accepted native runs are in the [verification report](../testing/ALPHA_5_FABRIC_1_21_1_20261028.md).
