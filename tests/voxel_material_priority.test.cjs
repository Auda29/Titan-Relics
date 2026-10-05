const test = require('node:test');
const assert = require('node:assert/strict');
const { withMaterialPriority } = require('../tools/voxel_material_priority.cjs');

const wood = { r: .3, g: .2, b: .1, a: 1 };
const leaf = { r: .1, g: .4, b: .1, a: 1 };
const position = { copy() { return this; }, round() { return this; }, hash() { return 7; } };
class Mesh {
    constructor() { this._voxels = new Map(); }
    addVoxel(p, colour) { if (!this._voxels.has(p.hash())) this._voxels.set(p.hash(), { colour }); }
}

test('wood survives either leaf/wood hit order without adding cells; legacy conversion stays first-hit', () => {
    for (const order of [[leaf, wood, leaf], [wood, leaf]]) {
        const result = withMaterialPriority(Mesh, [wood], () => {
            const mesh = new Mesh();
            order.forEach(c => mesh.addVoxel(position, c));
            return mesh;
        });
        assert.equal(result.mesh._voxels.size, 1);
        assert.deepEqual(result.mesh._voxels.get(7).colour, wood);
    }
    const legacy = new Mesh();
    legacy.addVoxel(position, leaf); legacy.addVoxel(position, wood);
    assert.deepEqual(legacy._voxels.get(7).colour, leaf);
});

test('failed conversion restores the original upstream method', () => {
    const original = Mesh.prototype.addVoxel;
    assert.throws(() => withMaterialPriority(Mesh, [wood], () => { throw Error('failed input'); }), /failed input/);
    assert.equal(Mesh.prototype.addVoxel, original);
});
