# Natürliche Innenräume, Minecraft 26.2 / Fabric

Niklas hat die überarbeiteten Innenräume am 27. Oktober 2026 freigegeben.
Neue Welten verwenden Großer Koloss V6, Kleiner Koloss V9, Turmruine V9,
Obelisk V6 Archäologie und den bereits freigegebenen Weltenbaum V5.
Der Spieler-Build liegt unter `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`.
Er wurde mit und ohne erneute Ressourcengenerierung bytegleich gebaut.
SHA-256: `4421a9a03cc3d926484196fc4f94db42c521bd110f1e58aa5cb68176aba76783`.

## Weltversion und Vorlagen

`relics.gameplay.integration.json` bindet die freigegebenen NBT-Exporte und
Gameplay-Sidecars an die neuen Roh- und Worldgen-Vorlagen. Der Build prüft
Marker, Freiräume, abgeleitete Vorlagen und Hashes auch bei `--skip-generation`
gegen die Quellen. Manipulierte Marker werden abgewiesen. Die zusätzliche
Worldgen-Ableitung behält Größe, Ursprung, Drehung und Terrainbedingungen der
jeweiligen alten Vorlage bei. Verteilung, Seltenheiten und Kartenkoordinaten
werden dadurch nicht neu ausgewürfelt.

Neue Welten speichern `interiors-20261027-v1` im eingefrorenen
Verteilungsjournal. Vorhandene Journale ohne dieses Feld bleiben `legacy`.
Vorhandene Welten ohne Verteilungsjournal behalten ihre bisherige Platzierung.
Die zwanzig bisherigen Roh- und Worldgen-Vorlagen sowie die öffentlichen
Struktur- und Poolkennungen bleiben erhalten. Dadurch ändern sich gespeicherte
Fingerprints und Ziele alter Welten nicht. Es gibt keine automatische
Nachrüstung bereits erstellter Welten. Unbekannte Versionen werden abgewiesen.

Die fünf neuen Designs ergeben zehn zusätzliche NBT-Ressourcen. Die
spielerische Initialisierung setzt eine vom Verteilungsplaner erzeugte,
mit dem Structure-Piece gespeicherte Herkunft voraus. Ein mit `/place template`
gesetztes Rohmodell oder ein Spieler-Nachbau erhält dadurch keine natürlichen
Belohnungen, Gegner oder Weltenbaum-Aura.

## Verhalten im Spiel

- Großer Koloss: konfigurierte Prüfung und Vault, Registrierung der
  Golemposition und der getrennten Arm-Truhe. Die Truhe enthält einen vollen
  Bergungsmagneten sowie 24–40 Kupfer, 8–16 Eisen, 0–4 Redstone und
  0–2 Amethystscherben. Die bestehende Begegnungs- und Anspruchslogik übernimmt
  Golem, Schlüssel und Vault-Belohnungen.
- Kleiner Koloss: eine einmalige Truhe mit 12–20 Kupfer, 4–8 Eisen,
  0–2 Redstone und 0–1 Amethystscherben. Mit 10 Prozent Wahrscheinlichkeit
  liegt ein defekter Magnet mit null verbleibendem Budget darin.
- Turmruine: fünf normale Endermen mit gespeicherten Initialisierungsaktionen.
  Entfernte oder verschwundene Endermen werden nicht erneut erzeugt. Die
  einmalige Truhe enthält mit 5 Prozent Wahrscheinlichkeit ein Enderauge,
  sonst 4–6 Enderperlen. Der unterbrochene Aufstieg bleibt erhalten.
- Obelisk: sechs gewöhnliche verdächtige Sandblöcke, eine garantierte
  Monolith-Schmiedevorlage und eine echte Expeditionskarte. Die gewöhnlichen
  Funde verteilen sich auf Scherbe 25, Ton 20, Ziegel 15, Knochen 10,
  Faden 10, Weizensamen 10, Eisennugget 5 und Kupfer 5 Prozent.
  Karten teilen das eingefrorene Koloss-Ziel. Steht bereits bei der
  Initialisierung fest, dass es keines gibt, enthält diese Fundstelle
  einmalig drei Smaragde. Noch ausstehende Ziele bleiben echte ausstehende
  Karten und nutzen die vorhandene Auflösungs- und Entschädigungslogik.
- Weltenbaum: Registrierung des natürlichen Aura-Ankers für die bestehende
  Regeneration im freigegebenen Wurzelbereich.

Zufallsentscheidungen hängen von Weltseed und stabiler Markerkennung ab.
Der Build verlangt derzeit genau eine Truhe pro Koloss beziehungsweise Turm,
damit das Materialbudget pro Bau eingehalten wird.

Nur ausgelassene Zellen in den vereinbarten Freiraumregionen werden geräumt.
Beim Visier kommen die im freigegebenen Vergleich entfernten Schalenblöcke
hinzu. Ausgeschlossene Quellblöcke, Glasreste und andere Strukturen bleiben
erhalten. Die erlaubte Terrainliste umfasst auch natürliche Stämme und Laub,
weil Nachbarchunks vor der lokalen Platzierung bereits Bäume setzen können.
Die freigeräumten Luftzellen werden gegen spätere Worldgen-Schreibzugriffe
geschützt. Normales Abbauen und Bauen bleibt möglich.

Die owning-chunk-Attachments speichern Herkunft und abgeschlossene Aktionen.
Blockentity-Inhalte und Abschlussmarker werden im selben Chunk gespeichert.
Die Initialisierung läuft auf dem Serverthread nach Veröffentlichung des
FULL-Chunks. Der Chunk-Ladecallback stellt nur Arbeit in die Warteschlange.
Das vermeidet einen im ersten Test gefundenen zyklischen FULL-Chunk-Wartezugriff.
Interaktionen mit noch nicht initialisierten Markern werden bis dahin gesperrt.

## Nachweise und Grenzen

Die maschinenlesbaren Ergebnisse stehen in
[natural-interiors-20261027-evidence.json](natural-interiors-20261027-evidence.json).
Isolierte echte Fabric-Server generieren die Bauten über geplante natürliche
Starts. Vollständige Grundflächen werden geladen, gespeicherte Blöcke gegen
die ausgelieferten Vorlagen und Freiräume gegen Luft und Schutzmasken geprüft.
Alle vier Drehungen sind vertreten. Native Truhen, Brushables, Vault,
Prüfung, Endermen und der Aura-Anker werden direkt abgefragt. Zwei
Obelisk-Karten zeigen auf dasselbe gespeicherte Ziel. Entfernte Truhen,
verbrauchte Fundstellen und entfernte Endermen bleiben nach Neustart entfernt.
Eine Welt mit von Beginn an deaktiviertem Koloss prüft die Smaragdentschädigung.
Eine zusätzliche Welt prüft das Fortsetzen teilweise generierter Pieces nach
dem Neustart. Altwelten beider bisherigen Verteilungsversionen wurden nur als
Kopien geöffnet; Ziel, Spawn und Fingerprint blieben erhalten.

Im Hauptlauf stimmten 1.242.456 geprüfte feste Blockzellen mit den Vorlagen
überein. Alle 57.398 zusätzlichen Freiraumzellen waren frei und geschützt.
Der Hashvergleich gegen die 1.095 vor der Integration erfassten Dateien
bestätigt 1.082 unveränderte Dateien und genau 13 beabsichtigte Änderungen
an Integration, Tests und Freigabedokumentation. Alle 35 im freigegebenen
Handoff gebundenen Exportdateien blieben bytegleich. Die vorhandenen lokalen
NeoForge-Dateien und die übrigen fremden Änderungen blieben ebenfalls erhalten.

Weitere Prüfungen: 121 bisherige Python-Tests, drei neue Integrationsprüfungen,
755 Worldgen-Assertions, 45 statische Mixin-Verträge, 648 Gameplay-Assertions,
1.008 Executor-Prüfungen, 675.716 Suchprüfungen und 198.924 synthetische
Verteilungsprüfungen. Die synthetischen Tests ersetzen die Serverläufe nicht.
Der Blockvergleich berücksichtigt native Blattabstände und dreht die
horizontalen Seiten von Glow Lichen entsprechend der Vorlage.

Die Tests umfassen Servergenerierung, gespeicherte Blockzustände und normale
Speicher-/Neustartzyklen. Eine visuelle Abnahme von Minecraft-Blocklicht, ein
vollständiger Survival-Durchlauf und beliebige harte Prozessabbrüche zwischen
Chunk-, Entity- und Spielerdateien sind damit nicht bewiesen. Es wurde kein
Nutzerprofil installiert und kein Release veröffentlicht. Die bestehenden
lokalen NeoForge-Arbeiten bleiben unverändert; dieser Integrationsstand ist
für Minecraft 26.2 / Fabric gebaut und getestet.

## Reproduktion

Mit dem vorbereiteten JDK 25 und den vorhandenen Abhängigkeiten:

```powershell
$jdk = 'build/toolchains/zulu25.36.205-ca-jdk25.0.4.1-win_x64'
python tools/build.py --java-home $jdk
python tools/test_distribution.py --java-home $jdk
python tools/test_gameplay.py --java-home $jdk
build/distribution-venv/Scripts/python.exe -m unittest discover -s tests -p test_natural_interiors.py
build/distribution-venv/Scripts/python.exe tools/test_natural_interiors_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar
```

Der letzte Befehl wird für die Randfälle zusätzlich mit `--unavailable`
und `--resume` ausgeführt. Die Server bleiben lokal, auf Whitelist beschränkt
und in neuen Welten unter `build/`. Das Testmod ist nicht im Spieler-JAR.
