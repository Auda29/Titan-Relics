const assert = require('node:assert/strict');
const { test } = require('node:test');
const { proxyMap, remapBlocks } = require('../tools/material_proxy.cjs');

test('semantic terrain remapping keeps bone untouched and prevents buried grass/floating sand', () => {
    const mapping = proxyMap({ bone: 'minecraft:bone_block', turf: 'minecraft:grass_block[snowy=false]',
        fill: 'minecraft:dirt', sand: 'minecraft:sand', support: 'minecraft:sandstone' },
    { turf: 'minecraft:lime_concrete', sand: 'minecraft:magenta_concrete' });
    const block = (x,y,z,name) => ({ voxel: { position: {x,y,z} }, blockInfo: { name } });
    const input = [block(0,0,0,'minecraft:lime_concrete'), block(0,1,0,'minecraft:bone_block'),
        block(2,0,0,'minecraft:lime_concrete'), block(4,0,0,'minecraft:magenta_concrete'),
        block(4,1,0,'minecraft:magenta_concrete')];
    const result = remapBlocks(input, mapping, { 'minecraft:grass_block[snowy=false]':'minecraft:dirt' },
        { 'minecraft:sand':'minecraft:sandstone' });
    assert.deepEqual(result.blocks.map(b=>b.blockInfo.name), ['minecraft:dirt','minecraft:bone_block',
        'minecraft:grass_block[snowy=false]','minecraft:sandstone','minecraft:sand']);
    assert.equal(input[0].blockInfo.name, 'minecraft:lime_concrete');
    assert.deepEqual(result.blocks.map(b=>b.voxel),input.map(b=>b.voxel));
    assert.equal(result.coveredCount,1);
    assert.equal(result.unsupportedCount,1);
});

test('rejects ambiguous proxies and targets outside the declared palette', () => {
    assert.throws(()=>proxyMap({a:'minecraft:dirt',b:'minecraft:sand'},
        {a:'minecraft:lime_concrete',b:'minecraft:lime_concrete'}), /Ambiguous/);
    assert.throws(()=>remapBlocks([],proxyMap({a:'minecraft:dirt'}),{'minecraft:dirt':'minecraft:air'}), /outside/);
});
