"""Generate the isolated 1.21.1 compatibility build; never alter 26.2 resources.

Loom performs the required named-to-intermediary remapping. This preparation
keeps the exact selected Alpha 4.9 NBT bytes and explicitly bridges older APIs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from integrate_relics import export_relics
from relic_catalog import ASSETS, ROOT, worldgen_resources

OUTPUT = ROOT / 'compat/mc1.21.1/build/generated'


def port_java(name: str, text: str) -> str:
    text = text.replace('net.minecraft.resources.Identifier', 'net.minecraft.resources.ResourceLocation')
    text = re.sub(r'\bIdentifier\b', 'ResourceLocation', text)
    text = text.replace('.lookupOrThrow(', '.registryOrThrow(')
    text = text.replace('.getMinY()', '.getMinBuildHeight()')
    text = text.replace('ChunkPos.pack(', 'ChunkPos.asLong(')
    text = text.replace('chunks.values().forEach(ChunkAccess::markUnsaved);',
                        'chunks.values().forEach(chunk -> chunk.setUnsaved(true));')
    text = text.replace('region.isWithinWriteZone(pos)', 'region.ensureCanWrite(pos)')
    text = text.replace('context.chunkPos().x()', 'context.chunkPos().x')
    text = text.replace('context.chunkPos().z()', 'context.chunkPos().z')
    text = text.replace('candidate.x()', 'candidate.x').replace('candidate.z()', 'candidate.z')
    if name == 'RelicWorldgen.java':
        # This preserved target is visual Alpha 4.9, not an unapproved gameplay backport.
        text = text.replace('        de.relics.gameplay.RelicItems.initialize();\n', '')
        text = text.replace('        de.relics.gameplay.RelicGameplay.initialize();\n', '')
        text = text.replace('public final class RelicWorldgen implements ModInitializer {',
            'public final class RelicWorldgen implements ModInitializer {\n'
            '    public static final net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType<TerrainSupportProcessor> TERRAIN_SUPPORT = () -> TerrainSupportProcessor.CODEC;')
        text = text.replace('TerrainSupportProcessor.CODEC);', 'TERRAIN_SUPPORT);')
        text = text.replace('.getValue(LithostitchedRegistries.', '.get(LithostitchedRegistries.')
        text = text.replace('PLACEMENT_CONDITION_TYPE.identifier()', 'PLACEMENT_CONDITION_TYPE.location()')
    if name == 'TerrainSupportProcessor.java':
        # Before 26.2 StructureProcessor is an abstract class, not an interface.
        text = text.replace(
            'public record TerrainSupportProcessor(int groundY, boolean supportArt, BlockState artFill, boolean rootSupport,\n'
            '        int maxSupportDepth, int surfaceContactDepth, boolean followArt) implements StructureProcessor {',
            'public final class TerrainSupportProcessor extends StructureProcessor {\n'
            '    private final int groundY, maxSupportDepth, surfaceContactDepth;\n'
            '    private final boolean supportArt, rootSupport, followArt;\n'
            '    private final BlockState artFill;\n'
            '    public TerrainSupportProcessor(int groundY, boolean supportArt, BlockState artFill, boolean rootSupport,\n'
            '            int maxSupportDepth, int surfaceContactDepth, boolean followArt) {\n'
            '        this.groundY = groundY; this.supportArt = supportArt; this.artFill = artFill;\n'
            '        this.rootSupport = rootSupport; this.maxSupportDepth = maxSupportDepth;\n'
            '        this.surfaceContactDepth = surfaceContactDepth; this.followArt = followArt;\n'
            '    }\n'
            '    public int groundY() { return groundY; }\n'
            '    public boolean supportArt() { return supportArt; }\n'
            '    public BlockState artFill() { return artFill; }\n'
            '    public boolean rootSupport() { return rootSupport; }\n'
            '    public int maxSupportDepth() { return maxSupportDepth; }\n'
            '    public int surfaceContactDepth() { return surfaceContactDepth; }\n'
            '    public boolean followArt() { return followArt; }')
        text = text.replace(
            "        // Minecraft 26.2 supplies only this chunk's cells unless a processor asks\n"
            '        // for the entire piece. Never read or write a neighbouring chunk here.',
            '        // 1.21.1 supplies the whole template. Clip before support reads/mask\n'
            '        // writes to preserve the 26.2 chunk-local behavior and avoid remote loads.\n'
            '        if (settings.getBoundingBox() != null) {\n'
            '            processed = processed.stream().filter(info -> settings.getBoundingBox().isInside(info.pos())).toList();\n'
            '        }')
        text = text.replace('public MapCodec<? extends StructureProcessor> codec() {\n        return CODEC;',
            'protected net.minecraft.world.level.levelgen.structure.templatesystem.StructureProcessorType<?> getType() {\n'
            '        return RelicWorldgen.TERRAIN_SUPPORT;')
    return text


def prepare(output: Path = OUTPUT) -> dict:
    metadata = json.loads((ROOT / 'compat/mc1.21.1/visual-alpha49.fabric.mod.json').read_bytes())
    if metadata['version'] != '0.1.0-alpha.4.9':
        raise ValueError('This compatibility profile is pinned to visual Alpha 4.9')
    resources = output / 'resources'
    resources.mkdir(parents=True, exist_ok=True)
    manifest = export_relics(resources / 'data/relics/structure', resources / 'relics.integration.json')
    manifest['compatibility_target'] = '1.21.1'
    manifest['template_identity'] = 'exact Alpha 4.9 raw and derived natural bytes; no DataVersion restamping'
    metadata['depends'].update(minecraft='1.21.1', java='>=21', fabricloader='>=0.19.5')
    metadata['depends'].pop('fabric-resource-loader-v1')
    metadata['depends']['fabric-resource-loader-v0'] = '*'
    mixins = {'required': True, 'package': 'de.relics.mixin',
              'mixins': ['StructureTemplateMixin', 'WorldGenRegionMixin', 'OreFeatureMixin'],
              'injectors': {'defaultRequire': 1}}
    # Loom 1.17 statically remaps mixin selectors; there is no legacy refmap.
    mixins.update(compatibilityLevel='JAVA_21')
    files = {
        'fabric.mod.json': metadata,
        'pack.mcmeta': {'pack': {'pack_format': 48, 'description': 'Relic Mod Alpha 4.9 for Minecraft 1.21.1'}},
        'relics.mixins.json': mixins,
        'relics.integration.json': manifest,
    }
    for name, data in worldgen_resources().items():
        # Optional biome entries remain optional. The game validates the older
        # jigsaw/placement codecs at runtime; no terrain/density policy is changed.
        files['data/relics/' + name] = data
    for name, data in files.items():
        path = resources / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')
    sources = []
    visual_sources = {'AllGridPlacementCondition.java', 'DryLandPlacementCondition.java',
                      'SeparatedPlacementCondition.java', 'TerrainSupportProcessor.java',
                      'RelicWorldgen.java', 'RelicProtection.java', 'ProtectedCells.java',
                      'StructureTemplateMixin.java', 'WorldGenRegionMixin.java', 'OreFeatureMixin.java'}
    for source in sorted((ROOT / 'src/main/java').rglob('*.java')):
        if source.name not in visual_sources:
            continue
        path = output / 'java' / source.relative_to(ROOT / 'src/main/java')
        path.parent.mkdir(parents=True, exist_ok=True)
        content = port_java(source.name, source.read_text(encoding='utf-8'))
        if source.name == 'TerrainSupportProcessor.java' and 'public final class TerrainSupportProcessor extends StructureProcessor' not in content:
            raise ValueError('Processor source shape changed; review the legacy adapter before building')
        path.write_text(content, encoding='utf-8', newline='\n')
        sources.append({'path': path.relative_to(output).as_posix(),
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    test_source = ROOT / 'src/test/java/de/relics/WorldgenTests.java'
    tests = port_java(test_source.name, test_source.read_text(encoding='utf-8'))
    tests = tests.replace('case "getMinY"', 'case "getMinBuildHeight"')
    tests = tests.replace('result.size() == 1 && reads.get() == before', 'result.isEmpty() && reads.get() == before')
    path = output / 'test/de/relics/WorldgenTests.java'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tests, encoding='utf-8', newline='\n')
    return {'minecraft': '1.21.1', 'java_release': 21, 'structures': list(ASSETS), 'sources': sources}


if __name__ == '__main__':
    print(json.dumps(prepare(), indent=2))
