# Vorbereitung der öffentlichen Beta

Stand 5. November 2026. Dieses Paket ist ein lokaler Entwurf zur Durchsicht,
keine Veröffentlichung oder Plattformfreigabe. Veröffentlichte Grundlage ist
Alpha 5.0.5; der geprüfte Beta-Kandidat ist noch unveröffentlicht. Der Nutzer
hat **Titan Relics** mit dem Untertitel *Colossal ruins of a forgotten age*
gewählt. Die Beta-Versionsnummer ist noch nicht beschlossen.

Die authentifizierte GitHub-Abfrage am 5. November bestätigt Alpha 5.0.5 als
Nicht-Draft-Prerelease mit vier passenden JARs und `SHA256SUMS.txt`. Sie bestätigt
auch `private: true` für das Repository. Eine anonyme Release-Abfrage liefert
HTTP 404. Bestehende GitHub-Links sind daher nur für Berechtigte nutzbar, keine
öffentlichen Download-, Dokumentations- oder Supportziele. Vor dem Start ist zu
entscheiden, ob das Repository öffentlich werden soll oder Dokumentation und
Fehlermeldungen an getrennte öffentliche Ziele gehen. Dieses Paket ändert keine
Sichtbarkeit. Die Seitenentwürfe verwenden die bisherigen Links nur zur späteren
Ersetzung beziehungsweise Prüfung.

## Vorbereitete Unterlagen

- [README](../../README.md), [Installation und Support](../players/INSTALLATION.md),
  [kurze Spieleranleitung](../players/PLAYER_GUIDE.md) und
  [GitHub-Fehlerformular](../../.github/ISSUE_TEMPLATE/bug_report.yml).
- [Modrinth-Projektseite und Einstellungen](MODRINTH_DRAFT.md).
- [CurseForge-Projektseite und Einstellungen](CURSEFORGE_DRAFT.md).
- [Release-Notizen als Vorlage](BETA_RELEASE_TEMPLATE.md).
- [Namensvorschläge und Kollisionsprüfung](../project/NAMING.md).
- [Prüfung des gesamten Vorbereitungspakets](../testing/PUBLIC_BETA_PREPARATION_20261105.md).

Die öffentlichen Texte sind Englisch, entsprechend dem bisherigen README und
den Plattformvorgaben. Der Dokumentationsindex verlinkt die Spielerunterlagen.
Das frühere README bleibt als [historische Momentaufnahme](../project/README_HISTORY_20261105.md)
erhalten. Alte Profile-READMEs sind weiter historische Build-Dokumentation;
die neue Installationstabelle ist der Einstieg für Spieler.

## Gemeinsame Dateizuordnung

`VERSION` ist in dieser Tabelle ein Platzhalter für die später ausdrücklich
gewählte Version, kein vorhandener Download. Jede Zeile ist eine eigene
Plattform-Datei beziehungsweise Modrinth-Version mit genau einem Spiel-/Loaderziel.

| Dateiname | Minecraft | Loader | Java | Pflichtabhängigkeiten |
|---|---|---|---|---|
| `relics-VERSION+mc1.21.1.jar` | 1.21.1 | Fabric | 21 | Fabric API 0.116.17+1.21.1; Lithostitched 1.8.0 Fabric 21.1 |
| `relics-VERSION+mc26.2.jar` | 26.2 | Fabric | 25 | Fabric API 0.161.0+26.2; Lithostitched 1.8.0 Fabric 26.2 |
| `relics-VERSION+mc1.21.1-neoforge.jar` | 1.21.1 | NeoForge | 21 | Lithostitched 1.8.0 NeoForge 21.1 |
| `relics-VERSION+mc26.2-neoforge.jar` | 26.2 | NeoForge | 25 | Lithostitched 1.8.0 NeoForge 26.2 |

Die Loader-Baselines stehen in der [Installationstabelle](../players/INSTALLATION.md).
Auf beiden Seiten Client und Server angeben. Mod Menu nur als optional für
Fabric behandeln. DH, Voxy, Shader, Seasons und Terrainmods sind keine
Pflichtabhängigkeiten. Kein Fabric-API-Eintrag auf NeoForge-Dateien.
Keine Quilt-/Forge- oder zusätzlichen Spielversions-Tags aus Ähnlichkeit ableiten.

## Bilder und Herkunft

Vier Originalbilder wurden für diese Vorbereitung erneut angesehen. Sie sind
1280 × 720 große Clientaufnahmen der aktuellen 26.2-Modelle. Für eine technische
Vorschau eignen sie sich mit den unten angegebenen Bildunterschriften.
Keines ist als natürlich entdeckte Survival-Szene freigegeben.

| Original | Vorgeschlagene englische Bildunterschrift | Auswahl |
|---|---|---|
| [Großer Koloss](../testing/images/beta-renderer-20261104/fabric-26.2/01-colossus-whole-model-front-operator-marker-replacements.png) | Large Colossus, placed in a renderer test scene. | Modellvorschau; sichtbare Chunkgrenzen, kein Titelbild |
| [Obelisk](../testing/images/beta-renderer-20261104/fabric-26.2/06-obelisk-whole-model-front-operator-marker-replacements.png) | Weathered Obelisk, placed for model inspection. | Modellvorschau; sichtbarer Testausschnitt |
| [Weltenbaum](../testing/images/beta-renderer-20261104/fabric-26.2/14-world-tree-whole-model-front-operator-marker-replacements.png) | World Tree and exposed roots in a renderer test scene. | Technischer Anhang; freigelegter Boden eignet sich nicht als Werbeaufnahme |
| [Turmruine](../testing/images/beta-renderer-20261104/fabric-26.2/18-ruined-tower-whole-model-front-operator-marker-replacements.png) | Ruined Tower exterior, placed for model inspection. | Beste der vier Außenansichten für eine gekennzeichnete Vorschau |

Vor der endgültigen Projektseite Titelaufnahme und wenige Außenansichten in
natürlich generierten Standorten des finalen Kandidaten aufnehmen. Keine
Innenraum-/Belohnungsübersicht als Titelbild verwenden. Das alte
[V3-Shaderalbum](../../relics/colossus/demo/README.md) ist historische Kunst und
kein Beleg der heutigen Modelle. Bilddateien nicht heimlich als neu ausgeben.

Ein finales Icon für Titan Relics ist noch zu gestalten.
Vorschlag: eine selbst gezeichnete, auch klein erkennbare Silhouette eines
gebrochenen Monuments. Keine fremden Logos oder neuen KI-Bildgenerierungen.
Die reproduzierbare Blender-/Voxel-Pipeline ist in
[BLENDER_WORKFLOW.md](../technical/BLENDER_WORKFLOW.md) dokumentiert. Das allein
beweist weder menschliche Urheberschaft aller Quellen noch Plattformzulässigkeit.

## Modrinth-Regeln vor einer Einreichung klären

Die am 5. November gelesenen [Modrinth-Regeln](https://modrinth.com/legal/rules),
Stand der Seite 13. August 2026, verlangen eine KI-Kennzeichnung auch bei
KI-gestützten Seitenbeschreibungen. Diese Entwürfe wurden mit Codex erstellt;
dieser Kennzeichnungsfall liegt hier konkret vor. Die Regeln schließen zudem
überwiegend KI-erstellte Projekte und KI-erstellte oder daraus abgeleitete
Seitenbilder aus. Eine Kennzeichnung allein hebt diese Ausschlüsse nicht auf.

Die Herkunft des Produktionscodes, der Strukturentwürfe, Generatorskripte und
Itemgrafiken muss vor einer Einreichung nachvollziehbar erfasst und anhand der
Regeln beurteilt werden. Ein Screenshot ist keine automatische Ausnahme für
die Herkunft der dargestellten Assets. Der Umfang dieser Herkunftsprüfung ist
mit den vorliegenden Dateien nicht abschließend belegt. Daher keine Zusage,
dass Modrinth diesen Stand akzeptiert. Falls die Einordnung unklar bleibt,
vor einer Einreichung beim Plattform-Support klären. Es wurde niemand kontaktiert.

Die Prüfung ist eine konkrete offene Plattformbedingung. Sie ist kein Anlass,
KI-Beteiligung zu verschweigen oder das Projekt durch bloße Umbenennung anders
einzureichen. Die [CurseForge-Moderationsregeln](https://support.curseforge.com/support/solutions/articles/9000197279-moderation-policies),
Stand 22. Oktober 2026, verlangen eigene klare Inhalts-/Versionsangaben und
eine sichtbare Kennzeichnung potenziell irreführender KI-veränderter
Vorschaubilder. Sie sind gesondert zu prüfen; eine automatische Übertragung
der Modrinth-Regeln wird nicht behauptet. Hier wurden keine neuen Bilder generiert.

## Entscheidungen zur Freigabe

Diese Punkte sind absichtlich offen und keine durch dieses Paket getroffenen
Entscheidungen:

- Namenskollisionen und Verfügbarkeit des vorgeschlagenen Slugs `titan-relics`
  auf beiden Plattformen prüfen. Der Name und Untertitel sind gewählt.
- Lizenz für Code und Assets; Metadaten aktuell `All-Rights-Reserved`.
- Ausdrückliche Regeln für Modpack-Nutzung, Weiterverteilung und gegebenenfalls
  externe Launcher. Modrinth behandelt Modpack-Berechtigungen nach den
  [veröffentlichten Berechtigungsregeln](https://support.modrinth.com/en/articles/8797527-obtaining-modpack-permissions).
- Plattformzulässigkeit/Herkunft, finales Icon und natürliche Titelbilder.
- Ergebnis des vollständigen Survival-Tests, letzte Fixes, Versionsnummer und
  ausdrückliche öffentliche Beta-Freigabe.

## Ablauf nach den Entscheidungen

1. Gewählte Angaben in beiden Seitenentwürfen, README, Metadaten und
   Release-Notizen konsistent einsetzen. Den internen Mod-ID-/Save-Namensraum
   `relics` erhalten; ein Anzeigename verlangt keine Datenmigration.
2. Die endgültige Quellrevision und alle vier Kandidaten mit SHA-256 binden.
   Bei Code-/Assetänderungen die betroffenen Prüfungen erneut durchführen;
   bisherige November-Belege gelten nur für ihre dort genannten Artefakte.
3. Die [bestehende Release-CI](RELEASE_CI.md) kann mit manuellem Dispatch
   bauen/testen, ohne zu veröffentlichen. Ein Tag-Push löst dagegen die
   GitHub-Veröffentlichung aus und gehört erst hinter die ausdrückliche Freigabe.
4. Die Projektseiten anhand der Entwürfe anlegen, nach Plattformprüfung je vier
   korrekte Dateien mit Release-Typ **Beta** vorbereiten. Aktuelle Spielversionstags
   und passende Abhängigkeitsdateien in jedem Portal prüfen. Falls ein Ziel fehlt,
   nicht ersatzweise eine andere Spielversion markieren.
5. Vor der tatsächlichen Freigabe Name/Lizenz/Modpack-Regeln, öffentliche
   Dokumentationslinks, Dateimetadaten und Sichtbarkeit prüfen. Keine
   Test-/Source-JARs oder Abhängigkeiten als Spielerdateien hochladen.
6. Nach Veröffentlichung alle vier JARs von jeder genutzten Plattform wieder
   herunterladen, SHA-256 gegen das freigegebene Bundle vergleichen und
   Spiel-/Loaderzuordnung, Abhängigkeiten und Downloadverfügbarkeit protokollieren.
   Erst dann Beta-Downloadlinks in README und Index einsetzen.

Das Paket richtet keine Upload-Automation ein, benötigt keine Zugangsdaten und
legt keine externen Projekte an. Die endgültige Downloadprüfung kann erst an
den tatsächlich veröffentlichten Dateien stattfinden und bleibt Roadmap-Punkt 6.
