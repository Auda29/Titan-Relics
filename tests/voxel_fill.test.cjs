const { test } = require('node:test');
const assert = require('node:assert/strict');
const { enclosedCells } = require('../tools/voxel_fill.cjs');

function shell(offset = [0, 0, 0]) {
    const cells = [];
    for (let x = 0; x < 5; ++x) for (let y = 0; y < 5; ++y) for (let z = 0; z < 5; ++z) {
        if ([x, y, z].some(v => v === 0 || v === 4)) cells.push([x+offset[0], y+offset[1], z+offset[2]]);
    }
    return cells;
}

test('fills two sealed chambers at negative offsets without bridging exterior space', () => {
    const cells = enclosedCells([...shell([-9, -5, -3]), ...shell([3, 2, 1])]);
    assert.equal(cells.length, 54);
    assert(cells.some(p => p.join() === '-7,-3,-1'));
    assert(cells.some(p => p.join() === '5,4,3'));
    assert(cells.every(p => (p[0] > -9 && p[0] < -5) || (p[0] > 3 && p[0] < 7)));
});

test('an opening drains the connected chamber; sealed neighbour stays filled', () => {
    const open = shell().filter(p => p.join() !== '2,2,0');
    assert.equal(enclosedCells(open).length, 0);
    assert.equal(enclosedCells([...open, ...shell([8, 0, 0])]).length, 27);
});

test('thin plates and empty input have no interior', () => {
    assert.deepEqual(enclosedCells([]), []);
    assert.deepEqual(enclosedCells([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]]), []);
    assert.throws(() => enclosedCells([[0.5, 0, 0]]), /integer/);
});
