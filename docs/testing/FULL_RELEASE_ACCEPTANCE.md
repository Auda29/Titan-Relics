# Abnahme für den ersten stabilen Release

Stand: 11. November 2026. Ausgangspunkt ist die veröffentlichte
[Beta 4](../releases/1.0.0-beta.4.md). Dieses Dokument ist die Checkliste für
den geplanten Übergang zu `1.0.0`. Es enthält Prüfaufträge, keine vorweggenommenen
Testergebnisse. Die neue Survival-Abnahme ist noch offen.

Ein erfolgreicher Spieltest kann den Ausstieg aus der Beta ermöglichen. Dafür
müssen auch die technischen Pflichtpunkte erfüllt und verbleibende Fehler
bewertet sein. Neue Relikte, weitere Minecraft-Versionen oder zusätzliche
Spielmechaniken sind dafür nicht erforderlich.

## Kurzfassung für deinen Spieltest

1. Den Schwertschädel in einer separaten neuen Creative-Welt kurz ansehen.
2. Eine neue Survival-Welt mit Beta 4 und bewusst ausgewähltem Preset starten.
3. Normal erkunden, Archäologie betreiben, einer gefundenen Karte folgen und
   Begegnung sowie Belohnungen des großen Kolosses im Survival spielen.
4. Kern und Magnet im Alltag verwenden. Bei weiteren Funden Zugang, Loot,
   Bodenanbindung und Nutzen der Relikte beobachten.
5. Über mehrere Sitzungen spielen, die Welt regulär schließen und Minecraft
   mehrfach vollständig neu starten. Auffälligkeiten und Reiseaufwand notieren.
6. Danach Save, Logs und ausgewählte Bilder zusammen mit dem ausgefüllten
   Kurzprotokoll am Ende dieses Dokuments schicken.

Zwei bis drei Spielabende sind ein sinnvoller Planungsrahmen. Entscheidend sind
die durchlaufenen Situationen und dein Urteil, nicht eine feste Stundenzahl.
Ein besonders langer Weg oder ein fehlender Fund ist ebenfalls ein Ergebnis.
Die Welt dann nicht einfach durch einen angenehmeren Seed ersetzen.

## Vorbereitung und saubere Trennung der Tests

- [ ] Genau eine passende Beta-4-JAR und die benötigten Abhängigkeiten verwenden.
  Minecraft, Loader, Modpack und zusätzliche Mods notieren; später kann ich den
  JAR-Hash und den Seed aus den gelieferten Dateien abgleichen.
- [ ] Neue Welt mit Strukturen anlegen. Das gewünschte Preset ausdrücklich neu
  auswählen, empfohlen für diesen Test: **Entdeckungen / Discoveries**.
  Biomwahl und eigene Änderungen mit einem Bild der Einstellungen festhalten.
- [ ] Schwierigkeit und normale Hilfsmittel wie Minimap, Boot oder Pferd notieren.
  Im Hauptlauf keine Locate-/Teleport-Befehle, externen Seedkarten, gegebenen
  Gegenstände oder Wechsel in Creative zum Beschaffen von Fortschritt verwenden.
- [ ] Das Modpack während dieses Laufs gleich lassen. Für Experimente mit anderen
  Mods, Generatoren oder Versionen eine Sicherung bzw. getrennte Welt verwenden.
- [ ] Falls Distant Horizons aktiv ist, Modus und Version notieren. Für die
  dokumentierte Referenz DH 3.3.3 den geprüften Modus `INTERNAL_SERVER` verwenden;
  `FEATURES` kann Relikte auslassen. Siehe [Supportgrenzen](../technical/MOD_COMPATIBILITY.md).

Der kurze Creative-Check und spätere Diagnosebesuche gehören in getrennte Welten
oder Kopien. Sie werden als solche markiert. Normales Bauen, Abbauen und Sterben
im Survival sind erlaubt. Eigene Änderungen an Relikten bitte erwähnen, damit
sie später nicht als Generierungsfehler gewertet werden.

## A. Deine Abnahme im Spiel

Alle Kästchen bleiben bis zum tatsächlichen Test offen. Zu einem erledigten Punkt
reichen eine kurze Notiz und bei Auffälligkeiten ein Bild bzw. die Stelle im Save.

### A1. Schwertschädel und natürliche Platzierung

- [ ] **Separater Creative-Check:** In einer neuen Beta-4-Welt den Schwertschädel
  an der Unterseite und am Übergang zum Boden ansehen. Keine schwebenden kurzen
  Kontaktstellen, abgeschnittenen Modellteile oder neu gewachsenen Erdsäulen.
  Vor der Aufnahme dort keine Blöcke entfernen. Seed, Koordinaten und Blick auf
  die betreffende Stelle sichern. Dieser Check belegt keine Fundhäufigkeit.
- [ ] Im Survival bei natürlichen Funden prüfen: Das Relikt wirkt vollständig,
  Zugänge und wichtige Bereiche sind erreichbar, Truhendeckel lassen sich öffnen.
  Absichtliche Ruinenlücken, Baumhöhlen und einzelne dekorative Freiräume sind
  kein Fehler. Im Zweifel mit Bild melden, statt das Modell zu reparieren.
- [ ] Überschneidungen mit Dörfern oder anderen Bauwerken festhalten. Einzelne
  Überschneidungen sind mit der gewünschten 50-%-Regel weiterhin zulässig.
  Versperrte zentrale Zugänge, zerstörte Belohnungen oder regelmäßig unbrauchbare
  Kombinationen müssen wir untersuchen. Ein einzelner Seed misst keine Quote.

### A2. Entdeckung und Reiseaufwand

- [ ] Mindestens einen Einstieg in die Reliktsuche durch normales Erkunden finden.
  Der Weg zur Archäologie und mindestens eine Kartenreise zum großen Koloss
  werden ohne Locate/Teleport gespielt. Eine zufällige frühe Koloss-Sichtung
  dokumentieren und die Kartenfunktion trotzdem separat nachvollziehen.
- [ ] Für wichtige Funde grob notieren: Spielzeit seit Start, Fundkoordinaten,
  Reisezeit, Verkehrsmittel und ob die Entdeckung zufällig oder mit Karte erfolgte.
  Auch längere Abschnitte ohne Fund notieren. Ich kann die Verteilung später im
  Save untersuchen; du musst nicht laufend Entfernungen ausrechnen.
- [ ] Beurteilen: Bieten Sichtungen unterwegs genug Abwechslung? Sind Schädel
  präsent, ohne ständig zu wiederholen? Sind große Relikte besonders, aber ihre
  Reise und Suche mit dem gewählten Preset noch lohnend?

Bestanden heißt hier: Du kannst den Einstieg und Fortschritt ohne Befehle
erreichen und empfindest den Erkundungsaufwand als vertretbar. Wiederholte
frustrierende Suchabende, bei denen du nur mit Locate weiterkommen würdest,
sind ein offener Abnahmebefund. Es gibt keine Garantie für einen Fund alle
2.000 Blöcke oder einen Koloss innerhalb einer maximalen Reisestrecke.

Du musst nicht alle sieben Reliktfamilien in dieser Survival-Welt finden.
Seltene, nicht gefundene Inhalte können wir anschließend in einer Kopie gezielt
prüfen. Solche Zusatzbesuche ersetzen die natürliche Entdeckungsreise nicht.

### A3. Archäologie, Karte und Koloss

- [ ] Die Fundstellen am Obelisken sind erkennbar und mit dem Pinsel benutzbar.
  Die notwendigen Werkzeuge und Vorräte lassen sich im normalen Spiel beschaffen.
  Die [Spieleranleitung](../players/PLAYER_GUIDE.md) darf als Hilfe dienen.
- [ ] Die gefundene Karte lässt sich verstehen und führt zum tatsächlichen großen
  Koloss. Eine lange Reise, unklarer Kartenstatus oder ein falsches Ziel werden
  jeweils getrennt dokumentiert. Mehrere Karten zum selben einzigartigen Koloss
  sind erwartetes Verhalten.

Wenn die Suche nachweislich kein gültiges Kolossziel findet, ist die vorgesehene
Smaragd-Kompensation zu prüfen. Diesen Fall halten wir als eigenen Befund fest.
Eine weitere Welt für die noch fehlende Begegnungsprüfung wählen wir erst nach
der Auswertung; der ursprüngliche Suchverlauf bleibt dokumentiert.

- [ ] Begegnung und Vault im Survival abschließen: Auslösung und Fortschritt sind
  nachvollziehbar, der Kampf funktioniert, der passende Schlüssel wird korrekt
  verwendet und die versprochene Belohnung lässt sich einsammeln.
- [ ] Nach Rückkehr und Neustart bleiben Ziel und abgeschlossener Fortschritt
  erhalten. Eine bereits beanspruchte persönliche Belohnung wird nicht erneut
  vergeben. Gewöhnliche Truhen und Archäologie bleiben gemeinsame endliche Funde.
- [ ] Beurteilen: Passen Kampfaufwand, Reise und Belohnung zusammen? Ausrüstung,
  Tode, Vorbereitung und genutzte Bau-/Kampftaktik kurz notieren.

### A4. Nutzen der Belohnungen und weiterer Relikte

- [ ] Den Maschinenkern in normalen Schmelz-/Kochaufgaben verwenden. Ladung ist
  verständlich, Leerlauf verbraucht sie nicht und der Kern bleibt bei Erschöpfung
  erhalten. Einmal regulär entleeren und nach Anleitung aufladen. Wenn das im
  Hauptlauf nicht erreicht wird, bleibt die praktische Aufladebewertung offen;
  die technische Funktion hat bereits gesonderte Testbelege.
- [ ] Den Bergungsmagneten beim Bauen, Abbauen oder Aufräumen benutzen. Aufnahme,
  Verschleiß und inaktive Aufbewahrung sind verständlich. Einen verschlissenen
  Magneten einmal mit normalen Materialien reparieren. Er muss dafür nicht
  vollständig kaputt sein. Nutzen und Materialkosten beurteilen.
- [ ] **Bei Turmfund oder im ergänzenden Survival-Check:** Der Aufstieg ist mit
  gewöhnlichem Bauen/Klettern möglich. Die obere Nische ist zugänglich; die Truhe
  enthält Federfall IV, 3 bis 6 Diamanten und 8 bis 16 Eisenbarren. Die untere
  Truhe funktioniert unabhängig davon. Belohnung und Aufstieg lohnen sich.
- [ ] **Bei Weltenbaumfund oder im ergänzenden Check:** Die Umgebung bietet einen
  nützlichen Ruhepunkt. Effekte, Beleuchtung und Tieraufkommen passen ins Spiel,
  ohne einen verpflichtenden Daueraufenthalt oder unbegrenzten Nachschub zu erzeugen.
- [ ] **Bei weiteren Funden:** Kleiner Koloss, Schädel und Monolith-Verzierung
  sind sinnvoll eingebunden. Ein kleiner Koloss ohne Magnet ist allein kein
  Fehler; dort ist ein Magnet nicht garantiert.

Für seltene Inhalte ist ein Zusatzcheck in einer markierten Weltkopie zulässig.
Zum Ziel darf dort teleportiert werden; Aufstieg, Kampf oder Gegenstandsnutzung
werden anschließend im Survival geprüft. Transport und Gegenstände aus diesem
Zusatzcheck zählen nicht zur natürlichen Reisemessung oder Ressourcenwirtschaft.

### A5. Alltag, Menü und Speichern

- [ ] Ein normaler Spieler kann Preset und Zusammenfassung verstehen. Advanced
  öffnen/schließen sowie Anwenden/Abbrechen ausprobieren. Abgebrochene Änderungen
  werden nicht übernommen. Die Darstellung darf keine exakte Seed-Vorschau vortäuschen.
- [ ] Mehrere Sitzungen absolvieren, darunter möglichst eine mindestens zweistündige
  Sitzung. Mindestens zweimal Minecraft vollständig schließen und dieselbe Welt
  wieder öffnen. Das ist eine Mindestprobe, kein allgemeiner Langzeitnachweis.
- [ ] Nach erneutem Laden stimmen eigene Bauten, Gegenstände, Ladungen, Karten,
  erledigte Begegnungen und bereits geleerte Truhen. Einen besuchten Reliktbereich
  zwischenzeitlich verlassen und später wieder aufsuchen.
- [ ] Normales Erkunden, Kampf und Speichern bleiben spielbar. Wiederkehrende
  Stillstände, anhaltende Verschlechterung oder auffällige Speicherprobleme mit
  Uhrzeit und Tätigkeit notieren. Einzelne neue Chunk-Ruckler sind nicht schon
  ein Modfehler; ich prüfe die Ursache anhand der Logs und bei Bedarf im Vergleich.

## B. Technische Pflichtpunkte vor der stabilen Veröffentlichung

Diese Prüfungen übernehme ich separat. Du musst den Survival-Lauf nicht auf acht
Installationen wiederholen. Vorhandene Belege werden nach Quellstand und Umfang
zugeordnet; unveränderte Funktionen müssen nicht vollständig neu abgenommen werden.

| Pflichtpunkt | Bestehensbedingung und vorhandene Grundlage |
|---|---|
| Aktueller Kandidat | Tatsächlich getestete JAR, Quellrevision, Einstellungen und Modliste sind festgehalten. Nach Fixes werden betroffene Fälle erneut geprüft; wir behaupten keine Prüfung eines später geänderten Builds. |
| Acht unterstützte Ziele | Fabric und NeoForge auf 1.21.1, 1.21.11, 26.2 und 26.3 bestehen die Release-CI. Beta 4 hat diese Matrix bereits bestanden. Für den stabilen Tag wird dessen eigener Build geprüft. |
| Aktuelle Client-Oberflächen | Start, Weltmenü, Welt laden/speichern/neu öffnen und sichtbare Ressourcen auf den acht Zielen kurz prüfen. Neue Menüansichten zusätzlich in DE/EN und repräsentativen GUI-Skalierungen abnehmen. Die älteren vier Renderer-Abnahmen belegen ihre damaligen Modelle, nicht automatisch neue Menüs oder zusätzliche Versionen. |
| Natürliche Generierung | Pläne und echte Starts stimmen überein; repräsentative Grundflächen sind vollständig. Schwertschädel-Korrektur und Gebäudefilter haben native Belege. Neue reproduzierbare Platzierungsfehler werden eingegrenzt und bei wesentlichen Auswirkungen behoben. |
| Spielstände und endliche Belohnungen | Alte veröffentlichte Weltrevisionen bleiben lesbar und erhalten ihre Regeln. Neustarts erzeugen keine duplizierten Belohnungen oder nachgefüllten Truhen. Kein unangekündigtes Retrogen. Beta-4-Bestandstest und vorhandene Reward-/Reload-Belege zuordnen. |
| Mehrspieler | Vorhandene Zwei-Client-Belege und automatisierte Reward-Tests zuordnen. Bei Änderungen an Teilnahme, persönlichen Ansprüchen oder gemeinsamer Beute gezielt mit Host/Gast einschließlich erneutem Verbinden nachprüfen. Ein Solo-Survival-Lauf ersetzt diesen Nachweis nicht. |
| Kompatibilität und Leistung | Referenzsetup und konkret getestete Living-World-Konfiguration benennen. Auffällige Dauerlast reproduzieren und dem Mod bzw. anderen Ursachen zuordnen. DH-Modi und weitere Einschränkungen dokumentieren; historische Messungen nicht als aktuelle universelle Freigabe ausgeben. |
| Veröffentlichung | Acht fertige JARs, Prüfsummen, Versions-/Loader-Metadaten, MIT, Credits und Release-Hinweise prüfen. GitHub und Plattformdateien nach Veröffentlichung herunterladen und verifizieren. Beta 4 hat dafür bereits einen vollständigen [Beleg](../releases/BETA_4_PUBLICATION.md). |

Der stabile Release muss nicht jede beliebige Modkombination unterstützen.
Dokumentierte Grenzen wie fehlendes Retrogen oder ein ausgeschlossener DH-Modus
dürfen bestehen bleiben. Eine reproduzierbare Störung im ausdrücklich unterstützten
Setup wird dadurch nicht zu einer akzeptierten Einschränkung.

## C. Fehlerbewertung und Entscheidung über 1.0.0

| Einstufung | Beispiele | Folge |
|---|---|---|
| Blocker | Beschädigter/unladbarer Save im unterstützten Setup, reproduzierbarer Absturz oder Hänger, durch Modfehler verlorener Fortschritt oder zugesagte Belohnung, Duplizierung endlicher Beute, unspielbare zentrale Zugänge | Vor 1.0.0 beheben und gezielt erneut testen. |
| Wesentlicher Abnahmebefund | Natürlicher Fortschritt bleibt praktisch aus, Kartenreise oder Kampf dauerhaft unverhältnismäßig, Kern/Magnet im Alltag unbrauchbar, häufige schwere Platzierungsfehler, neues Menü verhindert korrekte Einstellungen | Ursache klären, korrigieren oder den zugesagten Umfang ausdrücklich neu festlegen. Nicht stillschweigend als bestanden markieren. |
| Kleine Auffälligkeit | Kosmetischer Geländekontakt, kleine Text-/Darstellungsprobleme ohne Funktionsverlust | Als konkreten offenen Punkt dokumentieren; darf mit bewusster Abnahme später folgen. |

Ein Tod, eine schwierige Reise, eine erlaubte Gebäudeüberschneidung oder ein
seltener einzelner Fund ist für sich genommen kein Blocker. Entscheidend sind
Auswirkung, Reproduzierbarkeit und der vereinbarte Spiel-/Supportumfang.

Für die Freigabe müssen diese Punkte erfüllt sein:

- [ ] Die natürliche Survival-Kette und der Alltagsnutzen aus A sind bewertet.
  Nicht erreichte bzw. nur ergänzend geprüfte Inhalte sind ausdrücklich vermerkt.
- [ ] Die technischen Pflichtpunkte aus B sind mit passenden Belegen abgedeckt.
- [ ] Keine offenen Blocker oder ungeklärten wesentlichen Abnahmebefunde.
- [ ] Kleine Restpunkte und Supportgrenzen sind in den Release-Hinweisen genannt.
- [ ] Du bestätigst nach unserer Auswertung, dass Spielgefühl und Umfang für
  `1.0.0` passen, und beauftragst die stabile Veröffentlichung ausdrücklich.

Wir müssen nach einer kleinen Korrektur nicht den ganzen Survival-Lauf wiederholen.
Der betroffene Ablauf und relevante Regressionen werden erneut geprüft.
Änderungen an Verteilung oder grundlegender Belohnungswirtschaft brauchen dagegen
erneut passende Spielpraxis, bevor wir ihre Balance als abgenommen bezeichnen.

Die Modrinth-Projektmoderation ist ein gesonderter Plattformstatus. Beim
Beta-4-Veröffentlichungscheck war sie noch offen. Ein stabiler GitHub-/CurseForge-
Release kann technisch abgenommen sein, während diese Freigabe aussteht. Eine
Veröffentlichung als auf allen drei Plattformen freigegeben setzt auch deren
tatsächliche Freigabe voraus. Status und KI-Angaben werden dafür nicht umgangen.
Dieses Dokument legt keinen neuen Tag an und startet keine Veröffentlichung.

## D. Kurzprotokoll zum Ausfüllen

```text
Testversion / JAR-Dateiname:
Minecraft / Loader:
Modpack und eigene Zusatzmods:
Shader / DH / Voxy und verwendeter Modus:
Neue Welt / Preset / Biomwahl / eigene Änderungen:
Schwierigkeit / normale Karten- und Reisehilfen:
Gesamtspielzeit / Anzahl Sitzungen / vollständige Neustarts:

Schwertschädel-Check in separater Creative-Welt:
Natürlicher erster Reliktfund, ungefähre Zeit und Ort:
Obelisk / Archäologie / Kartenfund:
Kartenreise, Zeit, Verkehrsmittel und Ziel:
Koloss / Kampf / Vault / eingesammelte Belohnung:
Kern im Alltag / Entleerung und Aufladen:
Magnet im Alltag / Verschleiß und Reparatur:
Weitere natürliche Funde / längere Abschnitte ohne Funde:
Turm / Weltenbaum / andere ergänzende Checks:
Menüverständlichkeit / Speichern und Wiederöffnen / Leistung:

Was war zu selten, zu häufig, zu leicht oder zu mühsam?
Welche Belohnung war nützlich, welche hat sich nicht gelohnt?
Bewusste Änderungen an Relikten und abweichende Diagnose-/Cheatbesuche:
Fehler je mit Uhrzeit, Ort, Erwartung, tatsächlichem Verhalten und Bild:
Nicht getestete Punkte:
Mein Urteil: bereit für 1.0.0 / erst nach genannten Korrekturen / weitere Beta nötig
```

Für die Auswertung reichen die betreffende Welt aus `saves`, die Sitzungslogs
aus `logs`, Konfiguration und eine Modliste sowie ausgewählte Screenshots.
Bei einem Absturz auch den passenden `crash-reports`-Eintrag beilegen.
Minecraft vorher regulär beenden und erst dann den Save kopieren. Der gesamte
Launcher- oder Kontoordner ist nicht nötig. Große Dateien können wieder über
LocalSend kommen. Roharchive bleiben privat; im Repository landen nur die
zusammengefassten Befunde und zur Veröffentlichung bestimmte Bilder.

## Zugehörige Belege

- [Beta 4 und bekannte Grenzen](../releases/1.0.0-beta.4.md)
- [Veröffentlichung und verifizierte Downloads](../releases/BETA_4_PUBLICATION.md)
- [Letzter Creative-Spieltest](USER_PLAYTEST_20261111_AFTERNOON.md)
- [Schwertschädel-Korrektur](SWORD_SKULL_CONTACT_FIX_20261111.md)
- [Turmtruhe und Abnahme](../project/TOWER_UPPER_CHEST_20261111.md)
- [Bisherige Client-/Mehrspieler-Abnahme](BETA_CLIENT_GAMEPLAY_ACCEPTANCE_20261104.md)
- [Bisherige Renderer-Abnahme](BETA_RENDERER_ACCEPTANCE_20261104.md)
- [Historischer Szenariokatalog](GAMEPLAY_ACCEPTANCE_PLAN.md)

Historische Abstände, Zielmatrizen und offene Statusangaben werden anhand der
jeweiligen Revision gelesen. Sie ersetzen nicht die aktuellen Presets und
erzeugen keine zusätzlichen alten Freigabeanforderungen.
