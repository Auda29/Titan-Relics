# Innenraumentscheidungen vom 27. Oktober 2026

Grundlage ist die ausgefüllte Datei `relic-mod-innenraeume-entscheidung-alpha-5.pdf`
mit SHA-256 `ae679a1195120f54ccd3a6d9601d84c2712886dc0385046ca693c464b8ec3351`.
Die Bewertung bezieht sich auf die fünf Entwürfe aus der
[Innenraum-Übergabe](GAMEPLAY_INTERIORS_HANDOFF.md). Anschließend beauftragte der
Nutzer die Umsetzung aller Änderungen und verlangte für die 3D-Modelle einen
GPT-6.1-Terra-Worker mit Reasoning-Einstellung `xhigh`.

| Entwurf | Gesamtbewertung | Entscheidung | Priorität laut PDF |
| --- | --- | --- | --- |
| Großer Koloss V5 | 2 von 5 | Neu überarbeiten | Muss vor dem Release |
| Kleiner Koloss V8 | 3 von 5 | Mit Änderungen übernehmen | Sollte vor dem Release |
| Turmruine V8 | 4 von 5 | Mit Änderungen übernehmen | Sollte vor dem Release |
| Obelisk V5 Archäologie | 3 von 5 | Mit Änderungen übernehmen | Sollte vor dem Release |
| Weltenbaum V5 Wurzelbereich | 5 von 5 | Freigeben | Noch offen, kein Änderungswunsch |

## Großer Koloss

Die Cockpit-Sitze gefallen und sollen erhalten bleiben. Der Raum ist zu leer.
Mehr verfallene Maschinen und weitere räumliche Details sollen das Cockpit als
ehemals genutzten Maschinenraum erkennbar machen. Die Durchsicht durch das Visier
soll möglich werden. In der PDF wurden dunkles Glas und eine offene bzw.
aufgebrochene Ausführung als Alternativen genannt.

Für die beauftragte Überarbeitung wurde eine aufgebrochene Öffnung mit Resten
dunklen Glases als konkrete gestalterische Umsetzung angekündigt. Diese Auswahl
ist eine Ausführungsentscheidung, keine nachträglich behauptete Auswahl im PDF.
Die fünf vorhandenen Stationsreste, die vorgesehenen Begegnungsorte und der
Zugang zur separaten Arm-Truhe bleiben bei der Überarbeitung nutzbar.

## Kleiner Koloss

Der Grundentwurf gefällt. Mehr Details sollen den ausgeschlachteten,
stark zerfallenen Maschinenraum ausarbeiten. Brustzugang, Wartungsaufstieg und
der einzelne Truhenort bleiben erhalten. Intakte Bedienplätze werden dadurch
nicht neu eingeführt.

## Turmruine

Der Entwurf soll mit Änderungen übernommen werden. Die PDF wünscht eventuell
etwas mehr Details. Der anschließende Umsetzungsauftrag umfasst einen begrenzten
Detailpass. Halle, Begegnungsorte, Truhenort und bewusst unterbrochener Aufstieg
bleiben als bisheriger Entwurf erkennbar.

## Obelisk

Die archäologischen Fundbereiche sollen sichtbar gekennzeichnet werden, damit
Spieler sie entdecken. Die Kennzeichnung soll im tatsächlichen Modell vorhanden
sein. Die acht bestehenden Fundrollen und ihre Zugänglichkeit bleiben erhalten.

## Weltenbaum

Der Wurzelbereich ist gestalterisch freigegeben. Es gibt keine weiteren
Anmerkungen. Die vier Einzelkriterien sind im PDF noch offen; nur die
Gesamtbewertung wurde mit fünf Punkten vergeben. Die bestehenden Exporte und
Bilder des freigegebenen Entwurfs bleiben unverändert.

## Nachweis der Überarbeitung

Die vier überarbeiteten Entwürfe erhalten neue Versionspfade. Die bisherigen
Entwürfe bleiben als Vergleich erhalten. Die Übergabe soll NBT, Schematic,
editierbare Blender-Dateien, gebundene Marker, neue Ansichten und die Prüfungen
von Zugängen, Freiräumen und Exportgleichheit enthalten. Die neuen Ansichten
dienen zur Prüfung der umgesetzten Änderungswünsche. Die Gestaltungsfreigabe
ersetzt keine spätere technische Abnahme der natürlichen Generierung und des
Gameplays in Minecraft.

## Freigabe und Integration

Niklas hat die vier neuen Revisionen nach der Ansicht des zweiten
Bewertungsdokuments am 27. Oktober 2026 mit "sieht alles gut aus bitte
implementieren" freigegeben. Damit sind Großer Koloss V6, Kleiner Koloss V9,
Turmruine V9 und Obelisk V6 gestalterisch angenommen. Die vorhandene Freigabe
des Weltenbaums V5 gilt weiter. Die leeren Bewertungsfelder im zweiten PDF
werden durch diese Chatfreigabe nicht nachträglich ausgefüllt.

Die technische Umsetzung und ihre Laufzeitprüfungen stehen im
[Integrationsbericht](../testing/NATURAL_INTERIORS_20261027.md).
