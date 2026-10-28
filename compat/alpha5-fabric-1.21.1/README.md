# Alpha 5.0.1 for Minecraft 1.21.1 / Fabric

This separate profile ports the released Alpha 5 gameplay and all saved interior
revisions to Minecraft 1.21.1. The Alpha 4.9 profile and Fabric 26.2 release remain
separate. Player artifact: `relics-0.1.0-alpha.5.0.1+mc1.21.1.jar`.

Requires Minecraft 1.21.1, Java 21+, Fabric Loader 0.19.5+, Fabric API
0.116.17+1.21.1 and Lithostitched 1.8.0 for Fabric 1.21/1.21.1. Dependencies are
installed separately. Use one matching Relic Mod JAR.

## Compatibility behavior

- Distribution, the unique large Colossus, shared expedition-map targets,
  personal Trial/Vault rewards, immediate key consumption, finite Machine Core,
  per-item Salvage Magnet wear, archaeology and Tree effects are retained.
- All 40 templates and five frozen interior revisions are included. Existing
  native 1.21.1 visual-alpha worlds retain legacy generation. Create a new
  1.21.1 world for the complete Alpha 5 selection. Do not downgrade a 26.2 save.
- 1.21.1 has no firefly bushes or copper chests. Its generated templates use
  ferns at the authored plant positions; the same bounded grounding rule
  applies. Reward sites use ordinary chests inside the approved frames. Loot,
  chest placement/facing and clearances are unchanged.
- Integer custom-model data selects charge icons. Native 1.21.1 shaped recipes
  expose ingredients/results to its recipe book. The trim uses its older armor
  atlas paths and material palettes.
- Older furnace/NBT, mob spawning, chunk scheduling and registry APIs are
  adapted explicitly. Vanilla habitat checks and global/local animal caps stay
  active. There is no independent animal spawning timer.

## Build and verification

Use the pinned Gradle 9.5.1 and JDK 25 for the build tooling. Classes target Java
21. Prepare the primary frozen resources first, then build this profile:

```shell
python tools/build.py --java-home /path/to/jdk25
python tools/build_alpha5_port.py --loader fabric --minecraft 1.21.1 --java-home /path/to/jdk25 --gradle /path/to/gradle
```

Generated sources/resources stay under this profile's ignored `build/`. Player
JAR and the target-specific checksum are written to `dist/`. Archive checks
require all six selection manifests, 40 exact template bindings, Java 21,
production mixins and absence of tests/dependency JARs.

The optional `remapPortTestJar` task creates a separate validation mod. It is
never part of the player artifact. Native tests use isolated copies and Java 21:

```shell
python tools/build_alpha5_port.py --java-home /path/to/jdk25 --tasks build remapPortTestJar
python tools/test_alpha5_port_server.py --accept-eula --java /path/to/java21 --artifact dist/relics-0.1.0-alpha.5.0.1+mc1.21.1.jar --test-mod compat/alpha5-fabric-1.21.1/build/libs/relics-alpha5-port-checks+mc1.21.1.jar --suite
python tools/test_alpha5_natural.py --accept-eula --java /path/to/java21 --artifact dist/relics-0.1.0-alpha.5.0.1+mc1.21.1.jar --test-mod compat/alpha5-fabric-1.21.1/build/libs/relics-alpha5-port-checks+mc1.21.1.jar
```

The server harness uses the previously prepared local loader/dependency cache;
it opens no launcher saves and accepts the EULA only with the explicit option.
Server evidence uses simulated players. The earlier real-client acceptance on
26.2 is not reported as a new client acceptance for 1.21.1.
