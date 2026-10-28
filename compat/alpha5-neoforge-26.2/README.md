# Alpha 5.0.1 for Minecraft 26.2 / NeoForge

Native NeoForge port of the approved Alpha 5 gameplay and interior selection.
Player JAR: `relics-0.1.0-alpha.5.0.1+mc26.2-neoforge.jar`.

Requires Minecraft 26.2, Java 25+, NeoForge 26.2.0.88+ and Lithostitched 1.8.0
for NeoForge 26.2. Install dependencies separately. Use one Relic JAR for the
selected loader and game version. Fabric API is not required.

## Implementation

The [shared native adapters](../alpha5-neoforge-common/README.md) register items
during the native item registry event and use native lifecycle, player, chunk,
interaction and confirmed-death events. Cancelled protected block breaks notify
the client through the 26.2 break event. Natural animal extras honor NeoForge
spawn cancellation and share the ordinary spawn's population state.

All 40 original 26.2 templates remain unchanged. Copper chests, firefly bushes,
modern item definitions and native armor-trim resources are retained. There are
no 1.21.1 block substitutions. Native MapCodec attachments persist protection,
interior certificates, reward identities and personal delivery receipts.

## Build and tests

After preparing the primary frozen resources, use JDK 25 and Gradle 9.5.1:

```shell
python tools/build_alpha5_port.py --loader neoforge --minecraft 26.2 --java-home /path/to/jdk25 --gradle /path/to/gradle
```

The build checks Java 25 classes, native metadata, all template/manifest
bindings, absence of Fabric references and validation classes, and model/texture
references against the actual game client JAR. Output and target-specific
checksum are written to `dist/`.

The separate `build/validation/relics-alpha5-port-checks+mc26.2-neoforge.jar` is
only for isolated server checks. The harness uses the official prepared native
installation under `build/neoforge/runtime-26.2/` and records its library hashes.
On Windows it replaces only the loader logger's two extended throwable
renderers with ordinary full stack traces; levels, appenders and errors remain.

```shell
python tools/test_alpha5_port_server.py --loader neoforge --minecraft 26.2 --accept-eula --java /path/to/java25 --artifact dist/relics-0.1.0-alpha.5.0.1+mc26.2-neoforge.jar --test-mod compat/alpha5-neoforge-26.2/build/validation/relics-alpha5-port-checks+mc26.2-neoforge.jar --suite
python tools/test_alpha5_natural.py --loader neoforge --minecraft 26.2 --accept-eula --java /path/to/java25 --artifact dist/relics-0.1.0-alpha.5.0.1+mc26.2-neoforge.jar --test-mod compat/alpha5-neoforge-26.2/build/validation/relics-alpha5-port-checks+mc26.2-neoforge.jar
```

Use a fresh native world for the full Alpha 5 selection. Cross-loader save
conversion is not provided. Builds/tests do not change launcher profiles or
player saves. Server checks use simulated players and do not constitute a new
graphical two-client, shader/LOD or arbitrary modpack acceptance.
