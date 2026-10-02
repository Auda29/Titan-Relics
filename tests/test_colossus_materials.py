"""Check palette-only conservation, localized salvage and independent schematic reading."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from colossus_materials import encode_schematic,remap,preserve_connections,components
from schem_to_nbt import read_schematic


class MaterialStudyTests(unittest.TestCase):
    def test_salvage_keeps_support_bridge_and_does_not_join_existing_fragments(self):
        base={(x,0,0) for x in range(9)}|{(4,y,0) for y in range(1,6)}
        base|={(20,0,0),(21,0,0)}
        proposed={(x,0,0) for x in range(2,7)}|{(4,1,0),(4,2,0),(20,0,0),(21,0,0)}
        removable,protected=preserve_connections(base,proposed,1)
        self.assertTrue({(4,1,0),(4,2,0)}<=protected)
        self.assertTrue({(20,0,0),(21,0,0)}<=removable)
        self.assertEqual(len(components(base-removable)),1)
        self.assertEqual(removable|protected,proposed)

    def test_disconnected_metal_is_not_retained_to_fill_quota(self):
        copper="minecraft:cut_copper"
        blocks={(0,0,0):copper,(1,0,0):copper,(5,0,0):copper,(6,0,0):"minecraft:moss_block"}
        spec={"replacements":{copper:"minecraft:terracotta"},"salvage_zones":[
            {"name":"test","family":"copper","center_source":[0,0,0],"radius_source":8,"max_blocks":3}]}
        design={"source_bounds_blender":[[0,0,0],[7,0,1]],"blocks_per_source_unit":1}
        result,zones=remap(blocks,design,spec)
        self.assertEqual(result.keys(),blocks.keys())
        self.assertEqual(result[(5,0,0)],"minecraft:terracotta")
        self.assertEqual(result[(6,0,0)],"minecraft:moss_block")
        self.assertEqual(zones[0]["blocks"],2)
        self.assertEqual(blocks[(5,0,0)],copper)

    def test_schematic_round_trip_preserves_axes_air_offset_and_multibyte_palette(self):
        blocks={(i%13,i//13,1):f"minecraft:test_{i}" for i in range(140)}
        blocks[(12,11,2)]="minecraft:bone_block[axis=z]"
        size=(13,12,3);offset=[-19,7,23]
        encoded=encode_schematic(blocks,size,3105,offset)
        actual=read_schematic(encoded,"omit")
        self.assertEqual(actual,(size,blocks,3105,offset))
        self.assertEqual(encoded,encode_schematic(blocks,size,3105,offset))


if __name__=="__main__": unittest.main()
