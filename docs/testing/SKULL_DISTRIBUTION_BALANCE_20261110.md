# Schädelhäufigkeit und Verteilung, 10. November 2026

## Anlass und Änderung

Der Living-World-Spieltest mit Beta 1 enthielt in 150.240 gespeicherten Chunks
nur einen Obelisken und den großen Koloss. Eine anschließende Suche mit den
ursprünglichen serverfähigen Mods reproduzierte den Obelisken und fand die
nächsten anderen Relikttypen erst in 13.307 bis 29.744 Blöcken Entfernung
vom Spawn. Das sind Einzelfunde dieses Setups, keine allgemeine Seed-Statistik.

Neue Presets verwenden Generierungsrevision 2:

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
geändert. Neue Vorgaben werden nicht auf gespeicherte Weltpläne übertragen.

## Prüfung

Die gezielten Java-Tests bestehen mit 30 synthetischen Geländeseeds. Sie prüfen
unter anderem alte Würfelbelegungen, deterministische Suchfortsetzung,
Biom-/Wasserschutz und die gespeicherte Revision. Das ist kein Nachweis realer
Minecraft-Funddichten. Der Fabric-1.21.1-Kandidat wurde erfolgreich gebaut.

Die quantitative Prüfung gegen den nativen Living-World-Generator wird vor
Abschluss dieses PRs ergänzt. Das separate Diagnosemod
`DiscoveryBalanceChecks` zählt tatsächlich akzeptierte Produktionspläne in
einem festgelegten Fenster. Es ersetzt weder einen Survival-Durchlauf noch
eine allgemeine Leistungs- oder Shaderfreigabe.

Der ursprüngliche DH-Modus FEATURES bleibt eine bekannte Einschränkung.
Die Messung erfolgt ohne DH-Hintergrundgenerierung; sie repariert keine alten
DH-Chunks und beansprucht keine solche Reparatur.
