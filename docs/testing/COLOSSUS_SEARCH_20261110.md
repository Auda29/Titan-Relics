# Feinere Koloss-Suche, 10. November 2026

## Anlass und Verhalten

Im Beta-3-Spieltest mit Seed `701448007947040131` lag der einzige große Koloss
14.178,97 Blöcke vom ursprünglichen Spawn entfernt. Das Preset war Entdeckungen
mit 4.000 Blöcken Mindestabstand. Der gespeicherte Plan verzeichnete 1.555
Prüfpositionen. Einzelne Ablehnungsgründe wurden damals nicht gespeichert.

Die neue Generierungsrevision 3 verwendet die Policy
`relics-distribution-v5-colossus-search`. Die eigene Koloss-Suche arbeitet in
1.000 × 1.000-Blöcke-Zellen und 1.000 Blöcke breiten Entfernungsbändern.
Zunächst werden pro Zelle bis zu 16 flächig verteilte Chunk-Mittelpunkte geprüft.
Wenn deren Mittelpunkt-Biom und Bauhülle passen, folgen bei Bedarf bis zu 48
zusätzliche Positionen in derselben Zelle und demselben Entfernungsband. Erst
danach geht die Suche weiter nach außen. Zusammen decken die beiden Durchgänge
ein 8 × 8-Raster mit einer Position je 125-Blöcke-Teilfläche ab.

Beim Preset Entdeckungen kommen dadurch die Bänder zwischen 4.000 und 8.000
Blöcken vor entfernteren Standorten zum Zug. Ein passender Standort bleibt
Voraussetzung. Es gibt keine erzwungene Platzierung und keine Garantie auf
höchstens 8.000 Blöcke Entfernung oder den mathematisch nächsten Standort.
Innerhalb eines Durchgangs werden die Positionen nach Entfernung sortiert.
Die Nachsuche kann eine nähere Position im selben Band nachträglich prüfen.

Die Geländeprädikate von Revision 2 bleiben identisch. Gewichte, Suchzellen und
Abstandsregeln der normalen Relikte ändern sich nicht. Die neue Position des
Kolosses kann die Freihaltezone und dadurch benachbarte Reliktentscheidungen
verändern.

## Diagnose und bestehende Welten

Das Feld `colossusSearch` im Prüfplan speichert Suchdurchgang, Nachsuchzellen,
Prüfzahlen, abgeschlossene Bänder und die erste Ablehnungsursache jeder
abgelehnten Position. Unterschieden werden Mittelpunkt-Biom, Biom-Fußabdruck,
Baugrenzen, Geländeprädikat und Mindestabstand. Das Geländeprädikat fasst die
bisherigen Höhen-, Trockenheits-, Fluss- und Meeresprüfungen zusammen. Die
Diagnose behauptet nicht, jede gleichzeitig verletzte Bedingung aufzuschlüsseln.

Cursor, Nachsuchzellen und Zähler werden gemeinsam atomar gespeichert. Der
Statusbefehl und das Serverlog enthalten die Ergebnisse. Bestehende Revisionen
1 und 2 behalten ihre Algorithmen, fertig bestimmten Ziele und Suchcursor.
Vorhandene Konfigurationen werden nicht automatisch umgeschrieben. Eine erneute
Preset-Auswahl gilt für künftig erzeugte Welten. Pinned-Strukturen, bestehende
Karten und Belohnungsdaten werden nicht migriert.

## Prüfungen

- Java-Prüfungen für Verteilung, Einstellungen, asynchrone Generierung und
  Weltverträglichkeit sind erfolgreich. Die neue Suchprüfung umfasst 17.887
  Assertions zu flächiger Abdeckung, negativen Koordinaten, endlichen Grenzen,
  Nachsuche, Neustartcursor und unveränderten normalen Reliktentscheidungen bei
  identischem Koloss-Ziel.
- Die vollständigen Revision-2-Kandidatenfolgen in den Bändern 4.000 bis 16.000
  wurden für drei Seeds mit dem veröffentlichten Beta-3-JAR verglichen. Alle
  5.764 Kandidaten einschließlich Reihenfolge stimmen überein. Diese unabhängig
  bestimmten SHA-256-Testvektoren sind als Regressionstest hinterlegt.
- Der originale Revision-2-Prüfplan aus dem neuesten Nutzerarchiv lässt sich
  lesen und bleibt bytegleich. Der veröffentlichte Beta-3-Build lehnt den neuen
  Revision-3-Plan ab; der Kandidat liest ihn erfolgreich.
- Produktions- und Clientquellen für 26.2 sowie Fabric-1.21.1-Produktion und
  Testquellen wurden erfolgreich kompiliert. Der lokale Fabric-1.21.1-Build
  einschließlich der Asset-Prüfung ist erfolgreich.
- Die vollständige Python-Prüfung mit 195 Tests ist erfolgreich.

Der geprüfte, unveröffentlichte Fabric-1.21.1-Kandidat trägt noch die vorhandene
Versionsmetadatenangabe `1.0.0-beta.3`, ist aber **kein Ersatz** für das
veröffentlichte Beta-3-JAR. SHA-256 des Kandidaten:
`27175f8df4f4063400a30c8b6595ceb9df555ec0cc144e025b7a6632d8fb4c26`.
Der Release-Tag und die veröffentlichten Downloads bleiben unverändert.

## Native Messung

Die isolierte Living-World-Fixture verwendet denselben Generator-Fingerabdruck
wie der neueste Nutzer-Spieltest:
`65ea46667546c63df4145e5a606838b4fdacafbe6fed2efb47ab0515cff83830`.
Es werden eigene Testwelten erzeugt. Originalarchive und Spielstände bleiben
unverändert. Minecraft läuft ausschließlich mit den Testwelten. Alle Server
laufen nacheinander mit begrenzter CPU-, RAM- und I/O-Last.

| Seed | Ursprünglicher Spawn X/Z | Koloss-Mittelpunkt X/Z | Abstand vom Spawn | Prüfpositionen |
|---|---|---|---:|---:|
| `701448007947040131` | −272 / −336 | 88 / −4408 | 4.087,88 | 29 |
| `2090676289` | −336 / 80 | 1336 / 4344 | 4.580,10 | 263 |
| `731204` | 0 / 0 | 4792 / 776 | 4.854,42 | 384 |

Alle drei Standorte wurden mit unveränderten nativen Geländeprädikaten im ersten
Band von 4.000 bis 5.000 Blöcken akzeptiert. In diesen drei Fällen genügte der
erste Suchdurchgang; die zusätzliche Nachsuche war nicht erforderlich. Deren
Abdeckung und gespeicherter Cursor sind durch die gezielten Java-Prüfungen
abgedeckt.

Alle sechs Serverläufe sind erfolgreich und wurden mit Exitcode 0 beendet.
Nach einem Neustart jeder Testwelt blieben der gesamte gespeicherte Prüfplan,
die Zielposition und die Diagnosezähler identisch. Die native Evidenz enthält
die Artefakt-Prüfsumme, den Generator-Fingerabdruck und die getrennt erfassten
bekannten Meldungen des Referenz-Modpacks. Es gab keine zusätzlichen
Fehlermeldungen.

Für den neuesten Nutzer-Seed sinkt der gemessene Abstand gegenüber dem
gespeicherten Beta-3-Plan von 14.178,97 auf 4.087,88 Blöcke. Die Zahl geprüfter
Positionen sinkt von 1.555 auf 29. Der Spawn und der Generator-Fingerabdruck
stimmen mit dem bereitgestellten Test überein. Das ist ein Vergleich separater
Welten, keine Änderung des vorhandenen Spielstands und keine allgemeine
Erfolgsgarantie über alle Seeds.

Ein erster Prüflauf überschritt sein zu knappes Startzeitlimit von 180 Sekunden
während der gewöhnlichen Spawn-Vorgenerierung. Seine Suchauflösung fand bereits
den neuen Standort, aber dieser Lauf gilt nicht als vollständig bestanden. Der
Folgelauf verwendet ein längeres Zeitlimit und einen separaten Test-Mod, der
ausschließlich den Spawn-Chunk-Radius auf 0 setzt. Gelände- und Suchregeln werden
dabei nicht verändert. Dieser Test-Mod ist nicht im Spieler-JAR enthalten.

Der erste vollständige Serverlauf wurde vom Controller zunächst wegen bereits
vorhandener Data-Fixer- und Moonlight-Meldungen des Modpacks beanstandet. Die
exakten Meldungen wurden mit dem unveränderten Referenzlog abgeglichen. Der
Controller zeichnet diese bekannten Meldungen und die SHA-256 des Referenzlogs
gesondert auf; zusätzliche Fehlermeldungen führen weiterhin zum Abbruch. Frühere
Fehlerbelege bleiben erhalten. Die Fortsetzung prüft den gespeicherten Standort
und die Eingabe-Hashes, bevor sie einen Testlauf wieder aufnimmt.

Reproduktion mit einer vorhandenen isolierten Fabric-1.21.1-Fixture:

```sh
python3 tools/check_colossus_search.py \
  --fixture build/user-playtest-20261110/locate-run \
  --artifact build/colossus-search/relics-1.0.0-beta.3+mc1.21.1.jar \
  --checks compat/alpha5-fabric-1.21.1/build/libs/relics-alpha5-port-checks+mc1.21.1.jar \
  --java build/toolchains/jdk-21.0.13+9/bin/java \
  --seed 701448007947040131 --seed 2090676289 --seed 731204 \
  --restart --output build/colossus-search/native-final \
  --timeout 600 --accept-eula
```

Private Rohbelege liegen unter `build/colossus-search/`. Eine Suchauflösung
belegt einen vom nativen Generator akzeptierten Standort. Sie ersetzt weder
eine vollständige Block-/Kontaktprüfung des platzierten Modells noch einen
Survival-Test der allgemeinen Reliktdichte. Die offenen Abnahmen im
[bisherigen Balancebericht](SKULL_DISTRIBUTION_BALANCE_20261110.md) bleiben offen.
