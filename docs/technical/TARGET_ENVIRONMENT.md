# Alpha target environment

Inventory recorded: September 13, 2026. Documentation updated: October 1, 2026.
This record supports the [implementation plan](../project/UMSETZUNGSPLAN.md). The initial
inventory was read-only and describes the state before installation. Later
installation and upgrade steps are recorded separately below. Local paths are
historical machine-specific evidence, not required paths for other contributors.

## Confirmed test profile at inventory time

The user selected Modrinth profile `E:\Roaming\ModrinthApp\profiles\Relic Test`.
Launcher metadata confirmed:

| Property | Evidence |
| --- | --- |
| Minecraft | `26.2` |
| Loader | Fabric `0.19.5` |
| Launcher installation status | `installed` |
| Profile directory | Present |
| Installed mods | No JARs in `mods/` |
| Configuration and datapacks | Existing directories empty |
| Saves and logs | No save files or `logs/latest.log` |
| Graphics profile and JVM memory limit | Not yet verified from a run of this profile |

The only file was an empty `command_history.txt`. This established an empty
starting point, not a successful game launch. Fabric API, Lithostitched, Terralith,
Tectonic, Biomes O' Plenty, and Dungeons & Taverns were not yet installed there.

Versions were read through a SQLite connection using `mode=ro` to the launcher
database. Only the selected profile name, game version, loader, and loader version
were reported. The database and account information are not part of the repository.

## Java and Minecraft formats

Local runtime/compiler executables were checked with `-version`:

| Purpose | Local path | Result |
| --- | --- | --- |
| Available build JDK | `C:\Users\wecke\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe` | Temurin `25.0.4.1+1-LTS` |
| Java compiler | `C:\Users\wecke\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\javac.exe` | `javac 25.0.4.1` |
| Available Modrinth runtime | `E:\Roaming\ModrinthApp\meta\java_versions\zulu25.36.205-ca-jre25.0.4.1-win_x64\bin\java.exe` | Zulu `25.0.4.1+1-LTS` |

Availability did not establish which runtime the Relic Test client actually used.
The data-only mod build itself needs Python, not Java compilation; Java 25 is a
game/server requirement.

`version.json` and launcher metadata from the local client JAR
`meta/versions/26.2-0.19.5/26.2-0.19.5.jar` reported:

| Field | Value |
| --- | --- |
| Game ID | `26.2` |
| Required Java major version | `25` |
| NBT DataVersion / `world_version` | `4903` |
| Datapack format | Major `107`, minor `1` |
| Resource-pack format | Major `88`, minor `0` |
| Fabric entry point | `net.fabricmc.loader.impl.launch.knot.KnotClient` |

SHA-256 of inspected cache artifacts:

| File | SHA-256 |
| --- | --- |
| `meta/versions/26.2-0.19.5/26.2-0.19.5.jar` | `40896ee9f1e2bec3c934daac7e93d41e9e3d9c2f8ae0ca366d52ffbfd1afa290` |
| `meta/libraries/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar` | `93044e4dd46de5d8136701292f05e868da096d2c9fddb4793e4fdbcc63efc695` |

These paths are relative to `E:\Roaming\ModrinthApp`. Third-party JARs are not
tracked in Git.

## Worldgen integration dependencies

Compatible libraries and worldgen mods were available in
`E:\Roaming\ModrinthApp\profiles\TerraVista\mods`. The following selection was
used for separate integration-server tests. It is not a description of all mods
installed in Relic Test or evidence for the full TerraVista pack.

Versions/dependencies were read from each local JAR's `fabric.mod.json`. Hashes
identify those exact files.

| File | Mod ID / version | SHA-256 |
| --- | --- | --- |
| `fabric-api-0.160.0+26.2.jar` | `fabric-api` / `0.160.0+26.2` | `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e` |
| `lithostitched-1.8.0+beta6-fabric-26.2.jar` | `lithostitched` / `1.8.0+beta6` | `5743a7e11af1491aab6f4760c7cdce7284e2f0a4a89ffacd4ef43fd46e5e6d43` |
| `tectonic-3.0.26-fabric-26.2.jar` | `tectonic` / `3.0.26` | `4fa2b27fdccb60da9942af70b2d157feea4609049ad80950ec4c33db36502168` |
| `Terralith_26.2_v2.6.4.jar` | `terralith` / `2.6.4` | `d867c6f348e869c19e8a5979e9dd2c46ed058c1edb47090f6863c32cce484917` |
| `BiomesOPlenty-fabric-26.2-26.2.0.0.28.jar` | `biomesoplenty` / `26.2.0.0.28` | `e3a5571eb77225e800f8fc4334d452904705e945c26767bfb091f42889ae14b4` |
| `dungeons-and-taverns-5.3.2.jar` | `mr_dungeons_andtaverns` / `5.3.2` | `7a1abeacfd6b973d9753928889d765e4002a086f4cb23756d8586e7d347d4bba` |
| `GlitchCore-fabric-26.2-26.2.0.0.0.jar` | `glitchcore` / `26.2.0.0.0` | `f6c31bd291d1d19322dd0a7ec344df2c88e2d516d1985f09ffe50ef33a34afdc` |
| `TerraBlender-fabric-26.2-26.2.0.0.2.jar` | `terrablender` / `26.2.0.0.2` | `e4c54e7490cf6716ccc287f5ef674562666a13c6a4afabdc344d5cb62e9cb584` |

### Declared dependencies

- Fabric API requires Java `>=25`, Fabric Loader `>=0.18.4`, and Minecraft `~26.2-`.
- Lithostitched requires Fabric Loader `>=0.17` and Minecraft `~26.2`. It bundles
  Apollib `1.1.4`, which requires Fabric Loader `>=0.19` and bundles `json5-java`.
- Tectonic requires Lithostitched and also bundles Apollib `1.1.4`.
- Terralith requires Fabric Loader `>=0.19` and Lithostitched `>=1.7.12`.
- Biomes O' Plenty requires Fabric API, GlitchCore `>=26.2.0.0.0`, and TerraBlender `>=26.2.0.0.1`.
- GlitchCore and TerraBlender require Fabric API; their other libraries are bundled.
- Dungeons & Taverns requires `fabric-resource-loader-v0`, included in the selected Fabric API JAR.

These eight external JARs cover the declared dependencies. Fabric Loader 0.19.5
and Java 25 satisfy the minimum versions. Actual loader acceptance is documented
in the server reports rather than inferred solely from metadata.

TerraVista also contains nine separate Dungeons & Taverns vanilla-structure
overhauls. They were excluded, as were personal Biomes O' Plenty, Lithostitched,
Tectonic, TerraBlender, and Terralith configurations. Integration runs used default
settings and do not establish full-pack compatibility.

## Runtime evidence

The [Alpha 1](../testing/ALPHA_TEST_REPORT.md) and [Alpha 2](../testing/ALPHA_2_TEST_REPORT.md) reports
record startup, natural placements, and saved-block comparisons. Broader client
connection/visual acceptance, shader and LOD compatibility, multi-seed exploration,
and performance measurements remain separate requirements. File inventory alone
does not establish them.

## Initial alpha installation

On September 13, 2026, after the isolated base test passed, exactly three JARs were
copied to the previously empty `Relic Test/mods`:

- `relics-0.1.0-alpha.1+mc26.2.jar`, SHA-256 `1918fc1784952060adfd0919084383944dfb97ca60bca45d5f14069c7516583e`
- `fabric-api-0.160.0+26.2.jar`, hash listed above
- `lithostitched-1.8.0+beta6-fabric-26.2.jar`, hash listed above

Installed hashes matched the tested source files. Dependencies came from the
existing cache profile; TerraVista was not changed. No saves were created or
modified and no extra worldgen mods were installed in Relic Test. At that point
the profile had not been launched as a client. Separate completed server checks
are in the Alpha 1 report.

## Alpha 2 upgrade

After the user's Alpha 1 game screenshots, the Relic JAR was replaced on September
13, 2026 with `relics-0.1.0-alpha.2+mc26.2.jar`, SHA-256
`cc978cdb382ec5f7ad82cfcaddb1dbdc30d27fd3e3e56949729911e347c27dfa`.
The previous file was backed up under `build/profile-backups/alpha2-upgrade/`.
Only the new Relic version remained in `mods/`; both required dependencies kept
their previous hashes.

No Minecraft client was running during replacement. Saves were not changed.
New shapes appear only through new generation. Alpha 2 verification used separate
local test worlds.

## Blender asset toolchain

The October 2026 asset work used Blender **5.2.2**, Node **24.16.0**, and local
ObjToSchematic 1.0 at commit `b611b52c7a87cad99127908598bab019fe9e7c3f`.
These are development tools, not player dependencies. See
[Blender workflow](BLENDER_WORKFLOW.md) for setup and the legacy DataVersion 3105
conversion limitation. At that point, the new assets had not replaced the installed alpha models.

## Alpha 3 visual-test upgrade — October 1, 2026

The Relic Test profile now contains `relics-0.1.0-alpha.3+mc26.2.jar`, SHA-256
`530be00274f815d9f7fe93dab6dde3570988b1b1f0c1d21f007d2a0b5042671c`.
The old Relic JAR was backed up under
`build/profile-backups/alpha3-upgrade-20261001-205738/`. Other mods and existing
saves were not changed. The new creative save **Relic V3 Showcase
20261001-205738** contains all three models, already placed at matching ground
levels, with cheats enabled for inspection.

This is a visual-test installation, not full natural-worldgen acceptance.
The showcase has zero saved-block differences; natural generation still has
minor neighboring-chunk feature edits. See the
[Alpha 3 report](../testing/ALPHA_3_TEST_REPORT.md) for exact results and limits.
