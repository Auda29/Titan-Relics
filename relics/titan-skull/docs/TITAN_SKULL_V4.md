# Titan Skull V4 — Ingame-Erkenntnisse und Überarbeitung

Stand: 1. Oktober 2026.
Status: **V4-Planung, noch nicht umgesetzt.** Grundlage ist der
[Titan Skull V3](TITAN_SKULL_V3.md) in Alpha 3; V3 bleibt unverändert erhalten.

## Grundlage und Ziel

Schädel, Krone und Wirbelsäule sind bereits gut lesbar. Die größte Schwäche ist
der mitexportierte Hügel: V4 soll die Überreste als **alten, teilweise
verschütteten Fund im Gelände** zeigen, nicht als Objekt auf einem Podest.

Screenshot-Grundlage aus dem Profil „Relic Test“, Ordner `screenshots/`:

- `2026-10-01_21.33.35.png` und `2026-10-01_21.33.54.png`: zwei Luftansichten
  mit Schädel, Wirbelsäule, Hügelrand und umgebender Savanne.

Die Bilder liegen lokal; diese Notizen betten sie nicht ins Repository ein.
Natürliche Platzierung und bekannte technische Grenzen stehen im
[Alpha-3-Testbericht](../../../docs/testing/ALPHA_3_TEST_REPORT.md).

## Was erhalten bleiben soll

- Charakteristische Schädelsilhouette und Krone.
- Offene Augen-/Mundbereiche und der Anreiz, die Hohlräume zu erkunden.
- Gebrochene, versetzte und teilweise verschüttete Wirbelsäule mit Fragmenten.
- Monumentaler Maßstab; keine pauschale Verkleinerung aufgrund dieser Bilder.
- Zusammenhängende Geschichte von Schädel, Knochenresten und Ablagerungen.

## Beobachtungen und V4-Richtung

| Beobachtung | Geplante Überarbeitung |
| --- | --- |
| Der Hügel wirkt wie ein aufgesetztes Ausstellungspodest. | Asymmetrische Hügelform mit flach auslaufenden, unterschiedlich langen Übergängen zum Gelände. |
| Terrassen sind sehr gleichmäßig; einzelne Außenkanten wirken gerade. | Höhenlinien aufbrechen, lokale Senken und unregelmäßige Ausläufer statt geschlossener gleichmäßiger Stufen vorsehen. |
| Der graue Steinrand bildet einen auffälligen Sockel. | Stein nur an plausiblen Erosions- oder Bruchstellen zeigen, nicht als durchgehende Umrandung. |
| Kräftiges Grün hebt den gesamten Hügel von der trockenen Savanne ab. | Oberflächen und Bewuchs an das umgebende Biom anpassen; Moos gezielt als Akzent statt als flächige grüne Hülle einsetzen. |
| Die überwiegend braune Schädeloberfläche liest sich als Fels oder Statue. | Knochen-/Fossilmaterial klarer von Erde und Gestein absetzen; helle verwitterte Bereiche mit dunkleren mineralisierten Zonen kombinieren. |
| Die helleren Wirbel vermitteln „Knochen“ deutlicher als der Schädel. | Schädel und Wirbelsäule als zusammengehörige Überreste lesbar machen, ohne ihre Materialien überall zu vereinheitlichen. |

## Prioritäten

1. **Hügel und Außenrand:** den Podestcharakter beseitigen. Das hat Vorrang vor
   zusätzlichen Details am eigentlichen Schädel.
2. **Biomübergang:** Material- und Vegetationskontrast zur Umgebung reduzieren.
3. **Knochenwirkung:** Schädel und Wirbelsäule deutlicher als Überreste vermitteln.

Die technische Umsetzung bleibt offen: Ein stärker organischer Export allein
kann beliebiges Weltgelände nicht passgenau treffen. Geländeabhängige Platzierung,
Materialvarianten oder lokale Übergangsgestaltung müssen gesondert geprüft werden.
Nicht einfach einen größeren, weiterhin starren Hügel exportieren.

## Prüfkriterien für V4

- [ ] Aus mindestens zwei Luftansichten keine dominante gerade Sockelkante.
- [ ] Kein geschlossener grauer Steinring und keine gleichmäßig gestaffelte Podestform.
- [ ] Der Übergang funktioniert in trockener Savanne und einem grüneren zugelassenen Biom.
- [ ] Bodenperspektive zusätzlich prüfen; die bisherigen Bilder zeigen vor allem Luftansichten.
- [ ] Schädel, Krone und Wirbelsäule bleiben trotz Verschüttung klar lesbar.
- [ ] Schädelmaterial wirkt wie Knochen/Fossil statt überwiegend wie eine Felsstatue.
- [ ] Brüche, versetzte Wirbel und Hohlräume bleiben erhalten und werden nicht zugeschüttet.
- [ ] Alle vier natürlichen Rotationen, unterschiedliche Hänge und Chunkgrenzen prüfen.

## Abgrenzung

Keine neue besondere Belohnung oder eigens entworfene Mobmechanik; die bestehende
Gameplay-Richtung bleibt erhalten. Kleine Erz-/Terrain-Feature-Überschreibungen
sind ein separates technisches Thema, nicht die Erklärung für den sichtbaren
Podestcharakter. V4 benötigt eigene Export- und Ingame-Prüfungen und wird durch
diese Notizen noch nicht in den Build aufgenommen.
