"""Low, broken deposit fields with explicit burial and low-contact preservation."""
from deposit_relief import noise


def sculpt(blocks,ground,materials,*,moss_pads=False):
    """Preserve art coordinates; lower soil cores, not just their outer margins.

    Low root/body contacts are retained. Soil beneath elevated crania is allowed
    to disappear: those arches must no longer force a 25-block-high pedestal.
    Tree moss pads are a separately declared ground-only edit; wood is never soil.
    """
    terrain={v for k,v in materials.items() if k.startswith('terrain_')}
    terrain-={v for k,v in materials.items() if not k.startswith('terrain_')}
    def mutable(p,s):return s in terrain or (moss_pads and s==materials['moss'] and p[1]<=ground+5)
    ground_cells={p:s for p,s in blocks.items() if mutable(p,s)}
    art={p:s for p,s in blocks.items() if not mutable(p,s)}
    columns={}
    for x,y,z in ground_cells:columns.setdefault((x,z),[]).append(y)
    contacts={}
    for x,y,z in art:
        below=(x,y-1,z)
        if y<=ground+2 and below in ground_cells:
            contacts[x,z]=max(y-1,contacts.get((x,z),y-1))
    result=dict(art)
    for (x,z),ys in columns.items():
        # A thin, non-concentric surface around the buried relic. Most outer
        # former deposits finish below nominal ground and disappear into terrain.
        target=ground-2+int(4*noise(x+41,z-13,13))
        target=max(target,contacts.get((x,z),target))
        top=min(max(ys),target)
        for y in ys:
            if y<=top:result[x,y,z]=materials['terrain_fill']
        if (x,top,z) in result and (x,top,z) not in art:
            patch=noise(x-29,z+11,7)
            cap=materials['terrain_patch'] if patch>.65 else materials['terrain_top']
            if moss_pads and patch>.52 and any(ground_cells[x,y,z]==materials['moss'] for y in ys):
                cap=materials['moss']
            if cap in ('minecraft:gravel','minecraft:sand') and (x,top-1,z) not in result:
                cap=materials['terrain_fill']
            result[x,top,z]=cap
    assert all(result.get(p)==s for p,s in art.items())
    assert all((x,y,z) in result for (x,z),y in contacts.items())
    stats={'algorithm':'low-core-embedding-v3','terrain_states':sorted(terrain),'low_moss_pads_reworked':moss_pads,
        'immutable_art_cells':len(art),'immutable_art_cells_identical':True,
        'authored_low_contact_columns':len(contacts),'authored_low_contacts_preserved':True,
        'removed_cells':len(blocks.keys()-result.keys()),
        'changed_surface_states':sum(s!=blocks.get(p) for p,s in result.items()),
        'max_ground_above_nominal':max((p[1]-ground for p in result if p not in art),default=0)}
    assert stats['max_ground_above_nominal']<=1
    return result,art,stats
