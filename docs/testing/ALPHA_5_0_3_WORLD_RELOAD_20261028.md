# Alpha 5.0.3: world reload and modpack fingerprints

Status: published for Fabric and NeoForge, Minecraft 1.21.1 and 26.2.
[Release](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.5.0.3) and [download verification](alpha5-0-3-release-20261028-evidence.json).

## Failure and cause

TerraVista Living World stopped while reopening `Living World Relics` with
Fabric 1.21.1 Alpha 5.0.2. The server exception was raised by Relic's frozen
planning fingerprint check, before the player could join. The journal checksum,
world seed, border and saved interior revision were valid.

The old implementation hashed the JSON text emitted by the world-generation
codecs. JSON object iteration order is not stable across Java processes. Captures
from isolated copies of the full modpack were equal as parsed JSON but had
different SHA-256 hashes. In one server/client comparison, all 204 different
object orders were biome `spawners` maps. Arrays and actual values were equal.
This demonstrates a false mismatch in the old algorithm. It does not prove that
the original, hash-only journal had identical biome data when first created:
the old journal does not store the original signature, and its original hash
could not be reconstructed from the captured signatures.

## Change

- Recursively sort JSON object keys before hashing. Preserve array order and all
  values, including generator settings, biomes, tags, structure sets, templates,
  processors, pools and frozen interior contracts.
- Persist `fingerprintFormat: 1`. Missing format remains legacy format 0;
  unknown future formats are rejected without resetting a save.
- Migrate an exactly matching legacy hash automatically. Create and fsync an
  exact backup of the old planning journal before atomically writing format 1.
- An unmatched legacy hash remains blocked by default. Recovery requires an
  explicit JVM property bound to **both** the saved old hash and the current
  canonical hash. It applies only to legacy format 0, never to format 1.
- Seed, enabled families, border, supported contracts, journal checksum, frozen
  state and the exact saved unique Colossus terrain/transform are still checked
  before any migration. The property cannot waive these checks.
- Preserve the entire plan. Migration does not delete the journal, reroll a
  destination, replace the policy, move structures, refill loot or reset maps.

## Existing Living World: tested recovery

Only isolated copies under `build/reload-fingerprint-20261028/` were written.
Both original Modrinth profiles and their saves remained read-only.

Saved legacy fingerprint:
`3d2a76168db958d997dcb6fccaca4c0b2633fbdd2afbc58a716eaec2023271c8`

Current canonical fingerprint for the copied Fabric 1.21.1 setup:
`65ea46667546c63df4145e5a606838b4fdacafbe6fed2efb47ab0515cff83830`

After making a complete save backup, installing the matching 5.0.3 player JAR
and verifying that the original setup is intended, this exact one-time Java
argument permits the checked transition:

```text
-Drelics.distribution.legacyFingerprintMigration=3d2a76168db958d997dcb6fccaca4c0b2633fbdd2afbc58a716eaec2023271c8:65ea46667546c63df4145e5a606838b4fdacafbe6fed2efb47ab0515cff83830
```

Remove the argument after the successful load/save. It is not a general
compatibility switch. Do not substitute a new current hash to approve an
uninvestigated generator or datapack change. A complete world backup is still
needed: the mod's `.pre-canonical-<old-hash>.bak` covers the planning journal only.
Do not downgrade a migrated world to 5.0.2; it does not understand canonical hashes.

The copied world loaded through player login and stopped with all dimensions
saved. The exact original journal was backed up. Comparing the payloads showed
only `fingerprint` and `fingerprintFormat` changed. The unique destination,
planning progress, policy, seed, border, interiors and enabled families remained
equal. A subsequent real-client launch with the 5.0.3 player JAR, no recovery
argument and a new Java process also joined and saved successfully.

The test client was a real, hidden Minecraft client with the copied full modpack,
shaders and resource packs, using a public offline test identity. No launcher
account credentials were read or used. The test-only mixin writes the captured
signature and stops the isolated client after 100 in-world ticks. Other test
entrypoints were excluded from this full-modpack probe to avoid synthetic
fixture initialization in an existing user save. Existing unrelated modpack
warnings were still present; this is a targeted reload test, not blanket
certification of every mod interaction.

## Verification

- Production Java planner/journal: 198,942 assertions; executor/dependencies:
  1,008 assertions; versioned location search: 755,716 assertions.
- Regression cases: recursively reordered object keys; preserved array order;
  changed values/keys rejected; exact legacy transition; unmatched legacy
  rejection; approval tied to both hashes; backup preservation/collision;
  migrated state reload; missing and future fingerprint formats.
- All four player artifacts pass version, loader, class-target, frozen-template
  and asset-reference checks. No diagnostic classes are included in player JARs.
- All four native loader suites pass two server launches, recipe packet roundtrips,
  core, Trial/Vault rewards, magnet budgets and the Tree aura; natural animal
  cap checks also pass. The server suites use simulated players.
- Twelve focused Python storage/compression, 1.21.1 adaptation and asset tests pass.
  The unrelated full model-asset suite was stopped; no full-suite pass is claimed.
- The recovery candidate and final Fabric 1.21.1 player artifact have identical
  ZIP entries except `fabric.mod.json` (the version bump). Every class and
  gameplay/worldgen resource is byte-identical. The subsequent full-modpack
  client restart used the final 5.0.3 artifact.
- Native loader suites and client evidence are recorded in the
  [accompanying JSON](alpha5-0-3-world-reload-20261028-evidence.json).

Rebuild with the pinned JDK/Gradle and existing dependency cache:

```shell
python tools/test_distribution.py --java-home /path/to/jdk25
python -m unittest discover -s tests -p "test_alpha5_*.py" -q
python -m unittest discover -s tests -p "test_mc1211_compatibility.py" -q
python -m unittest discover -s tests -p "test_port_assets.py" -q
python tools/build.py --skip-generation --java-home /path/to/jdk25
python tools/build_alpha5_port.py --loader fabric --minecraft 1.21.1 --java-home /path/to/jdk25 --tasks build remapPortTestJar relicClasspath
python tools/build_alpha5_port.py --loader neoforge --minecraft 1.21.1 --java-home /path/to/jdk25 --tasks build relicClasspath
python tools/build_alpha5_port.py --loader neoforge --minecraft 26.2 --java-home /path/to/jdk25 --tasks build relicClasspath
```

Never run the probe or recovery against an original profile without explicit
permission. Work on complete copies; keep the original journal and world backup.
