"""Same-scale actual-block soil-relief comparisons, with focused root/annex views."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
WORK=ROOT/'.work/deposit-relief-review'
PAIRS=[('titan_skull_dry','Savanna Skull / irregular deposits',None,25),
       ('titan_skull_rock','Rock Skull / broken slope contours',None,25),
       ('small_colossus','Small Colossus / soil margins',None,22),
       ('world_tree','World Tree / root feet only',30,22),
       ('ruined_tower','Tower / lower annex walls and terrain',60,68)]


def render():
    import math
    import bpy
    from mathutils import Vector
    import render_ots_preview as renderer
    from build_deposit_relief import baseline_contract
    WORK.mkdir(parents=True,exist_ok=True);renderer.ATLAS=ROOT/'.work/foliage-preview-atlas'
    for name,title,cut,yaw in PAIRS:
        if '--tower-only' in sys.argv and name!='ruined_tower':continue
        record=json.loads((ROOT/'build/deposit-relief'/f'{name}.json').read_text())
        ground=record['ground_y'];paths=[ROOT/baseline_contract(name)['source'],ROOT/record['source']]
        bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
        config=paths[1].parents[2]/f'{paths[1].stem}.json';renderer.CONFIG=json.loads(config.read_text())
        cursor=0
        for path in paths:
            obj=renderer.blocks_from_nbt(path,predicate=lambda p:ground-1<=p[1] and (cut is None or p[1]<ground+cut))
            obj.rotation_euler.z=math.radians(yaw);obj.location.z=-ground;bpy.context.view_layer.update()
            corners=[obj.matrix_world@Vector(c) for c in obj.bound_box]
            lo,hi=min(p.x for p in corners),max(p.x for p in corners)
            obj.location.x=-cursor-hi;cursor+=hi-lo+20
        bpy.context.view_layer.update();center,corners=renderer.stage()
        bpy.data.objects['Presentation ground (not exported)'].location.z=-1.1
        scene=bpy.context.scene;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
        sun=bpy.data.lights.new('Relief daylight','SUN');sun.energy=1.8;sun.angle=.25
        lamp=bpy.data.objects.new(sun.name,sun);scene.collection.objects.link(lamp);lamp.rotation_euler=(.5,-.5,-.35)
        camera=scene.camera;camera.location=center+Vector((0,700,380));renderer.point_at(camera,center)
        rotation=camera.rotation_euler.to_matrix().transposed();projected=[rotation@(p-center) for p in corners]
        width=max(p.x for p in projected)-min(p.x for p in projected);height=max(p.y for p in projected)-min(p.y for p in projected)
        camera.data.ortho_scale=max(width,height*1800/900)*1.07
        scene.render.resolution_x=1800;scene.render.resolution_y=900;scene.cycles.samples=24
        scene.render.filepath=str(WORK/f'{name}.png');bpy.ops.render.render(write_still=True)


def compose():
    from PIL import Image,ImageDraw,ImageFont
    canvas=Image.new('RGB',(1800,2850),'#eee9de');draw=ImageDraw.Draw(canvas)
    font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
    draw.text((30,15),'GROUND RELIEF / LOWER TOWER WALLS',font=font(38),fill='#293934')
    draw.text((30,65),'Actual exported NBT / LEFT: Alpha 4.4 / RIGHT: revised / shared scale per pair',font=font(24),fill='#54615a')
    for i,(name,title,cut,yaw) in enumerate(PAIRS):
        y=115+i*540;draw.text((30,y),title,font=font(28),fill='#293934')
        image=Image.open(WORK/f'{name}.png').convert('RGB');image.thumbnail((1750,480),Image.Resampling.LANCZOS)
        canvas.paste(image,((1800-image.width)//2,y+45))
    output=ROOT/'docs/project/reviews/deposit-relief-20261006.png';canvas.save(output);print(output)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','6',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render',
                        *(['--tower-only'] if '--tower-only' in sys.argv else [])],cwd=ROOT,check=True)
        compose()
