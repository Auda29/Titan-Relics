# Obelisk v2 – Painted Desert

Stand: 01.10.2026

## Originalreferenz und Form

Referenz ist [Painted Desert von Josh White](https://www.instagram.com/p/Da0NEq7kUAO/).
Die beiden veröffentlichten Gemälde und die beigefügte Prozessanimation wurden
gesichtet. Lokale Referenzbilder liegen unter `.work/references/`.

Die Hauptmerkmale sind eine extrem schlanke Stele mit flacher Krone, beinahe
parallele große Flächen, warme mineralische Farben und ein starker Unterschied
zwischen beschatteter Hauptfläche und heller Seite. Horizontale Verwitterung
bleibt sparsam. Der Fuß verschwindet in farbig geschichteten Wüstenhügeln.

Der Entwurf setzt das mit einer parallelen, durchgehenden Steinmasse um:
22 × 18 Quelleinheiten vom Fuß bis zur flachen Oberkante. Eine zunächst erprobte
leichte Verjüngung ergab im Blockraster eine auffällige mittlere Stufe; die
parallelen Seiten bilden die ruhige Referenzsilhouette besser ab. Kleine Verluste
an zwei Kanten und zurückhaltende mineralische Bänder ergänzen die Form. Gelbe Terrakotta,
Sandstein, braune mineralische Spuren und eine hellere, exponierte Seite bilden
die Palette. Landschaft und Beleuchtung sind zusätzliche Präsentationsmittel.

## Größe und Untergrund

| Kennzahl | Obelisk v2 |
| --- | --- |
| Exportmaße X/Y/Z | **23 × 209 × 19 Blöcke** |
| Sichtbare Quellhöhe über Boden | ungefähr **176 Blöcke** |
| Unterirdischer Fuß | **32 Blöcke** |
| Gesetzte Blöcke | **90.497** |
| Blocktypen | **6** |
| Nichtleere 32er-Teilvorlagen | **7** |
| Durch Füllung ergänzte Innenzellen | **73.883** |
| Blöcke unter der nominalen Bodenlinie | **13.856** |

Der Maßstab ist eine gestalterische Annäherung. Das Bild zeigt keine eindeutig
kalibrierbare menschliche Figur; auch die Fluggeräte liefern keine bekannten
Maße. Das Verhältnis von sichtbarer Höhe zu projizierter Breite liegt ungefähr
bei 7:1. Ein Größenvergleich zeigt den bisherigen 70-Block-Obelisken und v2 bei
gleicher Blockgröße. Eine zwei Blöcke hohe Figur dient in der Landschaft als
zusätzlicher Vergleich.

Die gesamte Stele ist in der `.schem` und `.nbt` enthalten, einschließlich des
unterirdischen Fußes. Die umliegenden Hügel, die Figur und die türkisfarbene
Bodenmarkierung sind reine Vorschauobjekte.

## Massiver Kern

ObjToSchematic voxelisiert zunächst die Oberflächen. Für diesen Obelisken aktiviert
`design/obelisk-v2.json` ausdrücklich `"fill_enclosed": "core"`. Der lokale Adapter
füllt anschließend vollständig eingeschlossene Zellen mit der Atlasfarbe des
Kernmaterials, bevor die Minecraft-Palette zugewiesen und `.schem` geschrieben
wird. `core` steht hier für Sandstein.

Das Verfahren flutet zunächst die Außenluft über die sechs Blocknachbarn; nur
nicht erreichbare Innenzellen werden gefüllt. Öffnungen nach außen bleiben offen.
Diese Option ist für massive Bauwerke gedacht und wird für die Colossus-Modelle
nicht aktiviert. Es ist keine automatische Innenraum- oder Luftfreistellung für
Worldgen. Die Füllprüfung ist auf 32 Millionen Rasterzellen begrenzt.

Der Exportcheck bestätigt zusätzlich einen durchgehend belegten zentralen
7 × 209 × 7-Block-Prüfkörper. `07-solid-foot-section.png` zeigt einen Ausschnitt
der tatsächlichen NBT-Blöcke mit freigelegtem Kern.

## Erzeugen und prüfen

Werkzeuge und Einrichtung: [BLENDER_WORKFLOW.md](BLENDER_WORKFLOW.md).

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
& $blender --background --python-exit-code 1 --python tools/create_obelisk_v2.py
node tools/obj_to_schem.cjs design/obelisk-v2.json
python tools/schem_to_nbt.py design/generated/obelisk-v2/obelisk-v2.schem design/generated/obelisk-v2/obelisk-v2.nbt --air omit --tile-size 32
& $blender --background --python-exit-code 1 --python tools/render_ots_preview.py -- --config design/obelisk-v2.json
python tools/inspect_ots_result.py --config design/obelisk-v2.json
node --test tests/voxel_fill.test.cjs
```

Wichtige Ausgaben unter `design/generated/obelisk-v2/`:

- `obelisk-v2-source.blend`: bearbeitbare Blender-Quelle.
- `obelisk-v2.obj`, `obelisk-v2.schem`, `obelisk-v2.nbt`: Geometrie und Blockexport.
- `obelisk-v2.design.json`, `obelisk-v2.ots.json`, `obelisk-v2.manifest.json`,
  `verification.json`: Maßstabsannahme, Einstellungen, Blockzahlen und Prüfsummen.
- `obelisk-v2-blocks.blend`: NBT-Oberflächenmesh mit gepacktem Minecraft-Atlas.
- `obelisk-v2-landscape.blend`: NBT mit illustrativer Wüstenlandschaft.
- `obelisk-v2-foot-section.blend`: tatsächlicher Blockausschnitt mit solidem Kern.
- `obelisk-v2-review.png`, `obelisk-v2-reference-review.png`: beschriftete Übersichten.
- `05-blocks-landscape.png`, `06-size-comparison.png`, `07-solid-foot-section.png`:
  Landschaft, maßstäblicher Vergleich und Fußschnitt.

Schematic/NBT-Übereinstimmung, Palette, Koordinaten, Grenzen, Teilvorlagen und
massiver Kern werden am echten Export geprüft. Drei Node-Tests decken mehrere
geschlossene Hohlräume, negative Koordinaten, geöffnete Kammern und dünne Flächen ab.

Der Stand ist ein Asset-Prototyp mit DataVersion 3105 aus dem Legacy-Exporter.
Übernahme in Mod-Build und Worldgen sowie Ingame-Abnahme sind weiterhin offen.
Insbesondere benötigen die Höhe und die 32 Blöcke tiefe Basis eigene
Platzierungs- und Höhenprüfungen für die Zielwelt.
