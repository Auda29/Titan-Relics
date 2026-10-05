# Alpha 4 — current relic runtime tests

This report is evidence for the original Alpha 4 checksum below. It does not
qualify the subsequent [Alpha 4.1 screenshot revision](../project/SCREENSHOT_REVISIONS_20261005.md).

Recorded: October 4, 2026. Minecraft 26.2, Fabric Loader 0.19.5, Java 25,
Fabric API 0.160.0+26.2 and Lithostitched 1.8.0+beta6.

## Scope

Seven relic designs and ten raw/natural template pairs are selected as described
in [the integration contract](../technical/ALPHA_4_INTEGRATION.md). Blender models
and exported source files from the Structures thread are unchanged. Artistic
approval remains pending for Small Colossus V4, World Tree V2 and Ruined Tower V2.
No gameplay, uniqueness implementation or edits to existing saves are included.

## Automated checks

- 52 Python tests passed: current/historical export identity, center-anchor
  restoration, all-rotation footprint/reference bounds, burial/ceiling contracts,
  disjoint Skull biome mappings, all-family density/disable settings, stale-build
  rejection, persistent-leaf state handling, safe terrain-preview region/viewpoint
  helpers, full-model installation gates, reproducible packaging and existing
  asset/world-reader regressions, plus failure-preserving evidence summaries.
- 5 JavaScript tests passed: material-proxy mapping and enclosed-volume filling.
- Source exports preserve DataVersion 3105. The target game performs migration.

## Runtime status

The final artifact is `relics-0.1.0-alpha.4+mc26.2.jar`, SHA-256:

```text
1ab46b7d2427d3f7c9994b49ee5c0d928348174fbdf6fc794f919ea78826e2eb
```

Default and `--skip-generation` repeat builds produced the same checksum.
The final-artifact showcase has passed. Start-biome-based rock selection now
produces a complete natural rock Skull. The all-relic final natural run generated
every selected model/variant completely, with documented later feature edits.
The visual-test artifact and two new inspection saves are installed in Relic Test;
the strict natural block comparison remains **failed**, not relabeled. Summaries are in
[Alpha 4 evidence](alpha4-evidence.json), linked to full local reports by SHA-256.
All worlds, server libraries, logs and local reports remain under ignored `build/`.

An initial parallel launch exposed a run-directory collision in the old harness's
sub-millisecond timestamp suffix. Run directories now include a random UUID
suffix; this correction does not change the packaged mod or model geometry.

The final-artifact showcase (`run-20261004-152841-c838e15dd103`) verified all
**1,895,184 exported blocks** across ten placements, with no missing/incomplete
checked chunks or blocking log errors. Persistent-leaf distance recalculation
affected 24,962 World Tree leaves; this valid dynamic value is explicitly counted
while leaf type, position and persistence remain strict. The earlier unnormalized
comparison is retained in `run-20261004-145609-9989749f0ef4` as a failed report.

| Template | Checked export blocks | Mismatches | Occupied chunks |
| --- | ---: | ---: | ---: |
| Colossus | 223,161 | 0 | 104 |
| Obelisk | 94,422 | 0 | 15 |
| Skull meadow | 136,569 | 0 | 61 |
| Skull dry | 136,569 | 0 | 61 |
| Skull sand | 136,569 | 0 | 61 |
| Skull rock | 136,569 | 0 | 61 |
| Small Colossus | 215,766 | 0 | 45 |
| World Tree | 412,702 | 0 | 101 |
| Ruined Tower | 317,633 | 0 | 37 |
| Skull 2 | 85,224 | 0 | 44 |

The independent settings-pack run (`run-20261004-151057-230773cf46fc`) **passed**.
Disabling the crowned Skull family removed all four variants' locator candidates
(0–31 ms per query), while their manual templates remained usable. This subset
test is not a substitute for all-relic natural generation acceptance.

The initial natural run (`run-20261004-145410-862500`) found every relic design
and three crowned-Skull palettes with complete bounding boxes. Its strict result
**failed**, not hidden: large Colossus had 47 fixed-block edits, sand Skull had 90,
and no rock Skull was located in seed 731204. All seven other natural instances
had zero checked-block mismatches. The original rocky tag admitted only two
windswept biomes; the final mapping additionally admits stony shores and peaks,
without relaxing the all-site biome, ocean/river, slope or height filters.

## Preceding-artifact natural terrain result

Run `run-20261004-150710-f559ded08c43`, seed 731204, base dependencies only.
All seven relic designs and meadow/dry/sand crowned-Skull variants generated
**complete models**, with no missing/incomplete checked chunks, bounding-box
errors, runtime failures or blocking log errors. The server exited cleanly.

| Natural structure | Checked fixed blocks | Mismatches | Rotation |
| --- | ---: | ---: | --- |
| Colossus | 218,423 | 47 | Counterclockwise 90° |
| Obelisk | 94,422 | 0 | Counterclockwise 90° |
| Skull meadow | 21,475 | 0 | Clockwise 180° |
| Skull dry | 28,435 | 0 | None |
| Skull sand | 136,569 | 90 | Clockwise 180° |
| Small Colossus | 203,431 | 0 | Counterclockwise 90° |
| World Tree | 398,052 | 0 | Counterclockwise 90° |
| Ruined Tower | 317,633 | 0 | Counterclockwise 90° |
| Skull 2 | 40,160 | 0 | Clockwise 90° |
| Skull rock | Not located | Not verified | — |

Dirt, grass blocks and azalea leaves are the explicitly counted historical
natural exclusions, not removed from the templates; the flat showcase checks
them too. Colossus edits affect andesite (dirt, gravel, coal/iron ore, granite).
Sand-Skull edits are stone/lava/cave-air/sand writes and secondary sand updates.
Each is below 0.1% of checked fixed blocks, but the strict result stays **failed**.

The rock variant was not found within `/locate`'s search in this seed (155 seconds)
even with the expanded rocky mapping. The seed-42 diagnostic
`run-20261004-152114-892f97a27116` also located no rock variant and exited cleanly.
Its manual template is fully verified; natural site availability under the
all-footprint-biome restriction is not. Other locator times ranged from 0 to 67 seconds
(World Tree 29 seconds). These are diagnostic timings, not performance acceptance.
The new installation gate deliberately rejects missing variants even with the
minor-feature-edit override. This preceding report did not qualify installation;
the final all-variant run below subsequently provided complete-model evidence.

The final rock rule keeps the delegate's rocky **start-biome** selection, while
mineral deposits may span a biome edge. Only the extra pure-biome check over the
whole 180-block site is removed for rock. Meadow/dry/sand keep their strict sampled
biome checks, and all variants keep all-site height/slope/ocean/river checks.

The adjusted rock-only diagnostic (`run-20261004-152841-01f1909d905a`, seed 731204)
located a natural rock Skull at anchor `[-58944, 26160]`. Its complete rotated box
`[-59033,67,26102,-58855,145,26218]` spans 63 occupied chunks; all were full.
There are 1,171 mismatches of 136,569 checked blocks (0.857%): **stone terrain only**
became dirt, coal/copper/emerald ore, andesite, gravel or diorite. No fossil block
mismatches occurred. Its strict result stays failed. The incidental Small Colossus
near spawn was not deliberately footprint-loaded in that subset diagnostic and
is explicitly recorded as incomplete, not a new model-generation defect or
qualifying installation evidence. The all-relic run checks its full footprint.

## Final-artifact natural terrain result

Run **`run-20261004-152841-70da84418a4e`**, seed 731204, same JAR as the final
showcase. All ten selected structure/variant starts have matching full bounding
boxes, with no missing/incomplete checked chunks or verification/read errors.
The server started and exited cleanly with no blocking log errors.

| Natural structure | Checked fixed blocks | Mismatches |
| --- | ---: | ---: |
| Colossus | 218,423 | 60 |
| Obelisk | 94,422 | 0 |
| Skull meadow | 21,475 | 0 |
| Skull dry | 28,435 | 0 |
| Skull sand | 136,569 | 90 |
| Skull rock | 136,569 | 1,180 |
| Small Colossus | 203,431 | 0 |
| World Tree | 398,052 | 0 |
| Ruined Tower | 317,633 | 0 |
| Skull 2 | 40,160 | 0 |

The Colossus differences include andesite/armour becoming dirt, ore, gravel,
granite, stone, lava or cave air. Sand-Skull differences remain the terrain/lava
and secondary sand updates listed above. Rock-Skull differences are **stone
terrain only**, becoming dirt, ores, andesite, gravel or diorite; fossil blocks
match. Rock terrain edits are 0.864% of checked blocks, the other two below 0.1%.
Seven instances have zero checked-block mismatches. No exclusions were added to
hide feature edits, and the strict report stays failed.

## Test-profile installation and viewing

Installed in `E:/Roaming/ModrinthApp/profiles/Relic Test` with the existing
visual-test allowance (`--allow-feature-overwrites`). The installer required
complete evidence for all ten models/variants, the passing full showcase, matching
JAR hashes and less than 1% mismatch per natural instance; missing models cannot
be overridden. This permits visual inspection, not strict worldgen acceptance.

- Only the Relic JAR was replaced; other mods/dependencies were unchanged.
- Alpha 3 was hash-verified and backed up under
  `build/profile-backups/0.1.0-alpha.4-upgrade-20261004-153947/`.
- New flat save: **Relic Alpha 4 Showcase 20261004-153947**.
- New normal-terrain save: **Relic Alpha 4 Terrain 20261004-154033**, seed 731204.
- Both are creative with cheats. Existing saves, including both V3 review worlds,
  were not edited. Minecraft/Java clients were closed during installation.

The terrain copy omits the recorded manual-test regions `r.0.0.mca` through
`r.6.0.mca` (blocks/entities/POI), with a guard against removing any natural relic.
Source regions are never deleted. Its natural instances were rechecked after
preparation: all ten stayed complete, with unchanged 60/90/1,180 mismatches.
Normal difficulty, ordinary mob spawning and random tick speed 3 are restored.
Spawn is `[-29173,72,-54592]`, facing the natural Colossus west-side approach.
Preparation evidence: `build/terrain-preview/20261004-154033/report.json`.

### Natural-world viewpoints

Enable creative flight before teleporting to these aerial viewing positions:

| Relic | Command |
| --- | --- |
| Large Colossus | `/tp @s -29173 110 -54592 -90 0` |
| Obelisk | `/tp @s 6306 120 -7024 -90 0` |
| Skull meadow | `/tp @s -10400 115 -17511 180 0` |
| Skull dry | `/tp @s 5520 115 -617 0 0` |
| Skull sand | `/tp @s -22832 110 -31863 180 0` |
| Skull rock | `/tp @s -59081 115 26160 -90 0` |
| Small Colossus | `/tp @s -787 110 160 -90 0` |
| World Tree | `/tp @s -33591 160 -27328 -90 0` |
| Ruined Tower | `/tp @s -974 160 5280 -90 0` |
| Skull 2 | `/tp @s 7493 115 -5664 90 0` |

### Flat showcase viewpoints

Models are spaced along X, facing the negative-Z approach:

```mcfunction
/tp @s 90 110 -64 0 0
/tp @s 413 120 -64 0 0
/tp @s 826 115 -64 0 0
/tp @s 1210 115 -64 0 0
/tp @s 1594 115 -64 0 0
/tp @s 1978 115 -64 0 0
/tp @s 2360 110 -64 0 0
/tp @s 2777 160 -64 0 0
/tp @s 3127 160 -64 0 0
/tp @s 3508 115 -64 0 0
```

Order: Colossus, Obelisk, meadow/dry/sand/rock Skull, Small Colossus, World Tree,
Ruined Tower, Skull 2. These are prepared manual placements, not natural starts.

## Open acceptance limits

- Client visual review of the integrated current models and additional seeds.
- Systematic terrain-mod, shader/LOD and performance tests.
- Later neighboring-chunk feature writes can alter template blocks. Such edits
  must stay visible in the strict natural comparison, not silently be excluded.
- Omitted air preserves surrounding terrain and does not prove walkable interiors.
- Grid samples cannot prove perfect grounding or protection from other structures.
- Final frequency, large-Colossus uniqueness, rewards and encounters are pending.
