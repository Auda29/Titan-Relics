# Alpha 5.0.2 recipe codec verification, 28 October 2026

[Exact-artifact evidence](alpha5-0-2-recipe-codec-20261028-evidence.json) covers
Fabric 1.21.1, NeoForge 1.21.1 and NeoForge 26.2.

## Defect and correction

The published Fabric 1.21.1 Alpha 5.0.1 JAR reproduces the reported exception
with only the normal required dependencies and the new validation mod. Its
maintenance serializer uses `StreamCodec.unit(new MaintenanceRecipe(core))`.
That codec checks equality with one instance, but JSON loading supplies another
instance and the recipe class does not define value equality. The recipe packet
therefore fails to encode even without an additional modpack conflict.

The three patch targets map a constant Boolean variant to/from independent
recipe instances. The serializer ID continues to determine the variant, with
no additional payload bytes. Encoding another instance of the same variant
works; passing the opposite variant still fails. JSON recipes, patterns, charge
rules and crafting/component preservation are unchanged.

The NeoForge 26.2 adaptation is scoped to that generated target. The existing
Fabric 26.2 Alpha 5.0 release and primary sources are preserved.

## Tests

`RecipeNetworkChecks` runs on the actual production JAR under each native loader:

- Loaded recipes, a separately JSON-decoded instance and a fresh instance encode
  and decode through `Recipe.STREAM_CODEC`. Holder IDs round-trip independently.
- Decoded recipes retain their type, variant and recipe-book shape, reject full
  relics, restore depleted relics to the correct budget, preserve custom names and
  leave crafting input untouched. Opposite serializer variants are rejected.
- The complete 1.21.1 `ClientboundUpdateRecipesPacket`, containing all loaded
  recipes, encodes and decodes through its actual game codec. Both maintenance
  entries remain present exactly once and retain their crafting behavior.
- Modern 26.2 synchronizes properties and displays separately. Its native update
  packet and recipe-book add packet both round-trip. The two maintenance display
  IDs, flags and shaped dimensions survive.

Fabric 1.21.1 and NeoForge 1.21.1 each pass 104 network assertions per start;
NeoForge 26.2 passes 98. All checks run before and after a real server restart.
Buffers are fully consumed and released. These tests exercise actual encoded
packet bytes rather than merely recording `Connection.send` calls.

Each final target also passes the existing functional/restart suite: core fuel
processing and menu state, recipe/smithing behavior, native Trial/Vault states
and physical personal rewards, immediate key payment and saved outstanding
drops, per-item held-magnet accounting, 51 Tree-aura cases and shared population
caps. Native spawn cancellation is verified on both NeoForge targets.

## Scope and provenance

Archive comparison against each corresponding published Alpha 5.0.1 JAR finds
exactly two changed entries: the maintenance serializer class and loader version
metadata. Every other class and resource, all 40 templates and all six frozen
selection manifests are byte-identical. Earlier natural-generation evidence
remains applicable to those identical files; complete natural-world cases are
not repeated for this codec-only patch.

Updating a same-loader, same-game Alpha 5.0.1 world does not change the saved
generation fingerprint, structure selection or item components. No new world
is required for this patch. Cross-loader conversion is not provided.

Builds are verified from a separate staged Git export. Its tracked resources
retain their exact Git bytes; the verified primary bundle supplies only missing
generated files. Rebuilt JARs must equal the tested release candidates before
publication. Player archives exclude the validation mod/classes.

Both TerraVista profiles, their configuration and saves remain untouched.
The tests do not constitute graphical-client or full modpack acceptance.

All three staged-export player JARs and their validation JARs are byte-identical
to the tested candidates. Eight focused Python resource, native storage,
compression and documentation checks pass.
