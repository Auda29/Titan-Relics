# Beta: abschließende Rendererabnahme vom 4. November 2026

Die noch offene grafische Ergänzung zu Roadmap-Punkt 4 ist abgeschlossen. Auf Fabric und NeoForge, jeweils für Minecraft 1.21.1 und 26.2, wurden je 24 aussagekräftige Ansichten tatsächlich angesehen. Alle 96 Original-PNGs wurden vollständig dekodiert, im Repository erhalten und bytegleich gegen ihre Quellen geprüft. Es wurden keine fehlenden Texturen oder reproduzierbaren Modellfehler in diesen Ansichten festgestellt.

Zusammen mit der [Client-Teilabnahme](BETA_CLIENT_ACCEPTANCE_20261104.md) und der [funktionalen Gameplay-Abnahme](BETA_CLIENT_GAMEPLAY_ACCEPTANCE_20261104.md) erfüllt dies die Prüfliste von [Roadmap-Punkt 4](../project/PUBLIC_BETA_ROADMAP.md#4-alle-vier-zielversionen-im-echten-client-abnehmen) für den getesteten lokalen Kandidaten. Der natürliche Survival-Durchlauf, Modpack-/Leistungsmessungen und die öffentliche Freigabe bleiben eigene Aufgaben.

Die [JSON-Evidenz](beta-renderer-acceptance-20261104.json) enthält die vollständigen JAR-Prüfsummen, Bildbindungen, Szenenkommandos, Startargumente, Quellen- und Loghashes, protokollierte Prozessausgänge und verworfene Ansichten. Der [Collector](../../tools/collect_beta_renderer_evidence.py) prüft die Artefakte, Vollständigkeit und erhaltenen Bilder erneut.

## Geprüfte Matrix

| Ziel | Sichtprüfung | Getragene Monolith-Rüstung |
|---|---|---|
| Fabric 1.21.1 | [24 Originalbilder](images/beta-renderer-20261104/fabric-1.21.1/) | [Vorderseite](images/beta-renderer-20261104/fabric-1.21.1/23-worn-monolith-amethyst-armor-front-operator-equipment.png), [Rückseite](images/beta-renderer-20261104/fabric-1.21.1/24-worn-monolith-amethyst-armor-rear.png) |
| Fabric 26.2 | [24 Originalbilder](images/beta-renderer-20261104/fabric-26.2/) | [Vorderseite](images/beta-renderer-20261104/fabric-26.2/23-worn-monolith-amethyst-armor-front-operator-equipment.png), [Rückseite](images/beta-renderer-20261104/fabric-26.2/24-worn-monolith-amethyst-armor-rear.png) |
| NeoForge 1.21.1 | [24 Originalbilder](images/beta-renderer-20261104/neoforge-1.21.1/) | [Vorderseite](images/beta-renderer-20261104/neoforge-1.21.1/23-worn-monolith-amethyst-armor-front-operator-equipment.png), [Rückseite](images/beta-renderer-20261104/neoforge-1.21.1/24-worn-monolith-amethyst-armor-rear.png) |
| NeoForge 26.2 | [24 Originalbilder](images/beta-renderer-20261104/neoforge-26.2/) | [Vorderseite](images/beta-renderer-20261104/neoforge-26.2/23-worn-monolith-amethyst-armor-front-operator-equipment.png), [Rückseite](images/beta-renderer-20261104/neoforge-26.2/24-worn-monolith-amethyst-armor-rear.png) |

Die 24 Ansichten pro Ziel umfassen:

- Vorder- und Rückansicht von großem Koloss, kleinem Koloss, Obelisk, Weltenbaum, Turmruine und beiden Titanenschädeln.
- Spawner, Vault und Armtruhe des großen Kolosses, Fundbereich des Obelisken, obere Magnettruhe des kleinen Kolosses, Amethystzentrum und Pflanze des Baums sowie Truhenstand der Turmruine.
- Vorder- und Rückansicht eines vollständig getragenen Netheritsets mit Monolith-/Amethyst-Verzierung. Helm, Brust, Beine und Stiefel sind sichtbar; kein Menü oder Tutorial verdeckt die Rüstung.

Die gewöhnlichen Truhen und der Farn auf 1.21.1 sowie Kupfertruhen und Firefly Bush auf 26.2 sind jeweils auf beiden Loadern sichtbar. Die Rüstungsverzierung ist auf allen vier Zielen vorhanden und an den Körperteilen ausgerichtet. Eine neue künstlerische Gestaltung wurde nicht vorgenommen.

## Artefakte und Prüfaufstellung

Die vier JARs entsprechen unverändert den in der Gameplay-Abnahme genannten lokalen DISCOVERY-Testartefakten. Ihre SHA-256 beginnen mit `a10c4e6657985680`, `9ce11af173ebfd5e`, `86bb9380a3ed80d9` und `bfd259fe5369e3ad4` für Fabric 1.21.1, Fabric 26.2, NeoForge 1.21.1 und NeoForge 26.2. Dies ist keine neue Veröffentlichung der gleich benannten Alpha-5.0.5-Dateien.

Die Operator-Ausstellung platziert die Templates aus dem jeweiligen getesteten JAR und ersetzt die Gameplay-Marker durch die nativen Blöcke der Version. Das Ausstellungsgelände wird vorher freigeräumt; Innenräume verwenden Spectator und Nachtsicht. Die Rüstung wird als Operator-Ausstattung auf einer vorbereiteten Plattform angelegt. Damit werden die Darstellung und die Adaptionsblöcke geprüft. Natürliche Einbettung, tatsächliches Blocklicht, neue Belohnungsinteraktionen und Survival-Balance werden damit nicht zusätzlich abgenommen. Sichtbare Geländeschnitte und schwebende Ausstellungsmodelle sind Eigenschaften dieser Testaufstellung.

Die Fortsetzung verwendete ausschließlich `E:/Relic_Mod_QA/renderer-20261104/` für neue Weltkopien, Probe-Kompilate, Natives, Java-Tempdateien, Logs und Screenshots. Die Clients starteten einzeln und verborgen. `soundCategory_master:0.0` war vor dem Start gesetzt; die Bootstrap-Probe setzte MASTER zusätzlich fortlaufend auf 0. Nutzerprofile und Originalwelten wurden nicht verändert.

## Ergänzende Läufe und verworfene Bilder

Die fünf ergänzenden Läufe dieser Fortsetzung endeten alle mit Exitcode 0, erfolgreichem Speichern und vollständigen Bilddateien:

| Lauf unter dem E:-Scratch | Ergänzung |
|---|---|
| `fabric-1.21.1-135207-182607` | Getragene Rüstung vorn/hinten |
| `fabric-26.2-135428-525902` | Rüstung und Titan Skull 2 |
| `neoforge-1.21.1-135709-322190` | Rüstung, vollständiger Weltenbaum und Titan Skull 2 |
| `fabric-1.21.1-140138-749857` | Turm einschließlich Rückansicht und Truhe |
| `neoforge-26.2-140424-692447` | Weltenbaum und sichtbarer Firefly Bush |

Lesbare Bilder aus den zuvor auf Nutzerwunsch unterbrochenen E:-Läufen bleiben als einzelne Sichtbelege erhalten. Für diese alten Prozesse wird kein unbekannter Exit nachträglich als erfolgreich erklärt. Die beschädigten C:-Bilder aus dem früheren Bericht werden weiterhin nicht verwendet.

Bei der erneuten Sichtung wurden auch technisch lesbare, aber ungeeignete Aufnahmen verworfen: leere Himmelsansichten, Unterwasserbilder ohne sichtbaren Spieler und unvollständig geladene Weltenbaum-Meshes. Die konkreten Zuordnungen stehen im JSON. Die Ergänzungen ersetzen diese Ansichten und die beim Unterbrechen noch fehlenden Szenen.

Der Testhelfer stellt die gewünschte Kamera vor der Aufnahme erneut her und protokolliert Kameratyp, Spielermodus und Position. Für die Rüstung wird zuerst der Plattformbereich geladen. Zwei Sekunden Abstand nach einer Aufnahme geben dem Screenshot und dem letzten Bild vor dem Beenden Zeit zum Abschluss. Die Änderungen betreffen ausschließlich den Testhelfer; Produktions-JARs und Modellquellen bleiben unverändert.

## Netz- und Logbefunde

Die JVM-eigene `jdk.net.hosts.file` enthält nur localhost. Die tatsächlichen neuen Minecraft-Logs zeigen fehlgeschlagene Vanilla-Dienstauflösungen mit `UnknownHostException`, statt erfolgreicher Namensauflösung und nachfolgender HTTP-401-Antworten. Die Sperre ändert weder die Windows-Hostsdatei noch die Firewall. Sie ist keine Behauptung einer systemweiten Netzsperre. Dienstversuche bleiben ungefiltert in den Logs.

Die historischen Konto-/Realms-401-Meldungen und beiden Gast-Disconnect-Auffälligkeiten aus dem Gameplay-Bericht bleiben ausdrücklich bestehen. In dieser Rendererfortsetzung wurde keine neue Mehrspieler-Disconnect-Reproduktion durchgeführt. Die fünf ergänzenden Einzelclient-Läufe erzeugten keine neuen Crashberichte oder `acceptance-failure.txt`. Warnungen während der umfangreichen Operator-Fill-/Template-Kommandos sind kein gemessenes Gameplay-Leistungsbudget.

## Reproduktion und Abschluss

Beispiel mit einer akzeptierten frischen Ausgangskopie:

```powershell
python tools/test_beta_gameplay_client.py --fixture build/beta-client-acceptance-20261104/neo-client-1.21.1-110000-535487 --loader neoforge --minecraft 1.21.1 --scratch-root E:/Relic_Mod_QA/renderer-20261104 --visual-cases E:/Relic_Mod_QA/renderer-20261104/final-cases21.json
python tools/collect_beta_renderer_evidence.py
```

Die konkreten Szenendefinitionen und Java-Startargumente jedes ausgewählten Laufs sind zusätzlich im JSON enthalten. Ein erneuter Capture benötigt anschließend eine neue Sichtprüfung; der Collector allein beurteilt keine Bildinhalte. Seine manuelle Auswahl liegt unter `E:/Relic_Mod_QA/renderer-20261104/review-selection.json`.

Die Abschlussprüfung vergleicht die vorgefundenen lokalen Änderungen und die sieben geschützten Release-Referenzdateien. Autorisierte Ergänzungen sind dieser Bericht, JSON und Bilder, der Evidence-Collector, die Kamera-/Capture-Ergänzung im Testhelfer, der Folgehinweis im früheren Gameplay-Bericht und die Aktualisierung von Roadmap-Punkt 4. Es wurde kein vollständiger Produktbuild, Commit, Push, Tag oder Release ausgelöst. Alle Testclients sind beendet.
