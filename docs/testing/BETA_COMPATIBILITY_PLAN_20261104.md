# Beta Punkt 5: vorab festgelegter Prüfplan

Festgelegt vor den Vergleichsmessungen am 4. November 2026. Originalprofile bleiben unverändert; neue Läufe, Welten, Java-Tempdateien und Messdaten liegen unter `E:/Relic_Mod_QA/compatibility-20261104/`. Keine automatische Bereinigung, kein Release. Die Tests starten seriell, Clients stumm.

## Umfang

- Eingefrorene Mod-/Konfigurationsinventare von TerraVista für Fabric 26.2 und TerraVista Living World für Fabric 1.21.1. Die installierten Profil-JARs sind nicht automatisch der aktuelle Testkandidat.
- Kontrollierte Vergleichsläufe ohne/mit den unveränderten vier lokalen Kandidaten aus der Client-Abnahme. Gleiche Seeds, feste Chunk-Routen, vier aktive Java-Prozessoren und maximal 4 GiB Java-Heap. Versionsgleiche Infrastruktur-Mods bleiben in beiden Varianten vorhanden.
- Reale Chunkgenerierung mit Terrain-/Biommods, fremden Strukturen, einem Bereich um einen gültigen großen Koloss und mehreren aufeinanderfolgenden Vorabgenerierungsabschnitten. Kein `/place` als Nachweis natürlicher Relikterzeugung.
- Getrennte Clientprüfungen für Distant Horizons, Voxy, Iris/BSL und Serene Seasons. Der aktuelle Inventarstand enthält entgegen dem früheren deaktivierten Zustand wieder die aktive Brücke `ssdh-1.0.3+terravista.dh3.1.jar`. Aktueller Zustand und eine Variante ohne Brücke werden ausschließlich in getrennten Kopien untersucht. Das Originalprofil bleibt unverändert.
- DH-Fernberechnung vor dem ersten normalen Laden eines bekannten Reliktstandorts mit der normalen Generierung vergleichen. Eine absichtlich übersprungene Struktur ist kein Darstellungsbeleg. FEATURES und INTERNAL_SERVER getrennt bewerten.

## Messung

Jeder Lauf erhält eine eigene Welt. Festgelegte Seeds sind `731204` und `731205`; der zweite dient der Wiederholung der Modpack-Vergleiche. Eine initiale kleine Route wärmt die Generierung vor dem Vergleichsabschnitt auf. Vor dem Vergleich wird die Chunkmenge festgelegt und später im Lauf mit Relic sowie im Kontrolllauf identisch verwendet. Reihenfolge und kalter Start werden protokolliert; die Stichprobe begründet keine allgemeine Performancegarantie.

Gemessen werden Zeit bis zum vollständigen Laden des angeforderten Chunkabschnitts, tatsächliche Server-Tickdauer, Java-Heap, Prozessspeicher und Größe der erzeugten Weltdateien. Ein reiner Konsolen-Erfolg für `forceload` gilt nicht als fertig generierter Abschnitt. Die Testprobe prüft die geladenen Chunks und sammelt pro Phase echte Tickzeiten; sie verändert keine Produkt-JARs.

## Technische Budgets für diese Abnahme

Diese konkreten Prüfgrenzen werden vor der Ausführung festgelegt. Sie sind vorläufige technische Abnahmekriterien für diesen PC und diese Testlast, keine versprochene Mindestleistung auf anderer Hardware.

- Kein reproduzierbarer Absturz, Deadlock, beschädigter Spielstand oder Verlust eines eingefrorenen Reliktziels im unterstützten Setup.
- Serverstart innerhalb von 180 Sekunden. Ein gewöhnlicher Vergleichsabschnitt muss innerhalb von 180 Sekunden vollständig geladen sein; ein Abschnitt am großen Koloss innerhalb von 300 Sekunden.
- Gewöhnliche Chunkgenerierung mit Relic höchstens doppelt so langsam wie die Kontrolle oder höchstens 15 Sekunden zusätzlich, je nachdem, welche Grenze mehr Spielraum lässt. Für den zusätzlich erzeugten großen Koloss gelten höchstens 60 Sekunden zusätzlicher Aufwand pro Abschnitt.
- Nach abgeschlossener Generierung mindestens 200 Idle-Ticks messen. Idle-Mittel unter 25 ms und Idle-p95 unter 50 ms. Die belastete Generierungsphase wird separat ausgewiesen und nicht gegen das Idle-Budget umgedeutet.
- Kein Out-of-Memory bei 4 GiB maximalem Heap. Der gemessene Prozessspeicher wird zusätzlich ausgewiesen; er ist nicht mit Java-Heap gleichzusetzen.
- C: mindestens 4 GiB frei halten, E: mindestens 20 GiB. Bei Unterschreitung oder 12 GiB neuem Scratch-Verbrauch keine weiteren Starts. Unterbrochene Läufe gelten nicht als bestanden.

Budgetverletzungen werden untersucht oder als offene Einschränkung dokumentiert. Eine erfolgreiche einfache Kombination wird nicht auf ungetestete Versionen, komplette Modpacks oder Grafikadapter übertragen.
