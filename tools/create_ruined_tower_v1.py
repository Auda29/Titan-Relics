"""Build a dark breached tower with an authored top, no aircraft or V5 interiors."""
import math
from pathlib import Path
import random
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_colossus_v3 as shapes


def main():
    reset({'wall':'262e31','pier':'343c3f','worn':'414644','seam':'242a29','accent':'675345'})
    shapes.RNG.seed(20261003);rng=random.Random(401)
    shell=box('01 | Hollow monumental tower shell',(0,84,0),(56,192,48),'wall',1.4)
    subtract(shell,box('Open architectural interior',(0,92,0),(42,196,34),'wall'))
    # The reference top is cropped: these unequal terminations are our completion.
    for x,width,top in [(-20,17,156),(0,24,168)]:
        subtract(shell,box('Unequal broken top',(x,top+23,0),(width,46,60),'wall'))
    for x,y,width,height in [(-8,133,7,100),(15,153,6,60)]:
        subtract(shell,box('Long open sky slot',(x,y,0),(width,height,70),'wall'))
    damage(shell,(16,106,-23),(13,30),22)
    damage(shell,(-17,48,-23),(12,24),21)
    damage(shell,(-25,125,8),(11,17),30)
    damage(shell,(12,58,23),(15,20),20)
    # Lower threshold and the single round-topped opening, both real voids.
    subtract(shell,box('Lower hall threshold',(0,12,-22),(18,28,22),'wall'))
    subtract(shell,box('Arched opening lower',(10,72,0),(14,16,70),'wall'))
    subtract(shell,cylinder('Arched opening crown',(10,80,-36),(10,80,36),7,'wall',32))
    # Shallow vertical recesses stop short of the weathered outer contour.
    for x in (-22,-15,-1,5,23):
        subtract(shell,box('Recessed facade flute',(x,58,-24),(1.2,104,2.8),'wall'))
    for x in (-17,2,19):
        subtract(shell,box('Recessed rear flute',(x,58,24),(1.1,96,2.6),'wall'))
    for center,radii in [((-21,148,-24),(5,6)),((22,162,-24),(4,8)),((-25,15,-23),(7,10)),
                          ((19,24,23),(7,9)),((-17,120,23),(5,8)),
                          ((-25,156,-23),(6,4)),((24,179,-23),(5,7)),((5,168,23),(6,4))]:
        damage(shell,center,radii,12)
    # Recessed buttress masses remain ground-connected and do not bridge sky slots.
    for x,z,h in [(-27,10,151),(26,14,175),(-24,-17,139),(22,-18,64)]:
        box('02 | Continuous load-bearing edge pier',(x,(h-12)/2,z),(5.5,h+12,7),'pier',.65)
    for x,h in [(-29,83),(29,122)]:
        box('Outer surviving vertical fin',(x,h/2-2,20),(2.2,h+4,5),'seam',.2)
    # Tapered grounding skirts: wide below, never a flat circular plinth.
    for s in (-1,1):
        vertices=[(s*24,-12,-22),(s*38,-6,-22),(s*31,13,-22),(s*25,40,-22),
                  (s*24,-12,20),(s*38,-6,20),(s*31,13,20),(s*25,40,20)]
        obj=mesh('03 | Broken tapered buttress',vertices,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],'worn')
        recalculate(obj)
        damage(obj,(s*33,14,-16),(4,8),19)
    # Limited ledge remnants reserve architectural opportunities without fake stairs.
    box('Recessed lower bearing slab',(0,3,2),(42,4,30),'pier',.6)
    box('Intermediate rear ledge remnant',(-5,62,12),(29,3.2,9),'worn',.5)
    box('High torn ledge remnant',(-16,113,7),(8,3,19),'worn',.4)
    for i,(x,z,w,d,h) in enumerate([(-40,20,25,25,42),(40,18,22,20,28)]):
        annex=box(f'04 | Lower ruin {i+1}',(x,(h-5)/2,z),(w,h+5,d),'wall',1)
        subtract(annex,box('Open lower ruin chamber',(x,h/2+4,z),(w-8,h+9,d-8),'wall'))
        damage(annex,(x+3,h*.7,z-d/2),(w*.35,h*.34),12)
        subtract(annex,box('Lower ruin threshold',(x,5,z-d/2),(7,14,12),'wall'))
    # Individual fallen chunks below damaged elevations, never a complete ring.
    for i,(x,z,sx,sz,sy) in enumerate([(-47,-19,10,7,7),(-39,-34,8,10,6),(-25,-40,11,8,4),
                                      (32,-34,9,8,7),(47,-20,7,12,5),(20,39,11,9,5),(0,42,7,7,3)]):
        piece=box(f'05 | Fallen facade fragment {i+1}',(x,sy/2-1,z),(sx,sy,sz),'worn',.7)
        piece.rotation_euler.z=rng.uniform(-.4,.4)
    for x,y,z in [(-22,34,-24.8),(25,52,-25),(-40,14,6),(40,9,7.7)]:
        box('Old inset repair seam',(x,y,z),(1.3,12,.8),'accent',.15)
    deposits([(-34,-12,21,26,3.3,-15),(33,17,23,29,3.8,22),(4,33,27,16,2.3,0)],
             8,(-56,56,-48,48),('c0ae84','a9956b','aa946d'))
    save('relics/ruined-tower/design/ruined-tower-v1.json',{
        'name':'Ruined Tower V1','reference':'https://www.instagram.com/reel/DbqXYoVx2hR/',
        'new_relic_v1':{'family':'tower','void_probes_source':[[0,12,-23],[10,80,0],[-8,130,0]],
            'solid_probes_source':[[-27,35,10],[26,60,14]],
            'features':['three unequal upper terminations','round-topped opening','hollow shell','two lower ruins','real facade breaches'],
            'damage_target':'30–35% reconstructed exterior wall area; exact area not measured in V1',
            'source_top_authored':True,'aircraft_included':False,'v5_interiors':False}})


if __name__=='__main__':main()
