# Relic Mod

Seltene, monumentale Entdeckungen für Minecraft: ein Wüstenobelisk und ein überwachsener, begehbarer Maschinenkoloss mit abgetrenntem Arm.

**Aktueller Stand: 0.1.0-alpha.1 für Minecraft 26.2 / Fabric.** Die Bauwerke werden vollständig durch die Python-Generatoren dieses Repositorys erzeugt. Handarbeit in Minecraft ist für den Build nicht nötig. Diese Alpha erprobt Form, Export und natürliche Platzierung; sie ist noch keine gestalterisch und über viele Seeds abgenommene Version 0.1.

## Inhalt der Alpha

| Relikt | Gesamtabmessungen einschließlich Basis | Gestaltung |
| --- | --- | --- |
| Obelisk | 25 × 70 × 25 Blöcke | Schlanker, oben flacher Schaft, steinerne Basis und kleiner Rastplatz |
| Koloss | 100 × 66 × 76 Blöcke | Helm mit Visier, breite Schultern, geöffneter Brustring, Innenraum, Bewuchs und abgetrennter Arm |

Beide Relikte bestehen aus Vanilla-Blöcken und generieren in passenden neuen Oberwelt-Chunks. Ihre feste Grundform wird gemeinsam gedreht. Es gibt derzeit eine vorbereitete Variante je Typ. Optionale Biome aus Terralith und Biomes O' Plenty sind zugeordnet; diese Mods sind keine Pflichtabhängigkeiten.

## Installation

| Voraussetzung | Alpha-Testversion |
| --- | --- |
| Minecraft Java Edition | 26.2 |
| Java | 25 |
| Fabric Loader | 0.19.5 |
| Fabric API | 0.160.0+26.2 |
| Lithostitched | 1.8.0+beta6 für Fabric 26.2 |

Die genaue lokal vorgefundene Umgebung steht in [TARGET_ENVIRONMENT.md](docs/TARGET_ENVIRONMENT.md). Die ausgeführten Prüfungen und ihre Grenzen stehen im [Alpha-Testbericht](docs/ALPHA_TEST_REPORT.md).

1. Fabric für Minecraft 26.2 verwenden.
2. `relics-0.1.0-alpha.1+mc26.2.jar`, Fabric API und Lithostitched in den `mods`-Ordner legen.
3. Eine neue Testwelt mit aktivierter Strukturgenerierung anlegen. Die Alpha fügt keine Relikte in bereits erzeugte Chunks ein.

Die Projektseiten von [Lithostitched](https://modrinth.com/mod/lithostitched) und [Fabric API](https://modrinth.com/mod/fabric-api) bieten die Abhängigkeiten. Diese JARs werden nicht in unserem Release mitverteilt.

Mit Cheats beziehungsweise Server-OP lassen sich natürliche Standorte suchen:

```mcfunction
/locate structure relics:obelisk
/locate structure relics:colossus
```

Die Suche kann wegen der seltenen geeigneten Standorte dauern. Eine Position aus `/locate` allein bestätigt noch nicht, dass alle Chunks des Bauwerks erzeugt wurden. Zum Prüfen der Blockvorlagen können sie in einer separaten Kreativ-Testwelt auch mit `/place template relics:obelisk` beziehungsweise `/place template relics:colossus` gesetzt werden. Diese Befehle umgehen die Standortprüfung. Die angegebene Position ist die untere Ecke der Vorlage, nicht die Höhe ihrer begehbaren Oberfläche.

## Ohne Handarbeit bauen und ändern

Python 3.11 oder neuer genügt für Erzeugung, Tests und Modverpackung. Das Projekt enthält derzeit keinen eigenen Java-Code; deshalb sind Gradle, Loom und eine Java-Kompilierung für diesen Build nicht erforderlich.

```shell
python tools/build.py
python -m unittest discover -s tests -v
```

Unter Windows kann alternativ `./build.ps1` verwendet werden. Das Skript sucht Python im PATH und anschließend den vorhandenen Codex-Python-Runtimepfad. Es installiert nichts.

Das Ergebnis liegt unter `dist/`, zusammen mit `SHA256SUMS.txt`. Der Build erzeugt die NBT-Dateien aus den Quelldaten neu und verwendet feste Archivzeitstempel. Git versioniert Generatoren und Worldgen-Daten; generierte Bauwerke sind reproduzierbare Build-Ausgaben.

Die Funktionen `obelisk()` und `colossus()` in [tools/relic_assets.py](tools/relic_assets.py) bestimmen Geometrie, Materialien, Räume und Beschädigung. Änderungen an Breite, Höhe oder Bodenhöhe müssen mit den Geländefiltern in den Worldgen-Daten abgestimmt werden. Der Manifestexport dokumentiert Abmessungen, Bodenhöhe und Prüfsummen.

Der Export erzeugt ganze Vorlagen und zusätzlich starre Teilvorlagen. Die Mod verwendet ausschließlich die ganzen Vorlagen; der Arm kann nicht durch eine zufällig fehlgeschlagene Verbindung entfallen.

### Vorschauen

Der optionale Renderer benötigt Pillow und zeichnet die tatsächlich erzeugten Blöcke mit vereinfachten Farben:

```shell
python -m pip install Pillow
python tools/render_preview.py
```

Die Bilder entstehen in `design/generated/`. Es handelt sich um Geometrievorschauen vor der Einbettung in die Welt, nicht um Minecraft-Screenshots. Der Renderer wird für den Mod-Build nicht benötigt.

## Häufigkeit und einzelne Relikte einstellen

Ein zusätzliches Datapack kann die Verteilung für eine bestimmte Welt überschreiben. Beispiel für häufigere Funde ohne Kolosse:

```shell
python tools/configure.py --density frequent --disable colossus
```

Verfügbar sind `rare`, `normal` und `frequent`. `--disable` kann für `obelisk` und `colossus` wiederholt werden. Die Ausgabe `dist/relics-settings.zip` gehört in den Datapack-Ordner der gewünschten Welt und muss höhere Priorität als die Moddaten erhalten. Einstellungen bei Weltstart laden beziehungsweise den Server neu starten; bloßes `/reload` wird für diese Worldgen-Änderungen nicht als ausreichend vorausgesetzt.

Bereits erzeugte Relikte bleiben erhalten. Solange ein Typ deaktiviert ist, findet `/locate` auch seine bestehenden Standorte nicht; nach dem erneuten Aktivieren sind Suche und neue Generierung wieder möglich. Die Profile ändern die Verteilung von Kandidaten; Gelände und Biome bestimmen, wie viele davon tatsächlich bebaut werden. Es gibt noch kein Einstellungsmenü und keine eingebaute Statistik zu verworfenen Standorten.

## Bekannte Alpha-Grenzen

- Terrainprüfungen erfolgen über ein Raster. Kleine Wasserstellen und Geländekanten können zwischen den Messpunkten liegen.
- Der Innenraum ist innerhalb der Vorlage begehbar. Der Übergang vom äußeren Gelände zum Eingang kann einen Absatz bilden.
- Gegen Überschneidungen mit Dungeons & Taverns oder anderen Strukturen gibt es noch keine genaue Kollisionsprüfung.
- Die Relikte haben feste Formen. Seedabhängige Generatorvarianten sind ein Entwicklungswerkzeug und werden noch nicht pro Fund gewählt.
- Es gibt keine neue Beute, Bewegungsmechanik, Quests oder eigenen Soundeffekte.
- Ruinenturm, Titanenschädel und Weltenbaum sind noch nicht implementiert.

## Entwicklung und Nachweise

- [Technischer Umsetzungsplan](UMSETZUNGSPLAN.md)
- [Lore-Bibel](LORE-BIBLE.md)
- [Worldgen-Aufbau und Formatprüfung](docs/WORLDGEN.md)
- [Alpha-Testbericht](docs/ALPHA_TEST_REPORT.md)
- [Changelog](CHANGELOG.md)
- [Ursprünglicher Konzept- und Entwicklungsplan](Minecraft-Relikte-Modplan.md)

Eine offene Lizenz wurde noch nicht festgelegt. Die Modmetadaten kennzeichnen die Dateien daher als `All-Rights-Reserved`. Fremde Referenzbilder und Mod-JARs gehören nicht zum veröffentlichten Paket.
