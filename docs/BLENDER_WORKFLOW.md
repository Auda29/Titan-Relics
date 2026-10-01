# Relikte aus Blender nach Minecraft

Stand: 01.10.2026

## Entscheidung und aktueller Stand

Neue Reliktmodelle werden in Blender gestaltet, mit **VoxelVision** in
Minecraft-Blöcke übersetzt und als Sponge-`.schem` exportiert. Unser Konverter
erzeugt daraus Java-Structure-Templates (`.nbt`) ohne manuellen WorldEdit-Import
oder Structure-Block-Export:

**Blender → VoxelVision → `.schem` → `tools/schem_to_nbt.py` → `.nbt` → Worldgen**

Die Formatkonvertierung ist implementiert. Die automatische Einbindung dieser
Quellen in den Mod-Build steht noch aus. Die bestehende Alpha wird weiterhin durch
`tools/relic_assets.py` erzeugt. Ein echter VoxelVision-Export und dessen Darstellung
im Spiel wurden mit dem neuen Konverter noch nicht geprüft.

## 1. Modell und Blockexport vorbereiten

1. Pro Relikt die bearbeitbare `.blend`-Quelle behalten. Blender- und
   VoxelVision-Version sowie die Export-Einstellungen festhalten.
2. Den Maßstab in Minecraft-Blöcken früh festlegen. Silhouette, Wandstärken,
   Eingänge und begehbare Innenräume bereits im voxelisierten Ergebnis prüfen.
3. Eine Palette passend zur Zielversion wählen; zunächst möglichst Vanilla-Blöcke.
   Automatische Farbübersetzung ersetzt keine gestalterische Materialprüfung.
4. Zusammengehörige Teile wie Koloss und Arm im selben lokalen Koordinatensystem
   exportieren. Ursprung, Vorderseite und geplantes Bodenniveau dokumentieren.
5. Als Sponge-`.schem` Version 2 oder 3 exportieren. Nicht das alte `.schematic`
   oder Bedrocks `.mcstructure` verwenden.

Empfohlene Ablage für neue eigene Quellen:

- `design/blender/koloss.blend`: bearbeitbares Modell.
- `structures-src/imports/koloss.schem`: Blockexport.
- `design/imported/koloss.nbt`: zunächst separat gehaltenes Konvertierungsergebnis.

Diese Pfade sind eine Konvention, keine automatisch angelegten Projektordner.

## 2. Ohne Minecraft konvertieren

Python 3.11 oder neuer genügt; zusätzliche Python-Pakete sind nicht nötig.
Vom Repository-Hauptverzeichnis aus:

```shell
python tools/schem_to_nbt.py structures-src/imports/koloss.schem design/imported/koloss.nbt --air omit
```

Die Ausgabe enthält die vollständige Vorlage und `koloss.manifest.json` mit
Abmessungen, Blockanzahl, Datenversion, Quelloffset und Luftregel. Erneute Aufrufe
überschreiben die gleichnamigen Ausgaben. Blockzustände, einschließlich Ausrichtung
von Treppen und Stufen, werden übernommen. Die Konvertierung rotiert das Modell nicht.

### Luftregel bewusst wählen

| Option / Block | Wirkung |
| --- | --- |
| `--air omit` | Luftpositionen werden ausgelassen; vorhandenes Gelände bleibt dort stehen, auch in Innenräumen |
| `--air keep` | Alle Luftpositionen werden übernommen; auch Außenluft im Exportquader kann Gelände entfernen |
| `minecraft:structure_void` | Wird immer ausgelassen und verändert das Gelände nicht |

`--air` muss ausdrücklich angegeben werden. Der Konverter erkennt nicht automatisch,
welche Luft zu einem Innenraum gehört. Für begehbare, teilweise vergrabene Relikte
muss die gewünschte Trennung von freizuräumenden Räumen und unverändertem Gelände
in den Quelldaten oder einer späteren Verarbeitung bewusst umgesetzt werden.

### Große Vorlagen zusätzlich aufteilen

```shell
python tools/schem_to_nbt.py structures-src/imports/koloss.schem design/imported/koloss.nbt --air omit --tile-size 32
```

Zusätzlich entstehen `design/imported/koloss_tiles/tile_*.nbt` und Einträge im
Manifest mit relativen Ursprüngen und Teilgrößen. Zulässig sind Kantenlängen von
1 bis 128 Blöcken. Leere Teilbereiche werden nicht exportiert.

Die ganze Vorlage bleibt ebenfalls erhalten. Das Manifest ist **keine**
Minecraft-Platzierungsdefinition: Worldgen muss Teilvorlagen bei Bedarf separat
zusammenführen und gemeinsam drehen. Die aktuelle Alpha nutzt ganze Vorlagen,
nicht die Teilvorlagen.

## 3. Format- und Versionsgrenzen

- Unterstützt werden Sponge-Schematic-Versionen 2 und 3, gzip-komprimiert oder
  unkomprimiert. `.schem` und Java-Structure-`.nbt` sind verschiedene NBT-Schemata;
  ein bloßes Umbenennen funktioniert nicht.
- Koordinaten werden auf lokale Minecraft-XYZ-Positionen abgebildet. Der
  Schematic-Offset wird im Manifest dokumentiert, nicht auf die Blöcke addiert.
- `DataVersion` wird aus der Quelle übernommen. Es gibt keine Versionsmigration
  und keine Prüfung der Blocknamen gegen eine Minecraft-Registry. Die aktuelle
  Mod-Zielversion Minecraft 26.2 verwendet DataVersion 4903.
- Entities und Block-Entities, etwa Inventare in Truhen, werden ausdrücklich
  abgelehnt. Die erste Pipeline ist für statische Blockbauwerke gedacht.
- Sehr große Exporte benötigen entsprechend Speicher; der Konverter lädt die
  Quelle und Blockpositionen in den Arbeitsspeicher.

## 4. Worldgen und Mod-Build integrieren

**Noch ausstehender Integrationsschritt:** Der aktuelle Aufruf
`python tools/build.py` erzeugt `obelisk.nbt` und `colossus.nbt` erneut aus den
Python-Generatoren. Importierte Dateien nicht einfach unter diesen Namen in die
Ressourcen kopieren und danach einen normalen Build erwarten: Sie würden ersetzt.

Vor dem Wechsel einer Struktur auf Blender-Quellen muss der Build die `.schem`
automatisch konvertieren und die geprüfte Vorlage als Ressource übernehmen.
Außerdem müssen folgende Worldgen-Verträge zur neuen Geometrie passen:

- Struktur-ID und Template-Pool-Referenz;
- Abmessungen und gesamte Prüfgrundfläche einschließlich Arm und Trümmern;
- Bodenhöhe und daraus abgeleitete Höhenversätze;
- Biome, Höhen- und Hangprüfungen sowie Häufigkeit;
- gegebenenfalls feste Teilpositionen und gemeinsame Drehung.

Die bestehenden Regeln stehen in [WORLDGEN.md](WORLDGEN.md). Eine `.nbt` allein
definiert noch keine natürliche Generierung oder Gelände-Einbettung.

## 5. Prüfen

```shell
python tools/build.py
python -m unittest discover -s tests -v
```

Der Build erzeugt die bestehenden Alpha-Ressourcen, die einige Tests voraussetzen;
er testet noch keine Blender-Integration. Zum Stand dieser Anleitung bestanden
alle 22 Tests, einschließlich vier neuer Konvertertests mit synthetischen Quellen.
Sie prüfen beide Schematic-Versionen, Blockzustände, Koordinaten, Luftregeln,
mehrbyteige Palette-Indizes, fehlerhafte Eingaben, deterministische Ausgabe und
die Rekonstruktion aus Teilvorlagen.

Für den ersten echten VoxelVision-Export zuerst einen kleinen Obelisken durch die
Kette schicken. Im Spiel Größe, Palette, vier Drehungen, Luftverhalten und
Bodenkontakt prüfen. Danach den Koloss über Chunk-Grenzen und nach erneutem Laden
prüfen. Manuelle Testplatzierung ist eine Abnahmehilfe, kein erforderlicher
Konvertierungsschritt; natürliche Generierung bleibt ein eigener Test.
