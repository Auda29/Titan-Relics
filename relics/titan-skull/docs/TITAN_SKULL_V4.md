# Titan Skull V4 — Ingame-Erkenntnisse und Überarbeitung

Stand: 2. Oktober 2026.
Status: **Vier V4-Varianten exportiert und offline geprüft; Sichtabnahme ausstehend.** Grundlage ist der
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
| Der Hügel wirkt wie ein aufgesetztes Ausstellungspodest. | Mehrere flache, unterbrochene Ablagerungen mit unterschiedlich langen Ausläufern statt einer gemeinsamen Bodenplatte. |
| Terrassen sind sehr gleichmäßig; einzelne Außenkanten wirken gerade. | Höhenlinien aufbrechen, lokale Senken und unregelmäßige Ausläufer statt geschlossener gleichmäßiger Stufen vorsehen. |
| Der graue Steinrand bildet einen auffälligen Sockel. | Den umlaufenden Steinrand vollständig weglassen; auch die Steinvariante erhält keine separate Sockelumrandung. |
| Kräftiges Grün hebt den gesamten Hügel von der trockenen Savanne ab. | Oberflächen und Bewuchs an das umgebende Biom anpassen; Moos gezielt als Akzent statt als flächige grüne Hülle einsetzen. |
| Die überwiegend braune Schädeloberfläche liest sich als Fels oder Statue. | Knochen-/Fossilmaterial klarer von Erde und Gestein absetzen; helle verwitterte Bereiche mit dunkleren mineralisierten Zonen kombinieren. |
| Die helleren Wirbel vermitteln „Knochen“ deutlicher als der Schädel. | Schädel und Wirbelsäule als zusammengehörige Überreste lesbar machen, ohne ihre Materialien überall zu vereinheitlichen. |

## Festgelegte Hügelgestaltung und Biomvarianten

Entscheidung vom 2. Oktober 2026: **Die Verschüttung bleibt erhalten**, wird aber
als kleinerer, aufgebrochener Hügel aus mehreren unregelmäßigen Ablagerungen
gestaltet. Der Hügel wird nicht vollständig entfernt.

- Kein umlaufender Steinrand und keine durchgehende gemeinsame Bodenplatte.
- Flache Erhebungen zwischen und neben den Knochen, mit unterschiedlich langen,
  asymmetrischen Ausläufern und lokalen Senken.
- Freie Stellen zwischen den Ablagerungen lassen vorhandenes Weltgelände sichtbar.
- Untere Teile der Wirbelsäule bleiben eingegraben; Mundöffnung, wichtige
  Bruchstellen und erkundbare Hohlräume bleiben frei.

Nach Prüfung der vorgesehenen Biome sind **vier** Gelände-Materialvarianten umgesetzt.
Die ursprünglich gemeinsame Erdvariante ist in Wiese und trockene Erde aufgeteilt:

| Umgebung | Material der Ablagerungen |
| --- | --- |
| Wüste | Sand an der Oberfläche, darunter teilweise Sandstein |
| Grünes Grasland | Überwiegend Grasoberfläche, lokale grobe Erde, darunter Erde |
| Savanne / Steppe / Buschland | Überwiegend grobe Erde, vereinzelte Grasflächen, darunter Erde |
| Steinwüste | Stein mit Kies und verwitterten Bereichen, ohne umlaufenden Sockel |

Die Weltgenerierung soll anhand ausdrücklich zugeordneter Biome die passende
vorbereitete Template-Variante wählen. **Knochen- und Fossilmaterialien sind von
diesem Geländewechsel unabhängig.** Eine automatische Erkennung beliebiger
Mod-Biome ist damit nicht zugesagt; konkrete Biomzuordnungen und die technische
Auswahl der Varianten sind bei der Integration festzulegen.

Die Varianten verbessern den Materialübergang, passen die starre Grundform aber
nicht automatisch an jeden Hang an. Flach auslaufende Ränder und geeignete
Platzierungsbedingungen bleiben nötig. Die teilweise Verschüttung soll nicht
vollständig vom zufälligen Weltgelände abhängen.

## Prioritäten

1. **Hügel und Außenrand:** den Podestcharakter beseitigen. Das hat Vorrang vor
   zusätzlichen Details am eigentlichen Schädel.
2. **Biomübergang:** Material- und Vegetationskontrast zur Umgebung reduzieren.
3. **Knochenwirkung:** Schädel und Wirbelsäule deutlicher als Überreste vermitteln.

Die vier Materialexporte sind umgesetzt; ihre Auswahl und Platzierung bleiben
Integrationsaufgaben. Ein stärker organischer Export allein kann beliebiges Weltgelände nicht
passgenau treffen. Nicht einfach einen größeren, weiterhin starren Hügel exportieren.

## Prüfkriterien für V4

Offline-Ergebnis: 62 Anatomie-Meshes unverändert, 52,44 % weniger Gelände,
zwei freie Gelände-Lücken, keine fehlenden Innenzellen in den Ablagerungen.
Alle vier Varianten: 117 × 79 × 179, 136.569 Blöcke. Knochenpositionen und
-materialien sind zwischen den Varianten identisch. Schnee/Rotsand sind für
die derzeit vorgesehenen Biome nicht nötig.
Siehe [Exportnachweis und Vergleichsbilder](TITAN_SKULL_V4_EXPORTS.md).
Die folgende Liste bleibt die abschließende Sicht-/Ingame-Abnahme; Offline-Prüfungen
ersetzen keine Bewertung der Platzierung auf natürlichem Weltgelände.

- [ ] Aus mindestens zwei Luftansichten keine dominante gerade Sockelkante.
- [ ] Kein geschlossener grauer Steinring und keine gleichmäßig gestaffelte Podestform.
- [ ] Mehrere unterbrochene Ablagerungen und freie Stellen statt einer gemeinsamen Bodenplatte.
- [ ] Sand-, Erd- und Steinvariante erhalten dieselbe Knochengeometrie und unabhängige Knochenmaterialien.
- [ ] Biomzuordnung wählt die passende Geländevariante.
- [ ] Übergänge in Wüste, trockener Savanne, einem grüneren zugelassenen Biom und einer zugeordneten Steinwüste prüfen.
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
