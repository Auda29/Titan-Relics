# Alpha 4.9 — Minecraft 1.21.1 / Fabric compatibility build

Separate build profile for the existing ten Alpha 4.9 templates (seven relic
designs). It does not replace the primary Minecraft 26.2 build or install into
any launcher profile. **Do not open a 26.2 save in 1.21.1.** Use a new 1.21.1
world or a backed-up save already native to 1.21.1.

## Player requirements

- Minecraft **1.21.1**, Java **21+**, Fabric Loader **0.19.5+**.
- Fabric API **0.116.17+1.21.1**.
- Lithostitched **1.8.0 for Fabric 1.21/1.21.1**, which includes Apollib 1.2.0.
- Only one Relic Mod JAR: `relics-0.1.0-alpha.4.9+mc1.21.1.jar`.

Fabric dependencies and Minecraft classes are not bundled in the Relic JAR.
This is a Fabric build, not Forge/NeoForge. Gameplay remains visual-alpha scope.

## Build

Use **Gradle 9.5+** and a **JDK 21+**. Java bytecode is always compiled with
`--release 21`; Loom **1.17.21** remaps official names to the production
intermediary namespace. The shared 755-assertion Java test main is part of
Gradle's `check` task, not a JUnit test class.

From the repository root:

```shell
python tools/build_mc1211.py --gradle /path/to/gradle --java-home /path/to/jdk
```

Use `--test-java /path/to/java21` to run the assertions on the minimum supported
Java runtime. `--rerun-tasks` forces a fresh compilation/remap. The output is in
`dist/`; this profile's checksum/build-verification files are in
`compat/mc1.21.1/build/release/`, without replacing the 26.2 checksum file.
Dependencies can be downloaded by Gradle; Minecraft's mapping/EULA terms apply.

## Compatibility adaptations

- Keep all **20 raw/natural NBT payloads byte-identical** to Alpha 4.9. Legacy
  DataVersion 3105 remains unchanged; Minecraft migrates on load.
- Use data pack format **48**, older resource-loader module and Java 21 mixins.
- Bridge ResourceLocation, registry lookup, chunk positions/dirty marking,
  height-accessor and write-zone API names.
- Adapt the older abstract StructureProcessor and its registered type.
- **Clip the older full-template finalization list to the placement bounding
  box before support reads and protection-mask writes.** This preserves
  chunk-local behavior and avoids remote chunk loads.
- Keep biome/density/salt, separation, slope/dry-land grid and cave-contact
  contracts unchanged. Player mining/building remains unguarded.
- Use Loom's static mixin remapping, without an absent legacy refmap.

Generated sources/resources are isolated under this profile's ignored `build/`
directory. Main source files, model exports and installed worlds are untouched.

## Runtime validation

`tools/smoke_server.py --minecraft-version 1.21.1` selects the cached 1.21.1
server, matching Fabric dependencies and old gamerule names. Always pass a Java
21 executable with `--java` and explicitly accept the isolated server EULA.
Runtime worlds/logs go under `build/smoke-mc1.21.1/`, separate from 26.2 evidence.
The existing full template/block/protection verification rules still apply.
