"""Render same-scale V1/V2 pairs from actual NBT and assemble an October 4 review."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
WORK=ROOT/'.work/relic-v2-review'
PAIRS=[('Small Colossus','colossus','small-colossus',
        'New bronze-machine relative / domed helmet / torn cuirass'),
       ('World Tree','world-tree','world-tree',
        'Fine branch-grown foliage / irregular crown / tapering roots'),
       ('Ruined Tower','ruined-tower','ruined-tower',
        '180 -> 220 visible blocks / same footprint')]


def render(versions=('v1','v2'),yaw=22):
    import math
    import bpy
    from mathutils import Vector
    import render_ots_preview as renderer
    WORK.mkdir(parents=True,exist_ok=True)
    renderer.ATLAS=ROOT/'.work/foliage-preview-atlas'
    records=[]
    for title,relic,stem,note in PAIRS:
        bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
        cursor=0;objects=[];rows=[]
        for version in versions:
            name=stem+'-'+version;folder=ROOT/'relics'/relic/'design'/'generated'/name
            design=json.loads((folder/f'{name}.design.json').read_text())
            root=renderer.decode_nbt((folder/f'{name}.nbt').read_bytes());ground=design['ground_level_nbt_approx']
            obj=renderer.blocks_from_nbt(folder/f'{name}.nbt',predicate=lambda p,g=ground:p[1]>=g)
            obj.name=name+' / actual NBT';obj.rotation_euler.z=math.radians(yaw);obj.location.z=-ground
            bpy.context.view_layer.update()
            corners=[obj.matrix_world@Vector(c) for c in obj.bound_box]
            lo,hi=min(v.x for v in corners),max(v.x for v in corners)
            # Looking from +Y, screen-right corresponds to -X.
            obj.location.x=-cursor-hi;cursor+=hi-lo+35;objects.append(obj)
            rows.append({'version':version.upper(),'size':root['size'],'visible_height':root['size'][1]-ground,'blocks':len(root['blocks'])})
        bpy.context.view_layer.update()
        center,corners=renderer.stage()
        ground=bpy.data.objects['Presentation ground (not exported)'];ground.location.z=-.1
        scene=bpy.context.scene
        scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
        for obj in scene.objects:
            if obj.type=='LIGHT' and obj.data.type=='AREA':obj.data.energy=30000
        sun=bpy.data.lights.new('Pair daylight','SUN');sun.energy=1.6;sun.angle=.25
        lamp=bpy.data.objects.new(sun.name,sun);scene.collection.objects.link(lamp)
        lamp.rotation_euler=(.5,-.5,-.35)
        camera=scene.camera;camera.location=center+Vector((0,900,260))
        renderer.point_at(camera,center)
        rotation=camera.rotation_euler.to_matrix().transposed()
        projected=[rotation@(p-center) for p in corners]
        width=max(p.x for p in projected)-min(p.x for p in projected)
        height=max(p.y for p in projected)-min(p.y for p in projected)
        scene.render.resolution_x,scene.render.resolution_y=1800,1450
        camera.data.ortho_scale=max(width,height*1800/1450)*1.12
        scene.cycles.samples=32
        scene.render.filepath=str(WORK/f'{stem}.png');bpy.ops.render.render(write_still=True)
        records.append({'title':title,'stem':stem,'note':note,'versions':rows})
    (WORK/'pairs.json').write_text(json.dumps(records,indent=2)+'\n')


def compose():
    from PIL import Image,ImageDraw,ImageFont
    rows=json.loads((WORK/'pairs.json').read_text())
    canvas=Image.new('RGB',(2400,2530),'#eee9de');draw=ImageDraw.Draw(canvas)
    def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',size)
    draw.text((45,25),'RELIC REVISIONS / V1 -> V2',font=font(49,True),fill='#293934')
    draw.text((48,91),'Actual exported blocks / each pair shares one scale and ground level',font=font(28),fill='#54615a')
    for i,row in enumerate(rows):
        y=155+i*750
        draw.text((48,y),row['title'].upper(),font=font(34,True),fill='#293934')
        image=Image.open(WORK/(row['stem']+'.png')).convert('RGB')
        # Wide row: pair at left, concise measured comparison at right.
        image.thumbnail((1450,680),Image.Resampling.LANCZOS)
        canvas.paste(image,(48,y+48))
        x=990
        draw.text((x,y+140),row['note'].replace(' / ','\n'),font=font(31,True),fill='#293934',spacing=12)
        for j,v in enumerate(row['versions']):
            text=f"{v['version']}   {' x '.join(map(str,v['size']))}\n{v['visible_height']} visible block layers / {v['blocks']:,} blocks"
            draw.text((x,y+325+j*116),text,font=font(29),fill='#54615a',spacing=9)
        draw.text((x,y+590),'LEFT: V1     RIGHT: V2',font=font(28,True),fill='#293934')
        draw.line((48,y+735,2350,y+735),fill='#c6c6ba',width=2)
    draw.text((48,2460),'V2 visual candidates; game integration pending. Blender previews, not Minecraft screenshots.',font=font(27),fill='#54615a')
    output=ROOT/'docs/project/reviews/relics-v2-review.png';output.parent.mkdir(parents=True,exist_ok=True);canvas.save(output)
    print(output)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','8',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],cwd=ROOT,check=True)
        compose()
