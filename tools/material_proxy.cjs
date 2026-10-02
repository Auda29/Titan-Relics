/* Exact semantic material mapping after atlas-based voxelization.
 * Proxies isolate terrain from bone/stone materials even when final palettes overlap.
 */
const STATE = /^[a-z0-9_.-]+:[a-z0-9_./-]+(?:\[[a-z0-9_]+=[a-z0-9_]+(?:,[a-z0-9_]+=[a-z0-9_]+)*\])?$/;

function proxyMap(materials, proxies = {}) {
    const mapping = new Map();
    for (const [material, target] of Object.entries(materials)) {
        if (!STATE.test(target)) throw new Error(`Invalid target state: ${target}`);
        const proxy = proxies[material] || target;
        if (mapping.has(proxy) && mapping.get(proxy) !== target) {
            throw new Error(`Ambiguous proxy ${proxy}`);
        }
        mapping.set(proxy, target);
    }
    for (const material of Object.keys(proxies)) {
        if (!(material in materials)) throw new Error(`Unknown proxy material: ${material}`);
    }
    return mapping;
}

function remapBlocks(blocks, mapping, covered = {}, unsupported = {}) {
    const key = p => `${p.x},${p.y},${p.z}`;
    const occupied = new Set(blocks.map(b => key(b.voxel.position)));
    const allowed = new Set(mapping.values());
    for (const rule of [covered, unsupported]) {
        for (const [from, to] of Object.entries(rule)) {
            if (!allowed.has(from) || !allowed.has(to)) throw new Error(`Replacement outside palette: ${from} -> ${to}`);
        }
    }
    let coveredCount = 0, unsupportedCount = 0;
    const result = blocks.map(block => {
        const p = block.voxel.position;
        let name = mapping.get(block.blockInfo.name);
        if (!name) throw new Error(`Unmapped voxel material: ${block.blockInfo.name}`);
        if (covered[name] && occupied.has(`${p.x},${p.y+1},${p.z}`)) {
            name = covered[name];
            coveredCount++;
        }
        if (unsupported[name] && !occupied.has(`${p.x},${p.y-1},${p.z}`)) {
            name = unsupported[name];
            unsupportedCount++;
        }
        return { ...block, blockInfo: { ...block.blockInfo, name } };
    });
    return { blocks: result, coveredCount, unsupportedCount };
}

module.exports = { proxyMap, remapBlocks };
