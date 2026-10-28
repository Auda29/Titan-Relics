# Magnet pro Item, kleiner Koloss V10 und Friedlich-Korrektur

Stand 28. Oktober 2026, Minecraft 26.2 / Fabric.

Niklas bestätigt den defekten Magnetfund im kleinen Koloss, die Reparatur und
die Einträge im Crafting Book. Die neue Vorgabe zählt Magnetverschleiß pro
Item. Die einzige kleine-Koloss-Truhe wandert in einen Maschinenstand auf dem
oberen Podest der zweiten Treppe. Die Entscheidungen stehen im
[Feedbackbericht](../project/MAGNET_SMALL_COLOSSUS_20261028.md).

## Magnet

Ein 64er-Stack kostet 64 Punkte. Bei Teilaufnahmen zählt ausschließlich die
tatsächlich eingefügte Menge. Eine unterstützte Einfügung ist auf das restliche
Budget begrenzt. Fehlgeschlagene Aufnahmen und bloßes Anziehen kosten nichts.
Bei null endet die Unterstützung; normales Aufheben bleibt möglich. Beide
Hände, Inventar-Inaktivität, die bisherige Geschwindigkeit, die Kapazität von
1.000 und das Reparaturrezept bleiben erhalten. Der Tooltip nennt Items.

Der native Präsentationstest prüft drei Items in der Nebenhand, 64 in der
Haupthand, eine durch Inventarplatz begrenzte Aufnahme, einen inzwischen vollen
Inventarplatz, die letzten drei Punkte und anschließendes normales Aufheben.
Schlüssel-/Kernauswürfe und deren Belege werden im selben Lauf weiter geprüft.

## Kleiner Koloss

Die Truhe sitzt bei `[67,44,53]`, Richtung `west`, am oberen Ende des vorhandenen
Wartungsaufstiegs. Rahmen, gestufter Rücken und freie Bedienfläche machen sie
erkennbar. Beide Treppen bleiben erhalten. Der alte Platzhalter ist entfernt.
Der [Modellbericht](../project/SMALL_COLOSSUS_LANDMARKS_20261028.md) enthält
Bilder, Exportprüfungen, Blender-Wiederöffnung und Freiräume.

Neue Welten wählen `interiors-20261028-v3`. V1 und V2 behalten ihre bisherigen
Marker, Vorlagen und Fingerprints. Die V3-Freiräume des kleinen Kolosses räumen
zusätzlich native Erze und Bodenblöcke ausschließlich aus quellfreien Zellen.
Andere geschützte Strukturen und Flüssigkeiten bleiben erhalten. Der Build
enthält die älteren Vorlagen weiter. Vorhandene Welten werden nicht umgebaut.

## Ladeabsturz auf Friedlich

Der Originalbericht `crash-2026-10-28_08.51.30-server.txt` meldet
`Cannot create natural Enderman`. Die Welt war auf Friedlich eingestellt.
Minecraft 26.2 lehnt dort die native Erzeugung feindlicher Mobs ab. Die bisherige
Turminitialisierung behandelte diesen regulären Fall als fatalen Fehler.

Die Initialisierung prüft jetzt `EntityTypes.ENDERMAN.canSpawn(level)` und
schließt einen nicht erlaubten einmaligen Spawn ohne erzwungenen Mob ab.
Ein späterer Schwierigkeitswechsel füllt diesen Anspruch nicht erneut auf.

Der Absturz wurde mit der zuvor installierten JAR auf einer vollständigen
Kopie von `Relic Alpha 5_0 Terrain 4` reproduziert. Mit dem Hotfix lädt dieselbe
Kopie auf Friedlich; ein erneuter Start auf Normal erzeugt weder die fünf
abgeschlossenen Enderman-Aktionen noch verbrauchte Truhenbeute neu. Alle 172
Originaldateien blieben während des Tests bytegleich. Eine frisch generierte
Turmruine besteht den separaten Friedlich-/Neustarttest ebenfalls.

Der geprüfte Hotfix `a6bf93aa17c6b738f715e10ffac615e60f25fe7b82ee185481ce8cc7c6da87ec`
wurde bei geschlossener Instanz in `Relic Test` installiert. Die vorherige JAR
mit SHA-256 `caffeb247121ee1ea501ecf68eaa1c2af07801420c7dbeb5cae636f9d041acfe`
liegt bytegeprüft unter
`build/magnet-small-landmarks-20261028/crash-fix/installed-backup/relics-previous-caffeb247.jar`.
Die Originalwelt wurde weder gestartet noch bearbeitet.

## Abschließender Testbuild

`dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`

SHA-256: `b5e8b537ef69d8a74a1482cadbcae345eec245fb4f7d707b3806b31f3d7b4b52`.

Dieser Build enthält zusätzlich zum installierten Hotfix die V10-Vorlagen und
die V3-Revisionsauswahl. Für den neuen Truhenort ist eine neue Testwelt nötig.
Die [maschinenlesbaren Nachweise](magnet-small-colossus-20261028-evidence.json)
halten die jeweiligen Artefakte und endgültigen Testergebnisse getrennt fest.
Die Sichtprüfung und Minecraft-Beleuchtung bleiben manuell. Die getrennten
lokalen NeoForge-Arbeiten bleiben erhalten. Es wurde kein Commit oder Push erstellt.

Der vollständige Build wurde anschließend bei geschlossener Instanz ebenfalls
in `Relic Test` installiert und auf die obige Prüfsumme geprüft. Auch der
Zwischen-Hotfix ist unter `installed-backup/relics-hotfix-a6bf93aa.jar` gesichert.

Die Abschlussprüfung besteht mit 139 Python-Tests sowie den Gameplay-, Mixin-,
Platzierungs- und Verteilungsprüfungen. Die separate lokale NeoForge-Suite ist
ausgenommen. V10 besteht die natürliche Generierung und die Freiraumprüfung in
allen vier Drehungen. Vollständige V2- und teilweise generierte V1-Welten behalten
ihre bisherigen Vorlagen und Loot-Zustände. Die normale Turminitialisierung
erzeugt weiterhin fünf Endermen; unter Friedlich werden sie regulär ausgelassen.
