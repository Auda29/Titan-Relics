import gzip
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from relic_assets import AIR, colossus, obelisk, decode_nbt, encode_structure, export_models, tiles


def restore(root):
    palette=[]
    for block in root["palette"]:
        text=block["Name"]
        if "Properties" in block:
            text+="["+",".join(k+"="+v for k,v in block["Properties"].items())+"]"
        palette.append(text)
    return {tuple(b["pos"]):palette[b["state"]] for b in root["blocks"]}


class AssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models=[obelisk(),colossus()]

    def test_nbt_roundtrip_preserves_states_air_and_omissions(self):
        fixture={(0,0,0):"minecraft:stone",(1,1,1):AIR,(2,1,0):"minecraft:oak_leaves[persistent=true,distance=1]"}
        data=encode_structure(fixture,(3,3,3),4903)
        root=decode_nbt(data)
        self.assertEqual(root["DataVersion"],4903)
        self.assertEqual(root["size"],[3,3,3])
        self.assertEqual(root["entities"],[])
        self.assertEqual(restore(root),fixture)
        self.assertNotIn((2,2,2),restore(root))
        self.assertEqual(data[4:8],b"\0\0\0\0")
        self.assertEqual(data[9],255, "Gzip OS metadata must not depend on Python or host OS")
        self.assertRaises(ValueError,decode_nbt,gzip.decompress(data)[:-1])

    def test_rigid_tiles_reconstruct_exact_complete_model(self):
        for model in self.models:
            recovered={}
            for origin,size,blocks in tiles(model,32):
                self.assertTrue(all(0<v<=32 for v in size))
                decoded=restore(decode_nbt(encode_structure(blocks,size,4903)))
                for p,b in decoded.items():
                    self.assertTrue(all(0<=v<limit for v,limit in zip(p,size)))
                    whole=tuple(v+o for v,o in zip(p,origin))
                    self.assertNotIn(whole,recovered)
                    recovered[whole]=b
            self.assertEqual(recovered,model.blocks)

    def test_exports_are_reproducible_and_hashes_match_files(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"a"; b=Path(d)/"b"
            first=export_models(a,4903,single_template=True)
            second=export_models(b,4903,single_template=True)
            self.assertEqual(first,second)
            for entry in first["structures"]:
                for tile in entry["tiles"]:
                    data=(a/tile["path"]).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(),tile["sha256"])
                    self.assertEqual(data,(b/tile["path"]).read_bytes())
                full=entry["single_template"]
                self.assertEqual(hashlib.sha256((a/full["path"]).read_bytes()).hexdigest(),full["sha256"])

    def test_player_can_walk_from_outside_to_machine_room(self):
        model=self.models[1]
        start=tuple(model.landmarks["entrance"]); goal=tuple(model.landmarks["machine_room"])
        def standable(p):
            x,y,z=p
            return (model.blocks.get(p)==AIR and model.blocks.get((x,y+1,z))==AIR
                    and model.blocks.get((x,y-1,z),AIR)!=AIR)
        visited={start}; queue=[start]
        while queue:
            x,y,z=queue.pop()
            for p in ((x-1,y,z),(x+1,y,z),(x,y,z-1),(x,y,z+1)):
                if p not in visited and standable(p): visited.add(p); queue.append(p)
        self.assertIn(goal,visited)
        # Entire authored passage has player height clearance, including tile seams.
        for z in range(start[2],45): self.assertTrue(standable((40,10,z)),z)
        self.assertGreater(len(visited),250)

    def test_design_constraints_and_seed_variation(self):
        ob,co=self.models
        self.assertEqual(ob.landmarks["shaft"]["size"],[7,64,7])
        self.assertEqual(sum(y==69 for x,y,z in ob.blocks),49)
        self.assertGreater(sum(b==AIR for b in ob.blocks.values()),70)
        self.assertEqual(co.blocks[(40,26,23)],AIR)
        self.assertNotEqual(co.blocks,colossus(2914).blocks)
        for model in self.models:
            self.assertTrue(all(b.startswith("minecraft:") for b in model.blocks.values()))
            self.assertLess(len(model.blocks),model.size[0]*model.size[1]*model.size[2])
            for (x,y,z),b in model.blocks.items():
                self.assertTrue(0<=x<model.size[0] and 0<=y<model.size[1] and 0<=z<model.size[2])
                if "leaves" in b: self.assertIn("persistent=true",b)

    def test_worn_approach_preserves_terrain_before_the_short_entrance(self):
        model=self.models[1]
        self.assertEqual(model.landmarks["entrance"],[40,10,14])
        self.assertFalse(any(b==AIR and z<14 for (x,y,z),b in model.blocks.items()))
        for z in range(14,24):
            for x in range(39,42):
                self.assertNotEqual(model.blocks[(x,9,z)],AIR)
                self.assertEqual(model.blocks[(x,10,z)],AIR)
                self.assertNotEqual(model.blocks[(x,8,z)],AIR)
        # Terrain decoration can grow plants on moss even with random ticks off.
        for z in range(23,45):
            for x in range(37,44):
                self.assertNotIn(model.blocks[(x,9,z)],
                                 {"minecraft:moss_block","minecraft:grass_block","minecraft:dirt"})
        self.assertLess(sum(y==9 and z<23 and 35<=x<=45 and "deepslate" in b
                            for (x,y,z),b in model.blocks.items()),100)

    def test_breaches_expose_frame_without_blocking_machine_room(self):
        model=self.models[1]
        self.assertEqual(model.blocks[(48,61,33)],AIR)
        self.assertEqual(model.blocks[(57,34,30)],AIR)
        self.assertIn("basalt",model.blocks[(57,34,36)])
        self.assertEqual(model.blocks[(40,10,40)],AIR)
        self.assertGreater(sum(b=="minecraft:moss_block" for b in model.blocks.values()),200)


if __name__=="__main__": unittest.main()
