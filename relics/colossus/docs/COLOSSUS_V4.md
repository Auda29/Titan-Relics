# Colossus V4 — Ingame-Erkenntnisse und Überarbeitung

Stand: 1. Oktober 2026.
Status: **V4-Planung, noch nicht umgesetzt.** Grundlage ist der
[Colossus V3](COLOSSUS_V3.md) in Alpha 3; V3 bleibt unverändert erhalten.

## Grundlage und Ziel

Die Ingame-Bilder aus der normalen Gelände-Testwelt zeigen, dass die monumentale
Wirkung bereits funktioniert. V4 soll den Colossus stärker als **uralte,
beschädigte und teilweise eingesunkene Maschine** vermitteln, statt als
aufgestellte, weitgehend intakte Skulptur.

Screenshot-Grundlage aus dem Profil „Relic Test“, Ordner `screenshots/`:

- `2026-10-01_21.34.29.png` und `2026-10-01_21.34.32.png`: Bodenperspektive.
- `2026-10-01_21.34.46.png`: Vorder-/Seitenansicht mit abgetrenntem Arm.
- `2026-10-01_21.35.24.png`: Rückansicht.

Die Bilder liegen lokal; diese Notizen betten sie nicht ins Repository ein.
Natürliche Platzierung und bekannte technische Grenzen stehen im
[Alpha-3-Testbericht](../../../docs/testing/ALPHA_3_TEST_REPORT.md).

## Was erhalten bleiben soll

- Monumentaler Maßstab und breite, schwere Schulterpartie.
- Runder Taucherhelm, schmales Visier und seitliche Maschinenanschlüsse.
- Eigenständiger abgetrennter Arm und unterirdische Körperfortsetzung.
- Warme Metalltöne, Patina und Bewuchs als gemeinsame Materialidee.
- Gute Erkennbarkeit und Entdeckungswirkung aus der Spielerperspektive.

Die Bilder begründen keine pauschale Verkleinerung. V3-Abmessungen und Bodenniveau
bleiben zunächst die Ausgangsbasis, nicht bereits festgelegte V4-Exportwerte.

## Beobachtungen und V4-Richtung

| Beobachtung | Geplante Überarbeitung |
| --- | --- |
| Große Rundflächen auf Rücken und Schultern wirken zu gleichmäßig und intakt. | Größere, asymmetrische Panzerbrüche, freiliegende Schichtdicken und erkennbare innere Konstruktion statt nur kleiner Löcher. |
| Die braune Hauptoberfläche liest sich teilweise als Stein oder Terrakotta. | Metallplatten, Verbindungen, Kupferkanten und Oxidation klarer voneinander unterscheiden; große Flächen gezielt gliedern. |
| Der untere Panzerabschluss trifft abrupt auf das Gelände. | Unterschiedliche Verschüttungshöhen, Erdablagerungen, Geröll und herausragende Fragmente an den Kontaktstellen vorsehen. |
| Der abgetrennte Arm wirkt aus der Luft wie ein Rohr mit rundem Abschluss. | Hand, Finger beziehungsweise Gelenke sowie die Bruchstelle deutlicher lesbar machen. |
| Der Kopf-Hals-Übergang wirkt besonders hinten schmal und aufgesetzt. | Den Anschluss aus mehreren Richtungen prüfen und durch sichtbare Träger, Leitungen oder beschädigte Verbindungsteile nachvollziehbarer machen. |

Der aufgesetzte Eindruck am Hals ist eine **visuelle Beobachtung**, kein anhand
der Screenshots bestätigter schwebender oder technisch unverbundener Kopf.

## Prioritäten

1. **Geländekontakt:** den Eindruck des Einsinkens verbessern. Nicht einfach das
   ganze Modell tiefer setzen und damit Arm oder wichtige Details verschlucken.
2. **Rückseite und Panzerung:** Verfall und Maschinenaufbau deutlicher zeigen.
3. **Materialwirkung:** Metall, Rost, Patina und Bewuchs sinnvoll verteilen.
4. **Arm/Hand und Hals:** Lesbarkeit der einzelnen Bauteile verbessern.

## Prüfkriterien für V4

- [ ] Boden-, Front-, Seiten- und Rückansicht in echtem Gelände vergleichen.
- [ ] Kein dominanter gleichmäßiger Abschluss zwischen Panzerung und Boden.
- [ ] Rücken und Schultern wirken beschädigt, bleiben aber als schwere Panzerung erkennbar.
- [ ] Metallkonstruktion ist auch ohne Shader lesbar.
- [ ] Der Arm ist nicht nur als Rohr, sondern mit erkennbarem Hand-/Gelenkbereich lesbar.
- [ ] Kopf und Hals wirken konstruktiv verbunden, ohne unbeabsichtigte Luftspalten.
- [ ] Alle vier natürlichen Rotationen und unterschiedliche Geländehöhen prüfen.
- [ ] Ganze Struktur einschließlich Arm weiterhin vollständig über Chunkgrenzen erzeugen.

## Abgrenzung

Dies ist eine visuelle Überarbeitung, keine Umsetzung von Maschinenkern, Magnet,
Prüfung, Loot oder endgültigen Innenräumen. Schutz vor Terrain-Features und die
teure natürliche Suche bleiben eigene technische Aufgaben. Bei geänderten
Abmessungen müssen Bodenniveau, Platzierungsfilter und Zentrierung neu geprüft
werden; V4 wird nicht allein durch diese Notizen zum Standard-Build.
