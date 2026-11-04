# Beta: ergänzende echte Client-Gameplay-Abnahme, 2026-11-04

Nachtrag vom selben Tag: Die unten noch offenen Rendererfälle wurden nach der
Testpause auf E: abgeschlossen. Die [abschließende Rendererabnahme](BETA_RENDERER_ACCEPTANCE_20261104.md)
enthält die Vier-Ziele-Matrix, Rüstungsansichten und ausdrücklich verworfene Bilder.
Die folgenden Angaben beschreiben den damaligen Teilstand; historische Logbefunde
und beschädigte Belege bleiben unverändert dokumentiert.

Die funktionalen Fälle 1–5 des delegierten Auftrags wurden auf Fabric und NeoForge für Minecraft 1.21.1 und 26.2 ausgeführt und bestanden. **Keine vollständige Punkt-4-Abnahme:** Die Renderer-Matrix ist nur teilweise geprüft. Ein nachgewiesener Speichermangel auf C: verhindert den Abschluss. Zusätzlich enthielten die bisherigen Clientstarts unerwünschte Vanilla-Konto-/Realms-Anfragen; sie belegen keine vollständig auf Loopback beschränkte Netzumgebung. Diese Abweichung wird unten ausdrücklich ausgewiesen.

Maschinenlesbare Zustände, SHA-256, Prozessdaten, Kommandos und Bildbefunde: [JSON-Evidenz](beta-client-gameplay-acceptance-20261104.json). Die [vorherige Teilabnahme](BETA_CLIENT_ACCEPTANCE_20261104.md) und der separat akzeptierte [Weltlade-Guard](BETA_WORLD_LOAD_GUARD_20261104.md) bleiben unverändert. Roadmap-Integration übernimmt Root. Die natürliche Survival-Reise sowie Roadmap-Punkte 5/6 sind nicht Bestandteil dieses Berichts.

## Artefakte und Umgebung

Es wurden ausschließlich die vorhandenen DISCOVERY-JARs aus `build/beta-client-acceptance-20261104/artifacts/` verwendet. Keine Produktionsquelle wurde geändert, kein vollständiger Produktbuild ausgeführt.

| Ziel | Loader | SHA-256 des getesteten Relic-JARs |
|---|---|---|
| Fabric 1.21.1 | Fabric Loader 0.19.5 | `a10c4e665798568064ffb8eb37a25c8ded86d193ae5e4e3d785c3091243b9c16` |
| Fabric 26.2 | Fabric Loader 0.19.5 | `9ce11af173ebfd5e2db2ad85a38133c1b1bcc7832154a4dee0c5ee1df01a6508` |
| NeoForge 1.21.1 | NeoForge 21.1.256 | `86bb9380a3ed80d9bd2a15d51d1e444f2faba3a0aa53832acce52defce5cf50d` |
| NeoForge 26.2 | NeoForge 26.2.0.88 | `bfd259fe5369e3ad42a00550e11f20f44459b5a748a317d29d8f359233dee486` |

Java 21.0.10+8: `C:/Program Files/Java/jdk-21.0.10`; Temurin 25.0.4.1+1: `C:/Users/wecke/.gradle/jdks/eclipse_adoptium-25-amd64-windows.2`. Das defekte E:-JDK wurde nicht verwendet. Der Modrinth-Library-/Assetcache wurde nur gelesen. Alle Spielwelten, Client-Arbeitsverzeichnisse, Probe-JARs und Prozesse lagen unter `build/`; Fenster wurden verborgen. Fake-Token `0`, keine echten Accounts oder Nutzerprofile.

## Echte Crafting- und Schmiedewege

Die Probe öffnet den Werkblock mit `gameMode.useItemOn`, legt Zutaten mittels normaler Client-Menüpakete in die Slots und entnimmt das Ergebnis mit QUICK_MOVE. Der Server prüft anschließend alle Zutaten-Slots und das tatsächlich erhaltene Inventar. Setup-Zutaten werden durch die Operator-Fixture bereitgestellt; die Ergebnisse werden nicht direkt vergeben.

| Rezept | Vorher | Nach Ergebnisentnahme |
|---|---|---|
| Vorlage duplizieren | 1 Vorlage, 7 Diamanten, 1 Kupferblock | 2 Vorlagen, sämtliche Zutaten-Slots leer |
| Maschinenkern aufladen | Kern mit Budget 0, Amethyst, 2 Kohleblöcke | 1 Kern mit Budget 256, Zutaten verbraucht |
| Magnet reparieren | Magnet mit Budget 0, Amethyst, 4 Eisenbarren | 1 Magnet mit Budget 1000, Zutaten verbraucht |
| Schmiedevorlage anwenden | Vorlage, Diamantbrustplatte, Amethyst | Brustplatte mit `relics:monolith` / `minecraft:amethyst`, Zutaten verbraucht |

Alle vier Pfade bestanden auf allen vier Zielen. Die drei Crafting-Fälle öffnen zusätzlich das echte Rezeptbuch. Die Ergebnisse bleiben zusammen im Inventar: 2 Vorlagen, 1 Kern, 1 Magnet und 1 verzierte Brustplatte. Die gespeicherten NBT-Inventare stimmen nach vollständigem Prozessneustart exakt überein; ein weiterer Save/Menu/Reload im selben Prozess bestätigt dieselben Werte. Die Runtime-Snapshots bestätigen 256 beziehungsweise 1000 Budget, die NBT-Komponenten das angewandte Trim.

Geprüfte Bilder: [Rezeptbuch](images/beta-gameplay-20261104-recipe-book.png), [Fabric 1.21.1 Schmiede](images/beta-gameplay-20261104-smith-fabric21.png), [Fabric 26.2](images/beta-gameplay-20261104-smith-fabric26.png), [NeoForge 1.21.1](images/beta-gameplay-20261104-smith-neo21.png), [NeoForge 26.2](images/beta-gameplay-20261104-smith-neo26.png). Im kleinen GUI-Fenster überlagert das Rezeptbuch Teile des Rasters; der Tutorialhinweis verdeckt einen Teil der Rüstungspuppe. Ergebnis und Inventar sind sichtbar. Eine ungestörte Nahansicht der getragenen Rüstung bleibt als Rendererfall offen.

## Gemeinsame Ereignisse und persönliche Ansprüche

**Operator-vorbereitete Testarena:** Native Trial-Spawner-/Vault-Blöcke und registrierte Relic-Fixtures, ebener Boden, bereitgestellte Diamantschwerter und Unverwundbarkeit. Der Operator positioniert echte Spieler in der Arena, nahe den physischen Drops und am Vault. Die verwendeten ServerPlayer stammen ausschließlich aus tatsächlichen Clientverbindungen. Keine simulierten Spieler, keine direkte Reward-Vergabe, kein künstlicher `playerTouch`-Aufruf.

Die Clients greifen den vom Trial-Ereignis erzeugten Golem über ihren normalen Angriffspfad an. Der Sieg erzeugt für beide Teilnehmer legitime persönliche Schlüssel-Drops. Die Clients sammeln die ItemEntities auf, wählen den Schlüssel per Inventarpaket und benutzen den Vault über den Client-Netzpfad. Der Vault erzeugt einen separaten physischen Core-Drop für jeden berechtigten Spieler. Drop-UUID, Spieler-UUID, Ledgerphase und Empfangsbeleg werden aufgezeichnet.

Vier ergänzende Kurzläufe prüfen den Schlüsselverbrauch direkt am Serverinventar: Für beide Spieler gilt bereits `keys=0`, während die persönliche Core-Ausgabe noch `QUEUED` ist; gleichzeitig ist `keyPaid=true`. Erst später folgen physischer Core und DELIVERED. Die Abfrage läuft im Testtakt, nicht als Zeitmessung innerhalb eines einzelnen Pakethandlers.

| Ziel | Gemeinsamer aktiver QA-Zeitraum | Abgeschlossene Ereignisse | Eindeutige physische Drops | Persönliche Vault-Ansprüche |
|---|---:|---:|---:|---:|
| Fabric 1.21.1 | 20:38,482 | 11 | 44 | 22 |
| Fabric 26.2 | 21:07,457 | 12 | 48 | 24 |
| NeoForge 1.21.1 | 23:37,480 | 8 | 32 | 16 |
| NeoForge 26.2 | 20:55,020 | 10 | 40 | 20 |

Dies sind tatsächliche Zeiträume vom ersten gemeinsamen Arena-Setup bis zum letzten abgeschlossenen Ereignis, jeweils mindestens 20 Minuten. Zwischen Ereignissen liegen 45 Sekunden; jedes nächste Ereignis findet an einer neuen Fixture statt. Insgesamt 41 Ereignisse, 82 Schlüssel, 82 Cores und 164 unterschiedliche physische Drop-UUIDs. Host und Gast senden wiederholt echte Angriffe und Schlüsselbenutzungen. Die JSON-Evidenz zählt diese **Client-Anfragen**; wiederholte Anfragen sind keine zusätzlichen konsumierten Schlüssel oder erfolgreich treffenden Angriffe. Dies ist ein benannter funktionaler QA-Zeitraum, kein allgemeines Performancebudget und keine Survival-/Balanceabnahme.

In den frühen NeoForge-Langläufen wurden weggelaufene Golems durch Operator-Teleports wieder erreichbar gemacht: einmal NeoForge 26.2, zweimal NeoForge 1.21.1. Der wiederverwendbare Helfer führt diese Positionierung inzwischen selbst aus. Die betroffenen Aktionen sind als Operator-Intervention im Log sichtbar.

Nach Erhalt reconnectet derselbe Gast mit UUID `b2c6551d-8ddf-3bc0-84e1-962967c209f5` in einem neuen echten Clientprozess. Host-UUID: `00000000-0000-0000-0000-000000000001`. Vollständiger Prozessneustart erfolgt auf einer isolierten Kopie des zuvor gespeicherten Weltstands; anschließend folgt zusätzlich Save/Menu/Reload und ein weiterer Gastprozess mit gleicher UUID. Der unabhängige NBT-Vergleich bestätigt auf allen vier Zielen exakt gleiche vollständige Inventare und gespeicherte Empfangsbelege sowie identische Ledger. Jeder Spieler behält genau einen Core pro abgeschlossenem Ereignis, keine Schlüssel, keine doppelten Claims.

Spätes Eintreffen wird getrennt geprüft:

- **Während ACTIVE:** zunächst ein Teilnehmer, dann der real verbundene Gast als zweiter Teilnehmer; beide erhalten ihre persönlichen Schlüssel und Cores. Die abschließenden vier Kurzläufe enthalten zugleich den direkten Schlüsselverbrauchsbeleg.
- **Nach Ende:** neuer echter Spieler `BetaLate` wird an die bereits abgeschlossene erste Arena gebracht. Kein Inventar, kein Empfangsbeleg, kein nachträglicher Claim und keine Änderung am Ledger. Dasselbe gilt nach Save/Reload und erneutem Verbindungsaufbau. Kein Vault-Benutzungsversuch ohne vorhandenen Schlüssel wird als zusätzlich bestandener Negativfall behauptet.

## Renderer: geprüfte Bilder und verbleibende Lücken

Die Bilder sind tatsächliche Minecraft-Rendereraufnahmen und wurden mit `view_image` angesehen. Die neue Fixture liest die Weltgen-Templates und Markerpositionen aus dem getesteten JAR. Für V4 wird ausschließlich das Ausstellungsvolumen vor der unveränderten Template-Platzierung von Gelände freigeräumt. Die native Markerersetzung entspricht der Version. Spectator-Kamera und Night Vision machen Innenräume prüfbar. Dies belegt keine natürliche Geländeeinbettung oder natürliche Beleuchtung.

Vollständige Familienansichten sind jetzt vorhanden und geprüft: [Colossus](images/beta-gameplay-20261104-colossus.png), [Obelisk](images/beta-gameplay-20261104-obelisk.png), [Titan Skull](images/beta-gameplay-20261104-titan-skull.png), [Small Colossus](images/beta-gameplay-20261104-small-colossus.png), [World Tree](images/beta-gameplay-20261104-world-tree.png), [Ruined Tower](images/beta-gameplay-20261104-ruined-tower.png), [Titan Skull 2](images/beta-gameplay-20261104-titan-skull-2.png). Der Turm ist einschließlich Spitze und Sockel sichtbar. Es wurde kein Modell neu gestaltet.

Geprüfte Details: [Amethyst im Baum](images/beta-gameplay-20261104-tree-amethyst.png), [Firefly Bush 26.2](images/beta-gameplay-20261104-firefly-26.png), [Farnersatz 1.21.1](images/beta-gameplay-20261104-fern-21.png), [normale Truhe 1.21.1](images/beta-gameplay-20261104-chest-21.png), [Kupfertruhe 26.2](images/beta-gameplay-20261104-chest-26.png). Die retained Bilddateien sind bytegleich mit ihren ursprünglichen Screenshots; 17 ausgewählte Bilder sind im JSON mit konkretem Sichtbefund und beiden Hashreferenzen dokumentiert.

**Offen:** vollständige wiederholbare Sichtabnahme der Familien und Innenraum-Interaktionspunkte auf allen vier Zielen, ungestörte Rüstungsansicht sowie Ersatz der ungültigen letzten Aufnahmen. V3 hatte teilweise Gelände-/Blattüberdeckung. V4 korrigiert die Testaufstellung, aber die letzten acht PNGs sind wegen des dokumentierten Schreibproblems nicht lesbar. Sie werden ausdrücklich nicht als visuell bestanden gezählt. Die sieben hier verlinkten Familienansichten stammen überwiegend aus NeoForge 26.2; daraus wird keine Vier-Ziele-Modellvollabnahme abgeleitet.

## Nachgewiesenes Hindernis und Logabweichungen

Am 2026-11-04 um 12:24:53/54 scheiterten vier neue Fixture-Kopien mit `shutil.Error` und `[Errno 28] No space left on device`. `Get-PSDrive C` zeigte 0 freie Bytes. Bytegleiche, selbst erzeugte Test-JAR-Duplikate wurden hashgeprüft als Hardlinks zusammengefasst (1.234.447.659 Byte eingespart), ausschließlich der eigene Gameplay-Testordner wurde NTFS-komprimiert. Kein Dateiinhalt wurde dabei verändert; rund 2 GB wurden vorübergehend frei.

Bei den V4-Rendererläufen trat das Problem erneut auf. Die Original-Logs enthalten `Low disk space! Might not be able to save the world` und `Not storing chunk IO report due to low space`. Die acht letzten beschädigten PNGs sind einzeln im JSON ausgewiesen. Auch die jeweiligen `process.json`-Dateien sind leer; hier wird kein erfolgreicher Exit behauptet. Nach zunächst angefordertem `Minecraft.stop()` blieben die Prozesse im fehlschlagenden Save-I/O. Ausschließlich die zuvor anhand ihrer vollständigen Test-Launchargs identifizierten PIDs 30788 und 35136 wurden daraufhin beendet. Es laufen keine Gameplay-Testclients mehr.

Betroffene Läufe: `build/beta-client-gameplay-20261104/neoforge-26.2-122834` und `fabric-1.21.1-122844`. Betroffene Versionen sind damit konkret NeoForge 26.2 und Fabric 1.21.1; weitere Rendererstarts wurden wegen des gemeinsamen vollen Laufwerks nicht vorgenommen. Keine unbestätigte Produktursache wird angenommen.

Der Starter prüft jetzt vor Kopie/Start 2 GiB freien Scratch-Platz. Der tatsächliche erneute Aufruf brach vor jeder Mutation mit `QA scratch storage insufficient: 22753280 free bytes` ab. Diese Reserve ist eine Schutzbedingung für Testdateien, kein Gameplay-Performancebudget. Reparatur: ausreichenden freien Platz auf C: bereitstellen oder einen anderen Scratch-Ort ausdrücklich autorisieren; dann die verbleibenden Rendererfälle wiederholen. Die automatische Freigabeprüfung lehnte das Entfernen vier unvollständiger eigener Scratch-Kopien mit `blocked by policy` ab; diese Löschung wurde nicht ausgeführt.

Die 48 erfolgreichen funktionalen Prozesse sind **nicht fehlerlogfrei**. Vanilla-Konto-/Realms-Anfragen mit Offline-Fake-Token 0 lieferten 401-Fehler. Obwohl sämtliche Minecraft-Spielverbindungen Loopback-Verbindungen waren und keine externen Spieler beteiligt waren, widersprechen diese Dienstanfragen der verlangten vollständigen Netzbeschränkung. Der neue Starter setzt deshalb eine eigene `jdk.net.hosts.file` mit ausschließlich Loopback-Einträgen; Gaststarter erzeugen dieselbe Datei. Eine separate Probe auf beiden verwendeten JDKs bestätigt lokale Auflösung und `UnknownHostException` für externe Dienstnamen. Eine echte Minecraft-Wiederholung mit dieser neuen Sperre steht wegen des Speicherhindernisses noch aus. Die bisherigen Läufe werden nicht rückwirkend als vollständig netzisoliert deklariert.

Zwei Gastlogs enthalten nach dem Verlassen des Hosts außerdem `Connection reset` / `Negative index in crash report handler (13/21)`, einmal mit NeoForge-FATAL-Berichtsvorbereitung. Die betreffenden Gastprozesse endeten mit Exitcode 0; Zustandsprüfungen und die lange gemeinsame Sitzung waren vorher abgeschlossen. Diese Meldungen bleiben ungekürzt in der Evidenz und werden nicht als während des gemeinsamen Ereignisses aufgetretener Produktfehler oder als sauberes Disconnect-Ergebnis umgedeutet. Der neue Begegnungshelfer beendet den Gast bei Verbindungsende selbst.

## Reproduktion und Preservation

Neue wiederverwendbare Quellen: [Clientstarter](../../tools/test_beta_gameplay_client.py), [Gaststarter](../../tools/test_beta_gameplay_guest.py), [Rendererfälle](../../tools/prepare_beta_visual_cases.py), [unabhängige Evidenzprüfung](../../tools/collect_beta_gameplay_evidence.py) sowie `src/test/client/de/relics/testmixin/Beta*.java`. Probe-Kompilate sind getrennt vom Produkt-JAR. Fabric 1.21.1 wird über Loom remappt; die native 1.21.1-Preparation wurde nicht parallel dazu gestartet. Der vorhandene Neo26-Loggeradapter bleibt unverändert; keine Fehler oder Log-Level wurden gefiltert.

Beispielkommandos aus dem Workspace, nach Behebung des Speicherhindernisses:

```powershell
# Neuer funktionaler Lauf; der Starter gibt das neue build/-Verzeichnis aus.
python tools/test_beta_gameplay_client.py --fixture build/beta-client-acceptance-20261104/client-26.2-105935-270526 --encounter --port 25841
# In separatem Prozess, mit dem tatsächlich ausgegebenen Verzeichnis:
python tools/test_beta_gameplay_guest.py build/beta-client-gameplay-20261104/<neuer-lauf> 25841
# Gleicher gespeicherter Zustand in neuem Hostprozess, danach Save/Menu/Reload:
python tools/test_beta_gameplay_client.py --fixture build/beta-client-gameplay-20261104/<abgeschlossener-lauf> --verify --port 25842
python tools/test_beta_gameplay_guest.py build/beta-client-gameplay-20261104/<neuer-verify-lauf> 25842 --repeat
# Spät während ACTIVE: --encounter --late; nach Ende: --verify --late-end,
# dabei Gast mit --repeat --name BetaLate.
# Crafting ohne --encounter; anschliessende Persistenz mit --verify --solo.
# Weitere Ziele: --minecraft 1.21.1 beziehungsweise --loader neoforge,
# passende akzeptierte Fixture aus der untenstehenden Tabelle verwenden.
python tools/collect_beta_gameplay_evidence.py
```

| Ziel | Akzeptierte Ausgangs-Fixture unter `build/beta-client-acceptance-20261104/` |
|---|---|
| Fabric 1.21.1 | `client-1.21.1-110010-680449` |
| Fabric 26.2 | `client-26.2-105935-270526` |
| NeoForge 1.21.1 | `neo-client-1.21.1-110000-535487` |
| NeoForge 26.2 | `neo-client-26.2-110020-943280` |

Rendererfälle werden mit `prepare_beta_visual_cases.py --artifact <genaues-JAR> --minecraft <Version> --output <build/Datei.json>` erzeugt und mit `test_beta_gameplay_client.py --fixture <Fixture> --visual-cases <build/Datei.json>` gestartet. Alle konkreten Java-Kommandos, PIDs, Start-/Endzeiten, finalen Loghashes, generierten Probequellen und Probe-JAR-Hashes stehen im JSON. Die 24 erfolgreichen Hostläufe und 24 Gastläufe sind dort vollständig einzeln gebunden. Historische Host-`process.json` können noch Hashes von damals laufenden Gastlogs enthalten; maßgeblich sind die zusätzlich erfassten **finalen geschlossenen** Loghashes.

Die ursprüngliche Preservation-Baseline umfasst 1.735 vorhandene getrackte und ungetrackte Dateien. Der Abschlussvergleich findet ausschließlich die beiden ausdrücklich autorisierten Root-Audioänderungen an `tools/test_distribution_client.py` und `tools/test_world_load_neoforge_client.py`; deren aktuelle Hashes stimmen mit der protokollierten Autorisierung überein. Geschützte Produktions-/Test-/Dokumentationsdateien einschließlich Roadmap sowie fremde Änderungen bleiben unverändert. Keine Git-Indexänderung, kein Commit, Push, Tag oder Release.

Alle aktuell vorhandenen `options.txt` unter den beiden Beta-Testordnern sind mit ihren aktualisierten Hashes im JSON erfasst. Root meldete für die acht zuvor laufenden Test-PIDs erfolgreich geprüftes CoreAudio-Mute ohne Neustart. Die neuen Helfer setzen `soundCategory_master:0.0` vor jedem Start und zusätzlich MASTER 0.0 in-process. Keine Audioeinstellung außerhalb der Testprozesse und kein Nutzerprofil wurde geändert.
