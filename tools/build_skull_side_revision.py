"""Additive removal of the visually identified right/front chip only."""
import gzip,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_ots_result import read_structure
from colossus_materials import encode_schematic
from schem_to_nbt import convert,read_schematic
from relic_assets import nbt_payload
from verify_world import rotate
ROOT=Path(__file__).resolve().parents[1]
OLD='titan-skull-2-v2-embedded-v1'
STEM='titan-skull-2-v2-embedded-side-v1'
SOURCE=ROOT/f'relics/titan-skull/design/generated/{OLD}/{OLD}.nbt'
OUT=SOURCE.parent.parent/STEM
PIN='80d4cb89afd047eca45b54b53c95cd32d130b54dec834e6664e3fe3786a86dcd'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def chosen(p):return 85<=p[0]<=92 and 21<=p[1]<=25 and 3<=p[2]<=12

def record(e):return nbt_payload(10,{'pos':(9,(3,e['pos'])),'state':(3,e['state'])})
def main():
 assert sha(SOURCE)==PIN
 root,before=read_structure(SOURCE)
 _,sb,version,offset=read_schematic(SOURCE.with_suffix('.schem').read_bytes(),'omit');assert sb==before
 removed={p:s for p,s in before.items() if chosen(p)}
 assert len(removed)==147 and set(removed.values())=={'minecraft:dripstone_block'}
 # A one-cell empty moat proves the chosen volume cannot cut attached anatomy.
 assert not [p for p in before if 84<=p[0]<=93 and 20<=p[1]<=26 and 2<=p[2]<=13 and p not in removed]
 after={p:s for p,s in before.items() if p not in removed}
 OUT.mkdir(exist_ok=True)
 schem=OUT/(STEM+'.schem');nbt=OUT/(STEM+'.nbt')
 schem.write_bytes(encode_schematic(after,root['size'],version,offset));convert(schem,nbt,'omit',32)
 revised,check=read_structure(nbt);assert check==after
 assert {k:v for k,v in root.items() if k!='blocks'}=={k:v for k,v in revised.items() if k!='blocks'}
 retained=[e for e in root['blocks'] if tuple(e['pos']) not in removed]
 assert retained==revised['blocks']
 original_records=b''.join(map(record,root['blocks']));kept_records=b''.join(map(record,retained))
 assert original_records in gzip.decompress(SOURCE.read_bytes())
 assert kept_records in gzip.decompress(nbt.read_bytes())
 rotations=[]
 for rotation in ['NONE','CLOCKWISE_90','CLOCKWISE_180','COUNTERCLOCKWISE_90']:
  rb={rotate(p,rotation):s for p,s in before.items()};ra={rotate(p,rotation):s for p,s in after.items()}
  assert {p:s for p,s in rb.items() if p not in ra}=={rotate(p,rotation):s for p,s in removed.items()}
  assert all(rb[p]==s for p,s in ra.items())
  # Full template bounds, not sparse art bounds, preserve placement offsets.
  corners=[rotate((x,y,z),rotation) for x in (0,98) for y in (0,135) for z in (0,98)]
  lo=[min(p[i] for p in corners) for i in range(3)];hi=[max(p[i] for p in corners) for i in range(3)]
  rotations.append({'rotation':rotation,'size':[hi[i]-lo[i]+1 for i in range(3)],'rotated_min_offset':lo,'rotated_max_offset':hi,'schematic_offset':offset,'source':nbt.relative_to(ROOT).as_posix(),'sha256':sha(nbt),'remaining_cells_equal':True})
 handoff={'source':nbt.relative_to(ROOT).as_posix(),'version':STEM,'sha256':sha(nbt),'size':root['size'],'ground_y':28,'buried_clip_depth':6,'blocks':len(after),'source_offset':offset,'data_version':version,'baseline_source':SOURCE.relative_to(ROOT).as_posix(),'baseline_sha256':PIN,'baseline_blocks':len(before),'removed_count':len(removed),'removed_source_center':[40,1,-36],'removed_bounds':[[85,21,3],[92,25,12]],'removed_cells':[{'pos':list(p),'state':s} for p,s in sorted(removed.items())],'remaining_cell_records_sha256':hashlib.sha256(kept_records).hexdigest(),'remaining_cell_records_byte_identical':True,'other_root_tags_identical':True,'rotations':rotations,'schematic_sha256':sha(schem),'in_game_tested':False}
 dump(OUT/'handoff.json',handoff)
 print(json.dumps({k:handoff[k] for k in ['source','sha256','blocks','removed_count']}))
if __name__=='__main__':main()
