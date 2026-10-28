# Relic Mod Alpha 5.0.2 for Fabric 1.21.1

Fixes the recipe synchronization disconnect when joining a world. Maintenance
recipes now serialize by variant rather than Java object identity.

Install `relics-0.1.0-alpha.5.0.2+mc1.21.1.jar` with Minecraft 1.21.1.
Requires Java 21+, Fabric Loader 0.19.5+, Fabric API 0.116.17+1.21.1, Lithostitched 1.8.0 for Fabric 1.21.1.
Install dependencies separately and use one matching Relic JAR.

Updating from Alpha 5.0.1 on the same game version and loader retains existing
worlds and items. Recipe ingredients, crafting behavior, charge budgets and all
structure/resource files remain unchanged. Restart client and server after
replacing the previous JAR.

Tests encode and decode the complete native recipe synchronization packet,
check distinct recipe instances and verify decoded crafting behavior. Native
functional/restart checks pass. Graphical-client and full modpack acceptance
are separate; no TerraVista profile or save was changed.

[Build/install profile](../../compat/alpha5-fabric-1.21.1/README.md).
[Recipe fix verification](../testing/ALPHA_5_0_2_RECIPE_CODEC_20261028.md).
