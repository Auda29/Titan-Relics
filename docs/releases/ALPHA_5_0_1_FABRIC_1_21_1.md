# Relic Mod Alpha 5.0.1 for Fabric 1.21.1

Compatibility patch for the first Alpha 5.0 Fabric 1.21.1 port. It removes the
unavailable copper-armor palette from the Monolith trim atlas and adds a client
asset-reference gate to the build. Derived template gzip headers are fixed
across build platforms. Gameplay, reward rules and the approved interiors stay
the same.

Install `relics-0.1.0-alpha.5.0.1+mc1.21.1.jar` with Minecraft 1.21.1, Java 21+,
Fabric Loader 0.19.5+, Fabric API 0.116.17+1.21.1 and Lithostitched 1.8.0 for
Fabric 1.21/1.21.1. Replace the previous Relic JAR.

Includes the full Alpha 5 distribution, encounters, personal physical rewards,
cores, magnets, archaeology and Tree features. 1.21.1 uses ferns and ordinary
reward chests inside the approved structures. New native worlds get the full
selection; existing visual worlds retain legacy generation. Do not downgrade
a 26.2 save.

Validation includes actual Java 21 server functions/restarts, natural placement
and non-refill, exact templates/protection, 37 resolved client asset references,
native trim palette colors and reproducible builds. Simulated-player automation
is separate from graphical client acceptance.

[Build and reproduction](../../compat/alpha5-fabric-1.21.1/README.md).
[Final verification](../testing/ALPHA_5_0_1_1_21_1_20261028.md).
