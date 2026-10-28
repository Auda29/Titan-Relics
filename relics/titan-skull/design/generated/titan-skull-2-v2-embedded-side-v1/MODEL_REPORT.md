# Titan Skull 2: separaten Seitenbrocken entfernt

Neue additive Revision `titan-skull-2-v2-embedded-side-v1`. Auswahl durch Screenshot und NBT-Rendervergleich: Der isolierte Brocken liegt links der gestuften Calcite-Kieferkante unter dem breiten ueberhaengenden Zahn. Die Quellposition `(40, 1, -36)` passt zu dieser Ansicht. Die Kandidaten `(-43, 2, -12)` und `(20, 0.5, 48)` bleiben unveraendert. Die originale V2-Blenderdatei wurde separat lesend geoeffnet; `original-source-binding.json` bindet Objekt, Material, Quellkoordinaten und Exportgrenzen.

Entfernt: exakt 147 `minecraft:dripstone_block`, NBT-Grenzen inklusive `(85,21,3)` bis `(92,25,12)`. `handoff.json` enthaelt jede entfernte Koordinate und ihren Zustand. Ein leerer Ring von einer Zelle um diesen Bereich schliesst angeschnittene angrenzende Anatomie aus. Keine globale Material- oder Komponentenloeschung.

32.569 -> 32.422 Bloecke. Jeder verbleibende Blockeintrag wurde in Reihenfolge, Koordinaten und Zustand verglichen; seine originalen NBT-Recordbytes sind unveraendert. Der zusammenhaengende Record-Bytestrom wurde in den dekomprimierten NBT-Dateien nachgewiesen. Alle anderen Root-Tags inklusive Palette, Entities, DataVersion und Groesse sind gleich. Dies beweist auch den Erhalt von Wurzeln, Schwert, restlicher Anatomie und allen anderen Truemmern.

NBT SHA256: `0a8e66aebb437b9062f3bbcc87c84d38735fa361fbc8f179f99473a5185a4c80`. Groesse `[99,136,99]`, Schematic-Offset `[0,0,0]`, ground_y `28`, buried_clip_depth `6`. Alle vier Minecraft-Drehungen erhalten vollstaendige Template-Grenzen und ihre Drehungs-Offsets; Modellpfad und SHA stehen pro Drehung im Handoff. Es wurde kein Runtime-Pfad umgestellt.

NBT, Sponge-Schematic und 33 Tiles sind zellgleich. Editierbare Blenderquelle: versteckte Collection mit je Material editierbaren Voxelpunkt-Meshes, dazu texturierte Oberflaechen. Voxelpunkt-Koordinaten sind autoritativ; `recovered_voxels()` im Renderer liest sie zurueck. Frisches Wiederoeffnen hat alle 32.422 Zellen gegen NBT geprueft. Ein unabhaengiger Oberflaechen-Neuaufbau aus erneut gelesenem NBT stimmt bei Vertices, Faces und UVs ueberein.

`before-after.png`, `before.png`, `after.png`: gleiche screenshot-aehnliche Kamera, neutrales Tageslicht, tatsaechlich exportierte Voxel. Der Fluss und das Weltterrain wurden nicht nachgebaut. Die Perspektive ist angenaehert, nicht aus Weltkoordinaten rekonstruiert. Kandidatenansichten dokumentieren den Vergleich beider Seiten.

Fuenf Regressionstests bestanden: exakter Zellunterschied, erhaltene Recordbytes/Metadaten, Schematic/Tiles, vier Drehungen, aktuelle Blender-/NBT-Hashbindung. Logs liegen hier. `hashes.json` bindet saemtliche Revisionsartefakte sowie eigene Tools/Tests; der Hashmanifest selbst ist ausgenommen, um Selbstreferenz zu vermeiden.

Preservation zum Handoff: 1499 von 1509 Baseline-Dateien bytegleich, 10 separat ausgewiesene parallele Aenderungen, 0 fehlend. Dieser Worker hat keine Baseline-Datei geschrieben. `preservation.json` fuehrt alle unveraenderten Pfade und die beobachteten Root-Aenderungen mit Vorher-/Nachherhashes auf. Root kann danach weiterarbeiten.

Belegt sind Modellkorrektur und Artefaktkonsistenz. Natuerliche Generierung, TerrainSupportProcessor, TreeAura, Platzierung in einer echten Welt und Runtime bleiben offen. Keine Originalwelt oder Modrinth-Instanz geoeffnet; keine Integration, kein Commit, kein Push.
