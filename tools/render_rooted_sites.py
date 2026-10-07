"""Render actual saved-world comparison crops; textures/tints are preview approximations."""
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / 'build/rooted-embedding/20261007/views'
PAIRS = [('titan_skull_rock', 'FELSSCHÄDEL / Steinplatte entfernt, 6 Blöcke tiefer', 155),
         ('titan_skull_2', 'SCHÄDEL 2 / Bodeninsel entfernt, 6 Blöcke tiefer', 75),
         ('world_tree', 'WELTENBAUM / Wurzelbereich: verlängerte Wurzeln, Erdpolster entfernt, 4 Blöcke tiefer', 25)]


def render():
    import bpy
    from mathutils import Vector
    sys.path.insert(0, str(ROOT / 'tools'))
    import render_ots_preview as renderer
    from relic_assets import decode_nbt
    # Preserve saved state names, but use a documented visual fallback for modern
    # terrain textures absent from the legacy preview atlas.
    import shutil
    atlas_source = ROOT / '.work/foliage-preview-atlas'
    atlas = json.loads((atlas_source / 'vanilla.atlas').read_text())
    known = {a['name']: a for a in atlas['blocks']}
    all_names = {s['Name'] for path in VIEWS.glob('*.nbt') for s in decode_nbt(path.read_bytes())['palette']}
    fallbacks = {}
    for name in sorted(all_names - known.keys() - {'minecraft:grass_block'}):
        fallback = ('minecraft:oak_leaves' if 'leaves' in name else 'minecraft:oak_log' if 'log' in name else
                    'minecraft:blue_concrete' if name == 'minecraft:water' else
                    'minecraft:dirt' if 'dirt' in name else 'minecraft:stone')
        atlas['blocks'].append({'name': name, 'faces': known[fallback]['faces']})
        fallbacks[name] = fallback
    target_atlas = VIEWS / 'preview-atlas'
    target_atlas.mkdir(exist_ok=True)
    (target_atlas / 'vanilla.atlas').write_text(json.dumps(atlas))
    shutil.copy2(atlas_source / 'vanilla.png', target_atlas / 'vanilla.png')
    (VIEWS / 'texture-fallbacks.json').write_text(json.dumps(fallbacks, indent=2) + '\n')
    renderer.ATLAS = target_atlas
    renderer.CONFIG = {'preview': {'grass_tint': [.66, .88, .47]}}
    for name, title, yaw in PAIRS:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        cursor = 0
        for side in ('before', 'after'):
            obj = renderer.blocks_from_nbt(VIEWS / f'{name}-{side}.nbt')
            obj.rotation_euler.z = math.radians(yaw)
            bpy.context.view_layer.update()
            corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
            lo, hi = min(p.x for p in corners), max(p.x for p in corners)
            obj.location.x = -cursor - hi
            cursor += hi - lo + 20
        bpy.context.view_layer.update()
        center, corners = renderer.stage()
        # Camera looks down -Y; its screen-right is -X, giving before on the left.
        scene = bpy.context.scene
        camera = scene.camera
        camera.location = center + Vector((0, 800, 350 if name != 'world_tree' else 420))
        renderer.point_at(camera, center)
        projected = [camera.rotation_euler.to_matrix().transposed() @ (p - center) for p in corners]
        width = max(p.x for p in projected) - min(p.x for p in projected)
        height = max(p.y for p in projected) - min(p.y for p in projected)
        camera.data.ortho_scale = max(width, height * 2) * 1.06
        scene.render.resolution_x, scene.render.resolution_y = 1800, 900
        scene.cycles.samples = 16
        sun = bpy.data.lights.new('Daylight', 'SUN')
        sun.energy, sun.angle = 2.2, .3
        lamp = bpy.data.objects.new('Daylight', sun)
        scene.collection.objects.link(lamp)
        lamp.rotation_euler = (.45, -.5, -.4)
        scene.render.filepath = str(VIEWS / f'{name}.png')
        bpy.ops.render.render(write_still=True)


def compose():
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGB', (1800, 2540), '#eeeade')
    draw = ImageDraw.Draw(image)
    font = lambda n: ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', n)
    draw.text((30, 15), 'TIEFERE EINBETTUNG / DIESELBEN NATÜRLICHEN STANDORTE', font=font(33), fill='#2b3932')
    draw.text((30, 65), 'Links: Alpha 4.7   |   Rechts: neue Varianten   |   Gespeicherte Weltblöcke, gleicher Maßstab', font=font(24), fill='#2b3932')
    for row, (name, title, _) in enumerate(PAIRS):
        y = 120 + row * 775
        draw.text((30, y), title, font=font(28), fill='#2b3932')
        view = Image.open(VIEWS / f'{name}.png').convert('RGB')
        view.thumbnail((1740, 710), Image.Resampling.LANCZOS)
        image.paste(view, ((1800 - view.width) // 2, y + 45))
    draw.text((30, 2460), 'Blender-Ansichten echter Weltdaten; vereinfachte Texturen/Farben, kleine Pflanzen ausgeblendet. Keine Clientfotos.', font=font(20), fill='#2b3932')
    draw.text((30, 2495), 'Beim Baum ist nur der Wurzelbereich ausgeschnitten; die vollständige Krone gehört weiterhin zum Modell.', font=font(20), fill='#2b3932')
    output = ROOT / 'docs/project/reviews/rooted-embedding-20261007.png'
    image.save(output)
    provenance = json.loads((VIEWS / 'manifest.json').read_bytes())
    provenance['texture_fallbacks'] = json.loads((VIEWS / 'texture-fallbacks.json').read_bytes())
    provenance['comparison'] = {'path': output.relative_to(ROOT).as_posix(),
                                'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}
    output.with_suffix('.json').write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
    print(output)


if __name__ == '__main__':
    if '--render' in sys.argv:
        render()
    else:
        import subprocess
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe', '--background', '--threads', '5',
                        '--python-exit-code', '1', '--python', str(Path(__file__).resolve()), '--', '--render'], check=True)
        compose()
