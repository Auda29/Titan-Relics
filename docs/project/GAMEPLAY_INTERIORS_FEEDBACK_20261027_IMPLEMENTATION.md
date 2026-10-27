# Innenraumrevisionen vom 27. Oktober 2026

Die vier überarbeiteten Blockmodelle stehen im [neuen Handoff-Index](reviews/gameplay-interiors-feedback-20261027-handoff.json). Der fünfte Eintrag verweist unverändert auf den freigegebenen Weltenbaum V5. Der ursprüngliche Handoff-Index und seine Bilder bleiben erhalten.

- Großer Koloss V6: fünf vorhandene Stationen, zusätzliche beschädigte Aggregate, ein durch die tatsächlichen Schalenlagen geöffnetes Visier mit sieben Resten schwarzen Glases. Der zentrale Golemraum, der Weg von der Luke und der separate Armzugang bleiben erhalten. Der [direkte Cockpitvergleich](../../relics/colossus/design/generated/colossus-v6-interiors/colossus-v6-interiors-comparison-review.png) zeigt V5 neben V6. Das Reviewblatt enthält zusätzlich Ansichten von innen und außen.
- Kleiner Koloss V9: zusätzliche abgerissene Rippen und ausgeschlachtete Maschinenreste im unteren Innenraum. Zugang, Wartungsweg, einzelne Truhe und leerer oberer Cockpitbereich bleiben erhalten.
- Turmruine V9: begrenzte zusätzliche Trümmer im unteren Saal; die fünf Spawnpositionen, die Truhe und die fünf Unterbrechungen des Aufstiegs bleiben erhalten.
- Obelisk V6: unterbrochene, aufragende Sandsteinmarkierungen an beiden Ausgrabungsbereichen. Die acht Fundrollen und ihre offenen Oberseiten bleiben erhalten; Terrakotta und das Monument ab Y16 bleiben unverändert.

Die Versionsordner enthalten NBT, Schematic, Gameplay- und Design-JSON, editierbare Blender-Quellen, Reviewbilder und `verification.json`. Schnittbilder begrenzen die Ansicht; sie entfernen kein Dach aus dem Modell. Die beiden Visieraufnahmen nutzen zusätzliches Blender-Prüflicht und einen neutralen Himmel. Das ist kein Nachweis für Minecraft-Blocklicht oder die spätere Umgebung. Schwarzes Glas ist im Render transparent dargestellt.

Die Generatoren sind [build_gameplay_interiors_revision.py](../../tools/build_gameplay_interiors_revision.py), [render_gameplay_interiors_revision.py](../../tools/render_gameplay_interiors_revision.py), [review_gameplay_interiors_revision.py](../../tools/review_gameplay_interiors_revision.py) und [validate_gameplay_interiors_revision.py](../../tools/validate_gameplay_interiors_revision.py). Die Originalgeneratoren und ihre Versionszuordnung bleiben unverändert. Blender-Meshes sind editierbare Prüfquellen; Änderungen für einen neuen Export gehören in den Blockgenerator.

Die Prüfungen lesen NBT und Schematic unabhängig ein, vergleichen Größe, Offset, DataVersion 3105, Blockinhalt, Kacheln und Markerbindungen und kontrollieren Wege, Spawnfreiraum, geschützte Bereiche und die neuen Details. Schwarzes Glas wurde mit [InteriorRegistryEvidence.java](../../tools/InteriorRegistryEvidence.java) direkt im lokalen 26.2-Serverregister abgefragt; das [Ergebnis mit Server-JAR-Hash](reviews/gameplay-interiors-feedback-20261027-registry.json) ergänzt den ursprünglichen Registry-Auszug. Alle vier Blender-Dateien wurden nach dem Speichern erneut geöffnet und auf Bindung, Meshes und Marker geprüft.

Die Revisionen sind Kandidaten für die erneute Sichtprüfung. Eine technische Abnahme im Spiel, die natürliche Generierung, Rotation, Terrain, Loot-Initialisierung und echtes Blocklicht wurden in diesem Auftrag nicht getestet oder integriert.

## Unabhängige Abschlussprüfung

Der beauftragte Worker lief mit GPT-6.1 Terra und Reasoning-Einstellung `xhigh`.
Anschließend wurden alle neuen Übergabedateien anhand ihrer Hashes geprüft.
Alle 1.050 vor Beginn erfassten Bestandsdateien sind bytegleich erhalten,
einschließlich der ursprünglichen fünf Innenraumentwürfe, der ausgefüllten
Bewertung und der bestehenden lokalen NeoForge-Arbeiten.

Die vier Blender-Dateien wurden in einem weiteren frischen Blender-Prozess
schreibgeschützt geöffnet. NBT-Bindungen, Markerinhalt und Markerpositionen,
Mesh-Geometrie und die aus dem NBT berechneten äußeren Geometriegrenzen stimmen.
Die zehn bisherigen Handoff-Tests und die drei neuen Revisionstests wurden
unabhängig wiederholt und bestanden.

Ein neues ausfüllbares Bewertungsdokument liegt lokal unter
`output/pdf/relic-mod-innenraeume-ueberarbeitung-1-alpha-5.pdf`. Es enthält
16 Seiten mit großen Ansichten, eigenständigen Visierbildern, Cockpitvergleich,
Lageplänen und 38 Formularfeldern. Alle Seiten wurden gerendert und visuell
geprüft. Speichern und Wiederauslesen der Felder einschließlich Umlauten und
mehrzeiligen Kommentaren wurden getestet. Die vier neuen Gestaltungsentscheidungen
beginnen offen; die Freigabe des unveränderten Weltenbaums wird als bestehende
Entscheidung übernommen.

## Anschließende Freigabe

Die vier Revisionen wurden nach der erneuten Sichtprüfung am 27. Oktober 2026
von Niklas freigegeben und anschließend in die natürliche Generierung und die
Gameplay-Initialisierung eingebunden. Der frühere Hinweis auf ausstehende
Integration beschreibt den damaligen Modellauftrag. Der aktuelle technische
Stand und seine Nachweise stehen im
[Integrationsbericht](../testing/NATURAL_INTERIORS_20261027.md).
