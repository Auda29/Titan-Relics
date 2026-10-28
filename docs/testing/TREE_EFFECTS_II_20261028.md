# Prüfung der beiden Baum-Effekte

Regeneration II und Resistenz II sind innerhalb der 80-Block-Aura implementiert
und in Relic Test installiert. Die vorherige JAR wurde hashgeprüft gesichert.
Das Profil war geschlossen; keine Originalwelt wurde geöffnet oder verändert.

- SHA256: `8b07064ecec2f5b9e443f568866278e8c4e88aa19cc3fbccef67d4b61d928342`
- [Maschinenlesbare Evidenz](tree-effects-ii-20261028-evidence.json)
- [Auswahl und Verhalten](../project/TREE_EFFECTS_II_20261028.md)

665 Gameplay-Assertions und 52 statische Mixin-Verträge bestanden. Die native
Serverprüfung testet beide Effekte an 51 Positionen und Spielmodusfällen und
wiederholt die Prüfung nach Neustart. Je Effekt werden die inklusive Grenze
bei 80 Blöcken, Ausschluss außerhalb der Kugel, Dimension, Creative/Spectator
und Adventure geprüft. Beide Effekte besitzen den nativen Verstärkerwert 1,
also Stufe II, und eine Dauer von 6.000 Ticks.

Zusätzliche native Fälle bestätigen: Eine bestehende stärkere Stufe III oder
eine längere Stufe II wird nicht abgeschwächt oder verkürzt. Beim Verlassen der
Aura bleiben beide fünfminütigen Effekte erhalten. Trial-/Vault-Zustände und
Belohnungen, Schlüsselverbrauch, Magnet und Neustartansprüche bestehen ebenfalls.

Der Vergleich zum vorherigen JAR zeigt ausschließlich eine Änderung an
`RelicGameplay.class`. Sämtliche Ressourcen, Modelle, Templates, Weltmanifeste
und übrigen Klassen bleiben identisch. Das Packaging mit den geprüften Klassen
ist bytegleich reproduzierbar. Die vollständige zuletzt bestandene Testsuite
mit 156 Tests wurde für diese begrenzte Runtime-Änderung nicht erneut ausgeführt.

Die Änderung greift auch an registrierten Bäumen bestehender Welten. Eine neue
Welt ist nicht nötig. Kein Commit, Push oder Release in diesem Arbeitsschritt.
