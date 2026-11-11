# Creative-Spieltest vom 11. November 2026, Nachmittag

Der Spieltest bestätigt vollständige Relikt-Grundflächen und einen großen Koloss
knapp oberhalb des eingestellten Mindestabstands. Die Bodenkontaktprüfung des
Schwertschädels besteht weiterhin nicht. Das verbliebene Savannendorf am Koloss
liegt im vorgesehenen Behalten-Zweig des Gebäudefilters. Eine gemessene
Halbierung von Überschneidungen lässt sich aus diesem Archiv nicht ableiten.

## Grundlage und Grenzen

Ausgewertet wurde das über LocalSend empfangene `beta test.zip` mit 599.178.808
Bytes. SHA-256, zusammengefasste Messwerte und Prüfergebnisse stehen in
[der Belegdatei](user-playtest-20261111-afternoon-evidence.json).
Roharchiv, Spielstand, Logs und Aufnahme bleiben privat unter `build/` bzw. im
LocalSend-Eingang. Die Analyse liest den Save offline; Minecraft wurde damit
nicht gestartet und der Save nicht verändert.

Die Logs zeigen Minecraft 1.21.1, Fabric Loader 0.19.5 und die Mod-Versionszeichenfolge
`1.0.0-beta.3` im Living-World-Modpack. Die Zeichenfolge identifiziert keinen
bestimmten PR-Commit. Weltplan und Start-Zertifikate belegen
`relics-distribution-v5-colossus-search`, Generierungsrevision 3,
Gebäudefilter-Revision 1 und eingefrorene Innenräume `interiors-20261028-v5`.
Die SHA-256-Prüfungen der Verteilungs- und Gameplay-Journale bestehen.

Aktiv sind Entdeckungen/Landschaften, ein 2.000er Raster, 800 Blöcke
Relikt-Mindestabstand und 4.000 Blöcke Koloss-Mindestabstand. Alle sieben
Familien verwenden Landschaftsbiome. Die gespeicherte Gebäuderegel stammt
noch aus dem Stand vor der Korrektur der Mansion-ID in PR #3. Dieser Save
prüft daher nicht die korrigierte Mansion-Behandlung.

Die aktuelle Sitzung reicht von 13:34 bis 14:00 Uhr laut Log. Relikte wurden
mit `/locate` und Teleport aufgesucht. Sechs getrennte Besuchsgebiete sind kein
unabhängiger Dichtescan und keine Survival-Abnahme. Der Test erfolgte mit
weiteren Mods. Für eine Prüfung ausschließlich mit Minecraft, Loader und
Titan Relics gilt dieser Spieltest daher nicht.

## Verteilung und PR #2

Die Entfernungen beziehen sich einheitlich auf den gespeicherten Weltspawn
X = -64, Z = 96. Die Chat-Ausgabe misst dagegen vom jeweiligen Spielerstandort
und weicht deshalb geringfügig ab. Die Tabelle zeigt die Locate-Ziele dieser
Sitzung; sie behauptet keine erneute globale Nächste-Nachbar-Suche vom Spawn.

| Relikt | X | Z | Luftlinie vom Spawn | Besuch im Save |
|---|---:|---:|---:|---|
| Gekrönter Schädel | -568 | 1224 | 1.235 Blöcke | ja |
| Schwertschädel | -1032 | -3528 | 3.751 Blöcke | ja |
| Großer Koloss | -2952 | -2808 | 4.096 Blöcke | ja |
| Obelisk | 5352 | -1240 | 5.578 Blöcke | nur gesucht |
| Kleiner Koloss | 2472 | -10808 | 11.195 Blöcke | ja |
| Turm | -4440 | 13272 | 13.884 Blöcke | ja |
| Weltenbaum | -16264 | -6296 | 17.415 Blöcke | ja |

Die feinere Koloss-Suche hat nach 456 groben und 51 feineren Kandidaten ein
Ziel gefunden. Der große Koloss liegt nur 96 Blöcke über dem eingestellten
Mindestabstand. Die beiden Schädel sind in diesem Seed vergleichsweise nah.
Turm, kleiner Koloss und Weltenbaum bleiben deutlich weiter entfernt. Daraus
folgt keine garantierte Fundhäufigkeit für andere Seeds oder Modpacks.

## Überschneidungen und PR #3

Der Scan liest 31.687 gespeicherte Overworld-Chunks ohne Fehler. Davon sind
14.012 vollständig generiert; die übrigen liegen in früheren Generierungsstufen.
Sechs gültige Reliktstarts und 554 andere Strukturstarts sind gespeichert.
Diese Zahlen dürfen nicht als Reliktdichte einer zusammenhängend erkundeten
Fläche interpretiert werden.

Ein Savannendorf mit Startchunk X = -192, Z = -179 überschneidet die Koloss-
Bounding-Box. 66 seiner Stück-Bounding-Boxen schneiden die Relikt-Bounding-Box.
Das ist keine voxelgenaue Prüfung jedes Dorfblocks. Die gespeicherte Seed-
und Startkoordinate ergibt mit der Produktionsregel `selected = false`.
Dieses Dorf soll deshalb erhalten bleiben. Die Überschneidung ist kein
Nachweis einer Fehlfunktion der gewünschten 50-%-Regel.

Für die anderen fünf gespeicherten Relikte findet der Scan keine Überschneidung
mit fremden Struktur-Bounding-Boxen. Das Archiv enthält keinen Vergleichslauf
ohne Filter. Es beweist weder eine bestimmte Unterdrückungsquote noch, welche
nicht gespeicherten Gebäude der Filter tatsächlich entfernt hat. Der getrennte
native Vorher-/Nachher-Test aus PR #3 bleibt dafür der Beleg.

## Modellprüfung und offener Bodenkontakt

Der Offline-Prüfer vergleicht 1.054.682 Modellblöcke mit den eingefrorenen
V5-Ressourcen aus dem vorhandenen PR-3-Kandidaten. Dessen Hash steht in der
Belegdatei; er beweist nicht den Hash der vom Spieler verwendeten JAR.
Bei allen sechs Relikten sind die benötigten Chunks vollständig vorhanden.
Es gibt keine Lese- oder Verifikationsausnahme.

Das rohe Gesamtergebnis des strikten Prüfers bleibt **fehlgeschlagen**.
Die Abweichungen werden eingeordnet, ohne seine Regeln abzuschwächen:

- Der gekrönte Schädel besteht vollständig, einschließlich Bodenkontakt und Schutzmaske.
- Unter dem Schwertschädel meldet der Prüfer 43 kurze ungestützte Kontakte.
  Darunter wurden 27 Luftlücken gesondert geprüft. In Beispielen liegen ein
  oder zwei Luftblöcke über festem Boden; diese Füllzellen sind nicht als
  geschützte Platzierungen markiert. Derselbe Befundtyp ist bereits im
  [früheren Bericht](SKULL_DISTRIBUTION_BALANCE_20261110.md) offen.
  Eine neue Regression durch den Gebäudefilter ist damit nicht belegt.
- Der Nutzer bestätigt bewusste Änderungen am Weltenbaum und am Moosblock
  des Schwertschädels. Fehlendes Holz, Lava und verkohltes Holz dienen daher
  nicht als Beleg einer fehlerhaften Generierung. Die Zuordnung jedes einzelnen
  geänderten Blocks wurde nicht unabhängig rekonstruiert.
- Alle 67 als unterschiedlich gemeldeten Glow-Lichen-Zellen des Baums stimmen
  nach korrekter Rotation ihrer Seiten-Eigenschaften. Alle drei vorgesehenen
  Farn-/Wurzelerde-Paare sind vorhanden, geschützt und auf festem Boden.
  Zwei Paare wurden um ein bzw. zwei Blöcke nach oben an das Gelände angepasst.
  Die drei vermeintlich fehlenden Schutzbits betreffen alte Quellpositionen.
- Weitere Abweichungen betreffen Kupferoxidation, Blöcke von Immersive
  Weathering, gerissene Turmfliesen und vorgesehene Gameplay-Ersetzungen.
  Die Fliesenänderungen passen zu Verwitterung im Modpack; ihre genaue
  zeitliche Ursache ist aus dem Endstand allein nicht bewiesen.

Damit ist die kurze Bodenanbindung des Schwertschädels der weiterhin offene
Platzierungsbefund. Die vorhandenen Änderungen und die Grenzen des allgemeinen
Prüfers erlauben keine pauschale Aussage, dass jeder unveränderte Modellblock
und jeder Gameplay-Zustand bestanden habe.

## Loot, Bilder und PR #4

Am großen Koloss sind Vault und Trial-Spawner als passende Block-Entities
vorhanden. Die Armtruhe enthält unter anderem einen Bergungsmagneten.
Die Truhe des kleinen Kolosses ist initialisiert; ihr gespeicherter Inhalt
steht im Beleg. Die untere Turmtruhe enthält fünf Enderperlen. Das sind
beobachtete Endzustände, kein zusätzlicher Nachweis sämtlicher Loot-Chancen,
Entnahmen oder des Wiederbefüllungsschutzes.

Diese Archivwelt verwendet noch Turm V10 und Innenräume V5. Sie kann die neue
obere Truhe aus PR #4 nicht prüfen. Dafür gelten die getrennte
[visuelle Abnahme des Nutzers](tower-upper-chest-author-review-20261111.json)
und der [native V6-Test](tower-upper-chest-native-20261111.json).
Die fünf späteren Turmbilder sind bereits im gemeinsamen Screenshotarchiv
des Repositories gesichert.

Die drei jüngsten Archivbilder zeigen Schwertschädel und Weltenbaum.
Stichproben der rund 29 Sekunden langen Aufnahme zeigen den Aufenthalt am
Weltenbaum und anschließend das Spielmenü, keine Loot-Oberfläche oder
Survival-Reise. In den Logs findet sich keine Titan-Relics zugeordnete
Ausnahme. Fremde Modpack-/Entity-/Soundfehler sind vorhanden; der Server
speichert und beendet die Sitzung sauber.

Es wurden für diese Analyse weder Generierungsregeln geändert noch PRs
gemergt, Releases erstellt oder Plattformdateien ersetzt.
