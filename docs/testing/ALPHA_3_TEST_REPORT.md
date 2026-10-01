# Alpha 3 — V3 visual integration

Recorded: October 1, 2026. Minecraft 26.2, Fabric Loader 0.19.5, Java 25,
Fabric API 0.160.0+26.2, Lithostitched 1.8.0+beta6. Base dependencies only;
this is not a full TerraVista/terrain-mod integration test.

## Build and source checks

The default build selects Colossus v3, Obelisk v3 and Titan Skull v3. Their
packaged NBT bytes match the checked-in exports exactly, including DataVersion
3105. Minecraft performs template migration while loading them; the exporter
does not falsely stamp old data as version 4903.

The repeat-built artifact is `relics-0.1.0-alpha.3+mc26.2.jar`, SHA-256:

```text
530be00274f815d9f7fe93dab6dde3570988b1b1f0c1d21f007d2a0b5042671c
```

All **32 automated tests passed**. Checks cover source identity, dimensions, burial corrections, footprint
grid contracts, density settings including disabling Titan Skull, reproducible
packaging, four-rotation transforms, saved chunk reading, and safe editing of
only the new showcase world's title/cheat setting. Historical procedural-model
tests remain as regression fixtures, not V3 route acceptance.

## Runtime checks and corrections

Two modes use separate worlds at seed 731204:

- **Normal terrain:** locate all three relics, generate their actual rotated
  bounding boxes, then compare saved natural-start blocks with the launched JAR.
  Dirt, grass blocks and azalea leaves are excluded because later world features
  can modify them; exclusions remain explicitly counted.
- **Showcase:** flat grass surface at Y64, creative mode, mobs/random ticks disabled.
  Place all three models at their nominal burial depths and compare every saved
  export block, including dirt. This world is for visual comparison, not evidence
  of natural placement.

Initial attempts exposed two harness issues: the target game says "Unmarked" when
removing forced chunks, and `/locate` returns an anchor rather than the rotated
footprint center. The harness now recognizes that reply, reads the saved natural
start's bounding box and waits for every footprint chunk, avoiding partial-model
checks. An initial 49-point, ±8-block Colossus terrain filter made the locator
search exceed the server watchdog limit. The final provisional grid uses 25
samples over the same radius with ±16-block variation (Skull: ±12).

Full-box generation then exposed a real engine constraint: a corner-anchored
large template extends beyond the eight-chunk structure-reference radius.
Natural pools now use derived templates with a Y0 center jigsaw replaced by the
original block or omitted structure void. Raw manual templates and source
models stay byte-identical. The Skull also generates after ore/vegetation
features, to prevent its authored stone/moss hill being overwritten.

The final centered-build showcase run `run-20261001-205251-064900` passed with no block
mismatches, missing/incomplete checked chunks, or blocking log errors:

| Model | Checked blocks (including dirt) | Chunks containing model blocks |
| --- | --- | --- |
| Obelisk v3 | 93,153 | 4 |
| Colossus v3 | 221,221 | 104 |
| Titan Skull v3 | 264,355 | 89 |

The natural run `run-20261001-205251-300700` started and shut down cleanly and
generated all three complete bounding boxes without missing/incomplete chunks.
Its **strict block comparison did not pass**, because later neighboring-chunk
features still overwrite a small number of blocks:

| Model | Checked fixed blocks | Mismatches | Natural rotation |
| --- | --- | --- | --- |
| Colossus v3 | 216,461 | 13 | Counterclockwise 90° |
| Obelisk v3 | 93,153 | 0 | Counterclockwise 90° |
| Titan Skull v3 | 119,205 | 995 | Clockwise 180° |

The Colossus differences are underground lava/magma/stone/cave-air edits.
The Skull differences are exclusively its stone becoming ores, dirt, gravel,
granite or diorite. Skull materials themselves match. Moving the Skull to the
last feature stage reduces edits but cannot prevent adjacent chunks from later
writing features across their borders. These findings are not suppressed or
counted as a strict pass. A protection or integration solution remains open.

Natural locator anchors were Obelisk `[6384, -7024]`, Colossus
`[-29008, -54592]`, and Skull `[1888, -12240]`. The Colossus search took about
69 seconds in this seed; prefer the ready-made showcase for visual inspection.

## Test-profile installation

After source/hash checks and full showcase verification, the visual-test build
was installed in `E:/Roaming/ModrinthApp/profiles/Relic Test` with an explicit
`--allow-feature-overwrites` acknowledgement. The installer normally rejects
failed natural checks; this option only allows complete instances with less than
1% mismatches, no missing/incomplete chunks and no runtime/read errors. It does
not change the report's failed strict result.

- Only the Relic JAR was replaced; Fabric API and Lithostitched stayed intact.
- The previous Relic JAR was copied to
  `build/profile-backups/alpha3-upgrade-20261001-205738/` before replacement.
- A new creative save **Relic V3 Showcase 20261001-205738** was copied from the
  final showcase run. Cheats are enabled in that copy only.
- Existing saves were not changed. Minecraft/Java clients were not running.

Viewing positions in the new showcase:

```mcfunction
/tp @s 12 90 -60 0 0
/tp @s 346 100 -60 0 0
/tp @s 828 90 -60 0 0
```

These lead to the Obelisk, Colossus, and Titan Skull respectively. All models
are already placed; no `/place` or `/locate` command is required in this save.

## Remaining acceptance limits

- No Minecraft client screenshot or human visual approval is claimed.
- One seed and base dependencies only; four natural rotations, more seeds,
  terrain mods, shaders/LOD and performance testing remain open.
- `/locate` can still block the game while evaluating rare, large sites.
- Missing NBT cells preserve terrain; final interiors, access paths and gameplay
  rewards are not implemented. Existing worlds are not retroactively updated.
