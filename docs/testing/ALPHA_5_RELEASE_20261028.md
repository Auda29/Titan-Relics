# Alpha 5.0 release verification, 28 October 2026

Artifact: `relics-0.1.0-alpha.5.0+mc26.2.jar`. SHA256: `f588041e4ce79df9ee898e18c844f999c2ff4915cc0684e689df06e07147d7da`.

[Machine-readable evidence](alpha5-release-20261028-evidence.json) ·
[Release notes](../releases/ALPHA_5_0.md).

## Source and package

The separate Git export builds exactly the same JAR as the working checkout.
1,598 bound model/handoff records match byte-for-byte, including the original
line endings of hash-bound reports and scripts. Windows provenance paths are
resolved portably without changing any frozen manifest strings. The artifact
contains 40 templates and no test classes or third-party mod JARs.

The separate NeoForge port, its evidence and changes to six shared reader/target
files are excluded. NeoForge-only sections in shared README files remain in the
local working copy and are omitted from the release Git tree.

## Automated checks

- 677 headless gameplay assertions and 63 static mixin target contracts.
- 764 Java world-generation assertions.
- 1,008 executor/dependency, 755,716 search and 198,924 synthetic distribution assertions.
- The clean export completed 156 Python tests. Its five initial failures were
  subcases of the documentation-link test referring to the deliberately excluded
  NeoForge port. The export sections were corrected; all four documentation tests
  and the new full-handoff test passed on recheck. No runtime test failed.
- GitHub CI runs the complete final 157-test suite and the native animal test
  again on the release commit; publication requires a successful build.

The final JAR passed native natural placement for the Colossi, Obelisk, Tower,
Tree and corrected Skull 2, with full footprint/template, marker/loot, protected
clearance and restart checks. A V4 world retained its fingerprint, revision,
unique target and old template after upgrade. The Tower also loaded and restarted
on Peaceful without hostile creation or replenishing completed actions.

The two simulated-player fixture passed native Trial/Vault phases and event
packets, physical personal rewards, immediate key payment, restart/recovery,
both magnet hands, per-item and partial pickup accounting. The Tree aura passed
51 boundary/eligibility/effect cases before and after restart: 80-block sphere,
Regeneration II plus Resistance II, 6,000 ticks, normal merging and departure tail.

## Final Tree animal feature

The production natural-spawn hook observed eight ordinary and four extra animals
in an isolated Plains/grass fixture. Full global and local caps blocked extras;
each extra was charged to the same SpawnState. No standalone spawn occurred.
The same native test passed from the clean Git export. This measures bounded
attempts under normal rules, not a guaranteed herd or a claim of doubled density.

## User acceptance and limits

The user confirmed visual/functional playtesting and two real Minecraft clients
including reconnect without problems. This is user testimony, separate from
simulated-player automation. The animal hook was added afterwards and has the
native checks above; it does not introduce custom entities or client assets.

Long-term Survival balance and arbitrary modpack/shader/LOD combinations remain
alpha work. Normal restart checks do not prove atomic saves across every file
under arbitrary hard process termination. Full Alpha 5 selection needs a new
world; existing worlds keep their frozen structure revision.

Release target: [v0.1.0-alpha.5.0](https://github.com/Auda29/Relic-Mod/releases/tag/v0.1.0-alpha.5.0),
as a prerelease in the existing private repository.
