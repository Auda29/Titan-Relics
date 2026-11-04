# Beta P0: Weltladeprüfung vor dem Speichern

Stand: 4. November 2026. Punkt 1 ist implementiert und abgenommen.
Kein Push, Tag oder Release. Die Test-JARs tragen weiterhin
die Entwicklungsbasis `0.1.0-alpha.5.0.5`; sie sind keine neu veröffentlichte Version.

## Verhalten

Bestehende Reliktwelten werden nach dem Laden ihrer Datapacks und vor dem ersten
vanilla Welt-Schreibzugriff geprüft. Ein inkompatibler oder beschädigter
Verteilungsplan führt im Client zu einer Meldung mit Weltordner, belegbarer
Ursachenkategorie und Wiederherstellungshinweis. Der Zurück-Knopf führt ins Menü.
Unbekannte Ursachen werden als unbekannt angezeigt; ein alter globaler Hash
begründet keine Behauptung über eine bestimmte entfernte Mod.

Der Dedicated-Server beendet den Start mit einer entsprechenden Logmeldung.
Der Exitcode allein gilt nicht als Prüfergebnis. Die Tests verlangen zusätzlich
die Ablehnungsmeldung, einen ausgebliebenen Serverstart und gleiche Datei-Hashes.

Die Prüfung liest den vorhandenen Plan. Sie löscht oder ersetzt ihn nicht und
plant keine Relikte, Karten oder Belohnungen neu. Eine Welt ohne Verteilungsjournal
behält die bisherige Behandlung als Altwelt.

## Signaturen und bestehende Welten

`PlanningSignature` erfasst geladene Registry-, Generator-, Ressourcen- und
Template-Daten ohne `ServerLevel`. Der bisherige vollständige Signaturinhalt,
der kanonische Hash und der vorhandene Legacy-Vergleich bleiben erhalten.
Die tatsächlichen Template-Dateien werden gegen ihre eingefrorenen Hashes geprüft.

Fabric-Biomänderungen werden normalerweise im Server-Konstruktor angewendet;
Lithostitched-Modifikationen folgen noch später. Die Vorprüfung wendet diese
regulären Schritte auf dieselben geladenen Registries vorgezogen einmal an.
Beim folgenden normalen Start wird ausschließlich diese bereits ausgeführte
Anwendung übersprungen. Neue Welten behalten ihren bisherigen Ablauf.
Beim Schließen eines vorbereiteten `WorldStem` werden Vormerkungen verworfen
und der früh gesetzte globale Lithostitched-Seed wiederhergestellt. Das gilt
auch für einen anschließenden Abbruch im Vanilla-Ladeablauf.

Nach vollständiger erfolgreicher Runtime-Validierung entsteht zusätzlich
`data/relics_planning_environment_v1.json`. Diese Referenz muss kryptographisch
zum vorhandenen Plan passen; sie wird nicht durch eine abweichende Umgebung
überschrieben. Der Verteilungsplan und seine Ziele bleiben unverändert.

Nur Mitglieder der drei nachgewiesenen Saison-Tags
`sereneseasons:blacklisted_biomes`, `sereneseasons:tropical_biomes` und
`sereneseasons:lesser_color_change_biomes` dürfen abweichen. Dafür muss eine
passende Referenzsignatur vorliegen und die übrige vollständige Signatur gleich
sein. Verweist ein erfasster Generierungswert auf einen dieser Tags, bleibt auch
dieser Tag geschützt. Andere Tags oder ganze Mod-Namensräume sind nicht ausgenommen.

Eine bestehende Welt mit ausschließlich altem Hash muss deshalb zunächst einmal
mit dem ursprünglichen Setup erfolgreich geladen werden. Ohne diese belegbare
Referenz bleibt eine spätere Abweichung gesperrt. Legacy-Hashes werden nur über
die bestehende gesicherte Migration behandelt. Eine manuelle Legacy-Freigabe
kann eine bereits geprüfte Referenz nicht auf eine andere Umgebung umdeuten.

## Bestandene Prüfungen

- 22 neue Assertions zu Referenzbindung, schreibfreier Ablehnung, Tag-Verweisen,
  Legacy-Übergang und beschädigten/fremden Referenzen. Die vorhandenen Planer-,
  Einstellungs-, Such- und Executor-Tests einschließlich 30 synthetischer Seeds bestehen.
- Je ein echter Fabric- und NeoForge-Client auf Minecraft 1.21.1 und 26.2:
  zwei abgewiesene Ladevorgänge, deutsche Meldung, keine gestartete Welt,
  vollständige Dateierhaltung, erneuter Lock-Zugriff, Menü-Rückkehr sowie
  erfolgreicher Abbruch einer bereits bestandenen Vorprüfung und späterer Weltstart.
- Eine vollständige isolierte Living-World-Modpack-Kopie durchläuft den echten
  Fabric-1.21.1-Client. Der ursprüngliche Plan wird nach Wiederherstellung bytegleich geladen.
- Modpack-Server: Ohne ursprüngliche Referenz wird der Saisonwechsel abgewiesen;
  alle 733 gespeicherten Weltdateien bleiben gleich. Originalsetup, belegter
  Saisonwechsel und Wiederherstellung starten anschließend erfolgreich.
  Karten-, Spielerfortschritts- und Reliktdateien sowie das gespeicherte Kolossziel bleiben gleich.
- Servermatrix: je sechs Ablehnungen für Fingerprint/Referenz, Seed, Grenze,
  aktivierte Familien, unvollständigen Plan und Journal-Prüfsumme, danach
  Wiederherstellung. Alle 24 Fälle bestehen mit den endgültigen Artefakten.

Die [strukturierten Ergebnisse](beta-world-load-guard-20261104.json) binden
Server- und Clientläufe an die SHA-256 der vier geprüften JARs. Sie enthalten
auch die Modpack-Ergebnisse und den Erhalt der sieben fremden, bereits zuvor
geänderten Dateien. Die [deutsche Fehlermeldung](images/beta-world-load-guard-de.png)
wurde im tatsächlich gerenderten Client geprüft.

Beim Dateivergleich wird ausschließlich die vorübergehende `session.lock`
ausgenommen. Erfolgreiche Starts dürfen normale Autosaves erzeugen; diese werden
nicht als schreibfreie Ablehnung ausgegeben. Die vier kleinen Serverfixtures
verwenden eine leere Koloss-Biomauswahl für einen begrenzten Testlauf. Der
wirklich gespeicherte Koloss wird separat in der Modpack-Kopie geprüft.

## Reproduktion

- `tools/test_distribution.py`: reine Regressionstests.
- `tools/test_alpha5_port_server.py --world-load-checks`: sechs abgewiesene
  Planvarianten und anschließende Wiederherstellung in einer neuen Testwelt.
- `tools/test_distribution_client.py --world-load-world <isolierte Testwelt>`:
  echter Fabric-Client. Optional `--modpack-dir <isolierte Modpack-Kopie>`.
- `tools/test_world_load_neoforge_client.py`: entsprechender echter NeoForge-Client.
  Für 26.2 wird eine separate Clientinstallation unter `build/` verwendet.
- `tools/test_world_load_modpack.py`: vier Saison-/Referenzfälle. Akzeptiert
  ausschließlich zuvor isolierte Fixtures im `build/`-Verzeichnis dieses Repositories.

Alle Launcherprofile bleiben reine Lesequellen. Testwelten, Configs, Logs,
Probe-JARs und Clientinstallationen liegen unter `build/`. Die Diagnoseklassen
werden nicht in Spieler-JARs aufgenommen. Fremde lokale Änderungen werden
nicht Bestandteil des Fix-Commits.

Die automatische Prüfung belegt diese Loader-/Versionskombinationen und die
konkrete Modpack-Kopie. Sie ist keine allgemeine Freigabe beliebiger Modpacks.
Die weiteren Kompatibilitäts- und Survival-Arbeiten der
[Beta-Roadmap](../project/PUBLIC_BETA_ROADMAP.md) bleiben davon getrennt offen.

Ausgangspunkt: [Untersuchung des veröffentlichten Builds](BETA_WORLD_LOAD_INVESTIGATION_20261104.md).
