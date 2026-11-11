# Schwertschädel und fallender Modpack-Boden, 11. November 2026

Der eingesendete Creative-Save meldete 43 kurze ungestützte Kontakte unter dem
Schwertschädel. Eine neue isolierte Welt mit demselben Seed, denselben
gespeicherten Einstellungen und dem Living-World-Serverfixture reproduziert
42 Kontakte. Alle 25.149 Modellblöcke stimmen dort exakt. Zufällige Blockticks
sind vor der Generierung des Zielgebiets abgeschaltet. Der Befund besteht
also auch unabhängig von den bestätigten Spieleränderungen.

## Ursache

Die gezielte Laufzeitdiagnose an zwei betroffenen Spalten zeigt
`immersive_weathering:grassy_sandy_dirt` und `immersive_weathering:sandy_dirt`
als `FallingBlock`. Der bisherige Prozessor behandelt fallende Blöcke als
ersetzbar, damit schwebender Kies über einer Höhle keine falsche Basis bildet.
Er zählt deshalb auch eine durchgehend gestützte Bodenschicht zum auszufüllenden
Hohlraum. Zusammen mit ein oder zwei Luftblöcken überschreitet sie das Limit
von zwei Blöcken. Der Prozessor verwirft die gesamte vorgeschlagene Anbindung.

Die Diagnose-JAR blieb privat und ist kein Spielerdownload. Die eigentliche
Korrektur enthält keine Diagnoseausgaben.

## Korrektur und Grenzen

Nur Innenraumrevision `interiors-20261111-v6` erkennt eine durchgehend gestützte
Schicht fallenden Bodens als Untergrund. Das gilt für die bestehende begrenzte
Art-Anbindung des Schwertschädels. Die Baumwurzelbehandlung bleibt unverändert.
Der Prozessor prüft höchstens 32 Zellen in derselben senkrechten Spalte und
innerhalb der aktuellen Chunk-Bounding-Box. Er akzeptiert die Schicht nur,
wenn sie ohne Luft, Flüssigkeit, Vegetation oder Blätter festen Boden erreicht.

Die nativen Bodenblöcke bleiben erhalten. Ausschließlich die bisher zulässigen
kurzen Lücken werden mit dem jeweiligen Modellmaterial geschlossen. Das
Zwei-Block-Fülllimit, längere Hohlräume, Modell, Verteilung und Standortprüfung
ändern sich nicht. V1–V5 verwenden weiterhin den bisherigen Prozessorpfad,
auch bei der Generierung weiterer Chunks. Bereits platzierte Relikte werden
nicht repariert. Unveröffentlichte V6-Entwicklungswelten erhalten die korrigierte
Anbindung für neue Stücke.

Das historische Visual-Alpha-4.9-Profil entfernt den V6-Laufzeitblock beim
Erzeugen seiner Quellen. Es benötigt dadurch weiterhin keinen
Verteilungs-Runtime-Code und bleibt beim bisherigen Verhalten.

## Prüfung

Die Java-Prüfung besteht mit 776 Assertions, darunter neue Fälle für stabilen
Kies, Kies über Luft, Wasser, Blättern und Gras, das Suchlimit, die Chunkgrenze,
die Dimensionsunterkante und den Revisionsschutz. Produktion und Testquellen
für Fabric 1.21.1 kompilieren; die Spieler-JAR wird erfolgreich remappt.

Am reproduzierten Standort mit Seed `-826638008258703270`, Ursprung
`[-975, 38, -3585]` und Rotation `CLOCKWISE_90` besteht die korrigierte
V6-Welt den unveränderten strikten Prüfer. Es gibt keine Modellabweichung,
keine kurzen ungestützten Kontakte, keine fehlenden Chunks und keine fehlenden
Schutzbits. Das frühere fehlgeschlagene Ergebnis bleibt im Beleg erhalten.
Dies ist ein konkreter Modpack-Standort, keine allgemeine Survival-Abnahme.

Die [Belegdatei](sword-skull-contact-fix-20261111-evidence.json) enthält die
Vergleiche, Kandidaten-Hashes und den gesonderten V5-Bestandstest. Die 57
historischen Template-, Prozessorlisten- und Gameplay-Manifest-Dateien der
Ausgangs-JAR bleiben bytegleich. Der abweichende vollständige
Planungsfingerabdruck der V6-Welt stammt aus den neuen Innenraumverträgen;
die übrigen Signaturteile stimmen überein.
