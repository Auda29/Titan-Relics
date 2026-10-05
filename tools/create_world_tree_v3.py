"""Open, ramified canopy after the October 5 in-game screenshot review."""
import math
from pathlib import Path
import sys

from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
import create_world_tree_v2 as previous
from new_relic_v1_common import *


def crown():
    rng=previous.RNG
    terminals=[];primary=0
    # Unequal levels and curved directions avoid a stack of flat, isolated crowns.
    for y,angle,length,rise,width in [(63,195,65,48,9),(78,12,69,49,8.5),
                                     (91,117,61,62,7.7),(102,288,64,51,7),
                                     (116,37,59,50,6.2),(131,211,49,49,5),
                                     (142,95,39,48,4.5),(152,320,33,45,3.6),
                                     (119,166,53,55,5.8),(134,255,45,49,4.8)]:
        a=math.radians(angle);direction=Vector((math.cos(a),0,math.sin(a)))
        side=Vector((-direction.z,0,direction.x))
        origin=Vector((4 if y<120 else -2,y,4))
        points=[origin,origin+direction*(length*.33)+Vector((0,rise*.47,0)),
                origin+direction*(length*.7)+side*5+Vector((0,rise*.78,0)),
                origin+direction*length+side*9+Vector((0,rise,0))]
        previous.curved(f'02 | Wandering primary bough {primary}',points,[width,width*.65,width*.30,1.05])
        primary+=1
        # Subdivide along most of the bough, not just a cluster at its far end.
        for j in range(7):
            t=.16+j*.13
            segment=min(2,int(t*3));local=t*3-segment
            start=points[segment].lerp(points[segment+1],local)
            spread=(1 if j%2 else -1)*rng.uniform(12,24)
            end=start+direction*rng.uniform(6,15)+side*spread+Vector((0,rng.uniform(7,17),0))
            mid=start.lerp(end,.53)+Vector((0,3,0))
            previous.curved(f'03 | Crooked secondary {primary}.{j}',[start,mid,end],[2.2,1.3,.65],sides=9)
            for k in range(4):
                base=mid.lerp(end,.15+k*.24)
                outward=(end-start).normalized()
                tip=base+outward*rng.uniform(5,11)+direction*rng.uniform(-7,8)+Vector((0,rng.uniform(1,8),0))
                previous.curved(f'04 | Fine fork {len(terminals)}',[base,base.lerp(tip,.5)+Vector((0,1,0)),tip],[1.2,1.0,.9],sides=8)
                terminals.append(list(tip))
                # Sparse individual sprays expose woody forks between the clusters.
                for n,tleaf in enumerate((.25,.65,1.0)):
                    center=base.lerp(tip,tleaf)+Vector((0,.8,0))
                    radius=rng.uniform(4.2,6.4)
                    previous.leaves(f'05 | Small open spray {len(terminals)}.{n}',center,
                                    (radius,rng.uniform(3.2,5.0),radius*rng.uniform(.65,1.15)))
            if j%3==0:
                # Bare end beyond the leaf sprays adds irregular silhouette tips.
                tip=end+direction*5+side*(2 if spread>0 else -2)+Vector((0,2,0))
                previous.curved('Exposed weathered terminal',[mid,end,tip],[.8,.55,.38],sides=7)
    return len(terminals),terminals


def main():
    old_save=previous.save
    def save_revision(path,metadata):
        metadata['name']='World Tree V3 / Open ramified crown'
        metadata['visual_acceptance']='October 5 screenshot revision; review pending'
        metadata['revision_v2'].update(primary_boughs=10,secondary_boughs=70,
                                       leaf_clusters=metadata['revision_v2']['terminal_boughs']*3)
        metadata['revision_v3']={'feedback':'Screenshots 18/19: compact leaf pads and too few visible forks',
                                 'leaf_radius_range':[4.2,6.4],'foliage_per_terminal':3,
                                 'branching_distribution':'along the full primary bough; open peripheral twigs'}
        old_save('relics/world-tree/design/world-tree-v3.json',metadata)
    previous.crown=crown;previous.save=save_revision;previous.main()


if __name__=='__main__':main()
