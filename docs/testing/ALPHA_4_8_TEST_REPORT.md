# Alpha 4.8 — native-ground Skulls and rooted World Tree

October 7, 2026. Minecraft 26.2 / Fabric.

The user requested integrating the new structures and supplying TP commands.
The three [rooted/embedded candidates](ROOTED_EMBEDDING_20261007.md) are now
selected in the default build. The seven other exports, dependencies, density,
biomes, slope envelopes and separation rules are unchanged. Earlier source and
export files are preserved. The initial integration did not request publication;
the user subsequently authorized committing and pushing this work. No new release
tag is requested.

## Exact selection

| Structure | Export | Blocks | Raw ground Y | Mode |
| --- | --- | ---: | ---: | --- |
| Rock Skull | `titan-skull-v4-rock-embedded-v1` | 20,131 | 22 | Embedded original art; no authored platform or derived talus toe |
| Skull 2 | `titan-skull-2-v2-embedded-v1` | 32,569 | 28 | Embedded original anatomy/sword; no authored soil island |
| World Tree | `world-tree-v4-2-rooted` | 324,127 | 24 | Accepted art translated +12 Y; connected low root additions and runtime wood continuation |

Selection hashes and complete contracts match the historical
[candidate index](../project/rooted-candidates-20261007.json) exactly. Its
"default selection unchanged" status describes candidate preparation before
this integration, not the current `tools/relic_catalog.py`.

Rock Skull and Skull 2 sit six blocks deeper than Alpha 4.7; the accepted Tree
art sits four blocks deeper after the declared +12 Y export translation.
All retained anatomical cells remain exact. Tree wood/foliage above the new
root region is unchanged; 37,005 attached wood cells extend the existing roots.
Higher intentional arches remain unfilled.

## Air policy and historical cavity observation

The established omitted-air policy still preserves unspecified native terrain
and vegetation. No opening is automatically excavated, no source art is removed
to make a test pass, and no natural leaves are manually cleared.

The historical three-template candidate audit remains **failed** for its strict
air-only cavity category: three native oak-leaf cells intersect the edge of one
lowered Skull 2 probe. Their same-position Alpha 4.7 baseline evidence remains
in [the original audit](rooted-embedding-20261007-runtime-audit.json).
Its support category passed; that distinction must not be erased. Full current
runtime/installation evidence is recorded separately below.

## Build and regressions

Default and skip-generation builds match:
`2b2500a620cf54aa849600f1a49f5ecfcfcc97a48e1e57b4ac6a704178698e5d`.

The final full Python suite passes **91 tests**; Java runtime tests pass **751
assertions** and JavaScript tests pass **7 tests**. Python compilation and
`git diff --check` pass. All three selected candidate contracts, NBT/schematic
bytes and provenance reproduced in an isolated directory without editing sources.
Historical ground-v2/v3 checks remain pinned to their original exports rather
than being incorrectly applied to the newly selected rooted derivatives.
The first full Python run exposed three historical ground-v2 contact-count
failures: its builder inherited `embedded_art` from the current selection.
`baseline_contract` now removes later foundation/root/uphill flags, retaining
the historical soil-column policy and all original count assertions.

## Fresh runtime evidence

The [compact evidence](alpha4-8-evidence.json) records two fresh completed runs
of the final artifact, with seed **731204** and the normal **60000 ms watchdog**:

- Showcase `run-20261007-090359-5ec2549fe80a`: all ten raw templates,
  **1,534,370 blocks**, zero mismatches, complete bounds/chunks, exit 0.
- Natural `run-20261007-090359-448f2a8bf6a8`: all ten actual natural starts found
  by ordinary global `/locate`, **1,422,111 checked non-excluded model cells**,
  zero mismatches, complete bounds/chunks and no overlaps/read errors.
- **73,505 support undersides/soil contacts** are checked, including **17,779
  exposed-art undersides** for the three embedded models; zero unsupported.
- **1,725,140 template protection-mask cells** checked; zero unprotected cells.
  Persistent-leaf distance normalization and natural dirt/grass/azalea-leaf
  exclusions retain the established comparison rules.
- Both servers exit normally with code 0 and no blocking log errors. The global
  searches take **1.375–33.093 seconds** in this seed; this is not a general
  latency guarantee or a fresh terrain-mod compatibility claim.
- [Tree contacts](alpha4-8-tree-contacts.json): zero ground-level gaps and no
  missing expected wood. **175 raised edges** above ground are reported separately.
- [Buried raw-Y0 contacts](alpha4-8-buried-contacts.json): all **3,835** checked
  cells supported in the two retained ground-v3 models requiring this category
  (Small Colossus and Tower). The newly embedded models use exposed-art checks,
  not the removed Tree's historical 1,324-cell raw-Y0 category.

The [embedded support/cavity audit](alpha4-8-rooted-runtime-audit.json) confirms
1,441 local stone additions under Rock Skull, 1,197 dirt additions under Skull 2,
and 1,469 log +23 dirt additions under Tree; all lie below nominal ground.
Its **support category passes**, but its **strict air-only category and overall
`passed` remain false** for the same three native Skull 2 leaves. All three have
identical states at the same positions in the Alpha 4.7 baseline and no relic
protection bits. The audit returns exit 1; neither the failure nor vegetation is
removed. This is the omitted-air policy's retained native vegetation, not lost
anatomy or added supports above ground. The unchanged installation gate accepts
the complete core natural/showcase pair without an overwrite exception; that is
not a claim that every natural cavity is air-only.

## Profile installation and TP viewpoints

Alpha 4.8 is installed in "Relic Test" with the exact tested artifact hash above.
Alpha 4.7 was backed up and hash-verified outside `mods`; Fabric API and
Lithostitched are unchanged. No feature-overwrite override was used.

The new save is **`Relic Alpha 4.8 Showcase 20261007-091425`**. All 76 copied
files match the passing showcase source, except for the intentionally prepared
unique title/cheat metadata in `level.dat`. Creative mode and cheats are verified.
The [installation record](alpha4-8-installation.json) contains all ten TP commands;
each viewpoint is a fully generated chunk with an air camera cell.

Terrain-copy preparation stopped at the safety guard because an unrelated
TerraVista Java acceptance server was running. No copy/server launch or reload
probe took place. The user explicitly chose **finish with showcase only**;
the unrelated server was neither terminated nor bypassed. No Alpha 4.8 terrain
save exists, and the natural-run coordinates must not be presented as commands
for an installed terrain save. Existing Alpha 4.7 terrain worlds remain old art.

At preparation completion, all **16 previous worlds / 165,783 save files**, the
remaining original profile files and all **2,773 model/source files** match the
preparation inventory. No original world was opened or edited by this task.
There is no new client artistic acceptance or release tag. The subsequent push
request publishes the implementation and recorded evidence without new profile,
world, art or gameplay changes.
