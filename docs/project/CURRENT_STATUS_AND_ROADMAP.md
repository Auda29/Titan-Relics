# Current status and roadmap

Updated: November 5, 2026. This is the current implementation and work-status
index. Dated concept studies, builder handoffs and test reports retain their
historical scope. Their old "not implemented" or "pending integration" wording
does not create new work when a later release has completed it. Approved design
rules remain specifications unless superseded by a later recorded decision.

## Released baseline

The release line is [Alpha 5.0.5](../releases/0.1.0-alpha.5.0.5.md)
for Fabric and NeoForge on Minecraft **26.2 and 1.21.1**. The tag workflow builds,
checks and publishes all four targets. Java 25
is required for 26.2; Java 21 for 1.21.1. Use the matching loader dependencies
listed in the [installation instructions](../../README.md).

| Area | Implemented state |
|---|---|
| Distribution | Shared family budget, terrain validation and local search; one saved large Colossus per supported enabled world; common expedition-map destination |
| Large Colossus | V7 landmarks, five-operator cockpit, hatch, arm chest stand, central guard structure and Vault console; one attacking defense golem, participant keys, immediate Vault key payment and personal physical core rewards |
| Small Colossus | V11 shorter lower entrance and framed chest at the upper end of the second staircase; finite salvage and a 10% per-site chance for one broken magnet |
| Obelisk | V6 archaeology, finite shared finds, Monolith trim template and expedition map |
| Ruined Tower | V10 framed chest centered on the wall opposite the entrance; incomplete player-built ascent, five one-time ordinary Endermen and finite Ender reward |
| Titan remains | Both skull designs retain natural mobs and no reward chests; the isolated Skull-2 side chip is removed |
| World Tree | V5 root lighting and decorative amethyst; grounded luminous plants; Regeneration II and Resistance II in an 80-block sphere, five-minute departure tail and persistent natural-site anchor; bounded extra natural animal attempts |
| Items | Core capacity 256 completed operations; magnet budget 1,000 actual items, either selected hand, inventory-only inactive; charge/repair recipes and recipe-book presentation |
| Interiors and saves | Fresh worlds select `interiors-20261028-v5`; old supported revisions remain frozen. Structures and finite loot are not moved or replenished |
| Recipe synchronization | Alpha 5.0.2 fixed the maintenance-recipe packet codec on all four targets |
| World reopen | Alpha 5.0.3 sorts JSON object keys before hashing. Legacy fingerprint migration backs up the old journal; unmatched legacy hashes need a reviewed exact-transition approval |
| Release automation | A shared version tag builds, tests and publishes four JARs plus SHA256SUMS; downloads are verified before the draft becomes a published release |

The numerical item/effect/loot values are current starting values, with Survival
balance still open. The 1.21.1 ports use ferns and ordinary chests where 26.2
blocks are unavailable; the approved roles, loot and protected access remain.

## Evidence and player acceptance

- [Distribution correction](../testing/DISTRIBUTION_FIX_20261027.md): 30 fixed
  native-server runs, reverse-order planning and distance checks. The corrected
  sample contains 351 accepted repeatable opportunities; nine materialized sites
  cover all repeatable families and the crowned-skull palettes. This is not a
  complete in-game census of every site or a Survival travel-time measurement.
- [Alpha 5 gameplay release](../testing/ALPHA_5_RELEASE_20261028.md): natural
  placement, interior/loot initialization, saved revisions, native encounters,
  magnet accounting, Tree aura and animal-cap checks. The user confirmed two real
  clients including reconnect; automated simulated-player tests are separate.
- [Published 5.0.3 verification](../testing/alpha5-0-3-release-20261028-evidence.json):
  four downloaded player JARs and checksums, six frozen manifests and 40 templates
  per target. CI passed 172 Python tests, Java checks and native server/restart
  scenarios. Port text resources differ between Windows and Linux only in line
  endings; code and binary contents match the locally tested artifacts.
- [World-reload investigation and recovery](../testing/ALPHA_5_0_3_WORLD_RELOAD_20261028.md):
  the full Living World modpack loaded, saved and reopened in an isolated copy.
- **October 30 user confirmation:** after being asked to open the world, return
  to the menu and reopen it, then fully restart Minecraft and load it again, the
  user reported that everything worked. This confirms the targeted Living World
  reopen test. A broader exploration playtest is now in progress; its results
  are not yet recorded. A read-only profile check found 5.0.3 installed and a
  valid format-1 planning journal in the original Living World save.

## Alpha 5.0.4: distribution settings

The user approved presets and editable values after a 6,000-block exploration
route without a relic find. Alpha 5.0.4 added Expedition, Balanced and Discoveries
presets, block distances, per-family percentages and biome selection directly
inside the World tab of world creation. Mod-list configuration edits future-world
defaults; loaded local worlds expose a read-only viewer with rejection diagnostics.
It covers Fabric and NeoForge on both supported Minecraft versions. Settings
are frozen per new world; existing worlds retain their plans. Alpha 5.0.4 was
published on November 1, 2026. See the [release notes](../releases/0.1.0-alpha.5.0.4.md),
[usage and limits](../technical/DISTRIBUTION_SETTINGS.md)
and [current validation report](../testing/DISTRIBUTION_WORLD_MENU_20261101.md).

## Alpha 5.0.5: Colossus distance follows the preset

The new-world editor includes a separate Colossus minimum distance from the
original world spawn: Expedition 30,000, Balanced 15,000, Discoveries 8,000 blocks.
Custom values are supported. Existing worlds and older configurations without
the field retain their previous 30,000-block rule and saved destination/search
progress. Suitable terrain can still require a much more distant site.

All four local builds, an actual Fabric 1.21.1 world-creation client, and isolated
Fabric 26.2 natural generation/map/locate/restart tests passed. See the
[release notes](../releases/0.1.0-alpha.5.0.5.md) and
[validation report](../testing/COLOSSUS_PRESET_DISTANCE_20261103.md).

## Public beta roadmap

The [approved public-beta roadmap](PUBLIC_BETA_ROADMAP.md) now has four completed
gates and two remaining gates. These results concern an unpublished local
candidate based on 5.0.5, not newly published player JARs.

| Gate | Current state and evidence |
|---|---|
| 1. Understandable world-load rejection | Complete. Early checks explain incompatible saved environments, preserve world data and return clients to the menu. Four-target rejection/restoration evidence and Living World cases are in the [guard report](../testing/BETA_WORLD_LOAD_GUARD_20261104.md). |
| 2. Distribution controls | Complete under the user's revised scope. Existing presets, custom values and biome selection suffice. Discoveries is the factory default for new worlds without an existing choice; saved choices and plans remain unchanged. |
| 3. Survival playthrough | Open. The user is testing the complete natural exploration, archaeology, map, encounter and reward chain and its everyday balance. |
| 4. Actual client acceptance | Complete on Fabric/NeoForge for 1.21.1/26.2. Real multiplayer, crafting, personal rewards, late participation, restart persistence and 96 reviewed model/armor images are documented in the [gameplay](../testing/BETA_CLIENT_GAMEPLAY_ACCEPTANCE_20261104.md) and [final renderer](../testing/BETA_RENDERER_ACCEPTANCE_20261104.md) reports. |
| 5. Compatibility and performance | Complete within documented support conditions. Sixteen server runs, eight modpack client runs and a separate DH LOD view are in the [compatibility report](../testing/BETA_COMPATIBILITY_20261104.md). |
| 6. Publication and feedback | Prepared locally: player guide, installation/support, README, issue form, Modrinth/CurseForge page and file-metadata drafts, release template and name proposals. The user selected Titan Relics with the tagline Colossal ruins of a forgotten age. MIT is selected and permits modpack use under its notice conditions. The user supplied Modrinth and CurseForge preview links using titan-relics, but anonymous checks cannot yet verify either project. Platform settings/eligibility, final art, release approval and published-asset verification remain open. See the [publication package](../releases/PUBLIC_BETA_PREPARATION.md). |

The user renamed the repository to [Auda29/Titan-Relics](https://github.com/Auda29/Titan-Relics)
and made it public. Anonymous checks confirm public repository metadata, the
Alpha 5.0.5 release with four JARs and checksums, and the player guide. The issue
tracker is enabled and public; filing an issue requires a GitHub account. Current
links and the local remote now use the new URL. Registry/save IDs and existing
artifacts remain unchanged. This visibility change does not release the beta.
Modrinth's current AI-content rules still require a separate provenance/eligibility
assessment; acceptance by either platform is not claimed.

The compatibility tests cover paired generation routes, terrain and biome mods,
foreign structures, shader/LOD variants and seasons in isolated copies of
TerraVista and TerraVista Living World. Original profiles remained unchanged.
Relic raises measured process memory substantially. DH 3.3.3 FEATURES omits the
planned Relic start; INTERNAL_SERVER and rendering its prepared chunk data passed.
No production fix for FEATURES or old LOD-cache repair was implemented.
Voxy World Gen V2 was excluded from dedicated-server references because its
client LWJGL dependency fails there even without Relic. Actual clients retained it.
See the [player-facing support boundaries](../technical/MOD_COMPATIBILITY.md).

Historical partial reports retain their original failures and limits. Later
linked results close their specific pending cases. New content is not a Beta-1
prerequisite, and completing these tests does not itself authorize publication.

## Open work on the existing game

These are remaining validation/tuning tasks, not unimplemented core mechanics.

1. **Survival economy:** assess the core's daily usefulness and recharge cost,
   magnet lifetime/repair, small-site magnet availability, Tower loot and the
   value of mining the large Colossus. Tune from observed play; do not silently
   change approved acquisition/sharing rules.
2. **Discovery effort:** record natural finds, terrain rejections, travel time
   with/without maps and the aggregate rarity hierarchy in actual modpacks.
   Retain the completed 30-seed audit as evidence rather than listing it as undone.
3. **Beyond the completed compatibility sample:** long-term FPS/memory behavior,
   other pack versions, original high-radius Voxy generation and repair of old DH
   caches remain unverified. The bounded measurements above satisfy roadmap
   point 5 within their documented support conditions.
4. **Further runtime edge cases:** extend evidence for automation, late arrivals,
   map copies, abandoned trials and controlled hard interruptions across save
   boundaries. Many individual cases already have automated coverage; normal
   restarts do not establish universal atomic saves under arbitrary process kills.
5. **Visual/ecological balance in natural terrain:** assess real root lighting,
   animal abundance, distant readability and access under modded terrain. The
   Tree effects and natural-spawn hook are already implemented.

The [acceptance matrix](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md) is a case catalog;
its October 8 "not yet run" statements are historical. Match individual cases
to dated results before treating them as missing tests. The current broad
playtest does not reopen accepted models or require a new feature-design round.

## Later engineering options

- Precise geometry collision handling against unrelated structures remains a
  limitation; relic-to-relic separation is already implemented.
- Controlled planning-epoch/configuration migration is outside the first gameplay
  implementation. The 5.0.3 hash-format migration does not enable arbitrary
  generator, density, biome or asset changes in a frozen world.
- Legacy density datapacks and development diagnostics exist. The new-world
  settings menu shipped in Alpha 5.0.4; migration of an
  existing world's density remains outside its scope.
- Retroactive structure insertion and automatic conversion of old placed copies
  are outside the current scope.

## Optional content ideas

These proposals require a separate selection before implementation; none is a
committed Alpha-5.x feature. Preserve the accepted existing models.

| Idea | Recorded direction |
|---|---|
| Independent machine fragments | A separately generated hand or other fragment, possibly with later shelter/reuse; its own site selection and exploration composition |
| The Enclosed Ancient One | A huge ambiguous figure in greenish crystalline material between dark cliffs; transparency/glow need their own prototype |
| The Split Monument | A downward-tapering broken monument with a visible gap between fragments; geometry/material treatment still need design |
| More Titan remains and controlled variants | Further bone/skull sites, damage/pose/root/crown variants; retain the shared family budget rather than multiplying rates |
| Environmental storytelling | Restrained related damage, machine fragments in bone, later expedition marks or small-scale reuse; optional viewpoint-based texts, not definitive explanations |
| Atmosphere/material options | Subtle sounds, sparse lights, optional Biomes O' Plenty palettes and further large-structure generation experiments |

Sources: [lore catalog](LORE-BIBLE.md#7-optional-later-structures),
[visible-history review](LORE_GAMEPLAY_REVIEW.md#3-make-the-shared-past-visible-in-discoveries)
and [concept catalog](Minecraft-Relikte-Modplan.md). The builders' identity,
Titan nature, campaign motive and exact chronology may deliberately remain
unknown. Living Titans, revival quests, controllable mechs, custom bosses and
new dimensions are not selected additions. Skull/Tree reward chests are not planned.

## Publication decisions and next order

GitHub prereleases and their CI are delivered. The user selected the MIT License
for the project, including modpack use and redistribution under its notice
conditions. The license is recorded in `LICENSE` and current Fabric/NeoForge
metadata; new builds include the license and credits. Third-party reference works
retain their own rights. Existing Alpha release files are not replaced. Final
platform publication and approval remain pending.

Follow the [public-beta roadmap](PUBLIC_BETA_ROADMAP.md): finish the user's
Survival acceptance and publication preparation next. Gates 1, 2, 4 and 5 have
the evidence linked above. A public Beta 1 still requires explicit approval
and verification of the actual release artifacts. Content experiments remain separate
later decisions; independent machine fragments are the most direct recorded
design experiment.
