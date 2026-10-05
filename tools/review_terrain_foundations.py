"""Render a controlled downhill regression from actual skull NBT before/after support."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
WORK=ROOT/'.work/foundation-review'


def prepare():
    from relic_assets import decode_nbt,encode_structure
    from relic_catalog import ASSETS
    from terrain_foundations import supported_blocks
    contract=ASSETS['titan_skull'];raw=(ROOT/contract['source']).read_bytes();root=decode_nbt(raw)
    blocks={tuple(b['pos']):root['palette'][b['state']]['Name'] for b in root['blocks']}
    after,size,report=supported_blocks(blocks,contract)
    WORK.mkdir(parents=True,exist_ok=True)
    (WORK/'before.nbt').write_bytes(raw)
    (WORK/'after.nbt').write_bytes(encode_structure(after,tuple(size),root['DataVersion']))
    (WORK/'fixture.json').write_text(json.dumps({'contract':contract,'foundation':report},indent=2)+'\n')


def render():
    import bpy
    from mathutils import Vector
    import render_ots_preview as renderer
    data=json.loads((WORK/'fixture.json').read_text());contract=data['contract'];sx,_,sz=contract['size']
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for i,version in enumerate(('before','after')):
        offset=-i*(sx+90)
        model=renderer.blocks_from_nbt(WORK/f'{version}.nbt')
        ground=contract['ground_y']+(data['foundation']['vertical_padding'] if i else 0)
        model.location=Vector((offset,0,-ground))
        vertices=[];faces=[]
        for z in (-35,sz+35):
            for x in (-25,sx+25):vertices.append((x-sx/2+offset,-(z-sz/2),(z/sz-.5)*24))
        mesh=bpy.data.meshes.new('Controlled 24-block slope');mesh.from_pydata(vertices,[],[(0,1,3,2)]);mesh.update()
        obj=bpy.data.objects.new('Illustrative inclined terrain',mesh);bpy.context.collection.objects.link(obj)
        mesh.materials.append(renderer.material('Muted meadow slope',(.24,.29,.15)))
    bpy.context.view_layer.update()
    center,corners=renderer.stage()
    bpy.data.objects.remove(bpy.data.objects['Presentation ground (not exported)'],do_unlink=True)
    scene=bpy.context.scene;scene.camera.location=center+Vector((100,450,100));renderer.point_at(scene.camera,center)
    rotation=scene.camera.rotation_euler.to_matrix().transposed()
    projected=[rotation@(p-center) for p in corners]
    width=max(p.x for p in projected)-min(p.x for p in projected)
    height=max(p.y for p in projected)-min(p.y for p in projected)
    scene.camera.data.ortho_scale=max(width,height*2000/950)*1.08
    scene.render.resolution_x=2000;scene.render.resolution_y=950
    sun=bpy.data.lights.new('Foundation daylight','SUN');sun.energy=2;sun.angle=.3
    lamp=bpy.data.objects.new('Foundation daylight',sun);scene.collection.objects.link(lamp);lamp.rotation_euler=(.5,-.4,-.3)
    scene.cycles.samples=32;scene.render.filepath=str(WORK/'pair.png');bpy.ops.render.render(write_still=True)


def compose():
    from PIL import Image,ImageDraw,ImageFont
    canvas=Image.new('RGB',(2000,1140),'#eee9de');draw=ImageDraw.Draw(canvas)
    font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',n)
    draw.text((35,20),'TERRAIN CONTACT / CONTROLLED DOWNHILL TEST',font=font(38),fill='#293934')
    canvas.paste(Image.open(WORK/'pair.png'),(0,85))
    draw.text((35,1045),'LEFT: raw model / RIGHT: derived foundation',font=font(27),fill='#293934')
    draw.text((35,1090),'Actual NBT; illustrative slope from -12 to +12 blocks. This is not a Minecraft screenshot.',font=font(23),fill='#54615a')
    target=ROOT/'docs/project/reviews/terrain-foundations-20261005.png';canvas.save(target);print(target)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    else:
        prepare()
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','6',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],cwd=ROOT,check=True)
        compose()
