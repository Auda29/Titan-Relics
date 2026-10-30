# Alpha 5.0: Stand zur Veröffentlichung am 28. Oktober 2026

> **Current status, October 30, 2026:** This page is the dated Alpha 5.0 release record; the current patch is 5.0.3, including both loaders and the confirmed Living World reopen fix. See the
> [Alpha 5.0.3 status and roadmap](CURRENT_STATUS_AND_ROADMAP.md). Approved design requirements
> remain specifications; dated pending/unimplemented claims below are historical
> where superseded by the released implementation and linked evidence.

Version: **0.1.0-alpha.5.0**, Minecraft 26.2 / Fabric. Der bisherige Dateiname
bleibt als stabiler Link bestehen. Der Release bündelt den am 27. und
28. Oktober umgesetzten und vom Nutzer geprüften Gameplay-Stand.

## Fertiggestellt

- Gemeinsame Seltenheits-/Abstandsplanung, ein weltweiter großer Koloss und
  Expeditionskarten zum selben gültigen Ziel. Asynchrone Suche bis 500.000 Blöcke
  bei wiederholbaren Relikten.
- Koloss-Prüfung, sofortiger Schlüsselverbrauch, native Vault-/Spawner-Zustände
  und persönliche physische Belohnungen. Der Kern verarbeitet 256 Operationen.
- Magnet in beiden ausgewählten Händen, zehn Prozent schneller und Verschleiß
  pro tatsächlich aufgenommenem Item. Wartungsrezepte sind im Rezeptbuch.
- Koloss V7, kleiner Koloss V11, Turm V10, Obelisk V6 und Weltenbaum V5 sind
  integriert. Truhenstände, kürzerer kleiner Zugang, bereinigter Skull-2-Seitenbereich
  und der Monolith-Besatz mit korrigierten Rüstungsflächen sind enthalten.
- Baum-Aura mit Regeneration II und Resistenz II im Radius von 80 Blöcken und
  fünf Minuten Nachwirkung. Leuchtbüsche folgen tatsächlichem Boden.
- Begrenzte zusätzliche natürliche Versuche für Schweine, Hühner, Schafe und
  Kühe nahe gespeicherten Baumankern. Normale Spawnprüfungen und globale/lokale
  Populationsgrenzen bleiben wirksam. Kein Spawner und keine Auffülluhr.
- Friedlich-Laden, gespeicherte Innenraumrevisionen und einmalige Initialisierung
  bleiben erhalten; alte Strukturen werden nicht verschoben oder nachgefüllt.

## Abnahmen und Nachweise

Niklas hat Modelle und Funktionen im Spiel geprüft und den letzten Skull-/Baumstand
mit "sieht alles gut aus" bestätigt. Er bestätigt außerdem **zwei echte Clients
samt erneutem Verbinden ohne Probleme**. Diese Nutzerabnahmen sind getrennt
von automatisierten Serverprüfungen dokumentiert.

- [Release-Notizen und Voraussetzungen](../releases/ALPHA_5_0.md)
- [Finale Release-Prüfung](../testing/ALPHA_5_RELEASE_20261028.md)
- [Skull-/Baumkorrektur](TREE_SKULL_FEEDBACK_20261028.md)
- [Ausgewählte Baum-Effekte](TREE_EFFECTS_II_20261028.md)
- [V4-Modellintegration](INTERIORS_V4_20261028.md)

## Bestehende Welten und Grenzen

Für die vollständige Alpha-5-Auswahl eine neue Welt verwenden. Bestehende Welten
behalten ihre Revision auch für weitere Chunks. Baum-Effekte gelten an bereits
registrierten Ankern ebenfalls mit den neuen Werten.

Langzeit-Survival-Abstimmung und allgemeine Kompatibilität mit beliebigen Modpacks
bleiben Alpha-Arbeit. Normale Speicher-/Neustartprüfungen beweisen keine beliebige
gemeinsame Transaktion bei harten Prozessabbrüchen. Der separate NeoForge-Port
bleibt außerhalb dieses Fabric-Releases.
