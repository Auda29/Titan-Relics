# Worldgen der Alpha

Die Alpha verwendet Minecraft 26.2 auf Fabric mit Lithostitched 1.8.0+beta6. Obelisk und Koloss werden als vollständige, starre NBT-Vorlagen platziert. Eigener Java-Code ist dafür nicht nötig. Das bestätigte Profil `E:\Roaming\ModrinthApp\profiles\Relic Test` war bei der Bestandsaufnahme leer. Die Referenz-JARs für die Formatprüfung stammen aus dem vorhandenen TerraVista-Profil. Das ist kein Nachweis, dass dessen gesamtes Modpack bereits mit Relic Mod getestet wurde.

## Aufbau

| Ressource | Aufgabe |
| --- | --- |
| `data/relics/structure/obelisk.nbt` | Vollständiger Obelisk, 25 × 70 × 25 Blöcke |
| `data/relics/structure/colossus.nbt` | Vollständiger Koloss einschließlich Arm, 100 × 66 × 76 Blöcke |
| `worldgen/template_pool/<id>.json` | Genau eine starre Vorlage mit Gewicht 1 |
| `worldgen/structure/<id>.json` | Lithostitched-Standortprüfung um einen Vanilla-Jigsaw-Start |
| `worldgen/structure_set/<id>.json` | Unabhängige, seedabhängige Verteilung |
| `tags/worldgen/biome/has_structure/<id>.json` | Zugelassene Startbiome |
| `tags/worldgen/structure/relics.json` | Gemeinsamer Struktur-Tag für Suche und Datapack-Erweiterungen |

Die Jigsaw-Tiefe `size: 1` platziert das Startelement. Die Vorlagen enthalten keine Jigsaw-Blöcke, daher entstehen keine weiteren Teile. Kopf, Rumpf und Arm können dadurch nicht wegen einer fehlgeschlagenen Jigsaw-Verbindung entfallen. Die Engine speichert einen `PoolElementStructurePiece` mit der vollständigen Bounding Box und verarbeitet die Vorlage in den jeweiligen Generierungschunks. Die vom Generator zusätzlich erzeugten 32er-Kacheln sind bearbeitbare Exporte; die natürliche Generierung referenziert ausschließlich die vollständigen Vorlagen.

Die tatsächlichen Klassen `StructureTemplate.load`, `JigsawStructure` und `JigsawPlacement` aus dem lokal vorhandenen Minecraft-26.2-JAR wurden mit `javap` geprüft. Der NBT-Lader übernimmt die drei Größenwerte ohne die Größenbegrenzung des Structure-Block-Bedienfelds. Lithostitched ersetzt die Vanilla-Jigsaw-Platzierung durch seinen `AlternateJigsawGenerator`. Dieser übernimmt auch bei Tiefe 0 das Startelement, während der unveränderte Vanilla-Code zuvor zurückkehrt. Die Alpha verwendet vorsorglich Tiefe 1; ohne Anschlussblöcke entsteht weiterhin nur die vollständige Vorlage. Jigsaw verwendet die Mitte der gedrehten Bounding Box für die Höhenprojektion. Die tatsächliche Darstellung über Chunk-Grenzen muss zusätzlich im Spiel geprüft werden.

## Bodenhöhe und Drehung

Alpha 2 behält Abmessungen, Biome, Verteilung und Höhenversatz bei. Die neuen Risse und Panzerbrüche sind ausdrücklich gespeicherte Luftzellen. Der Kolosszugang beginnt lokal bei `[40,10,14]` statt `[40,10,0]`. Vor dem kurzen Vorplatz wird kein breiter Luftkorridor mehr ausgeschnitten. Unter den Pflasterresten liegen Erdstützen und eine unregelmäßige Bodenform. Das verbessert den Übergang, ersetzt aber keine Anpassung an jeden einzelnen Geländeblock.

Minecraft wählt eine der vier horizontalen Drehungen. Das gesamte Relikt dreht sich gemeinsam. Es gibt keine Spiegelung und keine zufällige Auswahl einzelner Körperteile.

Der lokale `ground_y` bezeichnet die erste Luftschicht über dem vorgesehenen Boden. Vanilla hat für das Pool-Element einen `groundLevelDelta` von 1. Deshalb gilt für `start_height.absolute` die Formel `1 - ground_y`.

| Relikt | `ground_y` | Starthöhe relativ zur Oberfläche | Y-Korrektur für Geländeprüfung |
| --- | --- | --- | --- |
| Obelisk | 3 | -2 | +2 |
| Koloss | 10 | -9 | +9 |

Damit liegt die Vorlage selbst bei `Oberflächenhöhe - ground_y`. Der Lithostitched-Prüfpunkt wird wieder auf die Oberflächenhöhe verschoben. Wer die Vorlagen oder ihre Bodenhöhe ändert, muss beide Zahlen in der Struktur-JSON und den Manifestvertrag zusammen ändern.

## Standortfilter

Die Filter prüfen ein quadratisches Raster um die Mitte des fertig gedrehten Bauwerks. Die Quadrate decken beide Ausrichtungen der rechteckigen Kolossgrundfläche ab.

| Regel | Obelisk | Koloss |
| --- | --- | --- |
| Rasterradius | 12 Blöcke | 50 Blöcke |
| Rasterabstand | 6 Blöcke | 25 Blöcke |
| Benötigte bestandene Punkte | alle 25 | alle 25 |
| Abweichung vom Oberflächenniveau der Mitte | höchstens 4 Blöcke | höchstens 8 Blöcke |
| Ozeanboden-Höhenkarte | 64 bis 230 | 64 bis 230 |
| Ozean-/Flussbiom am Prüfpunkt | nicht erlaubt | nicht erlaubt |

Vanilla prüft zusätzlich, dass der gesamte Startkörper mit acht Blöcken Abstand zu den vertikalen Dimensionsgrenzen hineinpasst. `terrain_adaptation: none` erzeugt keine rechteckige Geländeaufschüttung. Die unregelmäßige Basis gehört zur Vorlage. Ausgelassene NBT-Positionen lassen vorhandene Blöcke stehen; ausdrücklich gespeicherte Luft räumt Innenraum und Eingang frei. `ignore_waterlogging` übernimmt keine vorhandenen Flüssigkeiten in neue wasserfüllbare Blöcke.

Diese Raster sind eine erste Geländefilterung. Sie garantieren weder einen trockenen Eingang noch Kontakt an jedem Randblock. Kleine Wasserstellen, schmale Geländekanten und Hügel zwischen den Rasterpunkten können unentdeckt bleiben. Die Höhe kommt aus der Terrainberechnung vor späterer Vegetation und fremden Bauwerken. Eine hohe Inlandwasserfläche kann trotz des Meeresspiegelfilters bestehen. Kollisionsprüfungen gegen Dungeons & Taverns und andere Strukturen sind noch nicht implementiert.

## Biome und Terrainmods

Vanilla-Biome sind erforderlich. Ergänzende Terralith- und Biomes-O'-Plenty-Biome verwenden `required: false`, damit das Paket auch ohne diese Mods lädt. Die optionalen IDs wurden gegen Terralith 2.6.4 und Biomes O' Plenty 26.2.0.0.28 geprüft. Tectonic benötigt keine eigene Biome-Zuordnung; die Höhenfilter fragen den aktiven Chunkgenerator ab.

Die Auswahl ist absichtlich explizit. Ein allgemeiner Overworld-Tag würde Kolosse auch in dichten Wäldern und Obelisken in ungeeigneten Klimazonen zulassen. Zusätzliche Biome können über dieselben Tags in einem Datapack ergänzt werden. Für andere Dimensionen und Weltpresets mit abweichendem Meeresspiegel sind die Standardwerte nicht ausgelegt.

## Häufigkeit und Diagnose

| Relikt | `spacing` in Chunks | `separation` in Chunks | Salt |
| --- | --- | --- | --- |
| Obelisk | 64 | 32 | 206091301 |
| Koloss | 80 | 40 | 206091302 |

Diese Werte verteilen Kandidaten, keine garantierten Funde. Biome und Gelände können Kandidaten verwerfen. Es gibt bislang keine eingebaute Zählung der Ablehnungsgründe. Änderungen wirken auf künftig erzeugte Chunks. Bereits erzeugte Relikte bleiben erhalten.

Mit aktivierten Cheats beziehungsweise Server-OP können Strukturen gesucht werden:

```mcfunction
/locate structure relics:obelisk
/locate structure relics:colossus
```

Die automatische Suche kann bei seltenen passenden Biomen oder starkem Relief lange dauern. Gezielte Vorlagenprüfungen in einer eigenen Kreativ-Testwelt umgehen die natürliche Standortentscheidung:

```mcfunction
/place template relics:obelisk ~ ~ ~
/place template relics:colossus ~ ~ ~
```

Der angegebene Ort ist beim Vorlagenbefehl die untere Vorlagenecke. Der Befehl berücksichtigt `ground_y` nicht. Diese Platzierungen sind keine Nachweise natürlicher Generierung. Vier Drehungen, Eingang, Bodenkontakt, Chunkübergänge und erneutes Laden gehören zur visuellen Alpha-Abnahme.

## Formatnachweise und Grenzen der Prüfung

Minecraft 26.2 meldet in seiner `version.json` DataVersion 4903, Datapack-Version 107.1 und Java 25. Lithostitched 1.8.0+beta6 meldet `fabricloader >=0.17` und `minecraft ~26.2`; Apollib 1.1.4 ist im JAR enthalten. Fabric API 0.160.0+26.2 enthält die Ressourcenlader für Mod-Datapacks. Die genaue getestete Installation und tatsächlich ausgeführte Laufzeitprüfungen stehen im separaten Alpha-Testbericht.

Die offiziellen Beschreibungen von [Strukturtypen](https://github.com/Apollounknowndev/lithostitched/wiki/Structure-Types) und [Platzierungsbedingungen](https://github.com/Apollounknowndev/lithostitched/wiki/Placement-Conditions) erklären den delegierenden Wrapper und die Rasterfilter. Die konkreten Feldnamen wurden zusätzlich anhand der Codecs im oben genannten JAR geprüft. Ein erfolgreicher Ressourcen-Ladevorgang allein bestätigt keine optische oder vollständige Modpack-Abnahme.
