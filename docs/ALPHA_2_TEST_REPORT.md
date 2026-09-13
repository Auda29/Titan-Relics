# Alpha 2: Verfall und Geländeübergänge

Stand: 13.09.2026. Version `0.1.0-alpha.2` für Minecraft 26.2, Fabric Loader 0.19.5 und Java 25.

## Änderung und Sichtprüfung

Die vom Nutzer gezeigten Minecraft-Screenshots der Alpha 1 bestätigen die sichtbaren Grundformen. Sie zeigten zugleich große gleichmäßige Flächen und einen langen rechteckigen Vorweg am Koloss. Alpha 2 verändert deshalb die Generatoren:

- Der Obelisk erhält zusammenhängende Einschnitte, ausgebrochene Ecken, Sandverwehungen und kleine Trümmer am Sockel.
- Am Koloss fehlen größere Teile des Helms und Brustpanzers. Dahinter sind zurückgesetzte Basaltstreben sichtbar. Brustring und abgetrennter Unterarm sind beschädigt.
- Moos und dauerhafte Blattflächen konzentrieren sich auf eine Seite. Die andere Seite bleibt überwiegend dunkel und freigelegt.
- Die äußere Pflasterung ist nur noch neun Blöcke lang. Ihr Rand ist unregelmäßig und teilweise vermoost. Eine durchgehende Route von drei Blöcken Breite führt vom lokalen Eingang `[40,10,14]` in den Maschinenraum. Erdstützen und Bodenformen fassen die Pflasterreste ein.

Die neuen Geometrievorschauen wurden aus den tatsächlich erzeugten Blöcken gerendert und betrachtet. Sie zeigen Form, Schäden und Bewuchs vor der Geländeeinbettung. Sie sind keine neuen Minecraft-Screenshots. Eine visuelle Abnahme der Alpha 2 im Client steht noch aus.

## Automatische Prüfungen

18 Tests prüfen Export und Wiederholbarkeit, die Rekonstruktion aus Teilvorlagen, Blockzustände, den begehbaren Zugang, die begrenzte Vorplatzfläche und die Öffnungen vor den Innenstreben. Außerdem werden Einstellungs-Datapacks und der Anvil-Weltleser geprüft. Der Testserver wählt jetzt standardmäßig die JAR der aktuellen Metadatenversion, damit eine ältere Datei in `dist/` nicht versehentlich getestet wird.

Die Laufprüfungen verwenden frische lokale Welten mit Seed `731204`, die bereits genehmigte EULA-Zustimmung und den bestehenden Testserver-Harness. Im Basistest werden Fabric API und Lithostitched geladen. Der Integrationstest ergänzt Tectonic, Terralith, Biomes O' Plenty, Dungeons & Taverns und deren Pflichtabhängigkeiten mit den bereits dokumentierten Versionen. Der Einstellungstest prüft häufigere Obelisken und einen deaktivierten Koloss.

Jeder Lauf prüft natürliche Starts anhand der gespeicherten Weltblöcke gegen genau die gestartete Mod-JAR. Erde, Grasblöcke und Azaleenblätter bleiben ausdrücklich aus dem strikten Vergleich ausgenommen. Feste Materialien und gespeicherte Luft werden verglichen. Ein vorläufiger Lauf fand Gras auf einer Moosfläche innerhalb der freigehaltenen Eingangsbreite. Die Grenze zwischen äußerer Moosdekoration und innerem Pflaster wurde korrigiert. Der Luftvergleich wurde nicht gelockert.

Die konkreten Artefaktprüfsummen, Laufkennungen, Ergebnisse und Blockzahlen stehen in [testing/alpha2-evidence.json](testing/alpha2-evidence.json). Der [Alpha-1-Bericht](ALPHA_TEST_REPORT.md) bleibt als historischer Nachweis erhalten.

Alle 18 Tests und die drei abschließenden Serverläufe haben bestanden. Alle Server wurden mit Exit-Code 0 beendet. Basis und Integration bestätigen jeweils 4.737 Obelisk-Zellen und 82.672 Koloss-Zellen ohne Abweichungen oder fehlende Chunks. Im Einstellungstest entsteht der Obelisk vollständig; die Suche nach dem deaktivierten Koloss liefert keinen Fund. Der allgemeine Teilwert `world_blocks.passed` erwartet beide Typen und ist dort deshalb falsch. Der Gesamtwert des Server-Harness berücksichtigt die bewusst deaktivierte Struktur.

Die getestete und im Profil installierte JAR hat SHA-256 `cc978cdb382ec5f7ad82cfcaddb1dbdc30d27fd3e3e56949729911e347c27dfa`. Ein vollständiger Wiederholungs-Build erzeugte dieselbe Prüfsumme.

## Update und Grenzen

Die Struktur-IDs, Dimensionen und Standortregeln bleiben gleich. Die neue Version verändert keine schon gespeicherten Bauwerke. Nach dem Austausch der JAR Minecraft vollständig neu starten und eine neue Testwelt oder bislang nicht erzeugte Regionen verwenden. `/locate` kann in einer bestehenden Welt weiterhin einen alten Standort finden.

Die Bodenform bleibt eine feste Vorlage. Erdstützen und kurze Ränder verbessern den Übergang, können aber nicht jeden Hang, Wasserlauf oder fremden Bau überschneidungsfrei berücksichtigen. Weitere Seeds, menschliche Sichtprüfung, Shader/LOD und belastbare Leistungsmessungen gehören zur weiteren Abnahme.

Der bekannte Windows-Perflib-Diagnosefehler wird weiterhin separat in den Logs ausgewiesen. Er wurde nicht durch Änderungen am Betriebssystem unterdrückt. Build, 18 Tests und Wiederholungs-Build werden zusätzlich in GitHub Actions unter Linux geprüft. Die CI lädt keine zusätzlichen Actions-Artefakte hoch; Downloads werden als GitHub-Release bereitgestellt.
