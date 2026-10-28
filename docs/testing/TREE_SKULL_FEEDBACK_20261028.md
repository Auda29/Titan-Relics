# Skull-/Baumkorrektur: Prüfung vom 28. Oktober 2026

Der Minecraft-26.2-/Fabric-Testbuild ist in **Relic Test** installiert. Das Profil
war geschlossen; die vorherige JAR ist hashgeprüft gesichert. Keine Originalwelt
wurde für die Prüfung geöffnet oder verändert.

- JAR: `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`
- SHA256: `66b93cea03f14818ccfefe217c9f9266178c929fdf5789c2f56a1988a30534e4`
- Revision neuer Welten: `interiors-20261028-v5`, 40 enthaltene Templates.
- [Maschinenlesbare Evidenz](tree-skull-feedback-20261028-evidence.json)
- [Änderungen und Modellbild](../project/TREE_SKULL_FEEDBACK_20261028.md)

156 Python-Tests bestanden. Die getrennten, unveränderten NeoForge-Arbeiten
wurden nicht ausgeführt. Java: 665 Gameplay-Assertions, 52 statische Mixin-Verträge,
764 Worldgen-Assertions, 1.008 Executor-/Abhängigkeitsprüfungen, 755.716 Suchprüfungen
und 198.924 synthetische Verteilungsprüfungen bestanden.

## Skull

Die fünf Modelltests und die unabhängige Blender-Wiederöffnung bestehen. Der
Worker prüfte alle vier rechnerischen Drehungen. 147 Dripstone-Zellen des
isolierten Seitenbrockens entfallen; alle übrigen NBT-Blockeinträge bleiben
bytegleich. Die 66 Artefaktbindungen stimmen auch nach der gesamten Testsuite.

Natürliche Erzeugung wurde an drei akzeptierten Standorten in den Drehungen
0, 1 und 2 mit dem finalen JAR geprüft. Exportgeometrie, Bodenanschluss, Quellhash,
Templateauswahl und Neustart bestehen. Je Standort wurden die 111 entfernten
Zellen oberhalb der bisherigen Clip-Grenze auch in der Welt als frei von dem
alten Dripstone-Splitter bestätigt. Die übrigen 36 entfernten Quellzellen lagen
bereits unter dieser Clip-Grenze.

Ein V4-Save aus dem vorherigen Spielerbuild wurde anschließend mit V5 geöffnet:
Weltfingerprint, Innenraumrevision, Ziel und bisheriges Skull-Template blieben
erhalten. Der alte Skull erhält keine nachträgliche Modelländerung.

## Baum

Prozessortests prüfen tieferen und höheren Boden, fehlenden Untergrund, Wasser,
Container, Konflikte mit verbauten Wurzeln sowie die Grenze zum Nachbarchunk.
Der Terrainprozessor verändert nur die drei vorgesehenen Busch-/Erdpaare.
Er liest im eigenen Chunk und sucht maximal sechs Blöcke vertikal. Ein passender
Erdblock liegt bündig in einer vorhandenen festen Oberfläche. Es entstehen keine
Sockelsäulen. Nicht sicher platzierbare Paare entfallen vollständig.

Zwei natürliche Baumstandorte in den Drehungen 1 und 3 wurden einschließlich
vollständiger Geometrie, Schutzmarkierungen, Ankerregistrierung und Neustart
geprüft. Fünf der sechs Buschplätze wurden auf die tatsächliche Oberfläche
versetzt, zwischen vier Blöcken tiefer und zwei Blöcken höher. Ein ungeeigneter
Platz blieb ohne Busch und Sockel. Die fünf erzeugten Paare hatten festen
Untergrund und beide Zellen waren vor späteren Weltgenerierungsfeatures geschützt.
Alle übrigen exportierten Baumzellen stimmen weiterhin überein.

## Aura und bestehendes Gameplay

Die native Serverprüfung testet 45 Positionen und Spielmodusfälle, dann erneut
dieselben Fälle nach Neustart. Sie prüft 49,999, 50 und 50,001 Blöcke entlang
aller sechs Achsenrichtungen an positiven und negativen Ankern, diagonalen
Ausschluss, dimensionale Trennung und zwei Zellen entfernte Anker. Genau 50
Blöcke sind eingeschlossen. Regeneration I wird weiterhin für 6.000 Ticks
vergeben; Creative und Spectator bleiben ausgeschlossen, Adventure funktioniert.

Der vollständige Trial-/Vault-/Magnet-Test bestand zusätzlich vor und nach
Neustart. Physische Belohnungen, sofortiger Schlüsselverbrauch, persönliche
Aufnahme, beide Magnet-Hände, Verschleiß pro Item, Teilaufnahme und Restbudget
bleiben korrekt. Testklassen befinden sich nicht im Spieler-JAR.

## Bestand und Reproduktion

Die visuelle Basis und alle vier bisherigen Innenraummanifeste bleiben bytegleich.
Der JAR-Vergleich enthält sieben geänderte Runtime-Klassen, zwei zusätzliche
Skull-Templates und das V5-Manifest. Keine alte Ressource wurde entfernt; alle
bisherigen Templates und Kunstressourcen bleiben identisch. Ein zweites Packaging
reproduziert das JAR bytegleich.

Von 1509 gesicherten Bestandsdateien sind
1483 unverändert. Die Änderungen betreffen autorisierte
Runtime-, Test-, Integrations- und Dokumentationsdateien. Sämtliche bisherigen
Modellartefakte und die getrennten Kompatibilitätsarbeiten blieben unangetastet.

## Nächster Spieltest

Der 50-Block-Radius wirkt auch an registrierten Bäumen bestehender Welten.
Buschkorrekturen gelten für künftig erzeugte Baumstücke. Gespeicherte Strukturen
werden nicht umgebaut. Neue Skull-Geometrie und bereits erzeugte Baumstellen
deshalb in einer neuen Testwelt ansehen. Client-Sichtprüfung und die übrigen
Alpha-5-Release-Abnahmen bleiben eigenständige Prüfungen.

Vorherige installierte JAR: `build/tree-skull-feedback-20261028/installed-backup-f63fd48e.jar`.
Kein Commit, Push oder Release in diesem Arbeitsschritt.
