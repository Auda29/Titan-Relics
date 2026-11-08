# Additional Java release targets

Prepared for a subsequent release, not yet published. The existing `v1.0.0-beta.1` release and its four platform receipts remain unchanged.

The additional profiles target Minecraft Java 1.21.11 and 26.3, each on Fabric and NeoForge. Dependencies and Mojang download hashes are pinned in `compat/additional-targets.json`.

- 1.21.11 uses Java 21, Fabric API 0.141.6, NeoForge 21.11.48 and Lithostitched 1.7.2.
- 26.3 uses Java 25, Fabric API 0.165.2, NeoForge 26.3.0.101 and Lithostitched 2.0.6.
- Existing 1.21.1 and 26.2 dependency pins are retained.
- The forty frozen structure templates are preserved byte for byte. Generated resource JSON and runtime classes have version-specific adapters.

## Validation

All four production profiles compile, pass metadata/resource checks, and produce identical SHA-256 values across two builds. Each profile passed:

- Two production-server gameplay runs, including a restart, recipe and recipe-book packet round trips, furnace/core operations, finite rewards, magnet behavior, tree aura and natural animal spawn accounting. Native NeoForge event cancellation is included.
- Seven rejected world-load cases: changed fingerprint, seed, plan border, enabled families, unfinished plan, checksum and the actual saved world-border file. Every rejection preserved all world files.
- A restored world loading successfully with its journal byte identical.
- A naturally generated ruined tower retaining a valid structure start across a restart.

The [machine-readable evidence](JAVA_1_21_11_26_3_EVIDENCE.json) binds these results to all four JAR hashes. Test-seed destination coordinates are represented by hashes. The full Python suite passed 191 tests; two supplemental tests cover the console error gate. Release/platform and palette checks and actionlint also pass. The existing Fabric 1.21.1 profile compiles with Gradle 9.6.0.

All four native client variants passed menu smoke checks in isolated Xvfb displays with a dummy offline identity. They exercise title/defaults routing, the create-world tab, world settings and biome settings. Audio is muted and sound assets are omitted from this UI-only check. Client gameplay, shaders, other modpacks and the Survival run remain outside this validation.

Do not upload the local experimental JARs bearing the existing Beta 1 version. The next release tag supplies a shared final version for all eight artifacts.

## Loader and game adaptations

1.21.11 retains recipe displays and packet tests while adapting the crafting serializer and registry-provider arguments. Its abstract structure processor clips template processing to the current chunk. Lithostitched 1.7.2 preflight runs the pinned server-start hooks with the frozen stem registry and saved seed through scoped adapters; normal startup consumes that preparation once.

26.3 adapts the ore predicate and placement base class, biome resolvers and density samplers, recipe registry codec, block-state JSON, item-drop prediction, and trim texture palette metadata. Lithostitched 2.0.6 reads a server-level local it never uses in `BiomeInjectorManager.applyBiomeInjectors`; the scoped preflight adapter avoids that unused lookup before a server exists. The dependency is pinned and hash checked. This adapter must be reviewed before any Lithostitched update.

## Release pipeline

`tools/check_additional_ports.py` builds each new target twice, compares SHA-256 manifests, then runs isolated server gameplay, restart, frozen-settings, world-load rejection/recovery and natural-structure checks. Both branch CI and release CI invoke it. Tag publication remains downstream of successful validation.

Historical Alpha releases and `1.0.0-beta.1` retain four files. Subsequent 1.x releases require eight complete files. The platform uploader resolves each new target's exact dependencies and Java version, and preserves the historical four-file receipts. No tag, release, platform visibility or moderation state was changed for this work.

## Reproduce

Use Gradle 9.6.0, a Java 25 home and a Java 21 home:

```sh
python tools/check_additional_ports.py \
  --java-home /path/to/jdk25 \
  --java21-home /path/to/jdk21 \
  --gradle gradle
```

Optional native client/menu checks use `tools/test_additional_port_client.py` with
`--loader fabric` or `--loader neoforge`, `--minecraft`, `--java-home`, `--java`
and `--gradle`. They require `xvfb-run` and download hash-checked official client
libraries and visual assets. No launcher accounts or existing worlds are used.

The command accepts Minecraft's EULA for its isolated test servers. It downloads hash-checked dependencies into `build/`, binds only to loopback, and never opens launcher saves.

## Test harness details

The asynchronous destination search must resolve before taking the restart baseline. A Plains creature pack can consist entirely of ineligible horses, so animal checks sample independent populations while preserving the real production cap and hook. Minecraft 26.3's population fixture uses a test-only constructor bridge rather than counting unrelated live-world entities.

The console gate retains remote Yggdrasil public-key fetch failures as external service errors while continuing to reject loader, registry and worldgen errors. Online authentication remains enabled. The NeoForge logging adapter keeps all levels and full traces while avoiding the extended Log4j renderer's Netty native-class initialization problem.

## API references

- [Fabric 1.21.11 migration notes](https://fabricmc.net/2025/12/05/12111.html)
- [Fabric 26.3 migration notes](https://fabricmc.net/2026/09/15/263.html)
- [Fabric 26.1 Loom transition](https://www.fabricmc.net/2026/03/14/261.html)
