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

## 2. Verteilung nach tatsächlicher Spielerfahrung abstimmen

Priorität P0. Zuerst festlegen, welche Erkundungserfahrung die drei Presets bieten
sollen, dann anhand tatsächlicher Funde prüfen und bei Bedarf abstimmen.

Die Werte 30.000 / 15.000 / 8.000 sind Mindestentfernungen des großen Kolosses
vom ursprünglichen Weltspawn. Sie garantieren weder ein nahes Ziel noch eine
maximale Reisestrecke. Im [5.0.5-Testseed 731204](../testing/COLOSSUS_PRESET_DISTANCE_20261103.md)
lag ein gültiger Koloss trotz kleinerer Untergrenze über 100.000 Blöcke entfernt.
Auch ein Suchabstand von 3.000 bedeutet nicht ein Relikt alle 3.000 Blöcke.

- [ ] Für Expedition, Ausgewogen und Entdeckungen verständliche Ziele für erste
  Funde, Reisedauer und Seltenheit vereinbaren. Erst danach Zahlen als Freigabegrenze setzen.
- [ ] Die neuen Presets über mehrere feste Seeds mit Vanilla-Terrain und den
  tatsächlich unterstützten Terrain-Modpacks prüfen. Den vorhandenen Audit ergänzen.
- [ ] Suchversuche, Biom-/Gelände-/Abstandsablehnungen, tatsächliche natürliche
  Funde und Reisestrecken getrennt erfassen. Leere oder unbesuchte Gebiete nicht
  als fehlgeschlagene Generierung ausgeben.
- [ ] Fundraten kleiner Relikte und die erreichbaren Karten-/Kolossziele prüfen.
  Besonders Entdeckungen muss sich im Survival von Expedition unterscheiden.
- [ ] Nach Änderungen Eindeutigkeit des Kolosses, Mindestabstände, gemeinsame
  Kartenziele und Erhalt bestehender Welten erneut prüfen.

Freigabe: Die gewählten Ziele sind mit dokumentierten Seed-Ergebnissen und
Survival-Beobachtungen belegt. Seltene Funde dürfen Teil des Designs sein;
unerwartet lange ereignislose Strecken müssen erklärbar sein. Die konkreten
Balancegrenzen sind noch zu entscheiden.

## 3. Vollständigen Survival-Durchlauf abnehmen

Priorität P1. Die vorhandenen Einzelprüfungen zu einer zusammenhängenden
Spielerfahrung verbinden.

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

| Ziel | Vorhandener 5.0.5-Beleg | Noch für den Beta-Kandidaten abzunehmen |
|---|---|---|
| Fabric 1.21.1 | Build/Assets, echtes Menü und tatsächliche Welterstellung mit gespeichertem Zahlenwert | Vollständiger Survival- und Client-Abgleich mit Speichern/Laden |
| Fabric 26.2 | Build/Assets, native Generierung, Karten, Locate und Server-Neustart | Vollständiger Survival- und grafischer Client-Abgleich |
| NeoForge 1.21.1 | Build und Assetprüfung | Grafischer Clienttest und vollständiger Survival-Abgleich |
| NeoForge 26.2 | Build und Assetprüfung | Grafischer Clienttest und vollständiger Survival-Abgleich |

- [ ] Auf allen vier Zielen Darstellung, Bedienelemente, Rezepte, Belohnungen,
  Speichern, erneutes Laden und vollständigen Spielneustart prüfen.
- [ ] Versionsspezifische Block-/Modelladaptionen im Spiel ansehen, insbesondere
  die Ersatzblöcke auf 1.21.1.
- [ ] Die bestätigten Zwei-Client-Tests um die relevanten neuen Beta-Fälle und
  Zielversionen ergänzen: Teilnahme, persönliche Belohnungen, Wiederverbinden,
  spätere Ankunft und längere Sitzungen.
- [ ] Automatisierte simulierte Spieler, echte Clients und Nutzerabnahmen in den
  Ergebnissen jeweils ausdrücklich unterscheiden.

Freigabe: Für jedes angebotene Spiel-/Loader-Ziel gibt es einen zugeordneten
Client-Prüfbeleg. Reproduzierbare Darstellungs- oder Mehrspielerblocker sind behoben.

## 5. Kompatibilität und Leistung messen

Priorität P1. Vergleichbare Messungen mit denselben Seeds, Einstellungen und
Routen mit und ohne Relic durchführen.

- [ ] Unterstützte Modkombinationen und Versionen festhalten, einschließlich
  TerraVista und TerraVista Living World als konkrete Prüfumgebungen.
- [ ] Chunkgenerierungszeiten, Speicherbedarf, Serververzögerungen und Verhalten
  beim Laden großer Relikte erfassen. Messverfahren und Budgets vor der Abnahme festlegen.
- [ ] Terrain-/Biommods, fremde Strukturen und größere Vorabgenerierung prüfen.
- [ ] Distant Horizons, Voxy, Shader und Jahreszeiten getrennt untersuchen,
  damit Ursachen nicht ohne Beleg Relic zugeordnet werden.
- [ ] Den beim Nutzer bestätigten Einfluss des Serene-Seasons-/DH-Adapters als
  bekannte Kompatibilitätsbeobachtung dokumentieren. Das ist keine pauschale
  Unverträglichkeit von Serene Seasons mit Relic.
- [ ] Unterstützte Kombinationen, bekannte Probleme und nicht geprüfte Setups
  für Spieler unterscheidbar veröffentlichen.

Freigabe: Die unterstützten Setups laufen innerhalb der vereinbarten Budgets
ohne reproduzierbare Hänger oder Generierungsfehler. Grenzen und bekannte
Fremdmod-Probleme sind nachvollziehbar beschrieben.

## 6. Veröffentlichung und Rückmeldungen vorbereiten

Priorität P1, Voraussetzung für die öffentliche Freigabe.

- [ ] README, Dokumentationsindex und Downloadlinks auf den Beta-Kandidaten abstimmen.
- [ ] Eine kurze Spielanleitung für Reliktfunde, Archäologie, Karten, Kern,
  Magnet und Presets bereitstellen, ohne die gesamte Erkundung vorwegzunehmen.
- [ ] Bekannte Einschränkungen, Bestandswelt-Verhalten, unterstützte Setups und
  Abhängigkeiten klar aufführen.
- [ ] Eine Fehlermelde-Vorlage mit Mod-/Spiel-/Loader-Version, Seed und
  Koordinaten soweit relevant, Modliste, Reproduktionsschritten und passenden
  Log-/Crashberichten anlegen.
- [ ] Veröffentlichungsplattform und Lizenz-/Modpack-Freigabe ausdrücklich
  festlegen. Die Metadaten verwenden derzeit `All-Rights-Reserved`.
- [ ] Eine öffentliche Projektseite mit geeigneten Screenshots, Beschreibung,
  richtigen Spiel-/Loader-Zuordnungen und Abhängigkeiten vorbereiten.
- [ ] Für den tatsächlichen Beta-Release erneut alle vier veröffentlichten JARs,
  Metadaten, Prüfsummen und Downloadverfügbarkeit verifizieren.

Bei einer Veröffentlichung auf Modrinth sind dessen
[Versions- und Abhängigkeitsangaben](https://docs.modrinth.com/api/operations/createversion/)
sowie die [Regeln zur Modpack-Nutzung](https://support.modrinth.com/en/articles/8797527-obtaining-modpack-permissions)
zu berücksichtigen. Die Wahl einer Lizenz oder Plattform ist noch keine
durch diese Roadmap getroffene Entscheidung.

Freigabe: Ein neuer Spieler kann das richtige Paket installieren, die
grundlegenden Systeme verstehen, Einschränkungen erkennen und einen
nachvollziehbaren Fehlerbericht abgeben.

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
