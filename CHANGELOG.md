# Changelog

## Documentation update (2026-10-30)

- Add a current status/evidence/roadmap index; separate delivered Alpha 5 systems,
  open validation/tuning, later engineering and optional content concepts.
- Record the user-confirmed Living World reopen test and ongoing exploration
  playtest without claiming complete modpack or performance acceptance.
- Correct README limits and mark superseded visual-alpha/planning status as history.

## 0.1.0-alpha.5.0.3 (2026-10-28)

- Release stable canonical planning fingerprints and checked legacy migration with
  an original-journal backup for Fabric/NeoForge on 26.2 and 1.21.1.
- Add shared-tag release CI; publish and independently verify four player JARs
  plus checksums. Preserve frozen site identities, interiors and finite rewards.
- See [release verification](docs/testing/alpha5-0-3-release-20261028-evidence.json)
  and [world-reload report](docs/testing/ALPHA_5_0_3_WORLD_RELOAD_20261028.md).

## 0.1.0-alpha.5.0.2 ? recipe network codec fix (2026-10-28)

- Fix the maintenance recipe codec for Fabric 26.2, Fabric 1.21.1, NeoForge
  1.21.1 and NeoForge 26.2. Serialize the recipe variant without requiring object identity.
- Reproduce the reported join-time recipe error with the published Fabric 5.0.1
  JAR; add actual recipe/holder and full synchronization packet round-trip checks.
- Verify decoded crafting/component preservation and reject opposite variants.
  NeoForge 26.2 also round-trips the native recipe-book display packet.
- Add the full native Fabric 26.2 packet/gameplay/restart suite to CI; retain
  the exact already published 1.21.1 and NeoForge patch artifacts.
- Retain all structure/resource bytes, charge rules and existing same-target saves.
  Profiles and full modpack compatibility remain outside this patch's runtime scope.

## 0.1.0-alpha.5.0.1 ? Fabric 1.21.1 and native NeoForge ports (2026-10-28)

- Release Alpha 5 gameplay for Fabric 1.21.1, NeoForge 1.21.1 and NeoForge 26.2.
- Preserve all frozen interior revisions, shared map targets, physical personal
  rewards, immediate key payment, per-item held-magnet wear and 80-block Tree aura.
- Adapt 1.21.1 block/model/trim resources and recipe-book data; remove unavailable
  copper trim palette references. Retain native 26.2 assets in the NeoForge port.
- Use native NeoForge registration, persistent attachments and events, including
  cancellation-aware animal extras and client notification for protected breaks.
- Verify final packages with isolated functional/restart and natural-world tests,
  actual client asset checks, reproducible builds and separate staged Git exports.
- Retain the original Fabric 26.2 Alpha 5.0 artifact. New port server tests use
  simulated players; real-client acceptance remains specific to the original build.

## 0.1.0-alpha.5.0 — natural gameplay and approved interiors (2026-10-28)

- Add bounded extra natural animal attempts near saved Tree anchors for pigs,
  chickens, sheep and cows, with native habitat, distance, collision and population
  checks. No timer, forced refill or breeding bonus.
- Grant Regeneration II and Resistance II in the 80-block Tree aura, preserving
  the five-minute tail and normal merging with stronger or longer effects.
- Remove only the isolated 147-block Dripstone chip beside Titan Skull 2;
  retain skull anatomy, sword, roots, other fragments and old world selections.
- Ground World Tree firefly-bush/soil pairs on a safe surface in the same column,
  within six blocks vertically; omit unsafe sites without leaving soil pillars.
- Expand the saved Tree aura to an 80-block sphere, including spatial-bucket
  lookup across three cells, while keeping Regeneration I and the five-minute tail.
- Shorten the Small Colossus lower entrance by six blocks (V11) and frame the
  Tower chest at the middle rear wall opposite the entrance (V10). New worlds
  use V4; V1/V2/V3 world templates and fingerprints remain frozen.
- Rework Monolith trim on baked Minecraft 26.2 armor UVs: separate narrow angular
  details, clear helmet/arm/boot openings and native material palette colors.
- Record provisional acceptance of Large Colossus V7 and Obelisk V6. Small
  Colossus V11, Tower V10 and revised trim await visual in-game acceptance.
- Count magnet wear per item actually inserted, including partial pickups and
  exhaustion; keep ordinary pickup available and label the remaining item budget.
- Move the Small Colossus V10 chest into a framed stand at the top of the second
  stair. Keep the V3 selection for worlds created with that build.
- Skip native tower hostile-spawn actions that Minecraft disallows on Peaceful,
  preventing a repeated world-load crash without refilling completed actions.
- Add Colossus V7 arm-chest framing, a central Trial Spawner guard structure and
  a Vault console at the middle crew station. Reserve chest-lid/access air and
  remove native terrain ores within the bounded V7 clearance regions.
- Freeze the new interior revision for fresh worlds while retaining V6 templates,
  marker coordinates and fingerprints for existing saves. V7 is provisionally accepted; see [October 28 checks](docs/testing/COLOSSUS_LANDMARKS_20261028.md).
- Integrate approved Colossus V6, Small Colossus V9, Tower V9, Obelisk V6 and
  retained World Tree V5 into new gameplay worlds, with bounded clearances,
  marker initialization and saved completion state. Preserve legacy selections.
- Use native Trial Spawner/Vault phases and real personal reward drops, with
  owner/hopper protection and persisted pickup receipts. Consume the Vault key
  immediately on successful use; collect the separately ejected core later.
- Enable the charged magnet in either selected hand, leave other inventory
  slots inactive and increase attraction acceleration/speed by ten percent.
- Add maintenance recipe-book displays/unlocks. Extend asynchronous relic
  locating to 500,000 blocks without changing rarity or generation decisions.
- Record model approval, isolated natural-generation checks, two-player server
  reward/restart checks and the final build checksum in the
  [October 27 development status](docs/project/ALPHA_5_STATUS_20261027.md).
  Final graphical-client, complete Survival and real multiplayer acceptance
  remain open; the planned Tree animal-spawn adjustment is not implemented.

- Implement fresh-world shared distribution, terrain-valid Obelisk regions,
  deterministic spacing and one persisted natural large-Colossus destination.
- Gate candidate structure-start jobs asynchronously; preserve old worlds and
  accepted templates. Resume interrupted searches from an atomic planning journal.
- Connect expedition-map origins, copied maps and asynchronous relic `/locate`
  to the same saved destination. Add operator status, plan and map commands.
- Add production planner tests, isolated native-loader/save/reload/map checks and
  [dated distribution evidence](docs/testing/DISTRIBUTION_IMPLEMENTATION_20261025.md).
- Register Machine Core, Salvage Magnet, Colossus Key and Monolith template with
  original item sprites, bounded/versioned charge components, exact tooltips and
  three core/magnet icon states; no inventory status bar.
- Implement guarded appliance processing, held-item attraction/accounting,
  state-preserving recharge/repair and vanilla-style cosmetic trim/copy resources.
- Add scoped one-golem trial/AI, unlimited durable Vault claims, pending/resolved/
  compensated expedition-map origins and persistent spherical Tree-aura adapters.
- Reserve deliveries in a checksum-verified atomic journal, with player receipts
  and visible fail-closed handling of ambiguous recovery rather than blind reissue.
- Preserve historical exports, both skulls, existing worlds and the 1.21.1 visual
  Alpha 4.9 target. New worlds select the approved gameplay interiors.
- Add headless item/recipe/ledger tests and static mixin-target checks. Item-system
  client/multiplayer acceptance and the complete gameplay release gates remain open.

See [implementation evidence and limitations](docs/testing/GAMEPLAY_IMPLEMENTATION_20261008.md).

## Unreleased — gameplay architecture worktree

- Build versioned large/small Colossus interiors, unfinished Tower traversal,
  exterior Obelisk archaeology and World Tree base lighting/amethyst decoration.
- Deliver NBT/schematic, editable grouped Blender sources, gameplay sidecars,
  coordinate plans, cutaway reviews, 26.2 state checks and builder tests.
- Add optional `arm_clearance` for the detached-arm service passage.
- Preserve Alpha 4.9 selection and both skulls. Runtime initialization, light tests
  and visual acceptance remain pending.

## 0.1.0-alpha.4.9 — open cave contacts and sparse Tree strands

- Select World Tree V4.3 strands: preserve the accepted art and world pose,
  replacing the later bulk extrusion with 1,883 attached cells along 50 paths.
- Keep Skull 2's complete raw anatomy/sword export and ground Y28. Clip only
  7,309 deeply buried cells below raw Y22 from its derived natural template.
- Limit these two profiles to complete short contacts of at most two cells in
  the adjoining art material. Preserve longer caves and deep root clearances;
  do not build dirt walls, wooden piers or hanging partial columns.
- Retain eight other raw/natural templates, including rock Skull, and all
  dependency, density, biome, slope, separation and terrain-grid settings.
- Keep missing/short-contact failures separate from intentional cave clearances
  and the unchanged three-leaf strict air-only finding in Skull 2.
- Require fresh complete ten-variant acceptance before terrain-only profile
  installation, with a verified backup and preservation of old worlds/exports.
- Install the tested Alpha 4.9 JAR with a verified Alpha 4.8 backup and one
  new terrain inspection save. Preserve all 18 previous worlds and source
  exports; no additional flat world or manual cavity clearing is introduced.
- Record the verified visual-alpha baseline with annotated tag
  `v0.1.0-alpha.4.9`; no GitHub Release or downloadable asset is added.

See [Alpha 4.9 validation](docs/testing/ALPHA_4_9_TEST_REPORT.md).

## 0.1.0-alpha.4.8 — native-ground embedding and rooted World Tree

- Select the exact Rock Skull and Skull 2 embedded-v1 exports and World Tree
  V4.2 rooted derivative from the October 7 candidate index.
- Remove their authored soil/rock platforms without changing Skull anatomy or
  the rigid sword. Bury both Skulls six blocks deeper; retain native terrain.
- Preserve accepted Tree wood/foliage under the declared +12 Y export translation,
  add 37,005 connected low wood cells and place the accepted art four blocks deeper.
- Bypass derived soil platforms only for these embedded-art exports; optionally
  continue Tree roots with their original wood state instead of dirt pillars.
- Keep seven other exports, dependencies, density, biomes, slopes and gameplay
  unchanged. Preserve historical models and the failed native-leaf cavity audit.
- Require fresh full-pack showcase/natural acceptance before profile replacement;
  keep strict air-only cavity observations separate from supported model contacts.
- Install the tested Alpha 4.8 JAR with a verified Alpha 4.7 backup and a separate
  showcase save. Preserve all 16 previous worlds and model sources. The user
  chose showcase only; do not bypass the unrelated-server terrain-copy guard.

See [Alpha 4.8 validation](docs/testing/ALPHA_4_8_TEST_REPORT.md).

## 0.1.0-alpha.4.7 — ground contacts and natural placement

- Integrate the prepared runtime-contact update without changing the ten raw
  model exports, their burial depths or earlier sources.
- Support exposed solid-model undersides at/below nominal ground using stable
  biome-appropriate fill; preserve raised arches, authored cells and saved masks.
- Move the natural Jigsaw biome-query anchor to the surface while retaining the
  buried piece origin. Use the revised crowned-Skull site tolerance and uphill-only
  allowances for rock Skulls and Small Colossi.
- Retain the full terrain grid, biome tags, separation, density and dependencies.
- Include existing full showcase/natural acceptance and passing root/substrate
  audits, with ordinary locators under the normal 60-second watchdog.
- Keep profile installation, new worlds and gameplay outside the initial integration.
- Record the separately authorized Alpha 4.7 profile upgrade, verified Alpha 4.5
  backup, two new inspection saves and unchanged original worlds.
- Publish all 54 user screenshot views as six numbered contact sheets plus a
  selected-findings sheet, with native PNG hashes and a visual review. Proposed
  art refinements remain unimplemented; gameplay remains unchanged.

See [Alpha 4.7 validation](docs/testing/ALPHA_4_7_TEST_REPORT.md).

## 0.1.0-alpha.4.6 — deeper embedding, Skull 2 V2 and Tower V7

- Select the seven pinned ground-v3 derivatives and Titan Skull 2 V2, including
  deeper burial and narrower slope envelopes from the new artwork contracts.
- Keep crowned-Skull anatomy, Small Colossus art and accepted Tree wood/foliage
  unchanged; explicitly allow the Tree's low moss-pad terrain edits.
- Select Tower V7's connected collapsed bays and Skull 2 V2's settled pose.
  Preserve all earlier source/export files and raw-template byte identity.
- Pin the ground-v2 builder's historical geometry and burial independently of
  current selection; preserve deterministic before/after reproduction.
- Audit buried raw-boundary art contacts in saved natural/reloaded worlds,
  separately from authored in-grid supports and Tree ground-level roots.
- Retain dependencies, density, biome mappings, terrain-support policy and gameplay.
  Require fresh strict runtime acceptance before profile replacement; back up
  Alpha 4.5 and create separate new inspection saves without editing old worlds.
- Publish real-client photo overview/contact sheets from an isolated Alpha 4.6
  copy. Keep failed natural coverage and root/substrate audits explicit; the
  original “Relic Test” profile remains on Alpha 4.5.

See [embedding artwork](docs/project/EMBEDDING_20261006.md) and
[Alpha 4.6 validation](docs/testing/ALPHA_4_6_TEST_REPORT.md).

## 0.1.0-alpha.4.5 — deposit relief and lower Tower walls

- Select all eight pinned ground-v2 derivatives: the four crowned-Skull palettes,
  Small Colossus V7, World Tree V4.1, Ruined Tower V6 and Titan Skull 2 V1.
- Keep Large Colossus and Obelisk exports unchanged. Preserve earlier source art
  and byte-identical raw template packaging; derive supports from the new soil.
- Preserve every derivative's non-terrain cell exactly against its source, including
  the accepted Tree and shared moss materials. Check previous derived art contacts.
- Keep reproduction inputs independent of current mod selection to prevent repeated
  erosion and retain meaningful Alpha 4.4 before/after comparisons.
- Retain Alpha 4.4 dependencies, density, biome mappings, burial and runtime policy.
  Require fresh strict showcase/natural/reload acceptance before profile replacement.
- Back up Alpha 4.4, preserve existing worlds and create new inspection saves.
  Gameplay, rewards and artistic acceptance remain outside this integration.

See [deposit relief and Tower V6](docs/project/DEPOSIT_RELIEF_20261006.md) and
[Alpha 4.5 validation](docs/testing/ALPHA_4_5_TEST_REPORT.md).

## 0.1.0-alpha.4.4 — weathered Colossus, Tower sides and Tree ground contacts

- Select Small Colossus V7, World Tree V4.1 and Ruined Tower V5 with pinned raw
  export hashes. Preserve all earlier sources and the other seven selected exports.
- Retain every accepted V4 Tree non-terrain cell exactly; derive supports only
  from the revised soil contacts. Add regression and actual saved-world root
  contact checks without filling intentional raised root arches.
- Include the latest art pipeline's narrow wood/wood material-tie preservation,
  weathering/growth, side-wall breaches and grassy rubble base.
- Pin build/setup/runtime tools to Fabric API 0.161.0+26.2 and stable Lithostitched
  1.8.0, matching the user's updated test profile. Keep Minecraft 26.2 / Java 25.
- Require fresh all-template showcase and strict natural verification before
  profile replacement. Preserve old saves, back up Alpha 4.3 and create new saves.
- Keep gameplay, density, biome mappings and broader balancing unchanged.

See [October 6 art changes](docs/project/GROUND_WEATHERING_20261006.md) and
[Alpha 4.4 validation](docs/testing/ALPHA_4_4_TEST_REPORT.md).

## 0.1.0-alpha.4.3 — latest screenshot-follow-up structures

- Select Small Colossus V6, World Tree V4 and Ruined Tower V4 with pinned export
  hashes; preserve the other seven templates, earlier models and source exports.
- Recalculate padded footprints, ground contracts and conservative reservations
  for the revised geometry, including the wider Tree crown. Keep the Alpha 4.2
  support processor, saved exact-cell masks, biome mappings and density settings.
- Build and test a separately versioned artifact; require new full showcase and
  strict natural-placement evidence before updating the test profile. Keep old
  saves untouched and back up the previous Relic JAR.
- Leave artistic acceptance, gameplay and balancing outside this integration.

See the [art follow-up](docs/project/ALPHA_4_2_ART_FOLLOWUP.md) and
[Alpha 4.3 validation](docs/testing/ALPHA_4_3_TEST_REPORT.md).

## 0.1.0-alpha.4.2 — terrain placement correction candidate

- Keep the latest Small Colossus V5, World Tree V3 and Ruined Tower V3 exports;
  preserve all earlier source models and raw-template identity.
- Extend lowest earth columns to actual terrain with a chunk-local Java structure
  processor, without rewriting model cells or unrelated voids.
- Add conservative seed-based reservations between relic families without
  recursive generation or a denser height grid. Disabled sets release their space.
- Reject unsupported foundations and horizontal relic overlap at installation,
  even with the minor-feature-edit allowance. Add actual Java processor tests,
  checksum-verified compilation, portable CI setup and versioned inspection saves.
- Protect exact new model/support cells from late ore, stone, fossil and lake
  world-generation writes using persistent sparse chunk masks; normal player
  mining/building remains unrestricted. Require saved-mask coverage at installation.

See the [implementation](docs/technical/ALPHA_4_2_TERRAIN.md) and
[validation status](docs/testing/ALPHA_4_2_TEST_REPORT.md).

## 0.1.0-alpha.4 — seven current relic designs

- Select Colossus V4.1 materials B, Obelisk V4.2, crowned Skull V4 in four
  ground palettes, Small Colossus V4, World Tree V2, Ruined Tower V2 and Skull 2 V1.
- Preserve all source exports; pin hashes and copy manual templates byte-for-byte.
  Derive only replaceable center anchors for complete natural cross-chunk placement.
- Add all-family worldgen, height/burial/footprint limits and density/disable
  settings. Crowned Skull variants use disjoint biome tags and one shared set.
- Reject stale build resources, embed selection provenance and expand runtime
  inspection to all ten templates. Candidate artistic approval remains separate.
- Keep gameplay, large-Colossus uniqueness and existing saved structures unchanged.

See [Alpha 4 integration](docs/technical/ALPHA_4_INTEGRATION.md) and
[runtime evidence](docs/testing/ALPHA_4_TEST_REPORT.md).

## Unreleased — in-game review and demos

- Follow up the Alpha 4.2 screenshots with World Tree V4's spreading branch fans,
  Small Colossus V6's overlapping forged armour and darker pincers, and Ruined
  Tower V4's fractured skyline, stair gap and inner masonry relief. Add opt-in
  structural material priority so leaf intersections cannot erase the Tree's
  exported wood paths. New visual candidates and actual-NBT comparisons are
  documented in the [art follow-up](docs/project/ALPHA_4_2_ART_FOLLOWUP.md).
- Address the October 5 screenshot review with Small Colossus V5, World Tree V3
  and Ruined Tower V3 candidates. Add tapered soil-column foundations, padded
  placement footprints and saved-world foundation-contact checks in Alpha 4.1.
  Preserve the screenshot-era source models and Alpha 4 test evidence.
- Record rejection of Small Colossus V3 as too skeletal and the user's new
  primary reference, Vigilant-Class Archaean Colossi (reel Da-s0zqi7OQ). Inspect
  the full montage and opening dormant specimen; preserve observations and
  authored-completion boundaries in a dedicated reference brief.

- Record follow-up feedback on Small Colossus V2: its resemblance to the large
  Colossus is too strong; a clearly distinct appearance is required.

- Record October 4 V1 feedback: Titan Skull 2 visually accepted for now; revise
  Small Colossus beyond its test-model identity, make World Tree more natural,
  and increase Ruined Tower height. The user selected the large Colossus's visual
  family for the new small design and 220 visible blocks for the tower.

- Record per-relic V4 revision plans from the V3 in-game review; keep current
  models and build selection unchanged.
- Add three original Colossus V3 shader screenshots in a per-relic demo gallery,
  linked from the repository README and separated from Blender previews.
- Add normal-terrain preview-world preparation tooling and document the natural
  inspection world, viewpoints and remaining acceptance limits. Local saves,
  runtime logs and profile backups remain excluded from version control.

## 0.1.0-alpha.3 — V3 visual integration

- Select checked-in Colossus v3, Obelisk v3 and Titan Skull v3 exports in the
  default mod build, byte-for-byte, preserving source DataVersion for game migration.
- Add Titan Skull natural worldgen, biome tags, density presets and disable support.
- Update burial offsets, footprint grids and height limits for the large V3 models.
- Center natural templates on a replaceable named jigsaw so all parts stay within
  the engine's structure-reference range; place the Skull after terrain features
  to protect its authored hill. Keep raw manual templates and design exports intact.
- Expand integration tests and isolated server checks to all three structures;
  add a flat-world showcase mode with saved-block verification.
- Leave planned gameplay, final interiors and existing worlds unchanged.

See [V3 integration](docs/technical/V3_INTEGRATION.md) for contracts and viewing commands.

## Unreleased — asset pipeline and documentation

- Add reference-led Small Colossus V4 with a massive plated body, six-lens face,
  arched grille and heavy pincer hands. Include a documented reference study,
  Blender source, exports, body/optic/grille/connectivity checks and an actual-NBT
  V3/V4 comparison. Original reel frames and reference/model boards stay local.

- Add user-selected Small Colossus V3 slender sentinel: elongated mask, narrow
  articulated waist, stepped armour and two long attached arms in a listed sunken
  pose. Include Blender source, exports, structural/proportion checks and a
  separate actual-NBT V2/V3 same-scale review; visual acceptance pending.

- Add October 4 V2 candidates: newly modeled small bronze-machine Colossus,
  branch-grown World Tree and 220-visible-block Ruined Tower. Include editable
  sources, NBT/schematic exports, exact conversion/feature checks and same-scale
  V1/V2 reviews. Make preview shader-node lookup independent of translated names.

- Add four independent V1 models/exports after the reference study: Ruined Tower,
  World Tree, Small Colossus and sword-bearing Titan Skull 2. Include editable
  Blender sources, pinned OBJ conversion, NBT/schematic, tile/cavity checks,
  actual-block overview/detail reviews and reproducible commands. Keep accepted
  assets/archive intact; visual acceptance and game integration remain pending.

- Evaluate references for the next four relics without Blender work. Establish
  working size/proportion/damage briefs for Ruined Tower, World Tree, the archived
  smaller Colossus and independent Titan Skull 2. Verify the second skull's
  embedded sword and cavern setting; distinguish observed details from authored
  dimensions and hidden-side completion. Reference media remains local.

- Record user visual acceptance of Colossus material version B, including its
  post-salvage appearance: 25,423 copper blocks, 90 raw iron items and unchanged
  intact V4.1 geometry. This is the selected material asset for later integration.

- Revise Colossus salvage as separate material study B following user feedback:
  25,423 copper blocks and 90 raw iron items, under the requested 50,000 / 256
  limits. Retain exact intact V4.1 geometry and permanent support paths; verify
  head-to-buried-body connectivity and zero new component splits after mining.
  Add matched close reviews and a false-color metal-location map. Preserve study A.

- Add a separate shape-locked Colossus material study: preserve all 223,161 V4.1
  block positions and 491 source meshes, replace broad metal surfaces with less
  valuable materials, and retain 197 copper / 10 raw iron blocks at three local
  salvage sites. Add exact grid/state checks, schematic round-trip tests, resource
  accounting, and before/after hypothetical salvage reviews. Candidate review pending.

- Record visual acceptance of Obelisk V4.2 and all four Titan Skull V4 variants.
  Prioritize the remaining relic designs before V5 interior architecture.

- Record user visual acceptance of Colossus V4.1.
- Add Obelisk V4.2 with warmer ochre/clay sides, same-material fracture faces
  and two actual missing edge chunks. Preserve previous versions and verify
  that the notches survive export without contrasting replacement blocks.

- Added separate Colossus V4.1 frame export: supinated palm-up right hand with
  upward-curled fingers, preserving all 434 non-hand V4 meshes. Included a
  higher-ground inspection view and anatomical/export checks.
- Added separate Obelisk V4.1 export: consistent sandstone facets instead of
  contrasting patches, three branching surface cracks and four larger edge
  spalls. Preserved V4 scenery and verified open cracks over a solid core.

- Added four Titan Skull V4 exports (meadow, dry earth, sand, rock), preserving
  all 62 anatomy meshes while replacing the continuous hill with interrupted,
  tapered deposits and a lighter fossil palette. Reduced terrain by 52.44%.
- Added Obelisk V4 with restrained material weathering, four shallow edge chips,
  asymmetric sand and three foundation fragments; retained height, antiprism
  geometry, rotated crown and solid core. Both relics await visual acceptance.
- Added semantic terrain material remapping, supported sand/gravel and exposed
  grass rules, source/export validation, and V4 variant/comparison reviews.

- Added Colossus V4 open/frame export studies: asymmetrically damaged rear armour,
  a raised anatomically right hand, and two alternatives for the plain chest piston.
  Preserved 397 V3 source meshes and its body scale; added NBT detail comparisons,
  hand/rear/cavity checks, and a chest-only A/B difference check. Build selection
  remains V3. The user selected B / open machine frame on October 2, 2026;
  A remains available for comparison, and integration is pending.

- Archived the original Colossus concept under `relics/colossus/archive/first-concept/`
  as the basis for a second, smaller Colossus. Preserved models and exports and
  updated reproduction and size-comparison paths.

- Group each relic's design documents, asset configs, Blender/export files, and
  gameplay decisions under `relics/<relic>/`. Separate shared project, technical,
  and testing documentation under `docs/`; keep mod sources and tools separate.
  Update pipeline paths, asset provenance paths, ignore rules, and documentation
  links without changing geometry or the playable alpha. Add layout/link checks.

- Include generated review sheets, editable source Blender models, whole design
  NBTs, schematics, design/converter metadata, and verification records in version
  control so asset results can be viewed, edited, and downloaded without rebuilding
  the pipeline.

- Added Titan Skull v3 with nine partly buried vertebrae, two spinal fractures,
  loose fragments, and an extended solid hill. Preserved the v2 skull scale and
  added actual-NBT rear/detail views and burial/fracture checks.

- Added Titan Skull v2 at Colossus-head scale: approximately 76 blocks including
  crown, about 20% taller than the measured helmet shell. Added a solid exported
  moss/soil/stone mound, complete rear presentation, actual-NBT head comparison,
  and terrain-solidness/posterior-wall checks.

- Added Titan Skull v1 after the opening of *D.E.A.D.*: organic crown, hollow
  cranial vault, real eye/nose openings, long open jaw, teeth, and lateral spurs.
  Added its Blender/OBJ/schematic/NBT pipeline, green-hills presentation, cutaway,
  scale comparison, and exported cavity checks. Game integration remains pending.

- Added Obelisk v3: a tapered square antiprism with eight triangular faces, a
  45-degree rotated square crown, and an 8-block buried foot. Added full-height
  ground-line inspection and exported base/crown geometry checks.
- Recorded the current v3 design pair and its above-ground height comparison:
  approximately 177 layers for the Obelisk versus 132 for the Colossus. Updated
  English documentation, reproduction commands, and integration status.

- Added a local Blender → OBJ → ObjToSchematic 1.0 → Sponge schematic → Java NBT pipeline, replacing the proposed VoxelVision dependency.
- Added reference-based Colossus v2 (181 × 160 × 227 blocks) and Colossus v3 (181 × 209 × 227), with an underground abdomen and torn hip in v3.
- Added Obelisk v2 (23 × 209 × 19), inspired by Josh White's *Painted Desert*, with a flat crown, mineral bands, and a 32-block buried foot.
- Added opt-in enclosed-volume filling, used for the Obelisk's solid sandstone core, with flood-fill tests.
- Added textured previews from actual exported NBT blocks, landscape presentations, scale comparisons, underground inspections, and block-exact export verification.
- Added a Sponge v2/v3 converter with explicit air handling, optional tiles, and conversion manifests.
- Updated project status and translated repository documentation into English.

These are asset-development changes. The new Blender assets are not yet selected by the mod build or natural world generation. Alpha 2 remains the current playable build. Selected asset deliverables are tracked; intermediate files and local reference media remain excluded from Git.

## 0.1.0-alpha.2

- Added connected cracks, deeper edge damage, sand drifts, and base debris to the Obelisk.
- Added a broken helmet, exposed chest supports, a damaged chest ring, and notches in the detached Colossus arm.
- Concentrated denser moss and leaves on one side, with moss traces on vertical surfaces.
- Moved the approach 14 blocks inward. The short, irregularly paved entrance is edged with soil and fallen plates; a three-block-wide route to the machine room stays clear.
- Made the test server select the current project-version artifact by default, preventing accidental tests of retained older JARs.

New shapes appear only in newly generated areas. Existing relics are not rebuilt. Dependencies, structure IDs, and distribution are unchanged. See the [Alpha 2 test report](docs/testing/ALPHA_2_TEST_REPORT.md).

## 0.1.0-alpha.1

First implemented alpha for Minecraft 26.2 with Fabric.

- Automatically generated an Obelisk and a Colossus with an arm and interior.
- Added deterministic NBT exports, whole templates, optional tiles, and checksum manifests.
- Added natural placement through Lithostitched biome, height, and grid conditions.
- Added optional biome mappings for Terralith and Biomes O' Plenty.
- Added generated settings datapacks for density profiles and disabled relic types.
- Added a reproducible data-only Fabric build without custom Java classes.
- Added geometry previews, tests, and an isolated test-server workflow.

This alpha tests generation and integration. Visual design, terrain transitions, and density require further playtesting. See the [historical Alpha 1 test report](docs/testing/ALPHA_TEST_REPORT.md) for checks actually performed.
