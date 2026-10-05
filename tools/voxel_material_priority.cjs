/* Keep structural materials when two source surfaces occupy the same voxel.
 * Scoped to one conversion; the upstream checkout and legacy first-hit rule stay intact.
 */
const key = c => JSON.stringify([c.r, c.g, c.b, c.a]);

function withMaterialPriority(VoxelMesh, colours, run) {
    const preferred = new Set(colours.map(key));
    const original = VoxelMesh.prototype.addVoxel;
    let replacements = 0;
    VoxelMesh.prototype.addVoxel = function (position, colour) {
        const existing = this._voxels.get(position.copy().round().hash());
        if (existing && preferred.has(key(colour)) && !preferred.has(key(existing.colour))) {
            existing.colour = { ...colour };
            replacements++;
        } else {
            original.call(this, position, colour);
        }
    };
    try {
        return { mesh: run(), replacements };
    } finally {
        VoxelMesh.prototype.addVoxel = original;
    }
}

module.exports = { withMaterialPriority };
