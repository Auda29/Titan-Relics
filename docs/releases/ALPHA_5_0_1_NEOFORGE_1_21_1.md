# Relic Mod Alpha 5.0.1 for NeoForge 1.21.1

First native NeoForge release of Alpha 5 gameplay for Minecraft 1.21.1. Includes
the approved interiors, shared persistent distribution/map targets, defense
encounters, personal physical rewards, immediate key payment, finite cores,
per-item held-magnet wear, archaeology and the 80-block level-II Tree aura.

Install `relics-0.1.0-alpha.5.0.1+mc1.21.1-neoforge.jar` with Minecraft 1.21.1,
Java 21+, NeoForge 21.1.256+ and Lithostitched 1.8.0 for NeoForge 1.21/1.21.1.
Dependencies are separate; Fabric API is not required. Use one matching Relic JAR.

The port uses native registration events, persistent attachments and server
events. Animal extras respect native spawn cancellation and population caps.
Its player artifact contains no Fabric API or validation classes. The 1.21.1
resource adaptations use ferns, framed ordinary chests, integer charge icons,
native recipe-book data and the game's older armor-trim atlas.

Use a new native world for all Alpha 5 features. Cross-loader save conversion
and downgrading a 26.2 save are not provided. Native server and asset tests do
not claim new graphical-client, shader/LOD or arbitrary modpack acceptance.

[Build, native implementation and reproduction](../../compat/alpha5-neoforge-1.21.1/README.md).
[Final verification](../testing/ALPHA_5_0_1_1_21_1_20261028.md).
