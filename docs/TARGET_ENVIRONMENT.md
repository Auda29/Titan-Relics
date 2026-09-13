# Zielumgebung der Alpha

Stand: 13.09.2026. Dieser Nachweis ergänzt [UMSETZUNGSPLAN.md](../UMSETZUNGSPLAN.md). Die Bestandserhebung erfasst den Ausgangszustand vor der Alpha-Installation und erfolgte ausschließlich lesend. Die anschließende Installation ist am Ende dieses Dokuments gesondert erfasst.

## Bestätigtes Testprofil

Der Nutzer hat das Modrinth-Profil `E:\Roaming\ModrinthApp\profiles\Relic Test` als Ziel ausgewählt. Die Instanzmetadaten des Launchers bestätigen für genau dieses Profil:

| Eigenschaft | Nachweis |
| --- | --- |
| Minecraft | `26.2` |
| Loader | Fabric `0.19.5` |
| Installationsstatus im Launcher | `installed` |
| Profilverzeichnis | Vorhanden |
| Installierte Mods | Keine JAR-Dateien in `mods/` |
| Konfigurationen und Datapacks | Die vorhandenen Verzeichnisse sind leer |
| Spielstände und Logs | Keine Spielstanddateien und kein `logs/latest.log` vorhanden |
| Grafikprofil und JVM-Speichergrenze | Noch nicht aus einem Lauf dieses Profils verifiziert |

Die einzige vorhandene Datei im Profil ist eine leere `command_history.txt`. Das bestätigt einen leeren Ausgangsstand, aber keinen erfolgreichen Spielstart. Insbesondere sind Fabric API, Lithostitched, Terralith, Tectonic, Biomes O' Plenty und Dungeons and Taverns noch nicht in diesem Profil installiert.

Die Versionsprüfung erfolgte über eine lesende SQLite-Verbindung mit `mode=ro` zur Launcher-Datenbank. Ausgegeben wurden ausschließlich Profilname, Spielversion, Loader und Loaderversion der ausgewählten Instanz. Die Datenbank selbst und Kontodaten gehören nicht ins Repository.

## Java und Minecraft-Datenformat

Beide folgenden ausführbaren Dateien wurden mit `-version` geprüft:

| Zweck | Lokaler Pfad | Ergebnis |
| --- | --- | --- |
| JDK für Builds | `C:\Users\wecke\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe` | Temurin `25.0.4.1+1-LTS` |
| Java-Compiler | `C:\Users\wecke\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\javac.exe` | `javac 25.0.4.1` |
| Modrinth-Laufzeit verfügbar | `E:\Roaming\ModrinthApp\meta\java_versions\zulu25.36.205-ca-jre25.0.4.1-win_x64\bin\java.exe` | Zulu `25.0.4.1+1-LTS` |

Die verfügbare Modrinth-Laufzeit ist noch nicht als tatsächlich gestartete Laufzeit von Relic Test belegt.

Aus der lokalen Minecraft-Client-JAR `meta/versions/26.2-0.19.5/26.2-0.19.5.jar` wurden `version.json` und die zugehörige Launcher-Versionsbeschreibung geprüft:

| Feld | Wert |
| --- | --- |
| Spiel-ID | `26.2` |
| Erforderliche Java-Hauptversion | `25` |
| NBT-Datenversion / `world_version` | `4903` |
| Datapack-Format | Hauptversion `107`, Nebenversion `1` |
| Ressourcenpaket-Format | Hauptversion `88`, Nebenversion `0` |
| Fabric-Startklasse | `net.fabricmc.loader.impl.launch.knot.KnotClient` |

SHA-256 der geprüften Cache-Artefakte:

| Datei | SHA-256 |
| --- | --- |
| `meta/versions/26.2-0.19.5/26.2-0.19.5.jar` | `40896ee9f1e2bec3c934daac7e93d41e9e3d9c2f8ae0ca366d52ffbfd1afa290` |
| `meta/libraries/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar` | `93044e4dd46de5d8136701292f05e868da096d2c9fddb4793e4fdbcc63efc695` |

Diese Pfade sind relativ zu `E:\Roaming\ModrinthApp`. Fremde JAR-Dateien werden nicht ins Git-Repository aufgenommen.

## Verfügbare Worldgen-Integration für einen getrennten Test

Im bestehenden Profil `E:\Roaming\ModrinthApp\profiles\TerraVista\mods` liegen passende Bibliotheken und Worldgen-Mods. Die folgende Auswahl ist eine vorgeschlagene Integrationsumgebung für einen getrennten Testserver. Sie ist keine Beschreibung des installierten Zustands von Relic Test und keine Zusage einer bereits bestandenen Kompatibilitätsprüfung.

Die Versionen und Abhängigkeiten stammen aus `fabric.mod.json` der jeweiligen lokalen JAR-Datei. Prüfsummen beziehen sich auf diese konkreten Dateien.

| Datei | Mod-ID und Version | SHA-256 |
| --- | --- | --- |
| `fabric-api-0.160.0+26.2.jar` | `fabric-api` / `0.160.0+26.2` | `5f3dff88e1661166e222213302b25ace6c36dc3683804cbd4b5acf93138ea05e` |
| `lithostitched-1.8.0+beta6-fabric-26.2.jar` | `lithostitched` / `1.8.0+beta6` | `5743a7e11af1491aab6f4760c7cdce7284e2f0a4a89ffacd4ef43fd46e5e6d43` |
| `tectonic-3.0.26-fabric-26.2.jar` | `tectonic` / `3.0.26` | `4fa2b27fdccb60da9942af70b2d157feea4609049ad80950ec4c33db36502168` |
| `Terralith_26.2_v2.6.4.jar` | `terralith` / `2.6.4` | `d867c6f348e869c19e8a5979e9dd2c46ed058c1edb47090f6863c32cce484917` |
| `BiomesOPlenty-fabric-26.2-26.2.0.0.28.jar` | `biomesoplenty` / `26.2.0.0.28` | `e3a5571eb77225e800f8fc4334d452904705e945c26767bfb091f42889ae14b4` |
| `dungeons-and-taverns-5.3.2.jar` | `mr_dungeons_andtaverns` / `5.3.2` | `7a1abeacfd6b973d9753928889d765e4002a086f4cb23756d8586e7d347d4bba` |
| `GlitchCore-fabric-26.2-26.2.0.0.0.jar` | `glitchcore` / `26.2.0.0.0` | `f6c31bd291d1d19322dd0a7ec344df2c88e2d516d1985f09ffe50ef33a34afdc` |
| `TerraBlender-fabric-26.2-26.2.0.0.2.jar` | `terrablender` / `26.2.0.0.2` | `e4c54e7490cf6716ccc287f5ef674562666a13c6a4afabdc344d5cb62e9cb584` |

### Abhängigkeiten dieser Auswahl

- Fabric API verlangt Java `>=25`, Fabric Loader `>=0.18.4` und Minecraft `~26.2-`.
- Lithostitched verlangt Fabric Loader `>=0.17` und Minecraft `~26.2`. Es enthält Apollib `1.1.4` als eingebettete JAR. Apollib verlangt Fabric Loader `>=0.19` und enthält wiederum `json5-java`.
- Tectonic verlangt Lithostitched und enthält ebenfalls Apollib `1.1.4`.
- Terralith verlangt Fabric Loader `>=0.19` und Lithostitched `>=1.7.12`.
- Biomes O' Plenty verlangt Fabric API, GlitchCore `>=26.2.0.0.0` und TerraBlender `>=26.2.0.0.1`.
- GlitchCore und TerraBlender verlangen Fabric API. Ihre weiteren Bibliotheken sind eingebettet.
- Dungeons and Taverns verlangt `fabric-resource-loader-v0`. Die ausgewählte Fabric-API-JAR enthält dieses Modul.

Damit ist die in den Metadaten deklarierte Abhängigkeitenauswahl mit acht äußeren JAR-Dateien abgedeckt. Fabric Loader `0.19.5` und Java `25` erfüllen die genannten Mindestversionen. Erst ein Start bestätigt, dass der Loader die vollständige Kombination akzeptiert.

TerraVista enthält zusätzlich neun eigenständige Dungeons-and-Taverns-Overhauls für Vanilla-Strukturen. Sie gehören nicht zur obigen Basisauswahl. Ein erfolgreicher Test dieser acht JAR-Dateien belegt deshalb keine Verträglichkeit mit dem vollständigen TerraVista-Modpack.

TerraVista besitzt außerdem eigene Konfigurationen für Biomes O' Plenty, Lithostitched, Tectonic, TerraBlender und Terralith. Sie wurden für diesen Nachweis nicht übernommen oder als Alpha-Vorgabe festgelegt. Ein Test mit Standardkonfigurationen muss im Prüfbericht entsprechend bezeichnet werden.

## Noch durch Ausführung zu belegen

Ein Prüfbericht muss den Start des Alpha-Artefakts, natürliche Strukturplätze und tatsächliche Erreichbarkeit der Innenräume separat dokumentieren. Ebenfalls offen bleiben Clientverbindung, Darstellung im Spiel, Shader und LOD-Kompatibilität sowie die im Umsetzungsplan geforderten Messungen über mehrere Seeds. Der vorliegende Nachweis bestätigt Versionen und vorhandene Dateien, nicht diese Laufzeiteigenschaften.

## Installierter Alpha-Stand

Am 13.09.2026 wurden nach bestandenem isoliertem Basistest genau drei JAR-Dateien in den zuvor leeren Ordner `Relic Test/mods` kopiert:

- `relics-0.1.0-alpha.1+mc26.2.jar`, SHA-256 `1918fc1784952060adfd0919084383944dfb97ca60bca45d5f14069c7516583e`
- `fabric-api-0.160.0+26.2.jar`, Prüfsumme wie oben
- `lithostitched-1.8.0+beta6-fabric-26.2.jar`, Prüfsumme wie oben

Alle drei installierten Prüfsummen stimmen mit den geprüften Quelldateien überein. Die zwei Abhängigkeiten wurden aus dem vorhandenen Cacheprofil kopiert; TerraVista wurde nicht verändert. Es wurden keine Spielwelten angelegt oder verändert und keine zusätzlichen Worldgen-Mods in Relic Test installiert. Das Profil wurde noch nicht als Client gestartet. Die abgeschlossenen getrennten Serverprüfungen stehen im [Alpha-Testbericht](ALPHA_TEST_REPORT.md).
