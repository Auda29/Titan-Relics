# Innenraum-V4-Prüfung vom 28. Oktober 2026

Der finale Minecraft-26.2-/Fabric-Testbuild ist erstellt und in **Relic Test**
installiert. Das Profil war geschlossen; die bisherige JAR ist hashgeprüft
unter `build/interiors-v4-20261028/installed-backup-b5e8b537.jar` gesichert.
Keine Originalwelt wurde für die Tests geöffnet oder verändert.

- JAR: `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`
- SHA256: `f63fd48eba6acc84201800406916380946315b823022b6c08c6f1d343d70ef50`
- Neue Welten: `interiors-20261028-v4`; 38 Templates im Build.
- [Maschinenlesbare Ergebnisse](interiors-v4-20261028-evidence.json)
- [Änderungen und Reviewbilder](../project/INTERIORS_V4_20261028.md)

## Ergebnisse

150 Python-Tests bestanden. Die unabhängigen lokalen NeoForge-Arbeiten wurden
ausgelassen und bytegleich erhalten. Nach einer Korrektur am Report-Schreiber
bestanden erneut alle vier Tower-Tests: Die Prüfung bewahrt vorhandene
Zeilenenden hashgebundener Berichte auf Windows. Der LF-Bericht der Turmruine
ist wieder exakt an seinen Handoff gebunden.

Java: 663 Gameplay-Assertions, 52 statische Mixin-Verträge, 1.008 Executor-/
Abhängigkeitsprüfungen, 755.716 Suchprüfungen, 198.924 synthetische
Verteilungsprüfungen und 755 Worldgen-Assertions bestanden. Diese Prüfgruppen
sind getrennt von den tatsächlichen Minecraft-Serverläufen zu verstehen.

Small V11 und Tower V10 wurden jeweils an vier natürlich akzeptierten Standorten
in allen Drehungen erzeugt. Exportgeometrie, Bodenanschluss, freie Terrainzellen,
Schutzmarkierungen, Truhenstandorte, Truhenrichtung, Deckelfreiraum und Loot
bestanden. Nach Entnahme und Neustart gab es keine neue Befüllung. Tower V10
startet auf Normal seine fünf vorgesehenen Endermen; auf Friedlich werden
Spawnaktionen ohne Absturz abgeschlossen. Auch der Friedlich-Neustart bestand.

Beide Modelle bestanden je einen Upgrade-Test aus dem vorherigen Spielerbuild
`b5e8b537…`: Weltfingerprint, Revision V3, Ziel, alte Marker und Templates bleiben
erhalten. Ein weiterer Test speicherte nur den zentralen Chunk eines V3-Kolosses;
der finale Build erzeugte die restlichen Chunks weiterhin mit dem alten V3-
Template und bestand anschließend Neustart/Entnahmeprüfung. Alle drei bisherigen
Innenraummanifeste bleiben bytegleich. Keine Verschiebung oder Neubefüllung alter Fundstellen.

Der native Zwei-Spieler-Test bestand Trial-/Vault-Zustände und Ereignisse,
physische persönliche Belohnungen, sofortigen Schlüsselverbrauch und gespeicherte
Drops/Claims nach Neustart. Magnet: drei Items kosten drei Punkte, ein Stack
aus 64 kostet 64; beide Hände funktionieren, Inventarplätze bleiben inaktiv.
Teilaufnahme, letzte Restpunkte, Fehlaufnahme ohne Verschleiß und gewöhnliche
Aufnahme nach Verbrauch bestanden. Höchstgeschwindigkeit in beiden Händen:
0,385 gegenüber ursprünglich 0,35.

Ein Turmtest fand zunächst zwei native `minecraft:bush`-Blöcke in einer freien
Route. V4 räumt diese ausschließlich in quellfreien Clearance-Zellen der beiden
neuen Modelle. Die Wiederholung bestand alle Drehungen. Ein Testordner-Konflikt
bei zwei Turmstandorten desselben Seeds wurde durch die Drehung im Ordnernamen
behoben. Die finale Evidenz enthält erfolgreiche Wiederholungen mit dem obigen Hash.

Monolith wurde auf 60 frisch aus dem gepinnten Client exportierten Rüstungsflächen
mit nativen UVs geprüft. Beide Masken bleiben innerhalb tatsächlicher Netherite-
Deckflächen. Smaragd, Amethyst und Kupfer wurden mit nativen Materialpaletten
auf derselben Geometrie gerendert und angesehen. Erneute Extraktion reproduzierte
die UV-/Alpha-Evidenz bytegleich. Die Bilder verwenden Prüflicht und eine neutrale
Puppe; die Client-Sichtabnahme bleibt offen.

Alle Bindungen der beiden Modellhandoffs und des kombinierten Index stimmen.
Die 1339-Dateien-Sicherung meldet 1321 unveränderte Dateien;
die übrigen 18 sind autorisierte Runtime-, Ressourcen-, Test- und
Dokumentationsänderungen. Sämtliche vorherigen Modell- und Kompatibilitätsdateien
blieben erhalten. Der JAR-Vergleich zeigt nur vier geänderte Runtime-Klassen,
zwei Besatz-PNGs, vier neue Templates und das neue V4-Manifest; keine Entfernungen.
Itembilder, Rezepte, Atlasdefinitionen und alte Templates sind identisch.
Ein zweites Packaging reproduziert das JAR bytegleich.

## Noch im Spiel zu prüfen

Neue Geometrie in einer **neuen Testwelt** prüfen: kürzerer unterer Zugang,
oberer Truhenstand und Turmtruhe gegenüber dem Eingang. Bestehende Welten
behalten auch für weitere Chunks ihre gespeicherte Revision. Keine Welt löschen.
Monolith aktualisiert nach Spielneustart auch bereits verzierte Rüstung in alten
Welten. Großer Koloss und Obelisk behalten ihre Nutzerabnahme; Small V11, Tower
V10 und Besatz brauchen noch die Sichtfreigabe.

Kein neuer Release, Commit oder Push in diesem Arbeitsschritt.
