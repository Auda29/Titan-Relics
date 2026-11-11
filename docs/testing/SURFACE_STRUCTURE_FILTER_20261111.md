# Fremde Oberflächenbauten an Relikten, 11. November 2026

## Verhalten

Neue Welten erhalten eine eigene gespeicherte Fremdstrukturregel. Berührt ein
unterstütztes oberirdisches Bauwerk feste Relikt-Modellzellen, entscheidet ein
fester, unabhängiger 50-%-Wurf über das Auslassen seines vollständigen
`StructureStart`. Ein Vanilla-Dorf verschwindet damit als Einheit, einschließlich
seiner zugehörigen Häuser und Wege. Mehrere berührte Relikte lösen keine weiteren
Würfe aus. Bloße Nachbarschaft führt zu keiner Unterdrückung.

Die Entscheidung verwendet Seed, Dimension, Struktur-ID und Startchunk. Der
Filter verbraucht keine Zufallszahlen des nativen Bauwerksgenerators oder des
Reliktplaners. Er läuft nach der Strukturauswahl und vor Cache-Veröffentlichung,
Referenzbildung, Terrain-Anpassung und Blockplatzierung. Es gibt dadurch keinen
zusätzlichen Auswahlversuch aus demselben Strukturset.

Die Daten-Tags `relics:surface_overlap_targets` und
`relics:surface_overlap_exempt` benennen unterstützte Bauten und vorrangige
Ausnahmen. In Vanilla gehören beispielsweise Dörfer, Außenposten, Tempel und
Waldanwesen zu den Zielen. Die Regel enthält außerdem ausgewählte vorhandene
Nova-Structures-Bauten und den Terralith-Wüstenaußenposten. Tiefe Minen,
Fossile, kleine Ruinen und Geröll bleiben erhalten. Nicht aufgeführte fremde
Strukturen werden nicht verändert. Die zur Erstellung aufgelösten IDs werden
in der Welt gespeichert; spätere Tag-Änderungen stellen alte Welten nicht um.

Die Kollisionsprüfung verwendet einzelne dreidimensionale Bauwerksteile und
einen vorab geladenen Index fester Relikt-Vorlagenzellen. Leere Bereiche unter
Ästen oder zwischen Knochen sind keine belegten Modellzellen. Innenräume eines
fremden Bauwerksteils zählen als Gebäuderaum. Nachträglich vom Geländeprozessor
ergänzte Stützen sind nicht Teil dieses Vorlagenindexes.

## Startregion und Bestandsschutz

Um den gespeicherten ursprünglichen Bootstrap-Punkt bleiben fremde Bauwerke
innerhalb von 1.024 Blöcken in X- und Z-Richtung immer erhalten. Das gilt auch
für weiter entfernte Starts, deren Teile in diesen Bereich reichen. Diese
räumliche Ausnahme ist dauerhaft und unabhängig von Timing und Besuchsreihenfolge.
Sie verändert weder die Reliktverteilung noch deren Einstellungen.

Beim Weltstart wird geprüft, dass die native Abhängigkeit für einen vollständigen
Spawn-Chunk einschließlich der bisherigen 128-Block-Spawn-Suche in diese Region
passt. Ein unerwarteter externer Generierungsaufruf außerhalb des geprüften
Bereichs vor dem eingefrorenen Spawn erzeugt einen erklärten Fehler anstelle
einer gegenseitigen Wartekette. Solche abweichenden Spawn-Modifikationen sind
nicht allgemein als unterstützt nachgewiesen.

Wegen möglicher extrem großer Mod-Bauwerke werden höchstens 64 relevante
Reliktzellen pro geprüftem Bauwerk angefordert. Überschreitet ein Bauwerk diese
Grenze, bleibt es erhalten; dies wird als `oversizePreserved` diagnostiziert.
Die Planung nutzt bestehende gemeinsame Futures und Caches. Es kommen keine
Nachbarchunk-Abfragen oder synchronen Future-Warteaufrufe auf dem
Worldgen-Dispatcher hinzu. Änderungen an Chunk-Metadaten und Cache-Veröffentlichung
kehren über `WorldgenGate` auf die ursprüngliche native Ausführung zurück.

Fehlende `surfaceStructures`-Angaben bedeuten deaktiviert. Bereits veröffentlichte
und gespeicherte Strukturstarts werden über den nativen Ladepfad übernommen;
auch erst teilweise in Nachbarchunks platzierte Gebäude werden nicht entfernt.
Ein noch nicht abgeschlossener neuer Generierungsschritt veröffentlicht seine
Starts erst nach der Filterentscheidung. Es gibt keine nachträgliche Blocklöschung.

Aktivierte neue Welten verwenden Umschlagversion 2 des bisherigen Plan-Journals.
Die Relikt-Generierungsrevision bleibt 3. Ältere Builds verweigern die neue
Umschlagversion, statt den Filter stillschweigend zu ignorieren. Alte Welten
behalten Version 1 und unveränderte Planregeln. Getestete alte Journale bleiben
beim Laden und erneuten Speichern bytegleich.

## Nachweis unveränderter Reliktverteilung

Diese Produktionsdateien sind gegenüber der Ausgangsrevision `78244d1`
bytegleich:

- `DistributionPlanner.java`
- `DistributionSettings.java`
- `ColossusSearch.java`
- `LocationSearch.java`
- `GenerationRules.java`
- `BiomeRules.java`

Zusätzlich sind alle 124 bereits vorhandenen Relikt-Datenressourcen im
Fabric-1.21.1-Vergleichsbuild bytegleich zum bisherigen Spielerbuild. Die neuen
Struktur-Tags sind zusätzliche Ressourcen. Vorlagen, Belohnungen, Geländeprüfungen,
Presets, Abstände und Koloss-Suchregeln wurden nicht geändert.

## Prüfstand

- 195 Python-Tests bestehen.
- 10.682 neue Assertions zu Filterregel, negativem Koordinatenraum,
  Vierteldrehungen, leeren Modellbereichen, alten und neuen Journals,
  unveränderter Verteilung sowie verzögerter Cache-Veröffentlichung bestehen.
- Die bisherigen Verteilungs-, Einstellungs-, Positionssuch-, Koloss-Such- und
  Worldgen-Gate-Tests bestehen.
- Fabric 1.21.1: kompletter Build, Assetprüfung und remappter Diagnosebuild bestehen.

Der native Vergleich verwendet ausschließlich neue isolierte Welten mit den
serverfähigen Mods des gelieferten Living-World-Setups. Seed
`-4443928181842649648`, Preset Entdeckungen, Generierungsrevision 3. Baseline ist
der bisherige Fabric-1.21.1-Kandidat ohne Filter. Die Spielerarchive werden
weder geöffnet noch verändert. Server laufen nacheinander, auf Loopback, mit
einer CPU, 2.500 MiB Heap und einem 3-GiB-Scope mit niedriger I/O-Priorität.
Der Testtreiber stoppt und nötigenfalls beendet alle eigenen Java-Prozesse.

Im direkten Vergleich sind alle sechs gewöhnlichen Reliktpläne, der einzigartige
Koloss bei `(-3240, 3352)` und die geprüften Modellblöcke identisch. Das Wüstendorf
bei Startchunk `(-87, 149)` wird vollständig ausgelassen: von 123 Teilen zu keinem
gültigen Start. Das Schneedorf bei `(-543, -1098)` bleibt mit 103 Teilen erhalten.
Der Schrein mit 34 Teilen und die Mine mit 111 Teilen bleiben ebenfalls erhalten,
ebenso die geprüften kleinen Ruinen, die Taverne und das Fossil.

Alle sechs isolierten Serverläufe bestehen: Baseline, Filter, Filter-Neustart,
Laden der alten Welt mit dem neuen Build, umgekehrte Erstbesuche und der getrennte
Dorf-Starttest. Beide erneut geladenen Plan-Journale sind bytegleich mit dem
jeweiligen Zustand vor dem Neustart. Umgekehrte Erstbesuche liefern dieselben
aufgezeichneten Fremdstrukturentscheidungen, Reliktpläne und Modellproben.

Die künstlich dichte Dorf-Startwelt startet erfolgreich. 121 passende
Strukturstarts werden dort wegen der festen Startregion erhalten, kein Start
wird unterdrückt. Das ist ein gezielter Bootstrap-Test mit einem Test-Datapack;
der normale Modpack-Vergleich oben verwendet unveränderte Fremdstrukturregeln.
Alle sechs Java-Prozesse wurden mit Exit-Code 0 beendet.

Die erste CI-Ausführung fand einen Fehler im Testwerkzeug: Bei gezielten
Manipulationen eines neuen Weltplans wurde Umschlagversion 1 fest vorgegeben.
Die neue Konsistenzprüfung verweigerte deshalb schon das Lesen des Plans. Das
Werkzeug erhält jetzt dessen ursprüngliche Umschlagversion. Ausdrücklich
historische Kontrollfixtures entfernen die neue Filterregel und verwenden
weiterhin Version 1. Die Schutzprüfung im Mod wurde nicht abgeschwächt.
Die vollständige aktualisierte Acht-Ziel-CI bleibt ein eigener Freigabeschritt.

## Reproduktion und Belege

`tools/test_surface_structure_server.py` erwartet die beiden Spieler-JARs,
den remappten Fabric-1.21.1-Diagnosebuild, eine vorhandene isolierte Modpack-
Serverfixture und eine Eingabedatei mit Zellen, Strukturstarts und Blockproben.
`--accept-eula` ist für den isolierten Serverlauf erforderlich. Der Treiber
vergleicht neue Welten, lädt beide erneut und prüft alte Journalbytes.
`--extra-cases` ergänzt auf Basis dieser vier Belege eine neue Welt mit
umgekehrter Struktur-Erstbesuchsreihenfolge und eine getrennte Startwelt mit
künstlich dichten, verkleinerten Dörfern. Der zweite Fall prüft die Startregion,
nicht eine behauptete unveränderte Vanilla-Dorfverteilung.

Lokale vollständige Belege liegen unter `build/surface-filter-validation/`:
`preservation-proof.json`, `distribution-tests.log`, `python-tests.log`,
`fabric1211-build.log` und `native-living-world/evidence.json`. Die [konkreten Eingaben](surface-structure-filter-input-20261111.json) und die
Quellen der neuen Regeln liegen im PR. Rohwelten, Drittanbieter-
JARs und vollständige private Serverfixtures werden nicht ins Repository gepackt.

## Grenzen

Die Regel reduziert Überlagerungen. In den zugelassenen Fällen bleiben sie
möglich. Ein Mod kann eine sichtbare Siedlung aus mehreren unabhängigen Starts
aufbauen; diese werden nicht automatisch als ein gemeinsames Dorf erkannt.
Direkt platzierte Features oder Worldgen-Pfade außerhalb des nativen
`STRUCTURE_STARTS`-Ablaufs werden nicht allgemein abgefangen. Die Tests ersetzen
keine allgemeine Modpack-, LOD- oder Langzeit-Performancegarantie.

## Kompakter nativer Beleg

Die Spieler-JARs des Vergleichs enthalten den Laufzeitstand aus `e7a0d85`.
Spätere Änderungen an Testfixtures und Dokumentation verändern diesen geprüften
Laufzeitcode nicht. Der Vergleichsbuild ohne Filter stammt aus dem vorherigen
Entwicklungsstand von PR #2, nicht aus dem veröffentlichten Revision-2-Beta-3-JAR.

```json
{
  "implementation_commit": "e7a0d8570ba7882228cc8723d7344809658e151c",
  "minecraft": "1.21.1",
  "loader": "Fabric 0.19.5",
  "java": "21.0.13+9",
  "seed": -4443928181842649648,
  "generator_fingerprint": "65ea46667546c63df4145e5a606838b4fdacafbe6fed2efb47ab0515cff83830",
  "baseline_sha256": "27175f8df4f4063400a30c8b6595ceb9df555ec0cc144e025b7a6632d8fb4c26",
  "candidate_sha256": "10b12bfe0f3ceea14d50f8ec0afc2feb2ce549d64522e6c071a0652681571dfe",
  "passed_native_cases": [
    "baseline",
    "filtered",
    "filtered-reload",
    "legacy-reload",
    "reverse",
    "bootstrap"
  ],
  "bootstrap_preserved": 121,
  "unchanged_ordinary_sites": 6,
  "unchanged_data_resources": 124,
  "assertions": [
    "same six ordinary relic plans",
    "same unique Colossus",
    "whole foreign-start suppression observed",
    "filtered restart stable",
    "legacy snapshot bytes and structures preserved",
    "sampled model blocks unchanged",
    "reverse first-visit order stable",
    "native dense-village initial-spawn exception exercised"
  ]
}
```

## Ergänzender Test auf Vanilla-Gelände

Der [Vanilla-Vergleich](VANILLA_DISTRIBUTION_20261111.md) prüft denselben Seed
ohne Living-World- oder andere Terrain- und Strukturmods. Beide Builds sowie
beide erneut geladenen Welten behalten dieselben Reliktstandorte, Modellproben
und Fremdstrukturentscheidungen. Im geprüften Vanilla-Satz liegt kein positiver
Kollisionsfall vor. Dabei wurde die Waldanwesen-Ziel-ID auf den nativen Namen
`minecraft:mansion` korrigiert. Der Bericht trennt diese Ressourcenprüfung
vom nativen Vergleich des bisherigen Spieler-Builds.
