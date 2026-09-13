# Changelog

## 0.1.0-alpha.2

- Obelisk mit durchgehenden Rissen, tieferen Kantenausbrüchen, Sandverwehungen und Trümmern am Sockel.
- Koloss mit aufgebrochenem Helm, freiliegenden Streben im Brustpanzer, beschädigtem Brustring und Kerben im abgetrennten Arm.
- Dichtere Moos- und Blattflächen auf einer Seite, ergänzt um Moosspuren an senkrechten Flächen.
- Der Vorweg beginnt 14 Blöcke weiter innen. Der Zugang ist kurz, unregelmäßig gepflastert und von Erde sowie gefallenen Platten eingefasst. Eine drei Blöcke breite Route zum Maschinenraum bleibt frei.
- Testserver wählt standardmäßig das Artefakt zur aktuellen Projektversion, damit zurückbehaltene ältere JARs nicht versehentlich geprüft werden.

Die neuen Formen entstehen ausschließlich bei neuer Generierung. Bestehende Relikte werden nicht umgebaut. Abhängigkeiten, Struktur-IDs und Verteilung bleiben unverändert. Nachweise stehen im [Alpha-2-Testbericht](docs/ALPHA_2_TEST_REPORT.md).

## 0.1.0-alpha.1

Erste implementierte Alpha für Minecraft 26.2 mit Fabric.

- Automatische Erzeugung eines Obelisken und eines Kolosses samt Arm und Innenraum.
- Deterministische NBT-Exporte mit vollständigen Vorlagen, optionalen Teilvorlagen und Prüfsummenmanifest.
- Natürliche Platzierung über Lithostitched mit Biome-, Höhen- und Rasterbedingungen.
- Optionale Biome-Zuordnung für Terralith und Biomes O' Plenty.
- Generierbares Einstellungs-Datapack für Dichteprofile und deaktivierte Relikttypen.
- Reproduzierbarer Build einer datenbasierten Fabric-Mod ohne eigene Java-Klassen.
- Geometrievorschauen, Tests und isolierter Testserver-Ablauf.

Dies ist eine Alpha zur Erprobung der Erzeugung und Integration. Gestaltung, Geländeübergänge und Häufigkeit benötigen weitere Spieltests. Die Einzelheiten der tatsächlich ausgeführten Prüfungen stehen in [docs/ALPHA_TEST_REPORT.md](docs/ALPHA_TEST_REPORT.md).
