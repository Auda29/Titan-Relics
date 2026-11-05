# Installation and support

Prepared 5 November 2026. The published baseline is Alpha 5.0.5. Candidate-only
behavior is marked explicitly below. Public beta downloads are not available yet.

## Pick the right files

Download one player JAR from the
[Alpha 5.0.5 release](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.5.0.5).
Match both the Minecraft version and loader; Fabric and NeoForge JARs are separate.
Use the release's `SHA256SUMS.txt` if you need to verify a download.
The repository is currently private. Its release and issue links require access;
public alternatives will be announced with the beta, not guessed here.

These are the repository's pinned/tested dependency versions, not a claim that
every newer version works. Dependencies are not bundled.

| Game | Loader baseline | Java | Required dependencies |
|---|---|---|---|
| 1.21.1 | Fabric Loader 0.19.5 | 21+ | Fabric API 0.116.17+1.21.1; Lithostitched 1.8.0 Fabric 1.21/1.21.1 |
| 26.2 | Fabric Loader 0.19.5 | 25+ | Fabric API 0.161.0+26.2; Lithostitched 1.8.0 Fabric 26.2 |
| 1.21.1 | NeoForge 21.1.256 | 21+ | Lithostitched 1.8.0 NeoForge 1.21/1.21.1 |
| 26.2 | NeoForge 26.2.0.88 | 25+ | Lithostitched 1.8.0 NeoForge 26.2 |

Dependency projects: [Fabric API](https://modrinth.com/mod/fabric-api),
[Lithostitched](https://modrinth.com/mod/lithostitched). Select their matching
game/loader files. Fabric API is only required on Fabric. Mod Menu is optional
on Fabric; biome, terrain, shader and LOD mods are optional.

1. Install the selected game version and loader in your launcher.
2. Exit Minecraft. Put the matching Titan Relics JAR and dependencies into that
   profile's `mods/` directory. Remove the previous Titan Relics JAR when updating.
3. For multiplayer, install the matching mod/dependencies on the server and
   each client. Client rendering add-ons do not automatically belong on a server.
4. Start Minecraft and check that the loader recognizes the mod. Create a new
   Overworld with structure generation enabled for the complete current selection.
5. Set your preset under **Create World → World → Relic generation**, then create
   the world. Continue with the [player guide](PLAYER_GUIDE.md).

Use player JARs, never development checks, validation mods or sources archives.
There is no universal JAR for both loaders or both game versions.

## Updating and existing worlds

Back up the world and its mod/configuration setup before changing them. Update
within the same supported game/loader target. Downgrading a 26.2 save to 1.21.1
and cross-loader save conversion are not supported migration paths.

Existing worlds retain their saved relic selection, distribution settings and
unique Colossus destination/search progress, including in unexplored chunks.
New defaults do not rewrite them. Old relics and finite shared containers or
archaeology are not moved, refilled or regenerated for later players.

Changing biome mods, datapacks or mod lists can change the environment recorded
by a frozen relic plan. In the unpublished candidate, recognized incompatible
setups produce an explained refusal to load and return the client to the menu.
This guard is not an automatic migration and is not promised for Alpha 5.0.5.
Restore the original supported setup when a world is rejected. Do not delete
the saved plan or force fresh sites as a troubleshooting shortcut.

## Known limits

- The unpublished candidate's [compatibility notes](../technical/MOD_COMPATIBILITY.md)
  list exact tested modpacks and versions. They do not certify every dependency
  update, seed, shader, pack configuration or NeoForge variant of a Fabric pack.
- DH 3.3.3 `FEATURES` can omit relic starts in distant generation.
  `INTERNAL_SERVER` passed for new distant generation. Changing modes has not
  been established as a repair for old incomplete LOD caches.
- Voxy World Gen V2 2.4.3 requires client LWJGL in the tested setup and fails on
  a dedicated server even without Relic. Keep that add-on out of that server setup.
- Relic raises measured process memory. High-radius Voxy generation and long-term
  FPS/memory behavior remain unverified; there is no general performance guarantee.
- 1.21.1 uses ferns and ordinary reward chests where 26.2 blocks are unavailable.
- Natural travel effort and the everyday value/cost of rewards await the user's
  full Survival playthrough. No maximum travel distance is promised.

## Reporting a problem

Use the [bug report form](https://github.com/Auda29/Relic-Mod/issues/new?template=bug_report.yml).
Supply the complete Relic filename/version, Minecraft version, loader/version,
Java version, operating system and relevant mod versions. Explain what you did,
what you expected, what happened and whether it repeats after a restart.

Attach `logs/latest.log` from immediately after the failure. For a crash, also
attach the relevant `crash-reports/crash-*.txt` if one exists. For multiplayer,
include server logs and the affected client log. A screenshot alone usually
cannot explain a crash or world-load rejection.

For generation/map problems include the seed, dimension, coordinates, preset,
biome settings and whether the world predates the update. Say whether the area
was normally generated or prepared by DH/Voxy. For performance reports include
heap allocation, view/simulation distances, LOD generator settings and the action
being measured. Only claim a minimal-setup reproduction if you actually tested it.

Review attachments before posting publicly. Remove access tokens, server
addresses you want to keep private, chat and identifying local paths as needed,
while retaining the error message and stack trace. Never upload account files.
If the issue tracker already contains the same failure on the same version,
add your evidence there.
