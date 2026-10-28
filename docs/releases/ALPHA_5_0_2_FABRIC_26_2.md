# Relic Mod Alpha 5.0.2 for Fabric 26.2

Completes the Alpha 5.0.2 release family with the primary Fabric 26.2 build.
Maintenance recipes now serialize their variant rather than requiring Java
object identity, matching the corrected 1.21.1 and NeoForge releases.

Install `relics-0.1.0-alpha.5.0.2+mc26.2.jar` with Minecraft 26.2, Java 25+,
Fabric Loader 0.19.5+, Fabric API 0.161.0+26.2 and Lithostitched 1.8.0 for
Fabric 26.2. Install dependencies separately and use one matching Relic JAR.

Updating from Fabric 26.2 Alpha 5.0 preserves existing worlds and items. All
40 templates, selection manifests and other resource files are unchanged.
No new world is required for this patch. Restart client and server after
replacing the previous Relic JAR.

Native tests encode/decode recipe, holder, update and recipe-book packets and
check crafting, core processing, personal rewards, magnet wear, Tree effects
and natural animal caps before/after restart. Client/modpack acceptance remains
separate. No TerraVista profile or player save is modified by this release work.

[Verification and reproduction](../testing/ALPHA_5_0_2_FABRIC_26_2_20261028.md).
