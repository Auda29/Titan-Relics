# Colossus v3 – Referenzentwurf mit unterirdischer Hüfte

Stand: 01.10.2026

## Referenz und gestalterische Entscheidungen

Grundlage ist die **Anfangsszene (0–5 Sekunden)** von
[Archaean Colossi – The Archive In Between](https://www.instagram.com/reel/DaoBxUEiBNa/).
Das Video wurde für diese Studie tatsächlich gesichtet; lokale Einzelbilder
liegen ausschließlich unter `.work/references/`.

Sichtbare Hauptmerkmale und ihre Umsetzung:

| Original | Colossus v3 |
| --- | --- |
| Breite, fast hügelförmige bronzene Panzerung | Großer gewölbter Rumpf und dominante Schulterhauben |
| Runder Helm, schmaler dunkler Sehschlitz | Kuppelhelm mit ausgeschnittener Visieröffnung |
| Schwere gebogene Leitungen vor dem Kinn und seitliche Filter | Gerippter Atemschlauch, Auslass und konzentrische Filtergehäuse |
| Gealterte warme Metallflächen, Rost und grüne Ablagerungen | Kupferpalette, braune Terrakotta, Patina und Moospolster |
| Unregelmäßige Schäden an Stirn und unterer Schulter | Gezackte Durchbrüche mit zurückgesetzter Mechanik |
| Unterkörper verschwindet in Hügeln | Tief reichende Körperhülle; Geländeansicht verdeckt die unteren Partien |
| Langer röhrenförmiger Unterarm mit Hand im Vordergrund | Abgesetzter, beringter Unterarm in gemeinsamer Strukturkoordinate |

Rücken und verdeckte Mechanik sind gestalterische Ergänzungen: Die erste Szene
zeigt nur eine frontale Dreiviertelansicht. Der sehr große zentrale Brustring
des ersten Entwurfs wurde durch eine tief liegende, unregelmäßige Bruchstelle
ersetzt. Die Form ist als alternative Version angelegt.

## Maßstab

Der ursprüngliche **[Colossus v2](COLOSSUS_V2.md)** hatte **160 Blöcke** Gesamthöhe
statt 66 beim ersten Blender-Colossus. Die Ergänzung des unterirdischen Bauchs und der abgerissenen
Hüfte erhöht die Gesamthöhe auf **209 Blöcke**. Der oberirdische Maßstab wird
dabei auf den bereits gestalteten Entwurf kalibriert (Rundungsabweichung unter
0,5 %). Es ist weiterhin eine **Maßstabsannahme**, keine belegte Originalabmessung. Die Person im
Vordergrund und der Koloss liegen in stark unterschiedlichen Entfernungen;
ihre Pixelhöhen lassen sich nicht unmittelbar in Meter umrechnen.

Orientierungspunkte sind das Verhältnis von Helm und Panzerkörper, die Länge
des liegenden Arms und die Wirkung der Vegetation. Der Körper ist im Modell
ungefähr 190 Quelleinheiten breit, der Helm etwa 60–70 hoch und der separate
Arm einschließlich Hand ungefähr 110 lang. Die zusätzliche Hüfte endet an einer
unregelmäßigen Bruchkante mit freiliegenden Streben und Leitungen. Deshalb sind **die tatsächlichen XYZ-Maße im
`colossus-v3.manifest.json` maßgeblich**, nicht diese gerundeten Quellmaße.

Die Gesamtgrundfläche schließt den Abstand zum Arm ein. Ein Größenvergleich
stellt die NBT-Geometrien von v2 und dem ersten Koloss bei identischer
Blockgröße nebeneinander. Die Hügelansicht enthält eine zwei Blöcke hohe Figur
nahe dem Arm. Landschaft, Figur und weitere Vorschauhilfen sind nicht Teil des
Schematic-Exports.

Ergebnis des geprüften Exports:

| Kennzahl | Colossus v3 |
| --- | --- |
| Gesamtmaße X/Y/Z | **181 × 209 × 227 Blöcke** |
| Gesetzte Blöcke | **221.221** |
| Verwendete Blocktypen | **11** |
| Nichtleere 32er-Teilvorlagen | **124** |
| Blöcke unter der gedachten Bodenebene | **85.432** |

Alle Blockpositionen und Zustände stimmen zwischen `.schem` und `.nbt` überein;
die Teilvorlagen rekonstruieren die Gesamtvorlage verlustfrei. Der erste Koloss
wurde ebenfalls erneut anhand seiner unveränderten Prüfsummen geprüft.

## Unterirdische Fortsetzung

Der Brustpanzer wird unter der bisherigen Schnittkante fortgesetzt. Eine nach
unten schmaler werdende Bauchpanzerung geht in einen teilweise erhaltenen
Hüftbereich über. Die Außen- und Innenflächen der Panzerung sowie die freiliegende
Wandstärke an der Bruchkante sind modelliert; im Inneren laufen Träger aus dem
bisherigen Rumpf bis zu unterschiedlich langen Abrissenden. Es gibt keine Beine.

Das gedachte Bodenniveau liegt ungefähr bei NBT-Y **77**, also etwa 77 Blöcke
über dem tiefsten verbliebenen Träger. Dieser Wert beschreibt die aktuelle
Gestaltung und muss später in die Worldgen-Platzierung übersetzt werden.
Die Vorschau `colossus-v3-underground-review.png` zeigt die Freilegung mit einer
türkisen Bodenebene sowie einen echten NBT-Ausschnitt des Hüftbereichs.

Der Quellvergleich gegen den Entwurf vor der Erweiterung bestätigt dieselben
47.886 Modellpunkte oberhalb Quell-Y 20. Die notwendige Rundung der neuen
Exporthöhe verändert den Blockmaßstab lediglich um etwa 0,095 %. Der zusätzliche
Unterkörper ist in `.schem` und `.nbt` enthalten, nicht nur in der Geländeansicht.

## Reproduzieren

Die lokale Einrichtung steht in [BLENDER_WORKFLOW.md](BLENDER_WORKFLOW.md).
Vom Repository-Hauptverzeichnis aus:

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_colossus_v3.py
node tools/obj_to_schem.cjs design/colossus-v3.json
python tools/schem_to_nbt.py design/generated/colossus-v3/colossus-v3.schem design/generated/colossus-v3/colossus-v3.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/colossus-v3.json
python tools/inspect_ots_result.py --config design/colossus-v3.json
```

Wichtige Dateien unter `design/generated/colossus-v3/`:

- `colossus-v3-source.blend`: bearbeitbares Quellmodell mit benannten Bauteilen.
- `colossus-v3.obj`, `colossus-v3.schem`, `colossus-v3.nbt`: Konvertierungskette.
- `colossus-v3.design.json`: Referenz, Maßstabsannahme und Quellgrenzen.
- `colossus-v3.ots.json`, `colossus-v3.manifest.json`, `verification.json`: Export-
  und Prüfmetadaten einschließlich Prüfsummen.
- `colossus-v3-blocks.blend`: tatsächliche NBT-Geometrie mit gepacktem Texturatlas.
- `colossus-v3-landscape.blend`: NBT plus separat modellierte Präsentationslandschaft.
- `colossus-v3-review.png`: vier Ansichten von Quelle und Blockexport.
- `colossus-v3-reference-review.png`: Originalausschnitt, Geländeansicht und
  Größenvergleich. Benötigt das lokale Referenz-Einzelbild aus der Config.
- `05-blocks-landscape.png`, `06-size-comparison.png`: große Einzelansichten.
- `07-buried-body.png`, `08-hip-detail.png`: Freilegung mit Bodenebene und
  Ausschnitt der tatsächlichen unterirdischen NBT-Blöcke.
- `colossus-v3-underground.blend`, `colossus-v3-underground-review.png`: räumliche
  Inspektionsszene und beschriftete Übersicht zum versunkenen Unterkörper.

Die Quelle kann kopiert und manuell weiterbearbeitet werden; ein erneuter
Generatorlauf überschreibt nur die gleichnamigen generierten Dateien.

## Technischer Status

Es handelt sich um einen visuellen Modellprototyp. Die Bilder der Blöcke werden
aus der NBT gelesen und in Blender gerendert. Geländeansicht und Vergleichsbild
sind keine Minecraft-Screenshots oder Nachweise einer natürlichen Platzierung.

Die im Workflow beschriebenen Grenzen gelten weiterhin: Oberflächenvoxelisierung,
ausgelassene Luft (`omit`), Legacy-DataVersion 3105 und ausstehende
Worldgen-Übernahme. Die großzügige Kupferpalette folgt zunächst der Farbwirkung
der Referenz; Oxidationszustände, Blockmengen und Innenraumluft sind vor der
Spielintegration zu bearbeiten. Die deutlich größere Grundfläche erfordert
außerdem neue Standort- und Geländeprüfungen.
