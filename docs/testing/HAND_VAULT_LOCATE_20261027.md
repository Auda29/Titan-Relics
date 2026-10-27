# Schlüsselverbrauch, Magnethände und Reliktsuche

Umsetzung nach Niklas' Spieltest vom 27. Oktober 2026, Minecraft 26.2 / Fabric.
Dieser Stand ergänzt die vorherigen Berichte zu Innenräumen, Präsentation und
echten Belohnungsauswürfen.

## Vault

Ein erfolgreicher Vault-Klick verbraucht jetzt sofort genau einen Schlüssel.
Der Verbrauch wird durch einen gesonderten Spielerbeleg auf der Platte bestätigt.
Danach folgen Öffnung, Ausgabephase und der eigenständige Kern als Weltgegenstand.
Das spätere Aufheben des Kerns verbraucht keinen weiteren Schlüssel.

Bezahlte, noch nicht ausgegebene Kerne speichern `keyPaid`. Sie bleiben bei
Neustart oder einem gerade durch einen anderen Spieler belegten Vault in der
Warteschlange, ohne erneut einen Schlüssel zu verlangen. `PAYMENT_PENDING`
unterscheidet einen unterbrochenen Zahlungsschritt von der späteren
Entity-Reservierung und Aufnahme. Eine unklare Zahlung wird gehalten, statt
noch einmal zu belasten oder ungesichert einen Kern auszugeben. Bestehende
unbezahlte Warteschlangen bleiben unterstützt. Vorhandene Auswürfe und bereits
abgeschlossene Ansprüche werden nicht neu erzeugt.

Der echte Servertest prüft unmittelbar nach dem Klick null Schlüssel und null
Kerne im Inventar sowie den gespeicherten Zahlungsstatus. Das gilt auch für
einen zweiten Teilnehmer, dessen Auszahlung auf das Ende der ersten Animation
warten muss. Derselbe liegende Kern bleibt nach Neustart erhalten und wird
anschließend ohne weitere Zahlung abgeholt. Beide Spieler erhalten jeweils
genau einen Kern. Hopper- und Fremdspieler-Schutz sowie die Abweisung alter,
bereits quittierter Entity-Snapshots bleiben geprüft.

## Magnet

Ein geladener Magnet wirkt in der ausgewählten Haupthand oder in der Nebenhand.
Ein Magnet in einem anderen Inventar- oder ungewählten Hotbarplatz bleibt
inaktiv. Sind beide Hände mit geladenen Magneten belegt, wird die Haupthand
verwendet. Nur dieser Magnet verliert bei erfolgreicher Aufnahme einen Punkt.
Ein leerer Magnet in der Haupthand blockiert keinen geladenen in der Nebenhand.
Reichweite, Kollisionsprüfung, Survival/Adventure und die vorige Erhöhung der
Bewegung um zehn Prozent bleiben bestehen. Beide Übersetzungen nennen nun
Haupt- und Nebenhand.

Der Servertest bewegt und sammelt Drops mit beiden Händen. Die Höchstgeschwindigkeit
bleibt jeweils ungefähr 0,385 Blöcke pro Tick. Eine Aufnahme belastet nur den
aktiven Magneten. Anschließend werden beide Magnete in ungewählte Inventarplätze
gelegt: Ein frischer ruhender Drop wird über 24 Ticks weder angezogen noch
aufgenommen.

## Warum die anderen Relikte fehlten

Die Einstellungen und die installierte JAR der Testwelt
`Relic Alpha 5_0 Terrain 3` wurden nur gelesen. Seed:
`7176494076711744605`. Alle sieben Familien sind aktiviert. Der eingefrorene
Fingerprint lautet
`1065c923e12c1ea34e951a9bfee90bdbea46f3d977573aad572b8a75b3969097`.
Die Welt verwendet normalen Overworld-Noise mit den üblichen Biomen.

Die bisherige Suche prüfte wiederholbare Relikte nur innerhalb von 100.000
Blöcken um den jeweiligen Befehlsursprung. Der große Koloss liegt bereits bei
`-68776, -12600`. Von dort ist der nächste kleine Koloss 119.018 Blöcke entfernt,
der Weltenbaum 207.483 Blöcke. Für diese Typen war die Meldung über den leeren
alten Suchbereich korrekt. Das bedeutet keine Abwesenheit in der gesamten Welt.
Die Turmruine liegt näher und ist mit der vollständigen Typkennung auffindbar.

Die asynchrone Suche erreicht jetzt 500.000 Blöcke. Sie prüft nur Tickets, die
den angefragten Typ in mindestens einer der beiden Obelisk-Regionklassen liefern
können. Das überspringt unmögliche Typen ohne neue Geländeentscheidungen oder
geänderte Seltenheiten. Alle 10.000 Tickets wurden für jede Familie gegen beide
Regionfälle geprüft. Der große Koloss verwendet weiterhin sein gespeichertes
weltweites Ziel.

Alle fünf Ziele stimmen mit einem zusätzlichen ungefilterten 500.000-Block-
Referenzlauf überein. Der neue Lauf benötigt in dieser Reihenfolge etwa 15, 5,
58, 68 und 6 Sekunden; das sind keine zugesicherten Antwortzeiten. Besonders
seltene Typen können weiter längere Hintergrundsuchen benötigen.

Bestätigte Ziele ausgehend vom großen Koloss:

- Kleiner Koloss: `31560, -76616`.
- Turmruine: `-123320, 5336`.
- Weltenbaum: `134136, -55912`.
- Gekrönter Titanschädel, Sandvariante: `59368, 51752`.
- Titanschädel 2: `-123688, 88584`.

Vollständige Befehle für die jeweilige Suche:

```text
/locate structure #relics:small_colossus
/locate structure #relics:ruined_tower
/locate structure #relics:world_tree
/locate structure #relics:titan_skull
/locate structure #relics:titan_skull_2
```

`#relics:` allein ist keine Typkennung. Der vorhandene Sammel-Tag heißt
`#relics:relics`; er findet aber auch einen nahen bereits bekannten Koloss und
ersetzt deshalb nicht die gezielte Suche nach einem anderen Typ.

Kleiner Koloss und Weltenbaum wurden in einer separaten Welt mit identischem
Seed, Generator und Fingerprint über natürliche Starts vollständig generiert.
Alle 477.336 geprüften festen Modellzellen stimmen, zusätzliche Freiräume und
ihre Schutzmasken ebenfalls. Die Nutzerwelt wurde nicht in Minecraft geöffnet oder verändert.
Weder Verteilungspolitik noch Geländeregeln oder Innenraumexporte ändern sich.

## Build und Nachweise

`dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`

SHA-256: `caffeb247121ee1ea501ecf68eaa1c2af07801420c7dbeb5cae636f9d041acfe`.

Zwei Builds sind bytegleich. 663 Gameplay-Assertions, 52 statische
Mixin-Verträge, 1.008 Executor-Prüfungen, 755.716 Suchprüfungen,
198.924 synthetische Verteilungsprüfungen und sechs Ressourcentests bestehen.
Die Serverläufe verwenden zwei Survival-Testspieler mit Paketempfängern.
Die grafische Darstellung bleibt im tatsächlichen Client zu bestätigen.
Beliebige harte Abbrüche zwischen getrennten Spieler-, Entity- und Journaldateien
sind weiterhin keine bewiesene gemeinsame Datentransaktion.

Maschinenlesbare Belege:
[hand-vault-locate-20261027-evidence.json](hand-vault-locate-20261027-evidence.json).

```powershell
$jdk = 'build/toolchains/zulu25.36.205-ca-jdk25.0.4.1-win_x64'
python tools/test_gameplay.py --java-home $jdk
python tools/test_distribution.py --java-home $jdk
python tools/build.py --skip-generation --java-home $jdk
python tools/test_gameplay_presentation_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar
python tools/test_relic_locate_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar
```
