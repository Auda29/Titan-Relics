"""Finalize only Tower V10 artifacts and its independent five-asset handoff."""
import ast,copy,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_tower_chest import ROOT,OUT,OLD,STEM,V9

def record(p):
    raw=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
for source,target,title,sub in [
 ('01-overview.png','overview-review.png','RUINED TOWER V10 | GESAMTANSICHT','Vollstaendige NBT-Geometrie. Blender-Prueftageslicht, kein Minecraft-Blocklicht.'),
 ('02-entry.png','entry-review.png','VOM NORD-EINGANG ZUR MITTIGEN RUECKWANDTRUHE','Volle Exportgeometrie. Kamera im Eingang; kuenstliches Prueflicht. Kupfer = Platzhalter.'),
 ('03-close.png','close-review.png','ZUGANG ZUR TRUHE | BLICK NACH SUEDEN','Volle Exportgeometrie. Freier Zugang von Norden. Kuenstliches Blender-Prueflicht.'),
 ('04-hall.png','hall-review.png','EINGANG VORN | FUNDSTAND AN DER GEGENUEBERLIEGENDEN WAND','NBT-Schnitt X36..82 / Y11..24 / Z16..63. Prueftageslicht; Export bleibt vollstaendig.'),
 ('05-stand.png','stand-review.png','KLEINER RUINENSTAND | DECKEL UND VORDERSEITE FREI','NBT-Ausschnitt X55..61 / Y14..22 / Z54..58. Kupfer = Platzhalter. Prueftageslicht.')]:
    raw=Image.open(OUT/source).convert('RGB');canvas=Image.new('RGB',(raw.width,raw.height+112),'#182029');canvas.paste(raw,(0,112))
    d=ImageDraw.Draw(canvas);d.text((26,13),title,font=font(29),fill='white');d.text((26,64),sub,font=font(19),fill='#cedbe6');canvas.save(OUT/target,optimize=True)
baseline=json.loads((ROOT/'build/tower-chest-20261028/baseline.json').read_text(encoding='utf-8-sig'))
changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or record(ROOT/p)['sha256']!=h]
authorized={'tools/generate_gameplay_art.py','src/main/resources/assets/relics/textures/trims/entity/humanoid/monolith.png','src/main/resources/assets/relics/textures/trims/entity/humanoid_leggings/monolith.png','src/test/java/de/relics/GameplayPresentationChecks.java'}
unexpected=[p for p in changed if p not in authorized]
write(OUT/'preservation.json',{'baseline':'build/tower-chest-20261028/baseline.json','verified_files':len(baseline),'changed_files':changed,'authorized_root_trim_changes':sorted(authorized),'unclassified_external_changes':unexpected,'worker_modified_baseline_files':[]})
assert not unexpected,unexpected
side=json.loads((OUT/(STEM+'.gameplay.json')).read_text());verification=json.loads((OUT/'verification.json').read_text());blend=json.loads((OUT/'source-verification.json').read_text())
assert side['source_sha256']==verification['nbt_sha256']==blend['bound_nbt_sha256']
assert record(OUT/(STEM+'-source.blend'))['sha256']==blend['source_blend_sha256']
report=ROOT/'docs/project/TOWER_CHEST_20261028.md'
report.write_text('''# Ruined Tower V10, Modellhandoff vom 28.10.2026

Modellauftrag, noch nicht runtime-integriert; neue Turmform nicht vom Nutzer abgenommen.

## Lage und Gestaltung

Basis ist das hashgepruefte V9-NBT, SHA256 `4f5fd420eb1461b8e1b3f1c9f8f90ede3e801ea8d1e20972aab3d78d9a9fad8d`. V9-Reviewbilder und die tatsaechlichen Blocklagen wurden vor dem Bau angesehen. Masse 111 x 232 x 93, Ground-Y 12, DataVersion 3105 und Aussenform bleiben erhalten.

Die einzige Truhe steht jetzt bei **[58,15,55], facing north**. Marker-ID `tower-ender-chest-1`, Rolle `tower_ender_chest` und Platzhalter `minecraft:waxed_cut_copper` bleiben stabil. Die historische Rolle bezeichnet weiterhin eine normale native waxed_copper_chest, keine Endertruhe.

Der Eingang liegt auf der Nordseite bei [57,15,20]. Die hintere Hallenbegrenzung liegt bei Z58. Die Innenbreite X41..76 ergibt die mittleren Blockspalten X58/59. X58 liegt damit mittig und nur einen Block neben der Eingangsachse. Der Stand sitzt unmittelbar vor der gegenueberliegenden Wand: Ruecken auf Z56/57, Truhe davor auf Z55. Er liegt weder an der Eingangswand noch an einer Seitenwand.

Der kleine Aufbau besteht aus einem abgestuften Ruecken aus rissigen Tiefenschieferfliesen und poliertem Tiefenschiefer sowie Basaltpfeilern auf X56 und X60. Die Pfeiler enden unterschiedlich bei Y19 und Y18. Die Truhe steht auf dem erhaltenen Hallenboden Y14. Der Zugang X57..59/Z52..54 bleibt frei, ebenso die Zellen direkt ueber der Truhe Y16..21. Es gibt keinen Querbalken ueber dem Deckel, keine neue Kammer, Lichtquelle oder Mechanik.

46 Bloecke wurden hinzugefuegt, ausschliesslich X56..60/Y15..19/Z55..57. Genau ein Block wurde entfernt: der alte Truhenplatzhalter [72,15,55]. Keine Remaps. Sein Boden [72,14,55] bleibt erhalten. Saemtliche anderen V9-Zellen, die Hallentrennwaende, Truemmer, Pfeiler, die fuenf Enderman-Marker und der gesamte Wandaufstieg bleiben identisch. Auch die fuenf absichtlichen Treppenluecken bleiben erhalten.

## Terrain und Wege

Alle 322 bisherigen Regionen bleiben unveraendert. Hinzu kommt `tower-route-clearance-323`, Rolle `tower_route_clearance`, von [56,15,52] bis [60,21,57]. Sie umfasst Bedienplatz, Stand und Deckelfreiraum. Runtime muss vor jedem Raeumen ALLE im NBT belegten Zellen von diesen Regionen abziehen. Das schuetzt besonders den Ruecken und die vorhandene Trennwand auf X56. Die alte begrenzte Block-Allow-List bleibt erhalten; Root uebernimmt die Erz-Erweiterung.

Der neue dokumentierte Weg fuehrt vom Eingang auf X57 nach Z48, wechselt auf X58 und endet auf [58,15,54] vor der Truhe. Er besitzt durchgehend Boden und drei freie Zellen Hoehe. Die Wegsuche bestaetigt ausserdem den Anschluss vom Eingang zum Start des Wandaufstiegs [41,15,29]. Sie ist eine Voxelpruefung, kein Minecraft-Physiktest.

## Pruefungen und Bestandserhaltung

Vier Tests in `tests/test_tower_chest.py` bestehen. Der bestehende Handoff-Validator besteht neun Pruefgruppen. NBT und Schematic wurden unabhaengig gelesen und stimmen Block fuer Block ueberein. 69 Kacheln rekonstruieren den Export verlustfrei. Die Blockstates bestehen beide vorhandenen 26.2-Registryreports. Ergebnis: 271042 Bloecke, acht Marker, 323 Regionen.

Die Tests begrenzen alle Aenderungen auf den Stand und alten Platzhalter, vergleichen die uebrigen Marker und Regionen mit V9 und erhalten die gesamte Geometrie ab Y20 exakt. Die fuenf Spawnpositionen haben weiterhin jeweils identischen 3x3-Boden und vier Zellen freien Raum. Vier rechnerische Rotationen pruefen Spawn-/Deckel-/Bedienfreiraum, erhaltene Boeden, die Trennung von Quellsolids und Raeumzellen sowie die Truhenrichtung north/east/south/west.

Blender 5.2.2 hat die editierbare Quelle im Hintergrund erzeugt und in einem frischen Prozess erneut geoeffnet. Geprueft wurden NBT-Hashbindung, 21 Blockstate-Meshes, acht Marker-Empties samt Koordinaten und 72 Flaechen des neuen Stands gegen die exportierten Voxel. Die gespeicherte Quelle enthaelt die vollstaendige Geometrie; Renderausschnitte aendern weder NBT noch Blender-Quelle. Alle fuenf Ansichten wurden vom Worker visuell angesehen.

Der Abschluss vergleicht alle 1339 Bestandsdateien mit `build/tower-chest-20261028/baseline.json`; konkrete Ergebnisse stehen in `preservation.json`. Angekundigte externe Root-Aenderungen an Monolith-Trim und Ressourcentests werden separat ausgewiesen. Dieser Worker hat keine Baseline-Datei, Koloss-Ausgabe, Java-/Runtime-Datei, Ressource, Welt oder Profil geaendert. Kein Commit, Push, Checkout, Reset, Clean oder Worktree.

Loot und Begegnung bleiben unveraendert: eine normale Truhe, 5 Prozent ein Enderauge, sonst 4 bis 6 Enderperlen; fuenf normale Endermen ausser auf Friedlich. Keine Schwierigkeitseinstellungen wurden angefasst.

## Artefakte und Bilder

Ordner: `relics/ruined-tower/design/generated/ruined-tower-v10-chest/`. Hauptdateien tragen den Stamm `ruined-tower-v10-chest`: `.nbt`, `.schem`, `.gameplay.json`, `.design.json`, `.groups.json`, `.manifest.json` und `-source.blend`. Kacheln liegen in `ruined-tower-v10-chest_tiles/`.

![Eingangsrichtung und Rueckwand](../../relics/ruined-tower/design/generated/ruined-tower-v10-chest/entry-review.png)

![Hallenkontext](../../relics/ruined-tower/design/generated/ruined-tower-v10-chest/hall-review.png)

![Stand und freier Deckelraum](../../relics/ruined-tower/design/generated/ruined-tower-v10-chest/stand-review.png)

![Nahsicht mit voller Geometrie](../../relics/ruined-tower/design/generated/ruined-tower-v10-chest/close-review.png)

![Aussenansicht](../../relics/ruined-tower/design/generated/ruined-tower-v10-chest/overview-review.png)

Eingangs- und Nahsicht verwenden volle Exportgeometrie und kuenstliches Blender-Prueflicht. Hallenschnitt X36..82/Y11..24/Z16..63 und Standdetail X55..61/Y14..22/Z54..58 sind ausdruecklich reine Bildausschnitte. Der sichtbare Kupferblock ist der Platzhalter, keine animierte Truhe. Kein Bild belegt Minecraft-Blocklicht.

Werkzeuge: `tools/build_tower_chest.py`, `tools/render_tower_chest.py`, `tools/finalize_tower_chest.py`. Renderer separat mit `-- --verify` wiedereroeffnen und mit `-- --detail-only` Standdetail erzeugen. Tests: `build/distribution-venv/Scripts/python.exe -m unittest discover -s tests -p test_tower_chest.py -v`.

Der neue vollstaendige Index `docs/project/reviews/tower-chest-20261028-handoff.json` leitet sich vom vorliegenden `small-colossus-landmarks-20261028-handoff.json` ab und ersetzt ausschliesslich `assets.ruined_tower`. Die vier anderen Eintraege bleiben identisch, insbesondere Small Colossus V10. Die parallele V11 wurde weder gelesen noch uebernommen. SHA256 und Bytegroessen aller Tower-Artefakte, Tools, Tests und dieses Berichts stehen im Index.

Root uebernimmt die gemeinsame Runtime-Integration mit Small Colossus V11, Natur-/Rotation-/Neustarttests, native Deckelanimation, Spielerbuild und Nutzerabnahme. Gespeicherte V9-Revisionen muessen erhalten bleiben.
'''+'\nNBT SHA256: `'+side['source_sha256']+'`.\n\nBlender SHA256: `'+blend['source_blend_sha256']+'`.\n',encoding='utf-8',newline='\n')
# Normalize only new tower JSON files before binding them.
for p in OUT.glob('*.json'):write(p,json.loads(p.read_text()))
original=json.loads((ROOT/'docs/project/reviews/small-colossus-landmarks-20261028-handoff.json').read_text());index=copy.deepcopy(original)
files={p.name:record(p) for p in sorted(OUT.iterdir()) if p.is_file()}
for name in ('tools/build_tower_chest.py','tools/render_tower_chest.py','tools/finalize_tower_chest.py','tests/test_tower_chest.py'):
    p=ROOT/name;ast.parse(p.read_text(encoding='utf-8'));files[name]=record(p)
files[report.name]=record(report)
tiles={p.name:record(p) for p in sorted((OUT/(STEM+'_tiles')).glob('*.nbt'))}
assert len([r for r in files.values() if r['path'].endswith('.nbt')])==1
assert len([r for r in files.values() if r['path'].endswith('.gameplay.json')])==1
index['assets']['ruined_tower']={'files':files,'tiles':tiles,'size':side['size'],'ground_y':12,'blocks':verification['blocks'],'markers':8,'regions':323}
for k in original['assets']:
    if k!='ruined_tower':assert original['assets'][k]==index['assets'][k]
write(ROOT/'docs/project/reviews/tower-chest-20261028-handoff.json',index)
print('Tower handoff:',len(files),'files,',len(tiles),'tiles. Baseline changed:',changed)
