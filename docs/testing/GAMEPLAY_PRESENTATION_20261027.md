# Spawner, Vault und Rezeptbuch: Rückmeldung vom 27. Oktober 2026

Der Spieltest bestätigt angreifenden Golem, Schlüssel, Vault und nutzbaren
Maschinenkern. Gemeldet wurden fehlende Spawner-/Vault-Animationen und ein
fehlendes Rezept im Crafting Book. Die Bilder zeigen den Kern im Hochofen
sowie den erhaltenen, bei null Ladungen inaktiven Kern. Sie sind kein Nachweis
für den vollständigen Ablauf der Animationen.

## Ursache und Änderung

Die beiden Serveradapter unterdrückten den normalen Blockablauf. Beim Spawner
wurden nur Aktiv- und Abklingzustand gesetzt; beim Vault wurde jeder Zustand
laufend auf aktiv zurückgesetzt. Schlüssel und Kern gingen über die gespeicherte
persönliche Zustellung direkt ins Inventar. Der Kern war als verborgenes
Spezialrezept ohne Rezeptbuchanzeige registriert.

Die Zustellung bleibt persönlich und nutzt weiterhin Reservierungen und
gespeicherte Spielerbelege. Es entstehen keine zusätzlichen gemeinsamen
Schlüssel- oder Kern-Drops.

- Der Spawner erhält 40 Ticks Vorlauf mit synchronisierter Drehung sowie
  Erkennungs- und Spawn-Effekte. Nach bestätigtem Sieg folgt die Warte- und
  Ausgabephase mit Öffnen und Schließen des Verschlusses. Schlüssel werden
  frühestens nach 60 Ticks zugestellt; die Ausgabephase reicht bis Tick 80.
  Der bestehende 36.000-Tick-Cooldown und die Ein-Golem-Regel bleiben bestehen.
- Der Vault berücksichtigt anwesende Spieler mit noch offenem Anspruch.
  Die native Öffnungsphase dauert 14 Ticks, danach folgt die Ausgabephase.
  Der Kern wird frühestens nach weiteren 20 Ticks zugestellt. Normale
  Übergangsgeräusche und Ausgabeeffekte werden gesendet. Nach der Präsentation
  schließt der Vault, wenn kein berechtigter Spieler mehr davor steht.
  Mehrere Anspruchsberechtigte erhalten ihre gespeicherten Ausgaben nacheinander.
- Die absoluten Zeitpunkte werden im vorhandenen Gameplay-Journal gespeichert.
  Vorhandene Einträge ohne diese zusätzlichen Felder beginnen bei null;
  bereits verbuchte Ansprüche werden nicht zurückgesetzt.
- Kernaufladung und Magnetreparatur erhalten sichtbare, über das native
  Netzwerkformat übertragene Rezeptbuchanzeigen und Platzierungsdaten.
  Der Besitz des jeweiligen Gegenstands im Inventar schaltet das Rezept frei.
  Der Kern-Eingang wird im Rezept als leer dargestellt. Die strikte Prüfung
  der Ladung und der Erhalt eigener Gegenstandsdaten bleiben bestehen.

## Kernrezept

Einen ersten Kern gibt es aus dem Vault. Die Werkbank lädt einen vorhandenen
vollständig leeren Kern wieder auf: Amethystscherbe oben mittig, leerer Kern
direkt darunter, ein Kohleblock links und einer rechts vom Kern. Alle übrigen
Felder bleiben frei. Ergebnis ist derselbe Kern mit 256 Verarbeitungsvorgängen.
Teilweise geladene Kerne, lose Kohle und Holzkohle sind nicht zugelassen.

## Prüfung

`tools/test_gameplay.py` besteht mit 657 Gameplay-Assertions und 49 statischen
Mixin-Verträgen. Sechs Ressourcen-/Artwork-Tests bestehen ebenfalls. Die
zusätzlichen Prüfungen lesen die Rezeptbuchanzeige einschließlich leerem
Kernzustand und prüfen ihren nativen Codec sowie gespeicherte Ausgabezeitpunkte.

`tools/test_gameplay_presentation_server.py` startet einen echten, isolierten
Fabric-Server mit dem Spieler-JAR. Ein separates, nicht ausgeliefertes Testmod
erzeugt zwei Survival-Testspieler mit Paketempfängern anstelle grafischer
Clients. Es prüft den Golemvorlauf, genau einen Golem und zwei Teilnehmer,
bestätigten Tod, verzögerte Schlüssel, die wirkliche Vault-Interaktion durch die
Mixins, Öffnungs-/Ausgabezustände, Schlüsselverbrauch, genau einen Kern je Spieler
und Ablehnung eines wiederholten Anspruchs. Vier persönliche Zustellungen
besitzen bestätigte gespeicherte Belege. Die normalen Effektpakete 3011 bis
3017 werden beobachtet; ein tatsächlich freigeschaltetes Rezeptbuch sendet
seine Anzeige. Nach einem vollständigen Serverneustart sind Ansprüche,
Zeitpunkte und die vier abgeschlossenen Zustellungen weiterhin vorhanden.

Der Lauf ist Server-/Paketnachweis. Die Darstellung, Geräusche und Bedienung in
einem echten grafischen Client müssen beim nächsten Spieltest bestätigt werden.
Es wurden keine Nutzerwelt und keine laufende Minecraft-Instanz verändert.
Der Generator und die freigegebenen Innenraumdateien bleiben unverändert.
Für dieses Update ist keine neue Welt erforderlich. Nach Austausch der JAR
den Server beziehungsweise die Instanz neu starten. Für einen bereits in einem
Ofen liegenden Kern diesen einmal ins Inventar nehmen, um das Rezept freizuschalten.

## Artefakt und Reproduktion

Build: `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`

SHA-256: `0f25a3a57a471c5d3f393a5210cc9046bc92abc7d3fc3884f4095ebfe86d2f5c`

Die maschinenlesbaren Ergebnisse stehen in
[gameplay-presentation-20261027-evidence.json](gameplay-presentation-20261027-evidence.json).
Der vorherige Spieler-Build und die geänderten Ausgangsdateien liegen als
begrenzte Sicherung unter `build/gameplay-feedback-20261027/before.zip`.

```powershell
$jdk = 'build/toolchains/zulu25.36.205-ca-jdk25.0.4.1-win_x64'
python tools/test_gameplay.py --java-home $jdk
python tools/build.py --skip-generation --java-home $jdk
python tools/test_gameplay_presentation_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar
```
