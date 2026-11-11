# Verteilung auf Vanilla-Gelände, 11. November 2026

## Ergebnis

Die Reliktstandorte und die geprüften festen Modellblöcke stimmen zwischen dem
Stand aus PR #2 und dem Gebäudefilter aus PR #3 überein. Beide Welten behalten
beim erneuten Laden ihre Journalbytes, Strukturstarts und Modellproben. Die
alte Welt bekommt beim Wechsel auf den Filter-Build keine neue Gebäuderegel.

Im regulären Raster dieses Seeds bleiben allerdings nur vier gewöhnliche
Relikte und der einzigartige große Koloss. Die dünne Verteilung besteht schon
im Vergleichsstand ohne Gebäudefilter. Dieses Ergebnis ist kein Nachweis einer
allgemeinen Häufigkeit über mehrere Seeds. Es rechtfertigt eine getrennte
Prüfung der Biomen- und Geländeanforderungen für das Preset Discoveries.
Die Verteilungsparameter wurden bei diesem Test nicht angepasst.

Eine konkrete Ressourcenlücke wurde korrigiert: Die Vanilla-Struktur heißt
`minecraft:mansion`, nicht `minecraft:woodland_mansion`. Der zuvor optionale
falsche Eintrag konnte Waldanwesen nicht in den Filter aufnehmen. Alle elf
Vanilla-Ziel-IDs der korrigierten Tagdatei existieren in den offiziellen
Server-JARs von Minecraft 1.21.1 und 26.2. Die Änderung betrifft den Gebäudefilter
neuer Welten; gespeicherte Richtlinien bleiben eingefroren.

## Aufbau

- Minecraft Java 1.21.1, Fabric Loader 0.19.5 und Java 21.0.13+9.
- Nur Titan Relics, Fabric API 0.116.17+1.21.1 und Lithostitched 1.8.0.
- Keine Terrain- oder zusätzlichen Strukturmods, keine Shader oder externen Datapacks.
- Zusätzlicher privater Diagnosehelfer für lesenden Zugriff auf den echten
  Planer und Abfragen natürlicher nativer Strukturstarts und Modellblöcke.
  Keine geänderten Tickets, Platzierungsregeln oder künstlich platzierten Relikte.
- Seed `-4443928181842649648`, Preset Discoveries, Biomenmodus Landschaften.
- Ein serieller Java-Prozess, eine CPU, niedrige I/O-Priorität, isolierte Welten.

Das reguläre Raster enthält 81 Suchzellen mit je 2.000 Blöcken Kantenlänge.
Es umfasst X und Z von -8.000 bis 9.999, also 18 × 18 Kilometer. Vier zusätzliche
Zellen decken die weiter entfernten, gezielt per `/locate` gefundenen Familien ab.
Diese Zusatzbesuche zählen nicht zur Häufigkeit im regulären Raster.

Verglichen wurden zwei vorhandene Spieler-JARs:

- PR #2, feinere Koloss-Suche, ohne Gebäudefilter:
  `27175f8df4f4063400a30c8b6595ceb9df555ec0cc144e025b7a6632d8fb4c26`.
- PR #3, Laufzeitstand `e7a0d85`:
  `10b12bfe0f3ceea14d50f8ec0afc2feb2ce549d64522e6c071a0652681571dfe`.

Die nativen Vergleichsläufe prüfen damit den bisherigen PR-Build vor der
anschließenden Korrektur der Waldanwesen-ID. Diese kleine Ressourcenkorrektur
wurde zusätzlich gegen die oben genannten offiziellen Struktur-Registrierungen
geprüft; sie ändert keinen Planer- oder Generierungsalgorithmus.

## Beobachtungen

Im regulären Raster stehen drei Schwertschädel und ein Obelisk. Der große
Koloss liegt zusätzlich etwa 4.220 Blöcke vom gespeicherten Weltspawn entfernt.
Zwischen dem gefundenen Obelisken und dem Koloss liegen etwa 2.544 Blöcke.
Der Locate-Test des gekrönten Schädels sucht dabei nur die normale Palette,
nicht das nächste Exemplar über alle Schädelpaletten hinweg.
Alle gewöhnlichen Standorte einschließlich der vier zusätzlichen Besuchszellen
sowie das eindeutige Koloss-Ziel sind im Vergleich identisch.

Alle sieben Familien liefern an ihren `/locate`-Koordinaten einen gültigen
natürlichen Strukturstart. Je Familie wurden drei feste Vorlagenblöcke in
vollständig generierten Chunks gelesen. Alle 21 Blöcke stimmen mit der
mitgelieferten Vorlage überein und bleiben in allen vier Läufen identisch.
Das ist eine gezielte Generierungsprobe, keine vollständige Prüfung jedes
Modellblocks und keine Prüfung der Belohnungen oder Survival-Balance.

Von 158 abgefragten potenziellen Fremdstruktur-Starts sind 59 gültig:
53 Minen und sechs oberirdische Bauten. Die sechs Bauten bestehen aus vier
Dörfern, einem Außenposten und einem Wüstentempel. Keiner ihrer nativen
Bauwerksteile überschneidet im untersuchten Satz die Grundfläche eines
geprüften Relikts. Entsprechend wird keiner dieser Starts ausgelassen.
Alle bleiben mit derselben Gültigkeit und derselben Zahl von Teilen erhalten.
Frische Starts stimmen zwischen beiden Builds exakt überein, ebenso die
neu geladenen Starts. Minecraft berechnet beim Laden die Begrenzungsboxen
von Pool-Teilen erneut aus den Vorlagen; bei fünf Starts werden dadurch
vergrößerte Planungsboxen kleiner. Diese Änderungen sind im Kontrolllauf
und im Filterlauf exakt gleich. Der native Lade-Konstruktor von
`PoolElementStructurePiece` bestätigt die Neuberechnung. Der Filter meldet
null Unterdrückungen. Alle vier Java-Prozesse enden mit Exitcode 0 und ohne
ERROR-Einträge in ihren nativen Serverlogs.

Dieser Vanilla-Test weist daher keine positive 50-%-Unterdrückung nach.
Der positive native Kollisionsnachweis mit einem vollständigen ausgelassenen
Dorf steht im separaten [Living-World-Testbericht](SURFACE_STRUCTURE_FILTER_20261111.md).
Die hier beobachtete geringere Zahl von Überschneidungen ist eine Stichprobe
mit Vanilla-Strukturen, keine Häufigkeitsgarantie für andere Seeds oder Modpacks.

## Belege und Grenzen

Der [kompakte maschinenlesbare Beleg](vanilla-distribution-20261111.json)
enthält die Standorte, Hashes, Blockproben und Ergebnisse aller vier Läufe.
Ausführliche Logs, Ergebnisse und die isolierten Welten liegen lokal unter
`build/vanilla-creative-playtest-20261111/native-comparison/`.

Vor der Eingrenzung auf Generierungsdaten wurden auch ein grafischer Client
und Creative-Teleports zum Obelisken gestartet. Diese Kameraversuche sind
kein zusätzlicher Freigabenachweis und werden nicht als Veröffentlichungsgalerie
übernommen. Auf Wunsch des Nutzers konzentriert sich die Auswertung auf die
Verteilung und die Änderungen der beiden PRs.

Es gibt keine Aussage zur natürlichen Reisedauer, Survival-Balance, vollständigen
Loot-Interaktion oder Performance unter normalen Spielbedingungen. Der native
Vergleich verwendet einen Seed und Minecraft 1.21.1; die anderen Loader und
Spielversionen werden hier nicht als nativ spielgetestet ausgewiesen.
