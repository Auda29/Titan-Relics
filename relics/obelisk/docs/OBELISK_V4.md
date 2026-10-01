# Obelisk V4 — Ingame-Erkenntnisse und Überarbeitung

Stand: 1. Oktober 2026.
Status: **V4-Planung, noch nicht umgesetzt.** Grundlage ist der
[Obelisk V3](OBELISK_V3.md) in Alpha 3; V3 bleibt unverändert erhalten.

## Grundlage und Ziel

Der Obelisk funktioniert als weithin sichtbares Monument. V4 soll ihn stärker
als **altes, verwittertes Bauwerk und archäologischen Fundort** vermitteln,
ohne seine bereits abgestimmte Grundgeometrie aufzugeben.

Screenshot-Grundlage aus dem Profil „Relic Test“, Ordner `screenshots/`:

- `2026-10-01_21.34.15.png`: Bodenperspektive mit Wüste und Dorf als Größenvergleich.

Das Bild liegt lokal; diese Notizen betten es nicht ins Repository ein.
Natürliche Platzierung und bekannte technische Grenzen stehen im
[Alpha-3-Testbericht](../../../docs/testing/ALPHA_3_TEST_REPORT.md).

## Was erhalten bleiben soll

- Schlanke, monumentale Silhouette und Fernwirkung.
- Der abgestimmte verjüngte quadratische Antiprismus mit gedrehter oberer Fläche.
- Solider Kern statt eines neu erfundenen begehbaren Turms.
- Warme Wüstenpalette und der archäologische Schwerpunkt am Fuß.
- Der bewusst höhere sichtbare Aufbau im Verhältnis zum eingegrabenen Colossus.

Die Größe wirkt im Bild überzeugend. V4 soll zunächst die Material- und
Alterswirkung verbessern, nicht automatisch Höhe oder Grundform ändern.

## Beobachtungen und V4-Richtung

| Beobachtung | Geplante Überarbeitung |
| --- | --- |
| Sehr große, gleichmäßige Farbflächen wirken sauber und neu. | Gezielte Verwitterungszonen, mineralische Unterschiede, abgeriebene Oberflächen und einzelne Risse vorsehen. |
| Die goldgelbe Vorderfläche und zugespitzte Silhouette erinnern etwas an einen riesigen Bleistift. | Durch Materialwirkung, gebrochene Kanten und weniger durchgehende Farbbänder einen alten Monumentcharakter herstellen; nicht vorschnell die Antiprismus-Geometrie ersetzen. |
| Kanten und Flächen zeigen wenig sichtbare Alterung. | Unregelmäßige, begrenzte Abplatzungen und beschädigte Bereiche statt überall gleich starkem Zufallsrauschen. |
| Der Fuß steht ohne ausgeprägten Fundort direkt im Wüstengelände. | Sandverwehungen, teils verschüttete Fragmente und stellenweise freigelegte Fundamentreste als Übergang vorsehen. |

Die Wolken verdecken im Screenshot Teile der Spitze. Das ist **kein Beleg für
einen Material-, Export- oder Geometriefehler**; die Spitze separat bei freier
Sicht prüfen.

## Prioritäten

1. **Verwitterung und Materialwirkung:** alte Stein-/Mineraloberflächen statt
   einer frisch gebauten, gleichmäßig eingefärbten Säule.
2. **Fundort am Fuß:** natürliches Versanden und sichtbare Geschichte herstellen.
3. **Kantenschäden:** die Silhouette altern lassen, ohne ihre klare Form zu verlieren.

Die ruhigen großen Flächen sollen nicht vollständig verschwinden. Schäden und
Materialwechsel müssen die Geometrie unterstützen, nicht sie unlesbar machen.

## Prüfkriterien für V4

- [ ] Die Antiprismus-Form und gedrehte obere Fläche bleiben erkennbar.
- [ ] Aus Bodennähe und Entfernung wirkt das Relikt als altes Monument.
- [ ] Keine dominierende, durchgehend einfarbige „Bleistift“-Vorderfläche.
- [ ] Verwitterung wirkt zusammenhängend und nicht wahllos auf alle Blöcke verteilt.
- [ ] Sand und Fundamentreste verbinden den Fuß mit unebenem Wüstengelände.
- [ ] Der Fundort bekommt keine starre rechteckige Plattform oder gleichmäßigen Ring.
- [ ] Die Spitze bei freier Sicht sowie die vier natürlichen Rotationen prüfen.
- [ ] Soliden Kern, Platzierungshöhe und vollständigen Export weiterhin validieren.

## Abgrenzung

Die Fundortgestaltung nimmt die bereits vereinbarte archäologische Richtung auf,
implementiert aber noch keine Funde, Karten, Loot oder neuen Mechaniken.
Materialpalette, Schadensumfang und technische Geländeanpassung sind vor der
Umsetzung zu konkretisieren. V4 ersetzt V3 nicht ohne eigene Export- und
Ingame-Prüfung.
