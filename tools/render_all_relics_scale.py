"""Same-scale orthographic lineup of the seven current relic designs.

Host Python: python tools/render_all_relics_scale.py
Builds from actual NBT, then composes the PNG using host Pillow. Render-only
cropping hides buried cells at each asset's documented ground datum.
"""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
WORK = ROOT / '.work/all-relics-scale'
OUT = ROOT / 'docs/project/reviews/all-current-relics-scale.png'
ASSETS = [
    ('World Tree', 'V1', 'world-tree', 'world-tree-v1'),
    ('Ruined Tower', 'V1', 'ruined-tower', 'ruined-tower-v1'),
    ('Obelisk', 'V4.2', 'obelisk', 'obelisk-v4-2'),
    ('Large Colossus', 'V4.1 / materials B', 'colossus', 'colossus-v4-1-materials-b'),
    ('Titan Skull 2', 'V1 / embedded sword', 'titan-skull', 'titan-skull-2-v1'),
    ('Titan Skull', 'V4 / meadow', 'titan-skull', 'titan-skull-v4-meadow'),
    ('Small Colossus', 'V1', 'colossus', 'small-colossus-v1'),
]


def render():
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    import render_ots_preview as renderer

    WORK.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    renderer.ATLAS = ROOT / '.work/foliage-preview-atlas'
    records, objects = [], []
    cursor = 0
    for title, version, relic, stem in ASSETS:
        folder = ROOT / 'relics' / relic / 'design' / 'generated' / stem
        path = folder / f'{stem}.nbt'
        design = json.loads((folder / f'{stem}.design.json').read_text())
        nbt = renderer.decode_nbt(path.read_bytes())
        ground = design['ground_level_nbt_approx']
        obj = renderer.blocks_from_nbt(path, predicate=lambda p, g=ground: p[1] >= g)
        obj.name = title + ' / actual NBT / unit scale'
        obj.rotation_euler.z = math.radians(22)
        obj.location.z = -ground
        bpy.context.view_layer.update()
        corners = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
        lo, hi = min(v.x for v in corners), max(v.x for v in corners)
        width = hi-lo
        # Camera looks from +Y, so screen-right is world -X.
        center = cursor + width/2
        obj.location.x = -center-(lo+hi)/2
        cursor += width + 42
        objects.append(obj)
        records.append({'name': title, 'version': version, 'size': nbt['size'],
                        'ground_y': ground, 'visible_height': nbt['size'][1]-ground,
                        'blocks': len(nbt['blocks']), 'source': str(path.relative_to(ROOT)).replace('\\', '/'),
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'center_world_x': -center, 'rotation_degrees': 22,
                        'scale': list(obj.scale)})
    bpy.context.view_layer.update()
    corners = [obj.matrix_world @ Vector(v) for obj in objects for v in obj.bound_box]
    low = Vector(tuple(min(v[i] for v in corners) for i in range(3)))
    high = Vector(tuple(max(v[i] for v in corners) for i in range(3)))
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 5600, 1700
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'Standard'
    scene.world = bpy.data.worlds.new('Neutral daylight')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.78,.82,.86,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .8
    bpy.ops.mesh.primitive_plane_add(size=12000, location=((low.x+high.x)/2,0,-.1))
    bpy.context.object.name = 'Shared nominal ground / presentation only'
    bpy.context.object.data.materials.append(renderer.material('Warm neutral site',(.57,.55,.49)))
    light = bpy.data.lights.new('Broad daylight', 'SUN')
    light.energy, light.angle = 2.0, .25
    lamp = bpy.data.objects.new(light.name, light)
    scene.collection.objects.link(lamp)
    lamp.rotation_euler = (.55,-.45,-.35)
    camera = bpy.data.objects.new('Common orthographic camera', bpy.data.cameras.new('Common orthographic camera'))
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.data.type = 'ORTHO'
    camera.data.clip_end = 10000
    target = Vector(((low.x+high.x)/2,0,100))
    camera.location = target + Vector((0,1800,400))
    renderer.point_at(camera,target)
    rotation = camera.rotation_euler.to_matrix().transposed()
    projected = [rotation @ (v-target) for v in corners]
    min_y, max_y = min(v.y for v in projected), max(v.y for v in projected)
    shift = camera.rotation_euler.to_matrix() @ Vector((0,(min_y+max_y)/2,0))
    camera.location += shift
    camera.data.ortho_scale = max(high.x-low.x+100, (max_y-min_y+60)*5600/1700)
    # A real two-block scale marker next to the small machine.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(low.x-12,45,1))
    marker=bpy.context.object
    marker.name='Two-block human-height marker / not exported'
    marker.scale=(.65,.65,2)
    marker.data.materials.append(renderer.material('Scale marker',(.75,.18,.035)))
    bpy.context.view_layer.update()
    for row in records:
        point = world_to_camera_view(scene,camera,Vector((row['center_world_x'],0,0)))
        row['label_x_px'] = round(point.x*5600)
    records[0]['camera'] = {'type':'ORTHO','scale':camera.data.ortho_scale,
                           'elevation_degrees':math.degrees(math.atan2(400,1800)),
                           'pixels_per_block_horizontal':5600/camera.data.ortho_scale}
    (WORK/'lineup.json').write_text(json.dumps(records,indent=2)+'\n')
    scene.render.filepath = str(WORK/'lineup.png')
    bpy.ops.render.render(write_still=True)


def compose():
    from PIL import Image, ImageDraw, ImageFont
    rows=json.loads((WORK/'lineup.json').read_text())
    canvas=Image.new('RGB',(5600,2190),'#eee9de')
    draw=ImageDraw.Draw(canvas)
    def font(n,bold=False):
        return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
    draw.text((70,25),'ALL CURRENT RELICS / SAME SCALE',font=font(62,True),fill='#293934')
    draw.text((73,108),'7 current designs  /  Actual NBT blocks  /  One orthographic camera  /  Common ground level',font=font(35),fill='#54615a')
    canvas.paste(Image.open(WORK/'lineup.png').convert('RGB'),(0,175))
    for row in rows:
        x=row['label_x_px']
        draw.line((x,1810,x,1880),fill='#879087',width=2)
        draw.text((x,1895),row['name'],font=font(36,True),fill='#293934',anchor='mt')
        draw.text((x,1943),row['version'],font=font(27),fill='#54615a',anchor='mt')
        dims=' × '.join(map(str,row['size']))
        draw.text((x,1984),dims+' blocks',font=font(29,True),fill='#293934',anchor='mt')
        draw.text((x,2027),f'Above ground: ~{row["visible_height"]} blocks',font=font(27),fill='#54615a',anchor='mt')
    ppm=rows[0]['camera']['pixels_per_block_horizontal']
    x,y=80,2120
    draw.line((x,y,x+100*ppm,y),fill='#293934',width=4)
    for value in (0,25,50,75,100):
        u=x+value*ppm
        draw.line((u,y-8,u,y+8),fill='#293934',width=3)
        draw.text((u,y+13),str(value),font=font(23),fill='#293934',anchor='mt')
    draw.text((x+100*ppm+20,y-15),'blocks',font=font(25),fill='#293934')
    draw.text((760,2104),'Dimensions: width × total height × depth, including burial. Buried portions are hidden at the documented ground level.',font=font(29),fill='#54615a')
    draw.text((760,2149),'Skull V4: meadow shown; all four terrain variants share its size. Blender render, not an in-game screenshot. Leaf/grass tint approximate.',font=font(29),fill='#54615a')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(OUT)
    print(OUT)


if __name__=='__main__':
    if '--render' in sys.argv:
        render()
    elif '--compose' in sys.argv:
        compose()
    else:
        subprocess.run([sys.executable,'tools/prepare_foliage_preview.py'],cwd=ROOT,check=True)
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe',
                        '--background','--threads','10','--python-exit-code','1','--python',str(Path(__file__).resolve()),
                        '--','--render'],cwd=ROOT,check=True)
        compose()
