"""Ground-only follow-up: preserve the accepted V4 tree and add narrow root toes."""
import hashlib
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *

SOURCE=ROOT/'relics/world-tree/design/generated/world-tree-v4/world-tree-v4-source.blend'


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    meta=json.loads(SOURCE.with_name('world-tree-v4.design.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    # Root contact edges identified in the saved Alpha 4.3 world. Low elongated
    # earth fingers settle the feet without filling the taller intentional arches.
    # Low visible height must still have earth below the wooden toe. With the
    # helper's tapered floor, depth 8 would hide all soil inside some root cells,
    # leaving no soil column for the runtime support processor to extend.
    deposits([(42,-37,11,12,1.0,-40),(-8,-36,9,14,.9,-12)],40,(-20,58,-55,-18))
    meta.update(name='World Tree V4.1 / Root terrain contacts',
                visual_acceptance='User accepts V4 tree; October 6 ground-only follow-up pending')
    meta['revision_v4_1']={'source':SOURCE.relative_to(ROOT).as_posix(),'source_sha256':digest,
        'accepted_tree_geometry_preserved':True,'changed_materials':['terrain_top','terrain_patch','terrain_fill'],
        'ground_only':True,'basis':'Saved Alpha 4.3 root contact audit, October 6'}
    save('relics/world-tree/design/world-tree-v4-1.json',meta)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest


if __name__=='__main__':main()
