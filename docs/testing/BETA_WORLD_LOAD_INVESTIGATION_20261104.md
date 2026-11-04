# Beta P0: Weltladeabbruch untersucht

Stand: 4. November 2026. Die folgenden Befunde dokumentieren zunächst die
veröffentlichte Alpha 5.0.5 **vor der Implementierung des Fixes**.
Die frühe Ladeprüfung und Fehleroberfläche sind inzwischen implementiert.
Die anschließende Umsetzung ist abgenommen; siehe
[Umsetzung und Prüfstand](BETA_WORLD_LOAD_GUARD_20261104.md).

## Reproduktion

Eine Kopie von `Living World Relics v5` und der installierten Mod-/Konfiguration
wurde unter `build/beta-load-guard/reproduction` angelegt. Ausschließlich diese
Kopie wurde auf einem lokalen Fabric-1.21.1-Dedicated-Server gestartet. Die
Spieler-JAR ist die heruntergeladene Alpha 5.0.5 mit SHA-256
`8d02791f73361942907e13cc77c8bb3c89c231d17ff1c3703a5565b90e3d5acb`.
Ein ausschließlich im Test verwendetes Mixin erfasst die Signatur vor ihrem
Hashvergleich. Es ändert weder Prüfwerte noch Planentscheidungen.

| Fall | Ergebnis | Reliktjournal bytegleich | Koloss-Ziel gleich |
|---|---|---|---|
| Ursprüngliches Setup | Welt startet, regulär gestoppt | ja | ja |
| Serene Seasons und SSDH entfernt | Abbruch mit eingefrorener Prüfsummenabweichung | ja | ja |
| Beide Dateien wiederhergestellt | Dieselbe Testwelt startet wieder | ja | ja |

Der Abbruch ist anhand der Exception und des fehlenden erfolgreichen Starts
erkannt. Der Dedicated-Server-Prozess endet dabei mit Code 0; dieser Exitcode
allein ist daher kein erfolgreicher Ladetest.

Bei einem ersten Testlauf blieb SSDH aktiv und der Fabric Loader verweigerte
bereits wegen seiner fehlenden Pflichtabhängigkeit den Start. Erst der korrigierte
Versuch ohne beide Mods reproduziert die Relic-Prüfsummenabweichung. Das sind
unterschiedliche Fehlerfälle.

## Genaue Ursache in dieser Kombination

Gespeicherte Prüfsumme:
`65ea46667546c63df4145e5a606838b4fdacafbe6fed2efb47ab0515cff83830`.

Prüfsumme ohne die beiden Mods:
`c43874594b3e6dcff2d135120b26cf894a0962a78efca574811e76792214ded5`.

Die erfassten Signaturen unterscheiden sich **ausschließlich im Abschnitt
`biomeTags`**, dort in den Mitgliedern dreier Tags:

| Tag | Mitglieder vorher | Mitglieder nachher |
|---|---:|---:|
| `sereneseasons:blacklisted_biomes` | 26 | 10 |
| `sereneseasons:tropical_biomes` | 28 | 15 |
| `sereneseasons:lesser_color_change_biomes` | 11 | 10 |

Die Tag-Namen bleiben durch andere Packdaten erhalten. Es ändern sich ihre
Mitgliedslisten, nicht die Menge der Tag-Namen. Generator, codierte Biome,
Reliktstrukturen, Pools, Prozessoren und ausgewählte Innenräume bleiben in den
erfassten Signaturen identisch. Nach Wiederherstellung ist die gesamte Signatur
wieder identisch zum Ausgangszustand.

`TerrainValidator` nimmt derzeit sämtliche Biom-Tags in die Signatur auf.
Diese konkrete Abweichung belegt somit nicht, dass sich das Gelände oder ein
Reliktziel geändert hat. Daraus folgt aber keine allgemeine Freigabe beliebiger
Modänderungen oder eine sichere generelle Ausnahme für einen Mod-Namensraum.

## Warum ein später Exception-Handler nicht genügt

Der fehlerhafte Versuch verändert in der Testkopie bereits `level.dat` und
`level.dat_old`, obwohl das Reliktjournal unverändert bleibt. Allein ein
unverändertes Journal beweist also keine vollständige Erhaltung des Spielstands.

Der untersuchte Minecraft-26.2-Client schreibt in `Minecraft.doWorldLoad`
`LevelStorageAccess.saveDataTag` **vor** `MinecraftServer.spin`. Der bestehende
Relic-Hook in `DistributionSpawnMixin.prepareLevels` läuft dagegen erst im
bereits gestarteten Server. `IntegratedServer.onServerCrash` reicht dessen
Fehler an den Client weiter. Nur diese Weiterleitung zu unterdrücken würde
weder den frühen Schreibzugriff verhindern noch den Client-Ladewarteschritt,
Serverabbau und Ressourcenfreigabe korrekt abschließen.

Diese Aufrufreihenfolge wurde am tatsächlichen 26.2-Client-Bytecode untersucht.
Eine entsprechende grafische Laufzeitprüfung auf 1.21.1 und den NeoForge-Zielen
stand zum Untersuchungszeitpunkt noch aus. Sie ist inzwischen im verlinkten
Umsetzungsbericht belegt; die damalige Dedicated-Server-Reproduktion allein
ersetzt sie nicht.

## Nächste Implementierungsschritte

1. Die aktuelle Signaturberechnung aus der an `ServerLevel` gebundenen
   `TerrainValidator`-Initialisierung herauslösen. Sie muss mit bereits geladenen
   Registry-/Generator-/Ressourcendaten ohne Starten oder Speichern der Welt
   berechenbar sein. Bestehende Hashes und Legacy-Migration dürfen sich dabei
   nicht unbeabsichtigt ändern.
2. Den Vergleich in einen frühen Client-Ladepunkt nach Laden der Datapacks,
   aber vor dem ersten Welt-Schreibzugriff legen. Bei Abbruch Ressourcen und
   Weltzugriff schließen und zum passenden Menü zurückkehren. Für jeden
   angebotenen Loader und jede Spielversion den tatsächlichen Ladeweg prüfen.
3. Erwartete Kompatibilitätsfehler typisieren. Die Oberfläche soll Weltname,
   eine belegbare Ursache und die Wiederherstellung des ursprünglichen Setups
   nennen. Bei alten Welten ist allein der globale Hash gespeichert; unbekannte
   Ursachen dürfen nicht als konkrete Modänderung ausgegeben werden.
4. Die Aufnahme sachlich unbeteiligter Biom-Tags präzisieren. Dazu gehören eine
   begründete Definition der relevanten Daten und ein abgesicherter Übergang
   für alte globale Hashes. Keine automatische Neuplanung oder pauschale
   Umgehung der Integritätsprüfung einführen.
5. Fehlerfälle mit vollständigen Datei-Hashes vor/nach dem Versuch prüfen,
   einschließlich `level.dat`, Regionen, Entitäten und Gameplay-Journal.
   Danach Wiederherstellung und identische Ziele/Karten belegen. Server- und
   echte Clienttests sowie die vier Ziel-Builds durchführen.

Zum Abschluss der ursprünglichen Untersuchung blieben die Fehleroberfläche, der frühe schreibfreie Abbruch,
Ressourcen-/Lock-Freigabe, die sichere Behandlung alter Hashes und die vollständige
Abnahme offen. Zu diesem Untersuchungszeitpunkt wurden noch keine Runtime-Dateien
verändert. Die anschließende Implementierung und deren Abnahme stehen im oben
verlinkten Umsetzungsbericht. Nutzerprofile bleiben unangetastet.

## Belege

- [Strukturierte Ergebnisse](beta-world-load-investigation-20261104.json).
- Lokaler Reproduktionshelfer: `build/beta-load-guard/reproduce.py`.
- Drei Logs und Signaturen: `build/beta-load-guard/reproduction/`.
- Lokaler API-/Bytecodebefund: `build/beta-load-guard/minecraft-javap.txt` und
  `build/beta-load-guard/integrated-javap.txt`.
- [Beta-Roadmap](../project/PUBLIC_BETA_ROADMAP.md#1-weltladefehler-verständlich-abfangen).
