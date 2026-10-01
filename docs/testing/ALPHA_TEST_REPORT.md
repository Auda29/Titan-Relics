# Alpha 1 test report

Recorded: September 13, 2026. English translation: October 1, 2026.
Target: `0.1.0-alpha.1`, Minecraft 26.2, Fabric 0.19.5, Java 25.
This is a historical technical-alpha report. The broader visual acceptance
criteria in the implementation plan were not completed by these tests.

## Method

All server runs used separate, newly created worlds under `build/smoke/`, with
seed `731204`. The user explicitly accepted the Minecraft EULA for these local
tests. The server listened only on `127.0.0.1`, with a whitelist and no RCON.
Existing play worlds were not used.

The test loads Fabric and the mod, places both templates using `/place template`,
locates natural sites with `/locate`, fully loads the surrounding chunks, and
saves the world. A custom verifier then reads the saved Anvil regions and compares
block states, rotation, dimensions, and explicit air against NBT from the exact
mod JAR used by that run.

A successful locate command alone is not a passing generation test. Missing
chunks, incomplete structures, and mismatched fixed blocks fail verification.
Colossus grass, dirt, and azalea leaves are explicitly excluded from strict
comparison because later terrain and vegetation stages can alter them.

## Coverage

| Environment | Additional mods | Checks |
| --- | --- | --- |
| Base | Fabric API 0.160.0+26.2, Lithostitched 1.8.0+beta6 | Both templates and both natural relics |
| Worldgen integration | Tectonic 3.0.26, Terralith 2.6.4, Biomes O' Plenty 26.2.0.0.28, Dungeons & Taverns 5.3.2, GlitchCore, TerraBlender | Both templates and both natural relics |
| Settings | Base plus generated `frequent` datapack with Colossus disabled | Active datapack, natural Obelisk, unsuccessful Colossus search, and still-usable manual templates |

Integration used default configurations. Versions and hashes of all eight external
dependency JARs are recorded in [Target environment](../technical/TARGET_ENVIRONMENT.md).
TerraVista's nine additional Dungeons & Taverns overhauls and personal settings
were not included.

Automated source tests cover NBT round trips, deterministic exports, material
states, explicit air versus omitted positions, tile reconstruction, the walkable
machine-room route, settings, package metadata, and the world reader. The world
reader is also tested against deliberately missing distant chunks and wrong blocks.

## Artifact and run evidence

All **16 automated source tests** passed. Two complete local builds produced the
same mod JAR, SHA-256:

```text
1918fc1784952060adfd0919084383944dfb97ca60bca45d5f14069c7516583e
```

ZIP metadata, JSON line endings, and the gzip operating-system marker are fixed
for host independence. Different compression libraries may still produce
different compressed bytes, so Linux builds are checked separately.

[alpha-evidence.json](alpha-evidence.json) records the tested
artifact hash, run IDs, dependencies, located positions, and block comparisons.
Full console logs and worlds remain local in the named `build/smoke/` directories.

All three final server runs passed and exited with code 0. Base and integration
each produced both natural relics with no missing chunks or block mismatches.
The settings run confirmed the active datapack and a complete Obelisk under the
changed profile. The disabled Colossus search returned no result after about
0.063 seconds.

In the settings JSON, `world_blocks.passed` remains `false`: the standalone world
verifier expects both types by default. The server harness instead checks
`expected_natural_structures`, the complete Obelisk, and confirmed deactivation.
Its overall `passed: true` is the relevant result; the absent Colossus is intentional.

For the Obelisk, all **4,403 stored blocks across four chunks** were compared.
For the Colossus, **80,384 fixed block/air cells across 21 chunks** were compared,
including **19,798 explicit air cells**. Its **8,329 natural ground/leaf cells**
are separately recorded as excluded.

Alpha previews under `relics/<relic>/design/generated/alpha/` render actual generated geometry. They are
not Minecraft screenshots and do not show integration into surrounding terrain.

## Observed limits

- Runs cover one seed in three configurations. Visual review across at least
  three seeds and several sites per type remains outstanding.
- The inspected base-test Colossus entrance was reachable over a normal one-block
  step. Other locations may have worse transitions.
- At the time of these runs there had been no visual client playtest, shader/LOD
  acceptance, or test of the entire personal modpack. Later user-provided Alpha 1
  screenshots are discussed in the [Alpha 2 report](ALPHA_2_TEST_REPORT.md).
- Forced loading of large chunk areas sometimes caused delayed server ticks.
  Reliable comparative generation-time, memory, and density measurements were pending.
- The Windows host reported missing English performance-counter names
  (`Perflib 009`) and the associated JNA exception. Reports retain and identify
  those two diagnostic lines; logs are not described as entirely error-free.
  Other errors are not suppressed, and no operating-system repair was made.
- An initial `frequency: 0` deactivation attempt caused a long unsuccessful
  search. The settings tool now removes entries from the affected structure set.
  Existing structures remain, but cannot be located while that type is disabled.

## Repeat the checks

Generator/package tests require Python 3.11 or newer:

```shell
python tools/build.py
python -m unittest discover -s tests -v
```

On the current checkout these commands build and test the current version, not
the historical Alpha 1 artifact. Reproducing the recorded result requires its
matching source revision and dependencies.

The server harness uses the existing Windows cache and downloads no Minecraft
or mod files. Inspect and override paths through `--help`. With your own EULA acceptance:

```shell
python tools/smoke_server.py --accept-eula
python tools/smoke_server.py --accept-eula --integration
python tools/configure.py --density frequent --disable colossus --output build/relics-settings-test.zip
python tools/smoke_server.py --accept-eula --settings-pack build/relics-settings-test.zip --disabled-structure colossus
```

GitHub Actions builds on Linux, runs source tests, and compares consecutive builds.
Minecraft runtime evidence comes from the local runs described above.

The [first GitHub run](https://github.com/Auda29/Relic-Mod/actions/runs/34765846673)
passed the build, all 16 tests, and repeat-build comparison. Its Linux JAR matched
the Windows-tested/installed hash above. Its extra artifact-upload step failed
because the account's Actions storage quota was exhausted. The workflow now
omits automatic artifact uploads and records the package hash in the job summary;
download packages use GitHub Releases. Existing account artifacts were not deleted.
