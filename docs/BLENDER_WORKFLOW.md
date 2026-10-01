# Relikte aus Blender nach Minecraft

Stand: 01.10.2026

## Entscheidung und aktueller Stand

**Blender → OBJ → ObjToSchematic 1.0 → Sponge-`.schem` → Java-`.nbt` → Worldgen**

Wir verwenden die kostenlose, quelloffene **ObjToSchematic-Version 1.0** lokal.
VoxelVision ist nicht mehr Voraussetzung. Die aktuelle Webversion 2.0 ist ein
anderes Produkt; deren Pro-Funktionen werden für diese Pipeline nicht benötigt.

Der erste Koloss wurde mit **Blender 5.2.2**, Node **24.16.0** und dem offenen
ObjToSchematic-Commit `b611b52c7a87cad99127908598bab019fe9e7c3f` durch die Kette
geschickt: **99 × 66 × 71 Blöcke, 26.169 gesetzte Blöcke, neun Blocktypen**.
Die Vorschauen werden aus der konvertierten NBT-Datei mit Minecraft-Texturen
gerendert. Sie sind kein Ingame-Nachweis.

Die automatische Übernahme in den Mod-Build und die Abnahme in Minecraft stehen
noch aus. Die Alpha-Ressourcen werden weiterhin durch `tools/relic_assets.py`
erzeugt. Der neue Koloss ist eine erste Form- und Materialstudie.

**Alternative nach Sichtung der Originalreferenz:** [Colossus v2](COLOSSUS_V2.md)
nutzt einen bronzenen Kuppelhelm, Atemschläuche, breitere Panzerformen und einen
angenommenen Maßstab von 160 Blöcken Höhe. Die Erweiterung **[Colossus v3](COLOSSUS_V3.md)**
mit unterirdischem Bauch und abgerissener Hüfte hat insgesamt 209 Blöcke Höhe.
Configs: `design/colossus-v2.json` und `design/colossus-v3.json`;
Ausgaben: `design/generated/colossus-v2/` und `design/generated/colossus-v3/`.

**Obelisk nach Originalreferenz:** [Obelisk v2](OBELISK_V2.md) übersetzt Josh Whites
*Painted Desert* in eine schlanke, flach gekrönte Stele mit warmen mineralischen
Flächen. Die 23 × 209 × 19 Blöcke große Vorlage besitzt einen massiven Steinkern
und einen 32 Blöcke tiefen Fuß. Config: `design/obelisk-v2.json`.

## 1. Lokale Werkzeuge einrichten

Benötigt werden Blender, Git, Node.js mit npm und Python 3.11 oder neuer.
Pillow wird ausschließlich für das Übersichtsbild benötigt (`python -m pip install Pillow`).
Alle Befehle vom Repository-Hauptverzeichnis aus; Beispiele für PowerShell:

```powershell
git clone --branch ots-1.0 https://github.com/LucasDower/ObjToSchematic.git .work/ObjToSchematic
git -C .work/ObjToSchematic checkout b611b52c7a87cad99127908598bab019fe9e7c3f
npm.cmd --prefix .work/ObjToSchematic install --no-audit --no-fund
```

Upstream: [ObjToSchematic](https://github.com/LucasDower/ObjToSchematic),
Lizenz BSD-3-Clause. Der Quellcode bleibt in `.work/`, einschließlich seiner
Lizenzdatei. Er und seine Abhängigkeiten werden nicht in die Mod-JAR gepackt.
Der Legacy-Zweig erhält keine regulären Updates. Sein Lockfile benötigt unter
dem getesteten npm eine Ergänzung für `fsevents`; deshalb hier `install` statt
`ci`. Die geprüfte Upstream-Revision ist im Projekt-Config festgehalten.

Der mitgelieferte Headless-Einstieg wartet den inzwischen asynchronen Import
nicht ab und schreibt das Exportergebnis nicht auf die Platte. Unser Adapter
`tools/obj_to_schem.cjs` verwendet die vorhandenen Import-, Voxel- und
Exportklassen direkt und ergänzt Node-Loader für Webpack-Ressourcen. Änderungen
am Upstream-Quellcode sind dafür nicht nötig.

## 2. Koloss erzeugen, konvertieren und ansehen

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_blender_colossus.py
node tools/obj_to_schem.cjs design/colossus-ots.json
python tools/schem_to_nbt.py design/generated/ots/colossus.schem design/generated/ots/colossus.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py
python tools/inspect_ots_result.py
```

Ausgaben unter `design/generated/ots/`:

| Datei | Zweck |
| --- | --- |
| `colossus-source.blend` | Bearbeitbares Blender-Modell aus dem Generator |
| `colossus.obj`, `colossus.mtl` | Triangulierte Geometrie und Blender-Materialexport |
| `colossus.schem` | Tatsächlicher ObjToSchematic-Export, Sponge v2 |
| `colossus.ots.json` | Upstream-Revision, Einstellungen, Blockzahlen und SHA-256 |
| `colossus.nbt`, `colossus.manifest.json` | Ganze Java-Vorlage und Konvertierungsdaten |
| `colossus_tiles/` | 19 starre Teilvorlagen, maximal 32 Blöcke pro Kante |
| `colossus-blocks.blend` | Inspizierbares NBT-Oberflächenmesh mit gepacktem Texturatlas |
| `01-blender-source.png` | Ursprungsmodell mit einfachen Materialfarben |
| `02-blocks-front.png` bis `04-blocks-back.png` | Drei Ansichten der tatsächlichen NBT-Blöcke |
| `colossus-review.png` | Beschriftetes Vergleichsbild |
| `verification.json` | Blockgenauer Vergleich von Schematic, NBT und Teilvorlagen |

Die große Bodenplatte und der türkise Zwei-Block-Marker sind Präsentationshilfen
und werden nicht in die Struktur exportiert. Kleine modellierte Erdhügel gehören
dagegen zum Export. Die Bilder nutzen Blender-Beleuchtung und einen Legacy-Atlas.

Erneute Aufrufe überschreiben gleichnamige generierte Ausgaben. Vor eigenen
Änderungen die `.blend` z. B. nach `design/blender/colossus.blend` kopieren und
den OBJ-Ausgabepfad in einer eigenen Config festlegen. Generierte Dateien sind
nicht versioniert; Skripte und `design/colossus-ots.json` sind die reproduzierbaren Quellen.

## 3. Modell, Materialien und Koordinaten

- Der Generator arbeitet gedanklich in Minecraft-XYZ, Vorderseite **−Z**.
  Blender-Koordinaten sind `(X, −Z, Y)`; Export mit Forward `NEGATIVE_Z`, Up `Y`.
- OBJ immer trianguliert exportieren. Zusammengehörige Teile, insbesondere Arm
  und Rumpf, im selben Export und Koordinatensystem belassen.
- Die Config legt die gewünschte Höhe und die Materialpalette fest. OTS skaliert
  die gesamte Geometrie auf diese Höhe; ein angehängtes tieferes Teil verändert
  damit den Maßstab. Die tatsächlichen Maße stehen im Konvertierungsmanifest.
- Der CLI-Adapter unterstützt zunächst **benannte, einfarbige OBJ-Materialien**.
  Ihre Namen werden in der Config auf Atlas-Blöcke abgebildet und mit deren
  Durchschnittsfarbe voxelisiert. OTS übernimmt anschließend die Farbauswahl
  innerhalb dieser Palette: kein Dithering, Farbgenauigkeit 255, erste Oberfläche
  bei überlappenden Voxeln. Das ist keine allgemeine MTL-/Textur-Importpipeline.
- Unbekannte Materialien oder nicht im Atlas enthaltene Blöcke führen zu einem
  Fehler. Die Palette enthält Tiefenschiefer, Basalt, schwarzen Beton, Moos,
  Erde, Eichenbretter und verwittertes geschnittenes Kupfer.
- Der Legacy-Atlas enthält kein `waxed_weathered_cut_copper`; im Prototyp wird
  `weathered_cut_copper` verwendet. Vor dem Spieleinsatz ist eine gezielte
  Umstellung auf die gewachste Variante sinnvoll, wenn der Farbzustand bleiben soll.

**Geometriegrenze:** Der verwendete BVH-Ray-Voxeliser rastert Oberflächen und füllt
geschlossene Volumen nicht automatisch massiv. Auch ein massiver Blender-Würfel
ist danach zunächst eine Blockhülle. Für stabile Wände und einen gezielt
begehbaren Koloss müssen Materialfüllung und Innenraumdefinition separat
geprüft beziehungsweise ergänzt werden. Treppen und Stufen werden in diesem
ersten Adapter nicht erzeugt.

Für massive Vorlagen gibt es jetzt die ausdrücklich aktivierte Config-Option
`fill_enclosed`: Sie nennt ein Material aus `materials` und füllt nach der
Voxelisierung abgeschlossene Innenzellen. Obelisk v2 verwendet dafür Sandstein.
Die Colossus-Configs bleiben bei Oberflächenvoxelisierung. Details und Tests
stehen in [OBELISK_V2.md](OBELISK_V2.md).

## 4. Luftregel und NBT-Konvertierung

Der Konverter funktioniert unabhängig von ObjToSchematic mit Sponge v2/v3,
gzip-komprimiert oder unkomprimiert. Keine zusätzlichen Python-Pakete nötig:

```powershell
python tools/schem_to_nbt.py model.schem design/imported/model.nbt --air omit
```

| Option / Block | Wirkung |
| --- | --- |
| `--air omit` | Luft auslassen; Gelände bleibt dort stehen, auch in Innenräumen |
| `--air keep` | Gesamte Luft übernehmen; auch Außenluft im Exportquader räumt Gelände weg |
| `minecraft:structure_void` | Immer auslassen; bestehendes Gelände erhalten |

`--air` muss ausdrücklich angegeben werden. Weder die Oberflächenvoxelisierung
noch der Konverter unterscheiden automatisch freizuräumende Innenräume von
Außenluft. Die Vorschau auf leerer Bühne belegt daher keine Gelände-Einbettung.

Blockzustände werden übernommen, die Konvertierung rotiert nicht. Ein
Schematic-Offset wird im Manifest dokumentiert, nicht auf Blockpositionen addiert.
Entities und Block-Entities werden ausdrücklich abgelehnt. Große Exporte werden
vollständig in den Arbeitsspeicher geladen.

**Versionen:** Der Legacy-Exporter schreibt DataVersion **3105** (Minecraft 1.19).
Diese bleibt in der NBT erhalten; unsere Zielversion 26.2 verwendet **4903**.
Es gibt keine automatische Registryprüfung oder Versionsmigration. Eine bloße
Änderung dieser Zahl wäre keine Migration. Die verwendete Palette und ihre
Darstellung müssen vor der Übernahme im Zielspiel geprüft werden.

`--tile-size 32` erzeugt zusätzlich Teilvorlagen und relative Ursprünge im
Manifest (zulässige Kantenlängen 1–128). Leere Teile werden ausgelassen. Die ganze
Vorlage bleibt erhalten. Das Manifest ist keine Minecraft-Platzierungsdefinition;
Worldgen müsste Teile bei Bedarf gemeinsam platzieren und drehen.

## 5. Prüfungen und Worldgen-Übernahme

```powershell
python tools/inspect_ots_result.py --check-only
python -m unittest discover -s tests -p test_schem_to_nbt.py -v
```

Die Prüfung des echten Exports vergleicht alle Blockkoordinaten und Zustände,
Abmessungen, Datenversion, Palette, Quell-/Exportprüfsummen sowie die verlustfreie
Rekonstruktion aus Teilvorlagen. Die Konvertertests decken zusätzlich synthetische
v2/v3-Quellen, Luftregeln, Blockzustände, mehrbyteige Indizes, Fehlerfälle und
deterministische NBT-Ausgabe ab.

**Noch ausstehend:** `python tools/build.py` erzeugt `obelisk.nbt` und
`colossus.nbt` aus den bisherigen Python-Generatoren neu. Für eine Übernahme muss
der Build geprüfte Importquellen ausdrücklich unterstützen. Außerdem müssen
Struktur-ID, Template-Pool, Prüfgrundfläche, Bodenhöhe, Höhenversätze,
Biome/Hangprüfungen und gegebenenfalls Teilpositionen zur neuen Geometrie passen.
Siehe [WORLDGEN.md](WORLDGEN.md).

Nächste Abnahme: Form und Materialien beurteilen; anschließend Wandstärken,
Brüche, Geländeanschluss und Innenraumluft fertigstellen. Im Spiel vier Drehungen,
Blockpalette, Zugänglichkeit, Chunk-Grenzen und erneutes Laden prüfen. Natürliche
Generierung bleibt ein eigener Test.
