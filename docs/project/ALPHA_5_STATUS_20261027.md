# Alpha 5.0: Entwicklungsstand vom 27. Oktober 2026

Der aktuelle Stand ist `0.1.0-alpha.5.0-dev` für Minecraft 26.2 / Fabric.
Die freigegebenen Innenräume und ihre natürliche Gameplay-Initialisierung sind
integriert. Die jüngsten Korrekturen aus Niklas' Spieltest sind implementiert
und auf isolierten Servern geprüft. Die abschließende Abnahme im grafischen
Client steht für diesen letzten Build noch aus. Alpha 5.0 ist damit weiterhin
ein Entwicklungsstand, kein abschließend freigegebener Release.

## Implementiert

- Neue Welten verwenden die gemeinsame Seltenheits- und Abstandsplanung sowie
  einen gespeicherten weltweiten Standort des großen Kolosses. Expeditionskarten
  und Reliktsuche verwenden dieselben gültigen Ziele. Die asynchrone Suche nach
  wiederholbaren Relikten reicht nun 500.000 Blöcke weit.
- Großer Koloss V6, Kleiner Koloss V9, Turmruine V9 und Obelisk V6 sind nach der
  Sichtprüfung freigegeben. Der freigegebene Weltenbaum V5 bleibt erhalten.
  NBT, Schematic, Blender-Quellen, Reviewbilder und gebundene Marker liegen im
  [Handoff](reviews/gameplay-interiors-feedback-20261027-handoff.json).
- Neue Gameplay-Welten initialisieren die markierten Truhen, Fundstellen,
  Turmbegegnungen, Koloss-Prüfung, Vault und Baum-Aura. Abgeschlossene Aktionen
  werden nach einem normalen Neustart nicht erneut ausgeführt.
- Trial Spawner und Vault durchlaufen ihre nativen Zustände mit Ereignissen
  und Geräuschen. Schlüssel und Kern erscheinen als echte Weltgegenstände an
  der jeweiligen Quelle. Die persönlichen Belohnungen sind gegen Aufnahme durch
  andere Spieler, Hopper und Zusammenführen geschützt.
- Der Vault verbraucht beim erfolgreichen Benutzen sofort einen Schlüssel.
  Der Kern wird danach separat ausgeworfen. Seine spätere Aufnahme verlangt
  keinen weiteren Schlüssel. Bezahlte wartende Ansprüche bleiben gespeichert.
- Der Maschinenkern unterstützt die vorgesehenen Verarbeitungen mit 256
  Operationen. Er stammt aus dem Vault. Das Rezept lädt einen leeren Kern auf;
  es stellt keinen neuen Kern her. Wartungsrezepte haben Buchanzeigen und werden
  beim Mitführen des zugehörigen Gegenstands freigeschaltet.
- Der geladene Magnet funktioniert in der ausgewählten Haupthand oder in der
  Nebenhand in Survival/Adventure. Andere Inventarplätze bleiben inaktiv.
  Beschleunigung und Höchstgeschwindigkeit sind um zehn Prozent erhöht.
  Nur erfolgreiche Aufnahmen belasten den aktiven Magneten.

Bestehende Welten behalten ihre gespeicherte Verteilung und Innenraum-Auswahl.
Es gibt keine automatische nachträgliche Befüllung alter Relikte. Beide
Titanschädel und die bisherigen Exporte bleiben erhalten. Dieser Entwicklungsstand
enthält keine Gameplay-Portierung für 1.21.1 oder NeoForge.

## Nachweise

Die folgenden Berichte enthalten die jeweiligen Testumfänge und Grenzen.
Ältere Berichte beschreiben Zwischenstände; für Schlüssel, Magnet und Suche
gilt der letzte Bericht.

- [Modellfreigabe und Entscheidungen](INTERIOR_DECISIONS_20261027.md)
- [Modellrevisionen und unabhängige Exportprüfung](GAMEPLAY_INTERIORS_FEEDBACK_20261027_IMPLEMENTATION.md)
- [Natürliche Integration, Rotation, Loot und Neustart](../testing/NATURAL_INTERIORS_20261027.md)
- [Spawner-/Vault-Präsentation und Rezeptbuch](../testing/GAMEPLAY_PRESENTATION_20261027.md)
- [Echte persönliche Belohnungsauswürfe](../testing/REWARD_DROPS_20261027.md)
- [Sofortiger Schlüsselverbrauch, beide Magnethände und erweiterte Suche](../testing/HAND_VAULT_LOCATE_20261027.md)
- [Maschinenlesbarer Nachweis des letzten Builds](../testing/hand-vault-locate-20261027-evidence.json)

Der letzte Build besteht 663 Gameplay-Assertions, 52 statische Mixin-Verträge,
1.008 Executor-Prüfungen, 755.716 Suchprüfungen, 198.924 synthetische
Verteilungsprüfungen und sechs Ressourcentests. Isolierte native Serverläufe mit
zwei Survival-Testspielern prüfen Belohnungen, sofortige Zahlung, beide Hände,
inaktive Inventarplätze und normale Speicher-/Neustartzyklen. Das sind keine
zwei grafischen Minecraft-Clients.

Die Suche wurde zusätzlich mit dem Seed der Testwelt geprüft. Alle fünf Ziele
stimmen mit einem ungefilterten Referenzlauf überein. Kleiner Koloss und
Weltenbaum wurden dort natürlich generiert; alle 477.336 geprüften festen
Modellzellen stimmen. Nutzerprofil und Nutzerwelt wurden dabei nur gelesen.
Die Koordinaten und vollständigen `/locate`-Befehle stehen im letzten Bericht.

Niklas hat im Spiel bereits Golemangriff, Schlüssel, Vault-Kern, Kernverarbeitung,
Magnet in Survival und die korrigierten Blockanimationen bestätigt. Seine danach
gemeldeten Probleme mit Schlüsselverbrauch, Magnethand und Suche sind im letzten
Build korrigiert. Für diese Korrekturen fehlt noch seine erneute Client-Abnahme.

## Vor der Release-Freigabe offen

- Letzten Build in der Minecraft-Testinstanz prüfen: Schlüssel verschwindet beim
  Vault-Klick, Kern landet zunächst in der Welt, Magnet sammelt in beiden Händen
  und bleibt in ungewählten Plätzen inaktiv.
- Vollständigen Survival-Durchlauf an natürlich generierten Relikten abschließen,
  einschließlich Loot, Obelisk-Archäologie, Turmbegegnungen, Karten und Baum-Aura.
  Innenraumlicht und Sichtbarkeit im tatsächlichen Client beurteilen.
- Zwei echte Clients zusammen testen, insbesondere persönliche Auswürfe,
  aufeinanderfolgende Vault-Nutzung, erneutes Verbinden und Serverneustart.
- Erhöhte natürliche Tier-Spawnversuche am Weltenbaum sind noch nicht
  implementiert. Vor der Freigabe umsetzen oder ausdrücklich verschieben.
- Suchdauer und Spielbarkeit im vorgesehenen Modpack prüfen. Seltene Typen können
  längere Hintergrundsuchen benötigen. Beliebige harte Prozessabbrüche sind keine
  nachgewiesene gemeinsame Transaktion über Spieler-, Entity- und Journaldateien.

## Artefakt und Veröffentlichung

Lokaler Testbuild: `dist/relics-0.1.0-alpha.5.0-dev+mc26.2.jar`.

SHA-256: `caffeb247121ee1ea501ecf68eaa1c2af07801420c7dbeb5cae636f9d041acfe`.

Zwei Builds sind bytegleich. Das Spieler-JAR enthält keine Server-Testklassen.
Der Git-Push umfasst Quellcode, freigegebene Exporte, Generatoren und Nachweise.
`dist/` bleibt ein lokaler Buildordner. Ein Release-Tag oder ein GitHub Release
mit Download-Artefakt wird durch diesen Dokumentations-Push nicht angelegt.
Die separat vorbereiteten lokalen NeoForge-Arbeiten bleiben außerhalb dieses
Alpha-5-Commits.

Der vorgesehene Git-Inhalt wurde separat exportiert und ohne die lokalen
NeoForge-Dateien vollständig neu gebaut. Seine JAR hat dieselbe obige Prüfsumme;
alle 35 im Handoff gebundenen Dateien stimmen auch im Git-Export bytegenau.
Die JSON-Dateien der vier neuen Modelle behalten deshalb über eng begrenzte
Git-Attribute ihre ursprünglichen Zeilenenden. Die Dokumentationslinks im
Export wurden ebenfalls geprüft.

Die vollständige Python-Suite auf diesem Export besteht mit 127 Tests.
Vor dem Push wurden außerdem die oben genannten Gameplay-/Verteilungstests
und die 755 Java-Prüfungen für Platzierung und Schutzmasken erneut erfolgreich
ausgeführt. Diese Abschlussprüfungen starten keine Nutzerwelt.

Die lokale Gesamttestsuite meldet einen Fehler ausschließlich beim separat
vorbereiteten NeoForge-Port. Dessen Versionsschutz verlangt weiterhin Alpha 4.9
und lehnt den aktuellen Alpha-5-Quellstand ab. Dieser Port bleibt lokal erhalten;
seine Freigabe oder Aktualisierung ist nicht Teil dieses Commits.
