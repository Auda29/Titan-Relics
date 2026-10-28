"""Create labelled review images and a separate hash-bound V7 handoff."""
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
from build_colossus_landmarks import ROOT,OUT,OLD,STEM

font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
reviews=[('01-overview.png','overview-review.png','KOLOSS V7 | GESAMTANSICHT','Exportierte Geometrie; Prueftageslicht. Keine Runtime-Darstellung.'),
 ('02-arm-find.png','arm-review.png','ARMFUND | KUPFERBLOCK ALS TRUHEN-PLATZHALTER','Ausschnitt der exportierten Geometrie; darueber freier Deckelraum, Prueftageslicht.'),
 ('03-guard.png','guard-review.png','WACHSTRUKTUR | MITTIGER SPAWNER-PLATZHALTER','Ausschnitt von oben; dunkler Block in der Mitte = Trial-Spawner-Platzhalter.'),
 ('04-vault-console.png','vault-review.png','MITTLERE CREWSTATION | VAULT-KONSOLE','Ausschnitt; dunkler Block zwischen den Pfeilern = Vault-Platzhalter. Prueftageslicht.')]
for source,target,title,sub in reviews:
    raw=Image.open(OUT/source).convert('RGB'); canvas=Image.new('RGB',(raw.width,raw.height+112),'#182029')
    canvas.paste(raw,(0,112));d=ImageDraw.Draw(canvas);d.text((26,13),title,font=font(32),fill='white');d.text((27,64),sub,font=font(20),fill='#cedbe6');canvas.save(OUT/target,optimize=True)

def record(p):
    raw=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
original=json.loads((ROOT/'docs/project/reviews/gameplay-interiors-feedback-20261027-handoff.json').read_text())
index=json.loads(json.dumps(original));index['status']='Colossus V7 model handoff; visual review and runtime integration pending'
side=json.loads((OUT/(STEM+'.gameplay.json')).read_text());report=json.loads((OUT/'verification.json').read_text())
assert report['nbt_sha256']==side['source_sha256']
files={}
for suffix in ('.nbt','.schem','.gameplay.json','.design.json','.groups.json','.manifest.json','-source.blend'):
    files[suffix]=record(OUT/(STEM+suffix))
for p in sorted(OUT.glob('*.png')):files[p.name]=record(p)
for name in ('verification.json','source-verification.json'):files[name]=record(OUT/name)
tiles={p.name:record(p) for p in sorted((OUT/(STEM+'_tiles')).glob('*.nbt'))}
assert len(tiles)==report['tiles']
index['assets']['colossus']={'files':files,'tiles':tiles,'size':side['size'],'ground_y':side['ground_y'],
    'blocks':report['blocks'],'markers':report['markers'],'regions':report['regions'],
    'marker_coordinates':{m['role']:{k:m[k] for k in ('pos','facing','expected_block') if k in m} for m in side['markers']}}
for key in original['assets']:
    if key!='colossus':assert index['assets'][key]==original['assets'][key]
out=ROOT/'docs/project/reviews/colossus-landmarks-20261028-handoff.json'
out.write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Handoff:',out,'tiles',len(tiles),'files',len(files))
