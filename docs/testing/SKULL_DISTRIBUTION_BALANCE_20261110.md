# Schädelhäufigkeit und Verteilung, 10. November 2026

## Anlass und Änderung

Der Living-World-Spieltest mit Beta 1 enthielt in 150.240 gespeicherten Chunks
nur einen Obelisken und den großen Koloss. Eine anschließende Suche mit den
ursprünglichen serverfähigen Mods reproduzierte den Obelisken und fand die
nächsten anderen Relikttypen erst in 13.307 bis 29.744 Blöcken Entfernung
vom Spawn. Das sind Einzelfunde dieses Setups, keine allgemeine Seed-Statistik.

Neue Presets verwenden Generierungsrevision 2 und die Plan-Kennung
`relics-distribution-v4-discoveries`:

- Je Schädeltyp 15 % außerhalb und 25 % innerhalb von Obeliskgebieten.
- Passende Landschaften für alle Familien, einschließlich klassifizierter
  Modpack-Biome. Freigabe und Flächenprüfung verwenden dieselbe Auswahl.
- Schwertschädel mit ±8 statt ±4 Blöcken relativer Höhentoleranz.
- Bis zu 64 nahe Positionen pro großer Koloss-Zelle; Prüfung nach Entfernung.
- Koloss-Mindestentfernungen 4.000 / 8.000 / 15.000 für Entdeckungen,
  Ausgewogen und Expedition. Bei ungeeignetem Gelände erweitert sich die Suche.

Die übrigen Reliktanteile, Modelle, Belohnungen und Mindestabstände bleiben
erhalten. Eine maximale Reisestrecke oder garantierte Fundrate wird nicht
behauptet.

## Schutz bestehender Welten

Fehlende `generationRevision` bedeutet Revision 1. Diese behält ausdrücklich
ihre alte Würfelanordnung einschließlich Leerbereichen, Biom-/Geländeprüfungen
und Koloss-Suchreihenfolge. Die gepinnten Strukturressourcen werden nicht
geändert. Ältere Modversionen lehnen die neue v4-Kennung ab. Unpassende
Kombinationen aus Plan-Kennung und Generierungsrevision werden zurückgewiesen. Neue Vorgaben werden nicht auf gespeicherte Weltpläne übertragen.

## Prüfung

Die gezielten Java-Tests bestehen mit 30 synthetischen Geländeseeds:

- 22 Assertions zu Herkunft, Zurückweisung und Erhalt von Weltplänen.
- 1.008 Assertions zum Worldgen-Executor und seinen Abhängigkeiten.
- 755.716 Assertions zur versionierten Positionssuche.
- 198.942 Assertions zur Verteilung.
- 205.769 Assertions zu Einstellungen, Presets und Kompatibilität.

Sie prüfen unter anderem alte Würfelbelegungen, deterministische Suchfortsetzung,
Biom-/Wasserschutz, beide nativen Höhenbereich-Kodierungen und die gespeicherte
Revision. Das ist kein Nachweis realer Minecraft-Funddichten. Der
Fabric-1.21.1-Kandidat wurde erfolgreich gebaut. Die 195 Python-Tests bestanden;
die CI prüft die unterstützten acht Loader-/Minecraft-Ziele zusätzlich.

## Native Prüfung

Der geprüfte Fabric-1.21.1-Spielerbuild stammt aus `bde1834` und hat SHA-256
`82ab2162a06e42bbb35dfdcf05308bf97afe1262212da3c4dc07e794afa28124`.
Das Diagnosemod wird separat geladen und ist nicht Teil des Spielerbuilds.

Eine Kopie der gelieferten Spieltestwelt wurde mit genau diesem Kandidaten
geöffnet. Die bekannten Positionen von Obelisk und gekröntem Schädel wurden
reproduziert. Nach sauberem Serverstopp waren `relics_distribution_v1.json`
und `relics_gameplay_v1.json` bytegleich mit den Eingaben. Dieser erfolgreiche
Bestandstest stammt aus `native-v3/legacy-preservation`; der anschließende
Dichtelauf dieses Versuchs scheiterte an einer Diagnose-Suchgrenze und gilt
ausdrücklich nicht als bestandener Gesamtlauf.

Der anschließende Vergleich verwendet den nativen Generator mit den
serverfähigen Mods des Spieltests, einschließlich Tectonic 3.0.28,
Terralith 2.6.2, Biomes O' Plenty 21.1.0.14 und Lithostitched 1.8.0.
Die Ausgangsvariante liest die tatsächlich gespeicherten Einstellungen:
2.000er Raster, 800 Blöcke Reliktabstand, 6.000 Obeliskabstand,
2.400 Gebietsradius, 4.000 Kolossminimum, alte Schädelanteile sowie
Standardbiome für alle Familien außer dem Koloss. Sie ist kein nachträglich
angenommenes Werkspreset.

Je Seed werden dieselben 24 × 24 km um den tatsächlichen Weltspawn mit
Ausgangseinstellungen, Expedition, Ausgewogen und Entdeckungen geprüft.
Gezählt werden akzeptierte gewöhnliche Produktionspläne mit Mittelpunkt im
Fenster; der einzigartige Koloss wird separat ausgewiesen. Gelände,
Biom-Fußabdruck, Abstände, Obeliskgebiete und Kolossreservierung werden geprüft.
Die Angabe zum nächsten Schädel bezieht sich ausschließlich auf dieses Fenster.
Sie ist keine unbeschränkte globale Nächste-Nachbar-Suche.

Die Server laufen nacheinander mit einer CPU, maximal 5 GiB im Scope,
3 GiB Java-Heap und niedriger I/O-Priorität. Verwendet werden isolierte Kopien
unter `build/`, keine Launcherprofile. Roharchive und Spielstanddaten bleiben
außerhalb des Repositories.

### Spieltest-Seed 2090676289

Spawn `(-336, 80)`, Fenster X `[-12336, 11664)` und Z `[-11920, 12080)`.
Die Tabelle zählt gewöhnliche Relikte; Entfernungen sind auf ganze Blöcke
gerundet und werden vom Weltspawn gemessen.

| Einstellung | Obelisken | Gekrönte Schädel | Schwertschädel | Andere | Gesamt | Kolossentfernung | Nächster Schädel im Fenster |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gespeicherter Spieltest | 3 | 0 | 0 | 0 | 3 | 20.025 | keiner |
| Expedition, Revision 2 | 0 | 0 | 0 | 0 | 0 | 16.273 | keiner |
| Ausgewogen, Revision 2 | 2 | 2 | 2 | 2 | 8 | 12.933 | 8.356 |
| Entdeckungen, Revision 2 | 2 | 0 | 4 | 3 | 9 | 5.675 | 5.334 |

Ausgewogen akzeptiert außerdem einen kleinen Koloss und einen Turm;
Entdeckungen zwei Türme und einen Weltenbaum. Dieser Seed zeigt mehr
Schädelfunde und einen näheren Koloss, aber auch die Grenzen eines Presets:
Expedition bleibt im Fenster leer, und Entdeckungen enthält hier keinen
gekrönten Schädel. Ein kleineres Raster garantiert nicht mehr Exemplare jeder
Familie in einem einzelnen Gebiet.

### Natürliche Platzierung und offene Abnahme

Eine getrennte Welt mit Ausgewogen reproduzierte unabhängig Einstellungen,
Spawn, Generator-Fingerabdruck und Kolossziel der Zählauswertung. Dort wurden
der Koloss und beide Schädeltypen durch normale Chunk-Generierung materialisiert,
gespeichert und nach sauberem Serverstopp gegen das ausgelieferte NBT geprüft.
Der gesamte Platzierungstest **besteht noch nicht**:

- Gekrönter Schädel: 22.130 geprüfte Modellblöcke stimmen; keine fehlenden
  Chunks, keine ungestützten Bodenkontakte und vollständige Schutzmasken.
- Schwertschädel: alle 25.149 Modellblöcke stimmen und sind geschützt.
  Die Kontaktprüfung meldet jedoch **71 ungestützte kurze Bodenlücken**;
  zusätzlich sind 38 längere Freiräume nach der bestehenden Kontaktregel
  zulässig. Die Ursache der kurzen Lücken ist noch nicht geklärt. Die
  ausgewählte Stelle wurde durch die erweiterten Geländeregeln ermöglicht.
- Koloss: 263.974 von 263.977 geprüften Modellblöcken stimmen. Die drei
  Abweichungen sind die vorgesehenen Laufzeit-Ersetzungen durch Vault,
  Trial-Spawner und Truhe. Der Prüfer berücksichtigt diese Gameplay-Marker
  bisher nicht. Bodenanbindung und Schutzmasken bestehen.
- Es wurden keine fehlenden Modell-Chunks, Lesefehler oder Überlappungen
  zwischen diesen drei Relikten festgestellt. Das hebt die fehlgeschlagene
  Kontaktprüfung nicht auf.

Der erste Ladeversuch des Kolossgebiets überschritt das 60-Sekunden-Limit
des Testskripts. Ein begrenzter Wiederholungslauf mit längerem Limit generierte
und speicherte alle Modelle. Thread-Dumps zeigten währenddessen aktive native
Generierung. Das Skript lädt künftig kleine Chunk-Gruppen, damit zwischen
Abschnitten Server-Ticks möglich bleiben.

Der Downgrade-Test wurde separat gegen die veröffentlichte Beta-1-Binary
ausgeführt: Sie lehnt den gespeicherten v4-Plan ohne Schreibzugriff ab. Eine
wegwerfbare Kontrollkopie mit v3-Kennung und korrekter Prüfsumme wird akzeptiert.
Damit ist die Zurückweisung der neuen Kennung zugeordnet.

Vor der Freigabe des PRs bleiben offen:

1. Kurze Bodenlücken des Schwertschädels erklären und eine geeignete Korrektur
   beziehungsweise Geländegrenze nachweisen; die Prüfung bleibt streng.
2. Den Blockprüfer auf die freigegebenen Gameplay-Marker abstimmen und erneut
   prüfen, ohne beliebige Blockabweichungen zu erlauben.
3. Den geplanten zweiten nativen Seed `731204` auswerten. Bislang liegt nur
   der oben dokumentierte vollständige Dichtevergleich vor.

Die Rohbelege liegen lokal unter `build/skull-balance/`: Zählbericht
`native-v4/seed-2090676289/balance-audit.json` und Platzierungsbericht
`natural-balanced-v3/seed-2090676289/natural-block-verification.json`.
Der Zählbericht ist vollständig; dessen kombinierter Controllerlauf endete
anschließend wegen des fehlenden gekrönten Schädels im Entdeckungen-Fenster
mit Fehler. Der getrennte Platzierungslauf endete wegen der oben genannten
Kontakt-/Markerbefunde mit Fehler. Keiner wird als bestandener Gesamtlauf
ausgegeben. Rohdateien und Spielstände werden nicht veröffentlicht.

Das separate Diagnosemod `DiscoveryBalanceChecks` ersetzt weder einen
Survival-Durchlauf noch eine allgemeine Leistungs- oder Shaderfreigabe.

Der ursprüngliche DH-Modus FEATURES bleibt eine bekannte Einschränkung.
Die Messung erfolgt ohne DH-Hintergrundgenerierung; sie repariert keine alten
DH-Chunks und beansprucht keine solche Reparatur.
