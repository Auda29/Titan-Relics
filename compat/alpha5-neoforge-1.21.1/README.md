# Alpha 5.0.3 for Minecraft 1.21.1 / NeoForge

Native NeoForge port of the full Alpha 5 gameplay and approved interior selection.
Player JAR: `relics-0.1.0-alpha.5.0.3+mc1.21.1-neoforge.jar`.

Requires Minecraft 1.21.1, Java 21+, NeoForge 21.1.256+ and Lithostitched 1.8.0
for NeoForge 1.21/1.21.1. Install dependencies separately. Fabric API is not used.
Use one Relic JAR for the selected loader and game version.

## Native implementation

Items are constructed during the open native item registration event. Component
types and recipe serializers bind on their corresponding registry events.
Native attachments persist chunk protection, interior certificates, player
receipts and reward IDs. Absent reads do not create data. Protection retains
the native `neoforge:attachments/relics:placed_cells/sections` format.

NeoForge server/player/chunk events drive the shared gameplay. Reward completion
uses confirmed death drops, including deaths whose ordinary loot was cancelled.
Natural animal extras use NeoForge's finalization hook; native cancellation
creates no entity and charges no cap. Furnace processing calls the actual patched
NeoForge methods, including their furnace argument.

The 1.21.1 compatibility changes match the [Fabric profile](../alpha5-fabric-1.21.1/README.md):
ferns, ordinary reward chests in the approved frames, integer charge icons,
native shaped recipe-book data and legacy armor-trim atlas paths/palettes.

## Build and tests

After preparing the primary frozen resources, use JDK 25 and Gradle 9.5.1:

```shell
python tools/build_alpha5_port.py --loader neoforge --minecraft 1.21.1 --java-home /path/to/jdk25 --gradle /path/to/gradle
```

The build targets Java 21 and checks native metadata, all 40 template bindings,
all saved interior revisions, absence of Fabric references/dependencies/test
classes, and every item-model/trim asset reference against the game client JAR.
Player artifact and target-specific checksum go to `dist/`.

The separate `build/validation/relics-alpha5-port-checks+mc1.21.1-neoforge.jar`
belongs only in the isolated tests. Test packages are separate from production
packages, as required by the native module loader. The server harness reads the
prepared official NeoForge installation under `build/neoforge/runtime-1.21.1/`.

```shell
python tools/test_alpha5_port_server.py --loader neoforge --minecraft 1.21.1 --accept-eula --java /path/to/java21 --artifact dist/relics-0.1.0-alpha.5.0.3+mc1.21.1-neoforge.jar --test-mod compat/alpha5-neoforge-1.21.1/build/validation/relics-alpha5-port-checks+mc1.21.1-neoforge.jar --suite
python tools/test_alpha5_natural.py --loader neoforge --minecraft 1.21.1 --accept-eula --java /path/to/java21 --artifact dist/relics-0.1.0-alpha.5.0.3+mc1.21.1-neoforge.jar --test-mod compat/alpha5-neoforge-1.21.1/build/validation/relics-alpha5-port-checks+mc1.21.1-neoforge.jar
```

Use a new native 1.21.1 world for all Alpha 5 gameplay. Existing visual worlds
retain legacy selection. Switching loaders or downgrading a 26.2 save is not a
provided migration. Launcher profiles and their saves are not changed by builds
or tests. Native server tests use simulated players and do not claim a new
graphical two-client or modpack/shader acceptance.

Alpha 5.0.3 fixes maintenance recipe network serialization. Updating the same
game/loader from Alpha 5.0.1 retains existing worlds and items. Tests now encode
and decode real recipe synchronization packets; see the
[recipe-codec report](../../docs/testing/ALPHA_5_0_2_RECIPE_CODEC_20261028.md).
