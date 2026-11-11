# Fremde Oberflächenstrukturen bei Relikten seltener zulassen

Ursprünglicher Prüfstand: 11. November 2026, vor der Implementierung.
Der folgende Text hält die dabei ermittelten Anforderungen fest. Den inzwischen
umgesetzten Entwurf und seine Prüfungen dokumentiert der
[Implementierungsbericht](SURFACE_STRUCTURE_FILTER_20261111.md).

## Gewünschtes Verhalten

Die Reliktverteilung bleibt unverändert: dieselben Presets, Familientickets,
Kandidaten, Geländeprüfungen, Mindestabstände und Koloss-Suchregeln.

Bei einer tatsächlichen räumlichen Überschneidung mit einem geplanten Relikt
wird ein fremdes oberirdisches Bauwerk mit 50 % Wahrscheinlichkeit ausgelassen.
Die Entscheidung gilt einmal für den vollständigen Strukturstart einschließlich
aller zugehörigen Teile. Bloße Nachbarschaft wird nicht eingeschränkt.
Tiefe Minen, Fossile und kleine Geröllstrukturen sollen ausgenommen bleiben.

Das ist eine Halbierung der Annahmechance pro betroffener fremder Struktur,
keine Garantie, dass in einer kleinen Zahl besuchter Orte genau die Hälfte
verschwindet. In den übrigen Fällen bleiben die bisherigen Kollisionen möglich.

## Ergebnis

Minecraft bietet einen geeigneten Abschnitt vor der Blockplatzierung. Dort kann
ein vollständig geplanter Strukturstart aus der weiteren Generierung genommen
werden. Die bisherigen Reliktalgorithmen müssen dafür nicht umverteilt werden.

Die sichere Integration ist allerdings noch nicht nachgewiesen. Besonders der
erste Weltstart und das Zusammenspiel mit anderen Worldgen-Mixins benötigen
einen nativen Prototyp und gezielte Tests. Eine sofortige Freigabe allein auf
Grundlage dieser statischen Prüfung wäre nicht begründet.

## Geprüfter nativer Ablauf

Die lokalen Minecraft-Klassen für Fabric und die vorhandenen gepatchten
NeoForge-Artefakte wurden für 1.21.1, 1.21.11, 26.2 und 26.3 mit `javap`
untersucht. Bei den älteren partiellen NeoForge-Patch-JARs kam das zugehörige
benannte Vanilla-JAR als Klassenpfad-Ergänzung zum Einsatz.

In allen acht Zielkombinationen enthält
`ChunkStatusTasks.generateStructureStarts` diese Reihenfolge:

1. `ChunkGenerator.createStructures` plant die Strukturstarts und ihre Teile.
2. `ServerLevel.onStructureStartsAvailable` veröffentlicht die Ergebnisse an den
   Struktur-Cache.
3. Das Future des Generierungsschritts wird abgeschlossen.

Der Filter muss nach der vollständigen Strukturauswahl und vor Punkt 2 greifen.
Dann entstehen keine Blockreste, Straßen oder strukturgebundenen Bewohner aus
einem ausgelassenen Start. Spätere Referenzbildung, Terrain-Anpassung,
Strukturabfragen und Blockplatzierung müssen denselben gefilterten Start sehen.
Diese Folgewirkungen sind im nativen Test zu bestätigen.

Ein einfaches `INVALID_START` in `Structure.generate` reicht nicht als Entwurf:
Bei einem Strukturset mit mehreren Einträgen kann Minecraft nach einem
fehlgeschlagenen Generierungsversuch einen weiteren Eintrag ausprobieren.
Nachträgliches Herausnehmen des bereits ausgewählten Starts vermeidet diesen
zusätzlichen Auswahlversuch und verändert den nativen Zufallsstrom nicht durch
weitere eigene Würfe.

Auch ein Filter erst nach Abschluss des bisherigen `original`-Futures wäre zu
spät: Dann wurde der Struktur-Cache bereits benachrichtigt. Die vorhandene
Mixin-Integration muss daher gezielt erweitert werden.

## Vorgeschlagener Einbau

Der vorhandene asynchrone `STRUCTURE_STARTS`-Ablauf bleibt die Grundlage.
Eine mögliche Erweiterung ist eine pro Aufruf gekapselte Phase, welche die
native Cache-Benachrichtigung zunächst zurückhält, die vollständig berechneten
fremden Startgeometrien prüft und danach genau einmal veröffentlicht. Der
Generierungsschritt darf erst anschließend fertig werden. Dabei muss das
Zusammenspiel mit anderen Mixins geprüft werden; ein vollständiges Überschreiben
der nativen Methode ist kein bevorzugter Kompatibilitätsweg.

Die benötigten Reliktentscheidungen werden über den bestehenden seriellen
Planungsworker angefordert. Aus den tatsächlichen fremden Teilgrenzen und der
maximalen gepinnten Reliktausdehnung lässt sich eine begrenzte Menge relevanter
Reliktzellen bestimmen. Damit sind auch Häuser erfasst, deren Strukturstart in
einem anderen Chunk liegt. Eine angenommene feste Maximalgröße aller fremden
Mod-Strukturen ist dafür nicht notwendig.

Die Prüfung darf nicht von schon geladenen Nachbarchunks oder einer Liste
bereits besuchter Relikte abhängen. Sonst würde die Besuchsreihenfolge das
Ergebnis ändern. Es müssen die endgültig akzeptierten Reliktpläne sein, keine
lediglich geländetauglichen Kandidaten, die später an anderen Regeln scheitern.

`TerrainValidator` verwendet bereits vorab geladene eigene Vorlagen,
Grundhöhen und Noise-Biome. Die Reliktplanung benötigt deshalb keine fremden
Chunk-Blöcke. Der zusätzliche Filter darf diesen Vertrag nicht aufweichen.
Es dürfen keine synchronen `getChunk`-Aufrufe oder blockierenden `join`/`get`
auf dem Worldgen-Dispatcher hinzukommen. Eine wartende Planung muss über
`WorldgenGate` wieder auf der ursprünglichen Worldgen-Ausführung fortsetzen.
Anfragen und Zwischenspeicher brauchen feste Grenzen und gemeinsame Futures
für dieselben Zellen.

## Ein deterministischer Wurf pro fremdem Bauwerk

Der Wurf erhält eine eigene feste Kennung und verwendet Weltseed,
Dimensionskennung, fremde Struktur-ID und Startchunk. Er verbraucht keinen
Zufallswert aus Minecrafts Bauwerksgenerator oder dem Reliktplaner.

Der Wurf gehört dem fremden Start, nicht einem einzelnen Haus und nicht jedem
berührten Relikt. Mehrere Überschneidungen desselben Starts dürfen keine
zusätzlichen Würfe erzeugen. Das Ergebnis muss bei Neustart, parallelen
Chunk-Anfragen und umgekehrter Besuchsreihenfolge identisch bleiben.

Bei Vanilla-Dörfern enthält ein Start das gesamte geplante Dorf. Andere Mods
können eine sichtbare Siedlung aus mehreren unabhängigen Starts aufbauen. Eine
Zusammengehörigkeit solcher Starts lässt sich nicht allgemein aus Minecrafts
Strukturmodell ableiten; dafür wären modbezogene Regeln erforderlich.

## Oberirdisch und tatsächlich überschneidend

Der Generierungsschritt `SURFACE_STRUCTURES` ist allein keine ausreichende
Klassifizierung. Für die erste Umsetzung sind gezielte Struktur-Tags mit
unterstützten Vanilla- und Mod-Bauwerken sinnvoll. Beispielsweise gehören
Dörfer, größere Außenposten, Tavernen und Ruinenstädte hinein. Vorrangige
Ausnahmen schützen Minen, Fossile und kleine Geröllteile. Unbekannte fremde
Strukturen werden zunächst nicht verändert.

Der lokale Biomes-O'-Plenty-Build ergänzt etwa das Overworld-Biom `dryland`
im Tag für `minecraft:nether_fossil`. Der technische Name allein reicht daher
ebenfalls nicht zur Dimensionserkennung.

Für die Geometrie sind die tatsächlichen dreidimensionalen Teilgrenzen zu
verwenden. `StructureStart.getBoundingBox()` kann zusätzlich von der jeweiligen
Terrain-Anpassung vergrößert werden. Eine nur horizontale Prüfung würde auch
unterirdische Bauwerke treffen.

Eine gemeinsame Raumhülle kann leere Bereiche zwischen Ästen oder Knochen
enthalten. Der vorherige Spielstandvergleich hat solche Fälle bestätigt.
Ein vorab berechneter räumlicher Index der festen Relikt-Vorlagenzellen kann
diese Fehlklassifizierung begrenzen. Fremde Gebäudeinnenräume müssen dabei
weiterhin als Gebäuderaum zählen, auch wenn die fremde Vorlage dort Luft hat.
Die genaue Behandlung von Straßen, natürlichen Bodenanteilen und nachträglich
geerdeten Modellteilen muss am Prototyp festgelegt und überprüft werden.

## Offener kritischer Punkt: der erste Weltstart

`DistributionSpawnMixin` hängt die Reliktplanung vor `setInitialSpawn` an.
`finishSpawn` friert den tatsächlichen Spawn erst danach ein und startet dann
die endgültige Koloss-Suche. Bis dahin können endgültige gewöhnliche
Reliktentscheidungen wegen Kolossabständen und abhängigen Obelisken warten.

Würde der neue Fremdstrukturfilter in einem zur Spawn-Suche benötigten Chunk
auf eine solche Entscheidung warten, wäre eine gegenseitige Wartekette möglich.
Asynchrone Futures allein lösen diesen logischen Kreis nicht.

Ein erlaubter Entwurf muss für diese Startphase beweisen, dass alle benötigten
Entscheidungen ohne den noch unbekannten endgültigen Koloss auflösbar sind,
oder eine andere deterministische Bootstrap-Regel vorsehen. Ein fester,
gespeicherter räumlicher Ausnahmebereich um den Bootstrap-Punkt wäre eine
prüfbare Alternative, müsste aber aus den nativen Chunk-Abhängigkeiten
abgeleitet werden und würde die 50-%-Regel dort ausdrücklich ausnehmen.
Eine solche Ausnahme ist noch nicht beschlossen.

Nur bis zum Fertigwerden der Koloss-Suche ungeprüft durchzulassen wäre keine
geeignete Lösung: Das Ergebnis würde von Timing und Generierungsreihenfolge
abhängen. Dieser Punkt muss vor einer umfassenden Umsetzung entschieden
und nativ geprüft werden.

## Weltpläne und bestehende Gebäude

Die Filterregel benötigt eine eigene gespeicherte Revision. Sie sollte die
bisherige Generierungsrevision 3 und deren Reliktalgorithmen beibehalten.
Fehlende Filterangaben in alten Welten bedeuten deaktiviert. Eine Aktivierung
für neue Welten darf keine bestehende Welt stillschweigend umstellen.

Filterrevision, Wahrscheinlichkeit und die unterstützten Struktur-IDs beziehungsweise
Tag-Inhalte müssen zur Welt gehören. Änderungen an globalen Einstellungen oder
Datapacks dürfen sie nicht unbemerkt ändern. Ein neuer Planumschlag oder ein
anderer ausdrücklich geprüfter Versionsschutz muss verhindern, dass ältere
Modbuilds die neue Regel beim Laden einfach ignorieren.

Der Filter gilt nur für neu erzeugte Starts. Geladene und bereits gespeicherte
Starts werden nicht entfernt, auch wenn ein Gebäude bisher nur teilweise in
Nachbarchunks platziert wurde. Es gibt keine nachträgliche Blocklöschung.

## Erforderliche Abnahme

- Neue Welten starten, einschließlich Spawn an einer Reliktzelle und nahe einem
  Dorf. Keine Wartekette und keine ungeprüfte Abhängigkeit von `ready`.
- Ein-, Mehrfach- und über Chunkgrenzen reichende Überschneidungen; pro fremdem
  Start genau eine Entscheidung und keine Ersatzstruktur aus demselben Set.
- Derselbe Seed und dieselben Einstellungen mit vertauschter Besuchsreihenfolge,
  paralleler Generierung, Speichern und Neustart liefern dieselben Entscheidungen.
- Reliktpläne sind bei festgehaltenen Spawn- und Generator-Eingaben mit und ohne
  Filter gleich. Zusätzlich prüfen, ob geänderte fremde Bauten die native
  Spawn-Findung beeinflussen und damit indirekt die spawnbezogene Koloss-Suche.
- Ausgelassene Starts erzeugen keine Straßen-, Block-, Bewohner- oder
  Terrain-Anpassungsreste. `/locate`, Explorer-Karten und Spawn-Overrides nutzen
  die tatsächlich verbliebenen Strukturen.
- Vollständige und teilweise gespeicherte alte Strukturen bleiben erhalten.
  Alte Weltpläne laden unverändert; unzulässige Downgrades werden erklärt abgewiesen.
- Dörfer und die betroffenen Living-World-Strukturen werden erfasst; Minen,
  Fossile, Geröll und reine Nachbarschaft bleiben erhalten. Leere Teile großer
  Reliktgrenzen führen nicht zu unbeabsichtigten Löschentscheidungen.
- Native Gegenprüfung auf Fabric und NeoForge für alle unterstützten Spielziele,
  einschließlich begrenzter Planungszeit, Warteschlangen und Speichernutzung.

## Belegumfang

Die statischen Auswertungen liegen lokal unter
`build/foreign-structure-suppression-feasibility-20261111/`. `hook-audit.json`
enthält die Methoden-Signaturen und die geprüfte Reihenfolge für alle acht
Zielkombinationen. Die jeweiligen `*.txt`-Dateien enthalten die lokale
Bytecode-Auswertung; die Indexdateien benennen deren JAR-Quellen.

Diese Prüfung hat keine Produktionsquellen verändert, keine Welt geöffnet und
keinen Minecraft-Server oder neuen Release-Build gestartet. Die Laufzeit- und
Kompatibilitätsabnahme oben steht noch aus.

Relevante Produktionsstellen:

- [DistributionStartsMixin](../../src/main/java/de/relics/mixin/DistributionStartsMixin.java)
- [WorldgenGate](../../src/main/java/de/relics/distribution/WorldgenGate.java)
- [DistributionRuntime](../../src/main/java/de/relics/distribution/DistributionRuntime.java)
- [DistributionPlanner](../../src/main/java/de/relics/distribution/DistributionPlanner.java)
- [DistributionSpawnMixin](../../src/main/java/de/relics/mixin/DistributionSpawnMixin.java)
- [DistributionJournal](../../src/main/java/de/relics/distribution/DistributionJournal.java)
