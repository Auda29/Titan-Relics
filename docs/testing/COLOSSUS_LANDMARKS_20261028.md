# Koloss V7: Integration und Terrainprüfung

Stand 28. Oktober 2026, Minecraft 26.2 / Fabric, `0.1.0-alpha.5.0-dev`.
Die neue Modellrevision aus dem
[Modellbericht](../project/COLOSSUS_LANDMARKS_20261028.md) ist in die natürliche
Generierung eingebunden. Die Bilder zeigen Exportgeometrie mit Prüflicht und
Platzhaltern. Die gestalterische Endabnahme und das tatsächliche Minecraft-Licht
bleiben beim Nutzer.

## Verhalten

Der Arm enthält einen Maschinenstand aus Rückwand und Pfeilern um die einzige
Magnettruhe. Der neue Freiraum reicht über den Truhendeckel und schließt die
bisherige Lücke zwischen Armweg und Truhe. Der Trial Spawner sitzt in einem
offenen Wachrahmen in der Raummitte. Der Golem erhält daneben eine eigene freie
Spawnfläche. Der Vault sitzt in der Konsole der mittleren Crewstation und ist
von der Raumseite erreichbar. Die früheren Spawner-/Vault-Platzhalter sind
entfernt. Beute, persönliche Ansprüche und Mechanik bleiben gleich.

Der Vier-Welten-Test fand zusätzlich Kohleerz im begehbaren Armweg. Die bisherige
Freiräumung entfernte den Stein, ließ die enthaltenen Erze aber stehen. Der
V7-Koloss räumt in seinen begrenzten, quellfreien Bereichen deshalb zusätzlich
Overworld-Erze und weitere natürliche Bodenblöcke. Authored Strukturblöcke,
andere geschützte Strukturen und Flüssigkeiten werden dabei nicht entfernt.
Die Freiräume erhalten die bestehende Schutzmaske gegen spätere Dekoration.

## Gespeicherte Welten

Neue Welten wählen `interiors-20261028-v2` mit V7. Gespeicherte V6-Welten behalten
`interiors-20261027-v1`, ihre bisherigen Marker, Vorlagen und Fingerprints.
Visual-Alpha-Welten bleiben bei `legacy`. Der Build liefert beide Gameplay-
Manifeste und beide Koloss-Vorlagen mit. Unvollständig generierte V6-Teile werden
weiter mit ihrer gespeicherten Revision verarbeitet. Es gibt keine automatische
nachträgliche Umgestaltung, Verschiebung von Vault-Ansprüchen oder Auffüllung
geplünderter Truhen.

Für die neuen Aufbauten ist eine neue Testwelt nötig. Ein JAR-Update allein
ersetzt den bereits besuchten Koloss in einer bestehenden Welt nicht.

## Prüfungen und Artefakt

Die vier Modelltests prüfen Exportgleichheit, begrenzte Geometrieänderungen,
Wege, Golemraum, Deckelfreiraum und rechnerische Markerrotationen. Der neue
natürliche Servertest verwendet vier Weltseeds mit allen vier echten
Strukturdrehungen und einen V6-Updatefall. Er prüft vollständige Modellzellen,
Freiräume, Schutzmasken, Marker und deren Richtungen sowie Speichern, Neustart
und ausbleibende Loot-Auffüllung. Ein Survival-Testspieler mit Paketempfänger
durchläuft am natürlichen Koloss Golem, Schlüssel-Drop, sofortige Vault-Zahlung
und den separat ausgeworfenen Kern. Das ersetzt keinen grafischen Client.

Alle vier Drehungen bestehen. Zusammen mit dem vollständigen V6-Updatefall
stimmen 1.319.801 feste Modellzellen. Pro V7-Koloss wurden 16.055 freie und
geschützte Zellen geprüft, ohne blockierte oder ungeschützte Zellen. Auch ein
zweiter Updatefall mit zunächst nur dem zentralen V6-Chunk besteht: Die übrigen
Chunks werden auf der neuen JAR mit der alten Vorlage fertiggestellt; der
gespeicherte Fingerprint und die Marker bleiben gleich.

Die vorhandene Präsentationsprüfung läuft zusätzlich mit beiden Magnethänden,
Inventar-Inaktivität und einem 64er-Stack. Dieser Stack verbraucht genau einen
Punkt, entsprechend einer erfolgreichen Aufnahme.

Testbuild: `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`.

SHA-256: `783188f8d07f3b1cef04190cc20cae96257ec1c77a33a65e0326db93bf7b51ec`.

Der Build enthält 32 vollständige Strukturvorlagen und keine Testklassen. Eine
zweite Paketierung ist bytegleich. Die endgültigen Ergebnisse, Weltseeds,
Fingerprint-Vergleiche und Belegpfade werden im
[maschinenlesbaren Prüfbericht](colossus-landmarks-20261028-evidence.json)
festgehalten. Der erste Serverlauf mit den stehen gebliebenen Erzen bleibt als
fehlgeschlagener Zwischenstand erhalten.

Die abschließende Python-Suite besteht mit 133 Tests. Ausgenommen sind die
separaten lokalen NeoForge-Porttests, deren Alpha-4.9-Versionsschutz bereits
vor diesem Auftrag den Alpha-5-Stand ablehnte. Außerdem bestehen erneut 663
Gameplay-Assertions, 52 statische Mixin-Verträge, 755 Platzierungsprüfungen,
1.008 Executor-, 755.716 Such- und 198.924 synthetische Verteilungsprüfungen.
Die ursprünglichen Modell- und NeoForge-Dateien bleiben erhalten; die übrigen
vier Gameplay-Modelle und deren Marker sind unverändert.

## Reproduktion

```powershell
$jdk = 'build/toolchains/zulu25.36.205-ca-jdk25.0.4.1-win_x64'
python tools/build.py --java-home $jdk
python tools/test_gameplay.py --java-home $jdk
python tools/test_distribution.py --java-home $jdk
build/distribution-venv/Scripts/python.exe -m unittest discover -s tests -p test_colossus_landmarks.py
build/distribution-venv/Scripts/python.exe -m unittest discover -s tests -p test_natural_interiors.py
python tools/test_colossus_landmarks_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar --previous-artifact build/colossus-landmarks-20261028/previous-caffeb.jar
python tools/test_colossus_landmarks_server.py --accept-eula --upgrade-only --partial-upgrade --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar --previous-artifact build/colossus-landmarks-20261028/previous-caffeb.jar
python tools/test_gameplay_presentation_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar
```

Das vorherige JAR für den Updatefall hat SHA-256
`caffeb247121ee1ea501ecf68eaa1c2af07801420c7dbeb5cae636f9d041acfe`.
Alle Serverwelten liegen unter `build/`. Es wurde kein Nutzerprofil installiert,
keine Nutzerwelt verändert und kein Commit oder Push für diese Revision erstellt.
