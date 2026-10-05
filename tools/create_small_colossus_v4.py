"""Reference-led dormant plated Colossus after the opening of reel Da-s0zqi7OQ."""
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix,Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from new_relic_v1_common import *
import create_colossus_v3 as shapes

REFERENCE='https://www.instagram.com/reel/Da-s0zqi7OQ/'


def oriented_ellipsoid(name,center,u,v,normal,radii,material):
    obj=ellipsoid(name,(0,0,0),radii,material,32,20)
    c=Vector(center)
    for vertex in obj.data.vertices:
        p=vertex.co.copy();local=Vector((p.x,p.z,-p.y))
        vertex.co=xyz(c+u*local.x+v*local.y+normal*local.z)
    obj.data.update();return obj


def optic(name,center,normal,rx,ry,tilt=0,trim='edge'):
    normal=Vector(normal).normalized();u=Vector((1,0,0))
    u=(u-normal*u.dot(normal)).normalized();v=normal.cross(u)
    angle=math.radians(tilt);u,v=u*math.cos(angle)+v*math.sin(angle),v*math.cos(angle)-u*math.sin(angle)
    c=Vector(center)
    oriented_ellipsoid(name+' | armoured optical housing',c,u,v,normal,(rx+1,ry+1,2.9),'armor')
    oriented_ellipsoid(name+' | dark convex lens',c+normal*2.7,u,v,normal,(rx*.78,ry*.78,1.65),'dark')
    width=.75 if rx>4 else .55;vertices=[];faces=[]
    for i in range(40):
        a=i*math.tau/40
        for j in range(8):
            b=j*math.tau/8
            vertices.append(tuple(c+normal*(2.2+width*math.sin(b))
                                  +u*((rx+width*math.cos(b))*math.cos(a))
                                  +v*((ry+width*math.cos(b))*math.sin(a))))
            faces.append((i*8+j,i*8+(j+1)%8,((i+1)%40)*8+(j+1)%8,((i+1)%40)*8+j))
    rim=mesh(name+' | rolled optical rim',vertices,faces,trim);recalculate(rim)
    return {'name':name,'center_source':list(c),'normal_source':list(normal),
            'dark_probe_source':list(c+normal*4),'lens_radii':[rx*.78,ry*.78]}


def incision(obj,center,radii,latitude,start,end,width=.65):
    points=[shapes.sphere_point(center,radii,latitude,lon,.1) for lon in range(start,end+1,4)]
    cutter=shapes.tube('Recessed plate inscription cutter',points,width,'rust',8)
    recalculate(cutter);subtract(obj,cutter)


def settled_growth(name,center,radii,latitude,longitude,rx,ry):
    point=Vector(shapes.sphere_point(center,radii,latitude,longitude,0))
    normal=Vector(tuple((p-c)/(r*r) for p,c,r in zip(point,center,radii))).normalized()
    u=normal.cross(Vector((0,1,0))).normalized()
    if u.length<.1:u=Vector((1,0,0))
    v=normal.cross(u).normalized()
    # Tangential patches partly overlap the casing instead of hovering as flat pads.
    oriented_ellipsoid(name,point-normal*.4,u,v,normal,(rx,ry,1.2),'moss')


def torso():
    center,radii=(0,24,10),(28,33,24)
    body=ellipsoid('01 | Continuous massive plated torso',center,radii,'armor',56,36)
    # Shallow wear, not an open chest or a skeletal waist.
    damage(body,(22,18,-5),(3,5),5)
    for lat,start,end in [(-14,-105,110),(5,-90,85),(33,-70,75)]:incision(body,center,radii,lat,start,end,.75)
    for lon in (-65,-25,29,67):
        points=[shapes.sphere_point(center,radii,lat,lon,.1) for lat in range(-35,38,4)]
        cutter=tube('Vertical torso panel incision',points,[.65]*len(points),'rust',8);recalculate(cutter);subtract(body,cutter)
    for side in (-1,1):
        c=(side*29,31,10);r=(16,21,19)
        shoulder=ellipsoid('02 | Heavy protective shoulder casing',c,r,'armor',40,28)
        incision(shoulder,c,r,32,-115,100,.65)
        incision(shoulder,c,r,-12,-90,70,.7)
        for lat,lon in [(38,-48),(38,4),(38,54),(4,-70),(4,62)]:
            p=shapes.sphere_point(c,r,lat,lon,.25)
            ellipsoid('Shoulder plate rivet',p,(.85,.85,.85),'edge',12,8)
    # A broad covered posterior completes the obscured reference side.
    ellipsoid('Rear lower hip armour',(0,5,24),(21,13,13),'plate',36,24)
    for x in (-12,12):
        cylinder('Rear service coupler',(x,21,30),(x,21,35),4,'joint',20)
        shapes.arc('Rear service coupler rim',(x,21,35),(0,0,1),4.3,.75,'edge')
    for x in (-15,0,15):
        p=shapes.sphere_point(center,radii,-20,x*3,.3)
        ellipsoid('Lower torso fastening',p,(1.2,1.2,1),'edge',12,8)


def head():
    center,radii=(0,52,-1),(25,22,22)
    head=ellipsoid('03 | Broad integrated multi-optic head',center,radii,'armor',64,40)
    damage(head,(-19,68,-8),(2.8,3),5)
    for lat,start,end in [(48,-115,115),(64,-140,140)]:incision(head,center,radii,lat,start,end,.6)
    for lon in (-72,-10,10,72):
        points=[shapes.sphere_point(center,radii,lat,lon,.12) for lat in range(42,84,4)]
        cutter=shapes.tube('Crown engraved track',points,.58,'rust',8);recalculate(cutter);subtract(head,cutter)
    # Rear and temple plate boundaries never replace the six-lens front with a visor.
    for lon in (-122,122):
        # This fixed-axis tube frame is stable across the vertical meridian. The
        # legacy adaptive frame flips near vertical tangents and self-intersects.
        points=[shapes.sphere_point(center,radii,lat,lon,.12) for lat in range(-32,37,4)]
        cutter=tube('Temple panel incision',points,[.55]*len(points),'rust',8);recalculate(cutter);subtract(head,cutter)
    import bmesh
    bm=bmesh.new();bm.from_mesh(head.data)
    volume=bm.calc_volume();closed=all(edge.is_manifold for edge in bm.edges);bm.free()
    assert closed and volume>45000,f'Head mass damaged by Boolean detail: volume={volume}, closed={closed}'
    optics=[]
    for name,c,n,rx,ry,tilt in [
        ('Main left eye',(-13.5,59,-20),(-.30,.12,-1),6.6,4.8,-14),
        ('Main right eye',(13.5,58,-20.5),(.30,.10,-1),6.6,4.8,14),
        ('Upper left eye',(-5.2,67,-18),(-.12,.38,-1),2.8,2.5,-8),
        ('Upper right eye',(5.2,66.5,-18.5),(.12,.35,-1),2.8,2.5,8),
        ('Lower left cheek eye',(-13,43,-19),(-.25,-.15,-1),3,2.6,0),
        ('Lower right cheek eye',(13,42.5,-19),(.25,-.15,-1),3,2.6,0)]:
        optics.append(optic(name,c,n,rx,ry,tilt))
    # Protruding central muzzle with an arched vertical grille, matching the opening motif.
    before_muzzle=set(bpy.data.objects)
    muzzle=ellipsoid('04 | Bulky central grille housing',(0,47,-23),(11.5,12,10),'plate',48,32)
    subtract(muzzle,box('Arched grille recess',(0,46.5,-32),(15.5,18,12),'dark',4))
    box('Deep black grille chamber',(0,46.5,-28.7),(13,16,1.5),'dark',3)
    perimeter=[(-7.7,39,-32.5),(-8,47,-33),(-6.5,52.5,-32.8),(-3.5,55.6,-32),
               (0,56.4,-31.7),(3.5,55.6,-32),(6.5,52.5,-32.8),(8,47,-33),
               (7.7,39,-32.5),(-7.7,39,-32.5)]
    rim=shapes.catmull(perimeter,3)
    tube('Arched grille rolled edge',rim,[.8]*len(rim),'edge',10)
    grille=[]
    for i in range(-3,4):
        x=i*2.1;top=48+math.sqrt(max(0,7.5**2-x*x))
        cylinder('Vertical grille rib',(x,39.8,-33.1),(x,top,-33.1),.57,'joint',8)
        grille.append([x,46,-33.1])
    for x in (-4,4):
        points=[(x,54,-30),(x,57,-27),(x,58,-24)]
        shapes.tube('Muzzle incised-looking panel line',points,.48,'rust',6)
    # The reference's grille is subordinate to the broad face, not a giant mask
    # covering most of its height. Preserve the complete housing/rib assembly.
    pivot=Vector(xyz((0,47,-23)));factor=.82
    transform=Matrix.Translation(pivot)@Matrix.Scale(factor,4)@Matrix.Translation(-pivot)
    for obj in set(bpy.data.objects)-before_muzzle:obj.matrix_world=transform@obj.matrix_world
    grille=[[x*factor,47+(y-47)*factor,-23+(z+23)*factor] for x,y,z in grille]
    for lat,lon in [(72,-65),(72,65),(49,-88),(49,88),(22,-82),(22,82)]:
        p=shapes.sphere_point(center,radii,lat,lon,.3)
        ellipsoid('Head plate fastener',p,(.85,.85,.85),'edge',12,8)
    # Left temple port seen beside the rock; its opposing counterpart is an authored completion.
    for side in (-1,1):
        cylinder('Temple circular service cover',(side*22,51,0),(side*25.5,51,0),5,'plate',28)
        shapes.arc('Temple cover seam',(side*25.5,51,0),(1,0,0),4.8,.8,'edge')
    return optics,grille,volume


def limb(name,a,b):
    a,b=Vector(a),Vector(b);axis=(b-a).normalized()
    tapered(name+' | thick protected forearm',[a,a.lerp(b,.35),b],[8,9,8.5],'armor',24)
    # Only short banded joint sections are exposed between the enclosing shells.
    for t in (.08,.16,.25,.78,.90):
        p=a.lerp(b,t)
        cylinder(name+' | joint band',p-axis*.8,p+axis*.8,8.8 if t<.3 else 8.5,'joint',24)
        if t in (.08,.90):shapes.arc(name+' | metal cuff',p,axis,9.1,.8,'edge')
    return list(b)


def pincer(name,center,scale=1):
    center=Vector(center)
    def p(x,y,z):return center+Vector((x,y,z))*scale
    shell=ellipsoid(name+' | broad domed gripper casing',center,(13*scale,7*scale,14*scale),'armor',40,28)
    # Shallow concentric cut follows the shell instead of exposing a finger skeleton.
    incision(shell,tuple(center),(13*scale,7*scale,14*scale),30,-130,130,.55*scale)
    ports=[]
    for suffix,c,n,rx in [('central',p(0,6,-3),(0,.85,-.53),3.2),
                          ('outer',p(-6,4.5,3),(-.3,.9,-.2),2.5),
                          ('inner',p(6,4.5,3),(.3,.9,-.2),2.5)]:
        ports.append(optic(name+' | '+suffix+' hand port',c,n,rx*scale,rx*.85*scale))
    paths=[([(-9,-2,-8),(-11,-1,-18),(-7,-4,-28),(-1,-6,-32)],[3.9,3.3,1.8,.75]),
           ([(9,-2,-8),(11,-1,-18),(7,-4,-28),(1,-6,-32)],[3.9,3.3,1.8,.75]),
           ([(0,-4,-11),(0,-5,-18),(0,-6,-23)],[3,2, .8])]
    tips=[]
    for i,(path,widths) in enumerate(paths):
        samples=shapes.catmull([p(*q) for q in path],5);radii=[]
        for a,b in zip(widths,widths[1:]):radii.extend(scale*(a+(b-a)*t/5) for t in range(5))
        radii.append(widths[-1]*scale)
        obj=tapered(name+f' | curved blade tine {i+1}',samples,radii,'claw',10)
        # Flatten crosswise slightly for blade-like rather than cylindrical claw sections.
        for vertex in obj.data.vertices:
            vertex.co.z=center.y+(vertex.co.z-center.y)*.72
        tip=p(*path[-1]);tip.y=center.y+(tip.y-center.y)*.72;tips.append(list(tip))
        root=p(*path[0]);cylinder(name+' | pincer root bearing',root+Vector((-2,0,0))*scale,
                                  root+Vector((2,0,0))*scale,3.6*scale,'plate',16)
    return {'name':name,'center_source':list(center),'scale':scale,'ports':ports,'tine_tips_source':tips}


def main():
    reset({'armor':'b39a61','plate':'9c794e','edge':'bd935a','worn':'c3ac7e','rust':'66503a',
           'patina':'587560','joint':'45463b','dark':'102126','claw':'d0b47b',
           'moss':'56683b','growth':'405132'})
    shapes.RNG.seed(202610044)
    torso();optics,grille,head_volume=head()
    limb('Left',(-32,22,6),(-38,9,-19))
    limb('Right',(32,22,8),(36,8,-9))
    pincers=[pincer('Foreground left pincer',(-38,7,-31)),pincer('Right grounded pincer',(36,6,-21),.85)]
    for latitude,longitude,rx,ry in [(53,-126,3.8,3),(65,-100,3,2.5),(38,-112,2.8,4)]:
        settled_growth('Head casing settled growth',(0,52,-1),(25,22,22),latitude,longitude,rx,ry)
    settled_growth('Shoulder settled growth',(-29,31,10),(16,21,19),55,-35,4,3)
    settled_growth('Rear shoulder growth',(29,31,10),(16,21,19),38,100,3,4)
    for p,r in [((-44,9,-22),(4,2,6)),((30,8,-15),(3,1.5,4)),((-17,4,21),(7,2,6))]:
        ellipsoid('Localized settled growth',p,r,'moss',20,12)
    for x,z,w in [(-23,-18,4),(17,31,5),(44,7,4)]:
        obj=box('Small fallen casing fragment',(x,1,z),(w,2.5,w*.75),'plate',.5);obj.rotation_euler.z=.4
    deposits([(-16,10,24,27,3,0),(20,12,24,27,3.2,15),(-40,-29,18,24,2,-15),
              (36,-21,17,22,1.7,15)],8,(-62,62,-69,43))
    save('relics/colossus/design/small-colossus-v4.json',{
        'name':'Small Colossus V4 / Dormant Vigilant','reference':REFERENCE,'visual_acceptance':'V4 review pending',
        'revision_v4':{'primary_reference_segment_seconds':[0,4.5],
                       'reference_brief':'relics/colossus/docs/SMALL_COLOSSUS_V4_REFERENCE.md',
                       'direction':'Massive dormant plated specimen with multi-optic face and pincer hands',
                       'closed_source_head_volume':head_volume,
                       'head_optics':optics,'grille_rib_probes_source':grille,'pincers':pincers,
                       'solid_core_probes_source':[[0,20,10],[0,53,0]],
                       'body_connection_source':[0,20,10],'head_connection_source':[0,60,-5],
                       'continuous_body_source_y':[13,23,34],
                       'hidden_completion_authored':['back','second arm attachment','buried lower body','three-tine pincer anatomy'],
                       'archive_meshes_reused':0,'large_asset_meshes_reused':0},
        'new_relic_v1':{'family':'small-colossus','v5_interiors':False,'rewards_inherited':False}})


if __name__=='__main__':main()
