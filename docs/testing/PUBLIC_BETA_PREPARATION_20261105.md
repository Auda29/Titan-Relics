# Prüfung des Beta-Vorbereitungspakets

5. November 2026. Dokumentations- und Veröffentlichungsentwürfe; kein neuer
Produktbuild und keine neue Gameplay-Abnahme.

## Abgleich mit dem Arbeitsauftrag

| Anforderung | Vorliegendes Ergebnis |
|---|---|
| README und Index aktualisieren | [README](../../README.md) und [Index](../README.md) trennen veröffentlichtes Alpha 5.0.5 vom lokalen Kandidaten; alte README-Inhalte sind als [historische Momentaufnahme](../project/README_HISTORY_20261105.md) erhalten |
| Kurze spoilerarme Anleitung | [Spieleranleitung](../players/PLAYER_GUIDE.md) erklärt Presets, Archäologie, Karten, Kern, Magnet und Baumaura ohne Truhenkoordinaten oder vollständige Beutetabellen |
| Versionen, Abhängigkeiten, Grenzen | [Installation/Support](../players/INSTALLATION.md) enthält vier Zielkombinationen, gepinnte Abhängigkeiten, Bestandswelten, DH-/Voxy-Grenzen und Verweise auf die vorhandene Kompatibilitätsabnahme |
| Fehlerberichte | [GitHub-Formular](../../.github/ISSUE_TEMPLATE/bug_report.yml) fordert Versionen, Reproduktion und Logs; optionale Welt-/Leistungsfelder und Hinweise auf private Daten sind enthalten |
| Release-/Downloadvorbereitung | [Paket](../releases/PUBLIC_BETA_PREPARATION.md) mit vier Dateizuordnungen, Freigabe-/Downloadprüfung und [Release-Vorlage](../releases/BETA_RELEASE_TEMPLATE.md); keine erfundenen Beta-Downloads |
| Modrinth und CurseForge | Getrennte [Modrinth](../releases/MODRINTH_DRAFT.md)- und [CurseForge](../releases/CURSEFORGE_DRAFT.md)-Entwürfe mit Beschreibung, Metadaten, Release-Typ, Abhängigkeiten und offenen Entscheidungen |
| Namen | [Drei Vorschläge](../project/NAMING.md), wörtliche Suchabfragen, gefundene Kollisionen und ausdrücklich begrenzte Aussagekraft negativer Suchbefunde |
| Survival und Nutzerentscheidungen offenhalten | Roadmap-Punkt 3 bleibt offen; keine Festlegung von Name, Lizenz, Modpack-Freigabe oder öffentlicher Veröffentlichung |

## Durchgeführte Prüfungen

- 319 lokale Markdown-Datei-/Verzeichnisziele in neuen oder geänderten
  Dokumenten geprüft, einschließlich archiviertem README: keines fehlt.
- Fragmentziele in neuen Spieler-/Plattformdokumenten und README mit den
  Zielüberschriften abgeglichen: keine fehlenden Anker.
- YAML mit PyYAML 6.0.1 geparst. Eindeutige Feld-IDs, Zeichenketten in Dropdowns
  und die erforderlichen Versions-/Umgebungs-/Reproduktions-/Ergebnis-/Logfelder
  geprüft. Das ist eine lokale Strukturprüfung, kein auf GitHub eingereichter Test.
- `git diff --check` besteht. Änderungen betreffen Dokumentation und das neue
  Issue-Formular; keine Produktionsquellen, Assets oder Workflows geändert.
- Rezepte und Nutzungsregeln gegen `MaintenanceRecipe`, `CoreFurnaceMixin`,
  `SalvageMagnet`, `RelicItems`, `RelicGameplay` und die vorhandenen
  Verteilungs-/Gameplay-Unterlagen abgeglichen. Kein erneuter Lauf der bereits
  dokumentierten Gameplay-Tests, da sich das Spielverhalten nicht ändert.
- Vier Original-Rendererbilder erneut angesehen. Auswahl und Einschränkungen
  stehen im Veröffentlichungspaket. Die Testausschnitte werden nicht als
  natürlich generierte Survival-Szenen ausgegeben.
- Offizielle Modrinth-Regeln und CurseForge-Einreichungs-/Moderationshinweise
  gelesen und in den Entwürfen verlinkt. Die offene Modrinth-Herkunftsprüfung
  wird nicht durch eine behauptete Plattformfreigabe ersetzt.
- GitHub read-only über `gh api` abgefragt: Repository privat; Alpha-5.0.5-Release
  kein Draft, als Prerelease markiert, alle vier erwarteten JAR-Namen und
  `SHA256SUMS.txt` vorhanden. Anonymer API-Zugriff liefert HTTP 404. Die Abfrage
  bestätigt Metadaten/Existenz, keine erneute heruntergeladene Byteprüfung.

## Bewusst noch keine Freigabe

Das lokale Vorbereitungspaket ist fertig zur Durchsicht. Für die tatsächliche
Veröffentlichung fehlen Nutzerentscheidungen, Survival-Abnahme, öffentliche
Support-/Dokumentationsziele, geklärte Plattformzulässigkeit, finales Icon und
natürliche Titelaufnahmen sowie die Prüfung der final veröffentlichten Dateien.
Die Roadmap führt diese Punkte weiter offen. Keine Commits, Pushes, Tags,
externen Projektanlagen, Uploads, Kontakte oder Sichtbarkeitsänderungen.
