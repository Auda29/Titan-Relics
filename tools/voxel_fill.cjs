/* Six-connected exterior flood fill. Only sealed empty regions become solid.
 * Coordinates are integer XYZ; the one-cell exterior margin is intentional.
 */
function enclosedCells(positions) {
    if (!positions.length) return [];
    const low = [Infinity, Infinity, Infinity], high = [-Infinity, -Infinity, -Infinity];
    for (const pos of positions) {
        if (pos.length !== 3 || pos.some(v => !Number.isSafeInteger(v))) throw new Error('Expected integer XYZ coordinates');
        for (let i = 0; i < 3; ++i) {
            low[i] = Math.min(low[i], pos[i]-1);
            high[i] = Math.max(high[i], pos[i]+1);
        }
    }
    const [sx, sy, sz] = high.map((v, i) => v-low[i]+1);
    const volume = sx*sy*sz, plane = sx*sz;
    if (!Number.isSafeInteger(volume) || volume > 32_000_000) throw new Error('Solid fill exceeds 32 million cells');
    const state = new Uint8Array(volume), queue = new Uint32Array(volume);
    const index = (x, y, z) => x+z*sx+y*plane;
    for (const p of positions) state[index(p[0]-low[0], p[1]-low[1], p[2]-low[2])] = 1;
    let head = 0, tail = 1;
    queue[0] = 0;
    state[0] = 2;
    function visit(i) {
        if (state[i] === 0) { state[i] = 2; queue[tail++] = i; }
    }
    while (head < tail) {
        const i = queue[head++];
        const x = i%sx, z = Math.floor(i/sx)%sz, y = Math.floor(i/plane);
        if (x > 0) visit(i-1);
        if (x+1 < sx) visit(i+1);
        if (z > 0) visit(i-sx);
        if (z+1 < sz) visit(i+sx);
        if (y > 0) visit(i-plane);
        if (y+1 < sy) visit(i+plane);
    }
    const filled = [];
    for (let i = 0; i < volume; ++i) {
        if (state[i] === 0) filled.push([i%sx+low[0], Math.floor(i/plane)+low[1], Math.floor(i/sx)%sz+low[2]]);
    }
    return filled;
}

module.exports = { enclosedCells };
