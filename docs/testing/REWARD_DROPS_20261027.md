# Magnet und echte Belohnungsauswürfe

Niklas hat am 27. Oktober 2026 nach dem Survival-Test eine um etwa zehn Prozent
schnellere Magnetanziehung und echte Auswürfe aus Trial Spawner und Vault
angefordert. Diese Änderung ersetzt die persönliche Inventarzustellung für
Schlüssel und Maschinenkern aus dem vorherigen Präsentationsstand.

## Verhalten

Die Magnetbeschleunigung steigt von 0,08 auf 0,088 und die begrenzte
Geschwindigkeit von 0,35 auf 0,385 Blöcke pro Tick. Radius, Sicht-/Kollisionsprüfung,
Nebenhandpflicht, Survival/Adventure und das Budget von 1.000 erfolgreichen
Aufnahmen bleiben bestehen. Ein erfolgloser Aufnahmeversuch verbraucht nichts.

Jeder berechtigte Teilnehmer erhält nach dem Golemkampf einen echten Schlüssel
als ItemEntity oberhalb des Spawners. Der Vault wirft nach seiner Öffnungsphase
einen vollen Maschinenkern oberhalb des Blocks aus. Beide besitzen Anfangsbewegung,
Schwerkraft und eine kurze normale Aufhebesperre. Die bisherigen Blockzustände,
Geräusche und Effektpakete werden weiter verwendet. Die Gegenstände müssen
aufgehoben werden; der Auswurf allein fügt dem Inventar keinen Gegenstand hinzu.

Die Auswürfe bleiben bis zur Aufnahme dem jeweiligen berechtigten Spieler
zugeordnet. Ein volles Inventar verhindert weder den Auswurf noch löscht es den
Anspruch. Fremde Spieler, Magnete fremder Spieler und Hopper können ihn nicht
einziehen. Die markierten Weltgegenstände verschmelzen nicht, verfallen nicht
und werden vor gewöhnlichem Schaden geschützt. Nach dem Aufheben sind Schlüssel
und Kern normale übertragbare Gegenstände. Neu vom Spieler weggeworfene Items
übernehmen die interne Auswurfsmarkierung nicht. Gewöhnliche Hopper bleiben
funktionsfähig. Die bestehende Smaragdentschädigung für Karten bleibt eine
Inventartransaktion.

## Speicherung

Das vorhandene Gameplay-Journal erhält additive Zustände `DROP_RESERVED` und
`DROPPED` sowie die feste Entity-UUID und den Ursprung des Auswurfs. Vor dem
Einfügen eines Gegenstands in die Welt wird seine UUID gespeichert. Beim Kern
wird der Schlüssel genau einmal beim Auswurf bezahlt; ein gesonderter,
auf der Platte geprüfter Spielerbeleg bestätigt diesen Verbrauch.

Die ItemEntity speichert ihre Lieferkennung in einem Fabric-Attachment.
Beim Aufheben werden Empfänger, UUID, Lieferzustand und vollständiger
Gegenstand geprüft. Die Aufnahme durch die normale Inventarfunktion schreibt
anschließend den bisherigen Spielerbeleg. Erst dieser bestätigt `DELIVERED`.
Ein erneut geladener alter Entity-Snapshot einer bereits bestätigten Aufnahme
wird verworfen. Die Magnetabrechnung läuft weiterhin nach erfolgreicher
positiver Aufnahme durch denselben nativen Pfad.

Es werden keine entfernten Chunks zum Auswerfen oder Suchen nach verlorenen
Entities geladen. Offline-Teilnehmer behalten ihre gespeicherte Warteschlange;
die Ausgabe wartet auf den verfügbaren Spieler und geladenen Ursprungsbereich.
Ein fehlender oder unklar gespeicherter Gegenstand wird nicht automatisch als
zweiter Auswurf ersetzt. Beliebige harte Prozessabbrüche zwischen den getrennten
Spieler-, Entity- und Journaldateien sind weiterhin keine nachgewiesene gemeinsame
Datentransaktion. Unklare Aufnahmen werden mit der bestehenden Beleglogik
gehalten und nicht blind neu ausgegeben. Konsistente Sicherungen und Diagnose
bleiben für solche Fehlerfälle erforderlich.

## Tatsächlich geprüft

Der echte isolierte Fabric-Server verwendet zwei Survival-Testspieler mit
Paketempfängern. Ein separates Testmod wird nicht im Spieler-JAR ausgeliefert.

- Genau ein Golem, je ein persönlicher Schlüssel, Öffnungs- und Ausgabezustände
  sowie normale Effektpakete.
- Zwei gleichzeitig sichtbare Schlüssel als getrennte Weltgegenstände, auch
  bei vollem Inventar eines Teilnehmers. Kein direkter Inventarzugang.
- Aufhebesperre, fremder Spieler, Hopper-Sperre und unveränderte gewöhnliche
  Hopperaufnahme. Fehlgeschlagene Aufnahme bei vollem Inventar erhält das Item.
- Tatsächliche Vault-Interaktion, ein Schlüsselverbrauch pro Anspruch, echter
  Kern-Auswurf und Abweisung eines erneuten Anspruchs ohne zusätzlichen Verbrauch.
- Drei aufgenommene Belohnungen und ein liegender Kern werden gespeichert.
  Nach vollständigem Serverneustart existiert derselbe Kern mit derselben UUID.
  Der berechtigte Spieler hebt ihn anschließend auf; alle vier Belege sind gespeichert.
- Ein künstlich erneut geladener alter Kern-Snapshot mit der bereits quittierten
  UUID wird verworfen und erzeugt keinen zweiten Kern.
- Die native Magnetbewegung eines gewöhnlichen Drops erreicht
  `0.38500000000000006` Blöcke pro Tick. Drei Kupferbarren werden aufgenommen;
  das Magnetbudget sinkt für diese eine Aufnahme von 1.000 auf 999.
- 661 Gameplay-Assertions, 52 statische Mixin-Verträge und sechs Ressourcentests.

Die Serverläufe prüfen Weltgegenstände, Inventare, gespeicherte Belege und
ausgehende Effektpakete. Die Darstellung im grafischen Client bleibt beim
anschließenden Spieltest zu bestätigen. Der neueste Lauf und die Erhaltung
der bestehenden Dateien stehen in
[reward-drops-20261027-evidence.json](reward-drops-20261027-evidence.json).

## Update und Reproduktion

Build: `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`

SHA-256: `5df5f53d4ebe7e9a09ae28a64836648453969fd99c6365f1d56ccff005d8d3a3`

Alte JAR ersetzen und Instanz beziehungsweise Server neu starten. Die bisherigen
Ansprüche und bereits ausgegebenen Belohnungen bleiben erhalten. Ein schon
eingelöster Vault gibt deshalb durch dieses Update keinen weiteren Kern.
Für einen erneuten Vault-Auswurftest eignet sich eine frische Testwelt oder ein
Spieler ohne bisherigen Anspruch. Die Verteilung und alle freigegebenen
Innenraumexporte ändern sich nicht. Es wurde kein Nutzerprofil und keine
Nutzerwelt geändert. Der vorherige Build und die Ausgangsdateien sind unter
`build/reward-drops-20261027/before.zip` gesichert.

```powershell
$jdk = 'build/toolchains/zulu25.36.205-ca-jdk25.0.4.1-win_x64'
python tools/test_gameplay.py --java-home $jdk
python tools/build.py --skip-generation --java-home $jdk
python tools/test_gameplay_presentation_server.py --accept-eula --java-home $jdk --artifact dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar
```
