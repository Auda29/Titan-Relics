# Roadmap zur öffentlichen Beta

Vereinbart am 3. November 2026. Ausgangspunkt ist die veröffentlichte
[Alpha 5.0.5](../releases/0.1.0-alpha.5.0.5.md). Diese Roadmap beschreibt die
noch offenen Arbeiten und Freigabekriterien für die erste öffentliche Beta.
Eine Beta-Version oder ein Veröffentlichungstermin ist damit noch nicht festgelegt.

## Vorhandene Grundlage

- Die sieben Reliktfamilien, Begegnungen, Archäologie, Karten, Belohnungen,
  Kern, Magnet und Weltenbaum-Effekte sind implementiert.
- Presets, verständliche Zahlenwerte und Biomwahl werden pro neuer Welt
  gespeichert. Seit 5.0.5 folgt auch die Koloss-Mindestentfernung dem Preset.
- Fabric und NeoForge für Minecraft 1.21.1 und 26.2 werden durch die Release-CI
  gebaut und geprüft. Die vier veröffentlichten 5.0.5-JARs wurden heruntergeladen
  und anhand ihrer Prüfsummen verifiziert.
- Der bestehende 30-Seed-Verteilungsaudit, automatisierte Server-/Neustarttests
  und die vom Nutzer bestätigten Tests mit zwei echten Clients einschließlich
  erneutem Verbinden bleiben gültige Belege.
- Die vollständige Survival- und Modpack-Abnahme der öffentlichen Beta ist noch
  offen. Erfolgreiche Builds und einzelne Tests ersetzen diese Abnahme nicht.

Die sechs folgenden Arbeitspakete sind geplant. Ihre Kontrollkästchen werden
erst mit verlinktem Prüfbeleg oder ausdrücklich dokumentierter Nutzerabnahme
abgehakt. Historische Modell-Handoffs mit alten offenen Punkten begründen keine
erneute Umsetzung bereits integrierter und abgenommener Modelle.

## 1. Weltladefehler verständlich abfangen

Priorität P0. Beim testweisen Entfernen von Serene Seasons änderte sich die
gespeicherte Umgebung gegenüber dem eingefrorenen Verteilungsplan. Die
Kompatibilitätsprüfung beendete den Weltstart mit einer Exception. Vor der Beta
muss dieser erwartbare Konflikt verständlich behandelt werden.

- [x] Den Konflikt in einer isolierten Kopie reproduzieren und eingrenzen:
  In der geprüften Kombination ändern sich ausschließlich Mitglieder dreier
  Serene-Seasons-Biom-Tags. [Untersuchung vom 4. November](../testing/BETA_WORLD_LOAD_INVESTIGATION_20261104.md).
  Der abgesicherte Übergang ist im [Fix-Bericht](../testing/BETA_WORLD_LOAD_GUARD_20261104.md) dokumentiert.
- [x] Einen erklärten Ladeabbruch mit Rückkehr zum Menü ermöglichen, statt
  Minecraft wegen einer erwarteten Inkompatibilität abstürzen zu lassen.
- [x] Ursache, betroffene Welt und mögliche Wiederherstellung des ursprünglichen
  Setups verständlich anzeigen. Unbekannte Ursachen ausdrücklich als solche benennen.
- [x] Belegen, dass weder der Verteilungsplan gelöscht noch Standorte neu
  ausgewürfelt, Belohnungen erneuert oder Weltdateien still repariert werden.
- [x] Nach Wiederherstellung des unterstützten Setups dieselbe Welt erneut laden
  und gespeicherte Ziele, Fortschritt und Karten abgleichen.

Freigabe: In einem unterstützten Setup sind keine reproduzierbaren
Weltladeabstürze bekannt. Erkannte inkompatible Änderungen führen zu einer
verständlichen Meldung und lassen die gespeicherten Daten erhalten. Eine
pauschale Abschaltung der Integritätsprüfung ist keine Lösung.

Stand 4. November: Punkt 1 ist umgesetzt und abgenommen. Die endgültigen vier
Artefakte bestehen 24 gezielte Server-Ablehnungen samt Dateierhaltung und
Wiederherstellung sowie die echten Client-Ladewege. Die Living-World-Kopie
besteht zusätzlich die Saison-/Referenzfälle und den vollständigen Clientablauf.
[Umsetzungsbericht und Belege](../testing/BETA_WORLD_LOAD_GUARD_20261104.md).
Es wurde dafür kein neuer Release erstellt.

## 2. Verteilung über Presets und eigene Einstellungen steuern

Am 4. November 2026 hat der Nutzer entschieden, dass die vorhandenen Presets
und anpassbaren Werte diesen Punkt für die Beta abdecken. Zusätzliche feste
Balanceziele und eine neue Messreihe sind damit keine Freigabebedingung mehr.
Das Preset mit der höchsten Häufigkeit, „Entdeckungen“, wird zur Werksvorgabe
für neue Welten ohne bereits gespeicherte Auswahl.

Die Werte 30.000 / 15.000 / 8.000 sind Mindestentfernungen des großen Kolosses
vom ursprünglichen Weltspawn. Sie garantieren weder ein nahes Ziel noch eine
maximale Reisestrecke. Im [5.0.5-Testseed 731204](../testing/COLOSSUS_PRESET_DISTANCE_20261103.md)
lag ein gültiger Koloss trotz kleinerer Untergrenze über 100.000 Blöcke entfernt.
Auch ein Suchabstand von 3.000 bedeutet nicht ein Relikt alle 3.000 Blöcke.

- [x] Presets Expedition, Ausgewogen und Entdeckungen sowie verständliche
  individuelle Werte und Biomwahl bereitstellen.
- [x] Entdeckungen als Werksvorgabe verwenden. Bereits gespeicherte
  Installationsvorgaben und Weltpläne behalten ihre Werte.
- [x] Den Umfang nach ausdrücklicher Nutzerentscheidung als ausreichend für
  die Beta festhalten. Das ist keine neue empirische Bestätigung von Fundraten.

Freigabe: Durch die Nutzerentscheidung zum angepassten Umfang abgeschlossen.
Die [Verteilungseinstellungen](../technical/DISTRIBUTION_SETTINGS.md) beschreiben
die Presets und ihre Grenzen. Weitere Beobachtungen können aus dem Survival-Test
folgen; die bestehenden Seed-Befunde werden dadurch nicht umgedeutet.

## 3. Vollständigen Survival-Durchlauf abnehmen

Priorität P1. Die vorhandenen Einzelprüfungen zu einer zusammenhängenden
Spielerfahrung verbinden.

Der Nutzer übernimmt diesen Survival-Durchlauf selbst. Die Abnahme steht noch aus.

- [ ] Obelisk natürlich finden, Archäologie durchführen und eine Expeditionskarte erhalten.
- [ ] Kartenlesbarkeit, Orientierung und tatsächliche Reise zum großen Koloss bewerten.
- [ ] Zugänge, Begegnung, Teilnahme, Schlüsselverbrauch, Vault und physische
  Kernbelohnung in der natürlichen Struktur abschließen.
- [ ] Kern im Alltag einsetzen und aufladen; Magnet finden, reparieren und nutzen.
- [ ] Nutzen und Kosten von Beute, Kern und Magnet sowie die Baumaura einschließlich
  ihrer fünfminütigen Nachwirkung über eine längere Survival-Sitzung bewerten.
- [ ] Beobachtungen und notwendige Balanceentscheidungen protokollieren. Bereits
  vereinbarte Belohnungs- und Teilnahmeregeln nicht ohne eigene Entscheidung ändern.

Freigabe: Die Erkundungs- und Belohnungskette ist ohne manuelle Weltreparatur
spielbar. Verständlichkeit, Reiseaufwand und Belohnungsnutzen sind bewertet;
gefundene Blocker sind behoben und nachgeprüft.

## 4. Alle vier Zielversionen im echten Client abnehmen

Priorität P1. Bestehende Client- und Mehrspielerbelege gezielt ergänzen, besonders
für NeoForge. Nicht jeden bereits bestandenen Fall pauschal als ungetestet führen.

Stand 4. November 2026: Die erste Astra-High-Prüfrunde ist als
[Teilabnahme dokumentiert](../testing/BETA_CLIENT_ACCEPTANCE_20261104.md).
Auf allen vier Zielen bestehen die Neuweltanlage mit Discovery-Vorgabe,
ein vollständiger Clientprozess-Neustart und das Laden derselben Welt sowie
zwei echte Spieler über Loopback mit erneutem Gastbeitritt aus einem neuen
Prozess. Ein Turmausschnitt wurde jeweils im echten Renderer angesehen.
Die anschließende [Gameplay-Prüfung](../testing/BETA_CLIENT_GAMEPLAY_ACCEPTANCE_20261104.md)
belegt auf allen vier Zielen echtes Crafting und Schmieden mit Zutatenverbrauch,
persönliche Schlüssel und physische Core-Drops, unmittelbaren Schlüsselverbrauch,
späte Teilnahme, Wiederverbindung sowie Inventar-/Ledger-Erhalt nach Save/Reload
und vollständigem Prozessneustart. Je Ziel wurden über 20 Minuten gemeinsame
Aktionen ausgeführt. Die abschließende
[Rendererabnahme](../testing/BETA_RENDERER_ACCEPTANCE_20261104.md) ergänzt
96 tatsächlich angesehene Originalbilder, je 24 auf allen vier Zielen.
Die Modelle, Innenraumpunkte, 1.21.1-Ersatzblöcke und getragene Rüstung sind
damit geprüft. Beschädigte, leere und unvollständig geladene frühere Bilder
bleiben ausdrücklich verworfen. Punkt 4 ist für den dokumentierten lokalen
Kandidaten abgeschlossen; Survival und Modpack-/Leistungsmessungen bleiben
Punkte 3 und 5.

| Ziel | Vorhandene Belege | Abnahme in Punkt 4 |
|---|---|---|
| Fabric 1.21.1 | Clientanlage/-neustart, zwei echte Spieler, Crafting, persönliche Belohnungen, Persistenz und 24 Rendereransichten | Abgeschlossen |
| Fabric 26.2 | Clientanlage/-neustart, zwei echte Spieler, Crafting, persönliche Belohnungen, Persistenz und 24 Rendereransichten | Abgeschlossen |
| NeoForge 1.21.1 | Clientanlage/-neustart, zwei echte Spieler, Crafting, persönliche Belohnungen, Persistenz und 24 Rendereransichten | Abgeschlossen |
| NeoForge 26.2 | Clientanlage/-neustart, zwei echte Spieler, Crafting, persönliche Belohnungen, Persistenz und 24 Rendereransichten | Abgeschlossen |

- [x] Auf allen vier Zielen eine neue Welt ohne gespeicherte Vorgaben anlegen,
  die gespeicherte Discovery-Auswahl prüfen und die Welt nach vollständigem
  Clientprozess-Neustart wieder laden.
- [x] Zwei echte Spieler verbinden und den Gast nach vollständigem
  Prozessneustart mit derselben Spieleridentität erneut verbinden.
- [x] Tatsächliche Crafting-/Schmiedeergebnisse, Zutatenverbrauch und persönliche
  Reliktbelohnungen einschließlich Inventar-/Ledger-Persistenz prüfen.
- [x] Vollständige grafische Darstellung und Bedienungsansichten prüfen;
  insbesondere die ungestörte Ansicht der getragenen verzierten Rüstung ergänzen.
- [x] Versionsspezifische Block-/Modelladaptionen im Spiel ansehen, insbesondere
  die Ersatzblöcke auf 1.21.1.
- [x] Die bestätigten Zwei-Client-Tests um Teilnahme am selben Reliktereignis,
  persönliche Belohnungen, Wiederverbinden nach Belohnung, spätere Ankunft
  nach Ereignisfortschritt und längere Sitzungen ergänzen.
- [x] Automatisierte simulierte Spieler, echte Clients und Nutzerabnahmen in den
  Ergebnissen jeweils ausdrücklich unterscheiden.

Freigabe: Für jedes angebotene Spiel-/Loader-Ziel gibt es einen zugeordneten
Client-Prüfbeleg. Reproduzierbare Darstellungs- oder Mehrspielerblocker sind behoben.

Die grafischen Belege stammen aus einer Operator-Ausstellung der Templates,
nicht aus einer neuen natürlichen Survival-Generierung. Die im Gameplay-Bericht
offengelegten historischen Dienst- und Gast-Disconnect-Logbefunde bleiben
erhalten; die Rendererfortsetzung ist kein erneuter Disconnect-Test.

## 5. Kompatibilität und Leistung messen

Priorität P1. Vergleichbare Messungen mit denselben Seeds, Einstellungen und
Routen mit und ohne Relic durchführen.

Stand 4. November: Die Abnahme nach dem vorab festgelegten
[Prüfplan mit Messbudgets](../testing/BETA_COMPATIBILITY_PLAN_20261104.md)
ist unter den dokumentierten Supportbedingungen abgeschlossen. Der
[Prüfbericht](../testing/BETA_COMPATIBILITY_20261104.md) enthält 16 Serverläufe,
acht Modpack-Clientläufe und eine zusätzliche DH-Fernansicht. Originalprofile
blieben unverändert; Testwelten und Messdaten liegen auf E:.

- [x] Unterstützte Modkombinationen und Versionen festhalten, einschließlich
  TerraVista und TerraVista Living World als konkrete Prüfumgebungen.
- [x] Chunkgenerierungszeiten, Speicherbedarf, Serververzögerungen und Verhalten
  beim Laden großer Relikte erfassen. Messverfahren und Budgets vor der Abnahme festlegen.
- [x] Terrain-/Biommods, fremde Strukturen und größere Vorabgenerierung prüfen.
- [x] Distant Horizons, Voxy, Shader und Jahreszeiten getrennt untersuchen,
  damit Ursachen nicht ohne Beleg Relic zugeordnet werden.
- [x] Den beim Nutzer bestätigten Einfluss des Serene-Seasons-/DH-Adapters als
  bekannte Kompatibilitätsbeobachtung dokumentieren. Das ist keine pauschale
  Unverträglichkeit von Serene Seasons mit Relic.
- [x] Unterstützte Kombinationen, bekannte Probleme und nicht geprüfte Setups
  für Spieler unterscheidbar veröffentlichen.

Freigabe: Die unterstützten Setups laufen innerhalb der vereinbarten Budgets
ohne reproduzierbare Hänger oder Generierungsfehler. Grenzen und bekannte
Fremdmod-Probleme sind nachvollziehbar beschrieben.

Die [Spielerhinweise](../technical/MOD_COMPATIBILITY.md) unterscheiden geprüfte
Versionen und Einschränkungen. DH 3.3.3 FEATURES lässt Reliktstarts in der
Fernberechnung aus; INTERNAL_SERVER und die anschließende LOD-Darstellung
bestanden. Dafür wurde kein Produktionsfix eingebaut. Voxy World Gen V2 bleibt
in den Dedicated-Server-Referenzen ausgeschlossen, da es auch ohne Relic
clientseitiges LWJGL benötigt. Der erhöhte Speicherbedarf ist dokumentiert;
Langzeit-/FPS-Garantien und alte LOD-Cache-Reparaturen sind nicht abgenommen.

## 6. Veröffentlichung und Rückmeldungen vorbereiten

Priorität P1, Voraussetzung für die öffentliche Freigabe.

- [ ] README, Dokumentationsindex und Downloadlinks auf den Beta-Kandidaten abstimmen.
- [x] Eine kurze Spielanleitung für Reliktfunde, Archäologie, Karten, Kern,
  Magnet und Presets bereitstellen, ohne die gesamte Erkundung vorwegzunehmen.
- [x] Bekannte Einschränkungen, Bestandswelt-Verhalten, unterstützte Setups und
  Abhängigkeiten klar aufführen.
- [x] Eine Fehlermelde-Vorlage mit Mod-/Spiel-/Loader-Version, Seed und
  Koordinaten soweit relevant, Modliste, Reproduktionsschritten und passenden
  Log-/Crashberichten anlegen.
- [x] Projektlizenz MIT ausdrücklich festlegen und in Lizenzdatei/Metadaten
  übernehmen. Modpack-Nutzung, Änderungen und Weiterverteilung sind unter MIT
  mit Erhalt des Copyright-/Lizenzhinweises erlaubt. Fremde Referenzwerke
  werden nicht mitlizenziert.
- [ ] Die tatsächliche Veröffentlichung auf Modrinth/CurseForge freigeben und
  die jeweiligen Plattform-Verteilungseinstellungen prüfen.
- [ ] Eine öffentliche Projektseite mit geeigneten Screenshots, Beschreibung,
  richtigen Spiel-/Loader-Zuordnungen und Abhängigkeiten vorbereiten.
- [ ] Für den tatsächlichen Beta-Release erneut alle vier veröffentlichten JARs,
  Metadaten, Prüfsummen und Downloadverfügbarkeit verifizieren.

Bei einer Veröffentlichung auf Modrinth sind dessen
[Versions- und Abhängigkeitsangaben](https://docs.modrinth.com/api/operations/createversion/)
sowie die [Regeln zur Modpack-Nutzung](https://support.modrinth.com/en/articles/8797527-obtaining-modpack-permissions)
zu berücksichtigen. MIT ist inzwischen durch den Nutzer gewählt; diese
Lizenzentscheidung ist noch keine Freigabe zur Plattformveröffentlichung.

Stand 5. November: Das [lokale Veröffentlichungspaket](../releases/PUBLIC_BETA_PREPARATION.md)
enthält [Spielanleitung](../players/PLAYER_GUIDE.md),
[Installation/Support](../players/INSTALLATION.md),
[Fehlerformular](../../.github/ISSUE_TEMPLATE/bug_report.yml), überarbeitetes
README und Index sowie getrennte Modrinth-/CurseForge-Entwürfe mit gemeinsamer
Vier-Dateien-Matrix und einer Release-Vorlage. Die
[Namensentscheidung](NAMING.md) ist getroffen: **Titan Relics**,
*Colossal ruins of a forgotten age*. Der Nutzer hat anschließend
[Modrinth](https://modrinth.com/project/titan-relics) und die
[CurseForge-Vorschau](https://www.curseforge.com/minecraft/mc-mods/titan-relics/preview)
mit dem Slug `titan-relics` gemeldet. Anonyme Abrufe zeigen noch "Project not
found" beziehungsweise 404. Projektstatus und gespeicherte Felder sind noch
im Autorendashboard abzugleichen; eine Namenskollisionsprüfung ist damit
nicht ersetzt.
README/Index unterscheiden Alpha 5.0.5 vom unveröffentlichten Kandidaten;
die endgültige Beta-Version und ihre Downloadlinks bleiben offen. Die
Projektseiten liegen als prüfbare Entwürfe vor. MIT und die daraus folgende
Modpack-Erlaubnis sind festgelegt; finale Bilder/Icon und Plattformprüfung
fehlen noch. Der Nutzer hat das Repository
in [Auda29/Titan-Relics](https://github.com/Auda29/Titan-Relics) umbenannt und
öffentlich freigegeben. Anonyme Abfragen bestätigen die öffentliche Anleitung,
aktivierte Issues und den vorhandenen Alpha-Release. Die Einrichtung öffentlicher
Dokumentations- und Supportziele ist damit erledigt; Fehlermeldungen benötigen
ein GitHub-Konto.
Die aktuellen Modrinth-KI-Regeln sind als offene Herkunfts-/Zulässigkeitsprüfung
dokumentiert. Durch die Repository-Freigabe wurde noch keine Beta veröffentlicht.
Punkt 6 bleibt bis zur finalen Freigabe und Downloadprüfung offen.
Der [Prüfbericht des Vorbereitungspakets](../testing/PUBLIC_BETA_PREPARATION_20261105.md)
belegt den abgeschlossenen lokalen Dokumentationsumfang und seine Grenzen.

Freigabe: Ein neuer Spieler kann das richtige Paket installieren, die
grundlegenden Systeme verstehen, Einschränkungen erkennen und einen
nachvollziehbaren Fehlerbericht abgeben.

Nachtrag 6. November: Die lokale technische Vorbereitung ist umgesetzt und
[geprüft](../testing/BETA_TECHNICAL_PREPARATION_20261106.md). Alle vier Kandidaten
sind gebaut; der Upload-Workflow wartet noch auf die zusätzliche GitHub-
Berechtigung für Workflow-Dateien.
Modrinth wurde als Entwurf mit MIT, Text, Links, Kategorien und Start-Icon
konfiguriert, ohne Version oder Moderationseinreichung. Der Anzeigename in den
Mod-Metadaten lautet Titan Relics; `0.1.0-beta.1` ist als unveröffentlichter
Kandidat vorbereitet. Generierte Strukturressourcen sind aus den erhaltenen
Quellen wiederhergestellt. Uploadwerkzeug und separater manueller Workflow
sind implementiert und planen ohne Veröffentlichungsfreigabe ausschließlich.
Die [technische Dokumentation](../technical/PLATFORM_PUBLICATION.md) beschreibt
Sicherheitsprüfungen und Uploadbelege. Der Survival-Test, die tatsächliche
Release-Freigabe, Plattformzulässigkeit und der CurseForge-Dashboard-Abgleich
bleiben offen.

## Reihenfolge und Freigabe der Beta 1

1. Weltladefehler und Erkundungsbalance zuerst bearbeiten.
2. Den vollständigen Survival-Lauf und die Abnahme der Zielversionen durchführen.
3. Kompatibilität, Leistung und Veröffentlichungsvorbereitung abschließen.
4. Die oben beschriebenen Belege gemeinsam prüfen und die öffentliche Beta 1
   ausdrücklich freigeben.

Neue Reliktfamilien, große Modellumbauten, neue Dimensionen und eine Migration
der Verteilung bestehender Welten sind keine Voraussetzung für diese Beta.
Zusätzliche Inhalte bleiben eigene spätere Entscheidungen.

Weiterführend: [aktueller Stand](CURRENT_STATUS_AND_ROADMAP.md),
[Verteilungseinstellungen](../technical/DISTRIBUTION_SETTINGS.md),
[bisheriger Verteilungsaudit](../testing/DISTRIBUTION_FIX_20261027.md) und
[Gameplay-Abnahmekatalog](../testing/GAMEPLAY_ACCEPTANCE_PLAN.md).
