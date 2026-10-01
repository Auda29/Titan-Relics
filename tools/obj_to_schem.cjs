#!/usr/bin/env node
/* Local adapter for ObjToSchematic 1.0 (BSD-3-Clause). No upstream edits needed.
 * Usage: node tools/obj_to_schem.cjs config.json
 * Solid named materials only; the palette supplies their exact atlas colours.
 */
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const { execFileSync } = require('node:child_process');
const crypto = require('node:crypto');

async function main() {
    if (process.argv.length !== 3) throw new Error('Usage: node tools/obj_to_schem.cjs config.json');
    const configPath = path.resolve(process.argv[2]);
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const root = path.resolve(__dirname, '..');
    const repo = path.resolve(root, config.repository);
    const input = path.resolve(root, config.input);
    const output = path.resolve(root, config.output);
    if (input === output) throw new Error('Input and output must differ');
    if (path.extname(input) !== '.obj' || path.extname(output) !== '.schem') {
        throw new Error('Expected .obj input and .schem output');
    }
    const commit = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: repo, encoding: 'utf8' }).trim();
    if (config.commit && commit !== config.commit) throw new Error(`Expected upstream ${config.commit}, found ${commit}`);
    if (!Number.isInteger(config.height) || config.height < 3 || config.height > 380) {
        throw new Error('Height must be an integer from 3 to 380');
    }
    const upstream = createRequire(path.join(repo, 'package.json'));
    upstream('ts-node').register({
        transpileOnly: true,
        project: path.join(repo, 'tsconfig.json'),
        compilerOptions: { target: 'ES2020', module: 'commonjs' },
    });
    // Webpack normally imports this as raw text; Node needs the equivalent loader.
    for (const extension of ['.atlas', '.fs', '.vs']) {
        require.extensions[extension] = (module, filename) => {
            module.exports = fs.readFileSync(filename, 'utf8');
        };
    }
    require.extensions['.png'] = (module, filename) => { module.exports = filename; };
    const load = name => require(path.join(repo, 'src', name));
    const { ObjImporter } = load('importers/obj_importer.ts');
    const { MaterialType } = load('mesh.ts');
    const { Atlas } = load('atlas.ts');
    const { VoxeliserFactory } = load('voxelisers/voxelisers.ts');
    const { BlockMesh } = load('block_mesh.ts');
    const { SchemExporter } = load('exporters/schem_exporter.ts');
    const { ColourSpace } = load('util.ts');
    const { AppConstants } = load('constants.ts');
    const { StatusHandler } = load('status.ts');
    const { AppPaths } = load('util/path_util.ts');
    AppPaths.Get.setBaseDir(repo);
    const { locales } = require(path.join(repo, 'loc/base.ts'));
    await upstream('i18next').init({
        lng: 'en-GB', fallbackLng: 'en-GB',
        resources: Object.fromEntries(locales.map(locale => [locale.language_code, { translation: locale.translations }])),
    });
    const atlas = Atlas.load('vanilla');
    const palette = [...new Set(Object.values(config.materials))];
    for (const block of palette) {
        if (!atlas.hasBlock(block)) throw new Error(`Block absent from legacy atlas: ${block}`);
    }
    const source = fs.readFileSync(input, 'utf8');
    const mesh = await new ObjImporter().import({ name: input, text: async () => source });
    const materials = new Map();
    for (const tri of mesh._tris) {
        const block = config.materials[tri.material];
        if (!block) throw new Error(`Unmapped OBJ material: ${tri.material}`);
        materials.set(tri.material, {
            type: MaterialType.solid, colour: { ...atlas.getBlocks().get(block).colour },
            canBeTextured: false, needsAttention: false,
        });
    }
    mesh.setMaterials(materials);
    mesh.processMesh(0, 0, 0);
    console.log(`Imported ${mesh.getTriangleCount()} triangles, ${materials.size} materials`);
    const voxelOptions = {
        constraintAxis: 'y', voxeliser: 'bvh-ray', size: config.height,
        useMultisampleColouring: false, voxelOverlapRule: 'first',
        enableAmbientOcclusion: false,
    };
    const voxels = VoxeliserFactory.GetVoxeliser(voxelOptions.voxeliser).voxelise(mesh, voxelOptions);
    let filledVoxels = 0;
    if (config.fill_enclosed) {
        const block = config.materials[config.fill_enclosed];
        if (!block) throw new Error(`Unmapped fill material: ${config.fill_enclosed}`);
        const { enclosedCells } = require('./voxel_fill.cjs');
        const { Vector3 } = load('vector.ts');
        const fill = enclosedCells(voxels.getVoxels().map(v => [v.position.x, v.position.y, v.position.z]));
        for (const p of fill) voxels.addVoxel(new Vector3(...p), atlas.getBlocks().get(block).colour);
        filledVoxels = fill.length;
        console.log(`Filled ${filledVoxels} enclosed voxels with ${block}`);
    }
    voxels.calculateNeighbours();
    const blocks = BlockMesh.createFromVoxelMesh(voxels, {
        textureAtlas: 'vanilla', blockPalette: palette,
        dithering: 'off', ditheringMagnitude: 0, colourSpace: ColourSpace.RGB,
        fallable: 'replace-falling', resolution: 255, calculateLighting: false,
        lightThreshold: 0, contextualAveraging: false, errorWeight: 0,
    });
    const exported = new SchemExporter().export(blocks);
    fs.mkdirSync(path.dirname(output), { recursive: true });
    fs.writeFileSync(output, exported.content);
    const counts = {};
    for (const block of blocks.getBlocks()) {
        const name = block.blockInfo.name;
        counts[name] = (counts[name] || 0) + 1;
    }
    const report = {
        upstream: 'https://github.com/LucasDower/ObjToSchematic',
        commit,
        node: process.version, input: config.input, output: config.output,
        source_sha256: crypto.createHash('sha256').update(source).digest('hex'),
        schematic_sha256: crypto.createHash('sha256').update(exported.content).digest('hex'),
        height: config.height, triangles: mesh.getTriangleCount(),
        data_version: AppConstants.DATA_VERSION, voxel_options: voxelOptions,
        materials: config.materials, colour_resolution: 255, dithering: 'off', blocks: counts,
        fill_enclosed: config.fill_enclosed || null, filled_voxels: filledVoxels,
        note: config.fill_enclosed ? 'Surface voxelisation plus explicit sealed-volume fill; no worldgen integration.'
            : 'Surface voxelisation. No solid filling, interior-air classification or worldgen integration.',
    };
    fs.writeFileSync(output.replace(/\.schem$/, '') + '.ots.json', JSON.stringify(report, null, 2) + '\n');
    for (const message of StatusHandler.getAll()) {
        if (message.type === 'error') throw new Error(message.text);
        if (message.type === 'warning') console.warn(message.text);
    }
    StatusHandler.Get.clear();
    console.log(`${output}: ${blocks.getBlocks().length} blocks, DataVersion ${report.data_version}`);
}

main().catch(error => { console.error(error); process.exitCode = 1; });
