"""Block-exact isometric inspection of the upper treasure niche, without shaders."""
from PIL import Image,ImageDraw
from build_tower_upper_chest import OUT,STEM
from inspect_ots_result import read_structure

def render():
 _,all_blocks=read_structure(OUT/(STEM+'.nbt'))
 blocks={p:s for p,s in all_blocks.items() if 70<=p[0]<=75 and 173<=p[1]<=178 and 55<=p[2]<=58}
 image=Image.new('RGB',(1000,850),'#e4e8eb');draw=ImageDraw.Draw(image)
 def project(x,y,z):return (500+33*((x-72)-(z-56)),600+16*((x-72)+(z-56))-33*(y-173))
 def color(state):
  if 'waxed_cut_copper' in state:return (190,112,62)
  if 'lantern' in state:return (244,190,70)
  if 'basalt' in state:return (85,91,98)
  if 'cracked' in state:return (78,88,101)
  return (107,118,129)
 for (x,y,z),state in sorted(blocks.items(),key=lambda p:sum(p[0])):
  base=color(state)
  for neighbor,verts,shade in [((x,y,z+1),[(x,y,z+1),(x+1,y,z+1),(x+1,y+1,z+1),(x,y+1,z+1)],.82),((x+1,y,z),[(x+1,y,z),(x+1,y,z+1),(x+1,y+1,z+1),(x+1,y+1,z)],.62),((x,y+1,z),[(x,y+1,z),(x+1,y+1,z),(x+1,y+1,z+1),(x,y+1,z+1)],1.1)]:
   if neighbor in blocks:continue
   draw.polygon([project(*p) for p in verts],fill=tuple(min(255,int(c*shade)) for c in base),outline='#36404a',width=1)
 draw.text((32,25),'RUINED TOWER V11 | Upper platform treasure niche',fill='#17212b',font_size=24)
 draw.text((32,66),'NBT voxel inspection crop. Copper block = chest marker. Yellow block = lantern.',fill='#33404c',font_size=17)
 draw.text((32,800),'21 added blocks; existing platform, masonry and stair destination preserved.',fill='#33404c',font_size=17)
 out=OUT/'upper-niche-review.png';image.save(out);print(out)

if __name__=='__main__':render()
