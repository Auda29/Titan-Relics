"""Finish the review handoff without touching baseline or integration files."""
import json,hashlib,zipfile
from pathlib import Path
from build_skull_side_revision import ROOT,OUT,STEM,SOURCE,sha,dump
from PIL import Image,ImageDraw
base=ROOT/'build/tree-skull-feedback-20261028/baseline.json';baseline=json.loads(base.read_text())
changed=[];missing=[];unchanged=[]
for rel,expected in baseline.items():
 p=ROOT/rel
 if not p.exists():missing.append(rel)
 elif sha(p)!=expected:changed.append({'path':rel,'baseline_sha256':expected,'current_sha256':sha(p)})
 else:unchanged.append(rel)
dump(OUT/'preservation.json',{'baseline':str(base.relative_to(ROOT)),'baseline_sha256':sha(base),'baseline_files':len(baseline),'unchanged_count':len(unchanged),'unchanged_paths':unchanged,'concurrent_root_changes_observed_not_written_by_this_worker':changed,'missing':missing,'worker_existing_files_modified':[],'note':'Snapshot at handoff; Root may continue authorized TerrainSupportProcessor/TreeAura/tests/docs/integration edits.'})
for name in ['skull_side_tests.log','skull_side_verify.log','skull_side_origin.log']:
 (OUT/name).write_bytes((ROOT/'build'/name).read_bytes())
a=Image.open(OUT/'before.png').convert('RGB');b=Image.open(OUT/'after.png').convert('RGB')
sheet=Image.new('RGB',(a.width*2,a.height+60),'#202020');sheet.paste(a,(0,60));sheet.paste(b,(a.width,60));d=ImageDraw.Draw(sheet);d.text((25,20),'BEFORE - exported baseline NBT',fill='white');d.text((a.width+25,20),'AFTER - exactly 147 dripstone cells removed',fill='white');sheet.save(OUT/'before-after.png')
h=json.loads((OUT/'handoff.json').read_text());h['editable_source']=(OUT/(STEM+'-source.blend')).relative_to(ROOT).as_posix();h['editable_source_sha256']=sha(ROOT/h['editable_source']);h['source_verification_sha256']=sha(OUT/'source-verification.json');h['original_source_binding_sha256']=sha(OUT/'original-source-binding.json');h['tests']={'run':'python -m unittest discover -s tests -p test_skull_side_revision.py -v','passed':5,'log_sha256':sha(OUT/'skull_side_tests.log')}
h['screenshot']={'path':'C:/Users/wecke/.t3/userdata/attachments/3b16f7b5-d783-4edd-85e9-c9f42e834457-7627a8b9-3bd3-4838-9eab-278aa43d0015.png','sha256':sha(Path('C:/Users/wecke/.t3/userdata/attachments/3b16f7b5-d783-4edd-85e9-c9f42e834457-7627a8b9-3bd3-4838-9eab-278aa43d0015.png'))}
h['hash_manifest']='hashes.json';dump(OUT/'handoff.json',h)
report=f'''# Titan Skull 2: separaten Seitenbrocken entfernt

Neue additive Revision `{STEM}`. Auswahl durch Screenshot und NBT-Rendervergleich: Der isolierte Brocken liegt links der gestuften Calcite-Kieferkante unter dem breiten ueberhaengenden Zahn. Die Quellposition `(40, 1, -36)` passt zu dieser Ansicht. Die Kandidaten `(-43, 2, -12)` und `(20, 0.5, 48)` bleiben unveraendert. Die originale V2-Blenderdatei wurde separat lesend geoeffnet; `original-source-binding.json` bindet Objekt, Material, Quellkoordinaten und Exportgrenzen.

Entfernt: exakt 147 `minecraft:dripstone_block`, NBT-Grenzen inklusive `(85,21,3)` bis `(92,25,12)`. `handoff.json` enthaelt jede entfernte Koordinate und ihren Zustand. Ein leerer Ring von einer Zelle um diesen Bereich schliesst angeschnittene angrenzende Anatomie aus. Keine globale Material- oder Komponentenloeschung.

32.569 -> 32.422 Bloecke. Jeder verbleibende Blockeintrag wurde in Reihenfolge, Koordinaten und Zustand verglichen; seine originalen NBT-Recordbytes sind unveraendert. Der zusammenhaengende Record-Bytestrom wurde in den dekomprimierten NBT-Dateien nachgewiesen. Alle anderen Root-Tags inklusive Palette, Entities, DataVersion und Groesse sind gleich. Dies beweist auch den Erhalt von Wurzeln, Schwert, restlicher Anatomie und allen anderen Truemmern.

NBT SHA256: `{h['sha256']}`. Groesse `[99,136,99]`, Schematic-Offset `[0,0,0]`, ground_y `28`, buried_clip_depth `6`. Alle vier Minecraft-Drehungen erhalten vollstaendige Template-Grenzen und ihre Drehungs-Offsets; Modellpfad und SHA stehen pro Drehung im Handoff. Es wurde kein Runtime-Pfad umgestellt.

NBT, Sponge-Schematic und 33 Tiles sind zellgleich. Editierbare Blenderquelle: versteckte Collection mit je Material editierbaren Voxelpunkt-Meshes, dazu texturierte Oberflaechen. Voxelpunkt-Koordinaten sind autoritativ; `recovered_voxels()` im Renderer liest sie zurueck. Frisches Wiederoeffnen hat alle 32.422 Zellen gegen NBT geprueft. Ein unabhaengiger Oberflaechen-Neuaufbau aus erneut gelesenem NBT stimmt bei Vertices, Faces und UVs ueberein.

`before-after.png`, `before.png`, `after.png`: gleiche screenshot-aehnliche Kamera, neutrales Tageslicht, tatsaechlich exportierte Voxel. Der Fluss und das Weltterrain wurden nicht nachgebaut. Die Perspektive ist angenaehert, nicht aus Weltkoordinaten rekonstruiert. Kandidatenansichten dokumentieren den Vergleich beider Seiten.

Fuenf Regressionstests bestanden: exakter Zellunterschied, erhaltene Recordbytes/Metadaten, Schematic/Tiles, vier Drehungen, aktuelle Blender-/NBT-Hashbindung. Logs liegen hier. `hashes.json` bindet saemtliche Revisionsartefakte sowie eigene Tools/Tests; der Hashmanifest selbst ist ausgenommen, um Selbstreferenz zu vermeiden.

Preservation zum Handoff: {len(unchanged)} von {len(baseline)} Baseline-Dateien bytegleich, {len(changed)} separat ausgewiesene parallele Aenderungen, {len(missing)} fehlend. Dieser Worker hat keine Baseline-Datei geschrieben. `preservation.json` fuehrt alle unveraenderten Pfade und die beobachteten Root-Aenderungen mit Vorher-/Nachherhashes auf. Root kann danach weiterarbeiten.

Belegt sind Modellkorrektur und Artefaktkonsistenz. Natuerliche Generierung, TerrainSupportProcessor, TreeAura, Platzierung in einer echten Welt und Runtime bleiben offen. Keine Originalwelt oder Modrinth-Instanz geoeffnet; keine Integration, kein Commit, kein Push.
'''
(OUT/'MODEL_REPORT.md').write_text(report,encoding='utf-8')
files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='hashes.json')
files+=sorted(ROOT.glob('tools/*skull_side*.py'))+sorted(ROOT.glob('tests/*skull_side*.py'))
dump(OUT/'hashes.json',{p.relative_to(ROOT).as_posix():sha(p) for p in files})
print(json.dumps({'baseline':len(baseline),'unchanged':len(unchanged),'changed':changed,'missing':missing,'hashed_files':len(files)}))
