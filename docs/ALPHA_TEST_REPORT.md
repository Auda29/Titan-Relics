# Alpha-Testbericht

Stand: 13.09.2026. Ziel ist `0.1.0-alpha.1` für Minecraft 26.2 mit Fabric 0.19.5 und Java 25. Dieser Bericht beschreibt die technische Alpha-Prüfung. Die breitere gestalterische Abnahme aus dem Umsetzungsplan steht noch aus.

## Verfahren

Alle Serverläufe verwendeten eigene, neu angelegte Welten unter `build/smoke/` mit Seed `731204`. Die Minecraft-EULA wurde vom Nutzer ausdrücklich für diese lokalen Tests akzeptiert. Der Server lauschte nur auf `127.0.0.1`, mit Whitelist und ohne RCON. Bestehende Spielwelten wurden nicht verwendet.

Der Test lädt Fabric und die Mod, platziert beide Vorlagen mit `/place template`, sucht natürliche Standorte mit `/locate`, lädt die umliegenden Chunks vollständig und speichert die Welt. Danach liest ein eigener Prüfer die tatsächlich gespeicherten Anvil-Regionen. Er vergleicht Blockzustände, Drehung, Abmessungen und explizite Luftzellen mit den NBT-Dateien aus genau der beim Start verwendeten Mod-JAR.

Eine erfolgreiche Standortsuche allein zählt nicht als bestandene Generierung. Fehlende Chunks, unvollständige Strukturen und abweichende feste Blöcke lassen den Test fehlschlagen. Gras, Erde und Azaleenblätter sind beim Koloss ausdrücklich aus dem strikten Vergleich ausgenommen, weil spätere Gelände- und Vegetationsschritte sie verändern können.

## Testumfang

| Umgebung | Zusätzliche Mods | Prüfung |
| --- | --- | --- |
| Basis | Fabric API 0.160.0+26.2, Lithostitched 1.8.0+beta6 | Beide Vorlagen und beide natürlichen Relikte |
| Worldgen-Integration | Tectonic 3.0.26, Terralith 2.6.4, Biomes O' Plenty 26.2.0.0.28, Dungeons & Taverns 5.3.2, GlitchCore, TerraBlender | Beide Vorlagen und beide natürlichen Relikte |
| Einstellungen | Basis plus generiertes Datapack: `frequent`, Koloss deaktiviert | Aktives Datapack, natürlicher Obelisk, erfolglose Koloss-Suche und weiterhin nutzbare manuelle Vorlagen |

Die Integrationsumgebung verwendet Standardkonfigurationen. Die acht äußeren Abhängigkeits-JARs sind mit Versionen und Prüfsummen in [TARGET_ENVIRONMENT.md](TARGET_ENVIRONMENT.md) erfasst. Die neun zusätzlichen Dungeons-and-Taverns-Overhauls und persönlichen Einstellungen aus TerraVista gehören nicht zu diesem Test.

Die automatischen Quellcodeprüfungen decken NBT-Roundtrip, deterministische Exporte, Materialzustände, Luft und ausgelassene Positionen, Rekonstruktion aus Teilvorlagen, den begehbaren Weg zum Maschinenraum, Einstellungen, Paketmetadaten und den Weltleser ab. Der Weltleser wird auch gegen absichtlich fehlende entfernte Chunks und falsche Blöcke geprüft.

## Artefakt und Laufnachweise

Die 16 automatischen Quellcodeprüfungen wurden erfolgreich ausgeführt. Zwei vollständige lokale Builds erzeugten dieselbe Mod-JAR mit SHA-256 `1918fc1784952060adfd0919084383944dfb97ca60bca45d5f14069c7516583e`. ZIP-Metadaten, JSON-Zeilenenden und der Gzip-Betriebssystemmarker sind festgelegt, damit sie nicht vom jeweiligen Rechner abhängen. Unterschiedliche Kompressionsbibliotheken können dennoch abweichende komprimierte Bytes erzeugen; der Linux-Build wird deshalb separat geprüft.

Die abgeschlossenen Laufnachweise werden in [testing/alpha-evidence.json](testing/alpha-evidence.json) zusammengefasst. Diese Datei enthält den SHA-256 des getesteten Artefakts, die konkreten Laufkennungen, Abhängigkeiten, gefundenen Positionen und Blockvergleiche. Die vollständigen Konsolenprotokolle und Testwelten liegen lokal in den angegebenen `build/smoke/`-Verzeichnissen und werden nicht ins Repository aufgenommen.

Alle drei abschließenden Serverläufe haben bestanden und mit Exit-Code 0 beendet. Basis und Integration lieferten jeweils beide natürlichen Relikte ohne fehlende Chunks oder Blockabweichungen. Im Einstellungstest wurde das aktive Datapack bestätigt; der Obelisk entstand vollständig mit dem geänderten Verteilungsprofil. Die Suche nach dem deaktivierten Koloss endete nach rund 0,063 Sekunden ohne Fund.

Im JSON des Einstellungstests bleibt das allgemeine Feld `world_blocks.passed` auf `false`, weil der separat nutzbare Weltprüfer standardmäßig beide Relikttypen verlangt. Der Server-Harness bewertet diesen Test anhand von `expected_natural_structures`, der vollständigen Obelisk-Prüfung und der nachgewiesenen Deaktivierung. Deshalb ist sein übergeordnetes `passed: true` maßgeblich; der fehlende Koloss ist in diesem Test beabsichtigt.

Beim Obelisken werden alle 4.403 gespeicherten Blöcke über vier Chunks verglichen. Beim Koloss sind es 80.384 feste Block- und Luftzellen über 21 Chunks, darunter 19.798 explizite Luftzellen. Seine 8.329 natürlichen Boden- und Blattzellen sind gesondert als ausgelassen ausgewiesen.

Die Geometrievorschauen unter `design/generated/` werden aus den echten generierten Blöcken gerendert. Sie sind keine Minecraft-Screenshots und zeigen noch keine Einbettung in das umgebende Gelände.

## Festgestellte Grenzen

- Die Läufe prüfen einen Seed in drei Konfigurationen. Die im Umsetzungsplan vorgesehene Sichtprüfung über mindestens drei Seeds und mehrere Funde je Typ ist noch offen.
- Im Basistest ist der Geländezugang zum Koloss an der untersuchten Stelle mit einem normalen Ein-Block-Absatz erreichbar. Andere Standorte können ungünstigere Übergänge haben.
- Es gab noch keinen visuellen Client-Spieltest, keine Shader-/LOD-Abnahme und keinen Test des gesamten persönlichen Modpacks.
- Beim erzwungenen Laden großer Chunkbereiche meldet der Server zeitweise verzögerte Ticks. Eine belastbare Vergleichsmessung für Generierungszeit, Speicherbedarf und Verteilung wurde noch nicht durchgeführt.
- Der Windows-Host meldet fehlende englische Leistungszählernamen (`Perflib 009`) mit der zugehörigen JNA-Ausnahme. Die Berichte bewahren diese zwei konkreten Diagnosezeilen auf und kennzeichnen das Log als nicht vollständig fehlerfrei. Andere Fehler werden dadurch nicht ausgeblendet. Am Betriebssystem wurde nichts repariert.
- Ein erster Deaktivierungsversuch mit `frequency: 0` führte zu einer langen erfolglosen Struktur-Suche. Das Einstellungswerkzeug entfernt nun die Einträge des betreffenden Struktursets. Vorhandene Bauwerke bleiben bestehen; während der Deaktivierung ist auch ihre Suche ausgesetzt.

## Tests wiederholen

Die Generator- und Pakettests benötigen nur Python 3.11 oder neuer:

```shell
python tools/build.py
python -m unittest discover -s tests -v
```

Der lokale Server-Harness ist für den vorhandenen Windows-Cache ausgelegt und lädt keine Minecraft- oder Mod-Dateien herunter. Seine Pfade lassen sich über `--help` nachvollziehen und anpassen. Mit eigener EULA-Zustimmung:

```shell
python tools/smoke_server.py --accept-eula
python tools/smoke_server.py --accept-eula --integration
python tools/configure.py --density frequent --disable colossus --output build/relics-settings-test.zip
python tools/smoke_server.py --accept-eula --settings-pack build/relics-settings-test.zip --disabled-structure colossus
```

Die GitHub-Actions-Prüfung baut die Mod unter Linux, führt die Quellcodeprüfungen aus und vergleicht zwei aufeinanderfolgende Builds. Die Minecraft-Laufzeitnachweise stammen aus den beschriebenen lokalen Tests.

Der [erste GitHub-Lauf](https://github.com/Auda29/Relic-Mod/actions/runs/34765846673) bestand Build, alle 16 Tests und den Vergleich der Wiederholungs-Builds. Seine Linux-JAR hat dieselbe oben angegebene Prüfsumme wie die auf Windows getestete und installierte Datei. Sein zusätzlicher Artefakt-Upload scheiterte am ausgeschöpften Actions-Speicherkontingent des Kontos. Der Workflow verzichtet deshalb auf automatische Artefakt-Uploads und schreibt die Paketprüfsumme in die Job-Zusammenfassung. Downloadpakete werden über GitHub-Releases bereitgestellt. Bestehende Konto-Artefakte wurden nicht gelöscht.
