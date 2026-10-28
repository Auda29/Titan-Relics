# Relic Mod Alpha 5.0.2 for NeoForge 26.2

Corrects the maintenance recipe codec to serialize its variant rather than
Java object identity, matching the fixed 1.21.1 ports.

Install `relics-0.1.0-alpha.5.0.2+mc26.2-neoforge.jar` with Minecraft 26.2.
Requires Java 25+, NeoForge 26.2.0.88+, Lithostitched 1.8.0 for NeoForge 26.2.
Install dependencies separately and use one matching Relic JAR.

Updating from Alpha 5.0.1 on the same game version and loader retains existing
worlds and items. Recipe ingredients, crafting behavior, charge budgets and all
structure/resource files remain unchanged. Restart client and server after
replacing the previous JAR.

Tests encode and decode the complete native recipe synchronization packet,
check distinct recipe instances and verify decoded crafting behavior. Native
functional/restart checks pass. Graphical-client and full modpack acceptance
are separate; no TerraVista profile or save was changed.

[Build/install profile](../../compat/alpha5-neoforge-26.2/README.md).
[Recipe fix verification](../testing/ALPHA_5_0_2_RECIPE_CODEC_20261028.md).
