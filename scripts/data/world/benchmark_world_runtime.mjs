import { readFile, readdir } from 'node:fs/promises'
import { gzipSync, brotliCompressSync, constants } from 'node:zlib'
import { performance } from 'node:perf_hooks'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { stripTypeScriptTypes } from 'node:module'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../../..')
const cdfPath = resolve(root, 'data/production/world/world-income-cdf-2024.json')
const bytes = await readFile(cdfPath)

const parseTimesMs = []
let document
for (let iteration = 0; iteration < 5; iteration += 1) {
  const start = performance.now()
  document = JSON.parse(bytes.toString('utf8'))
  parseTimesMs.push(performance.now() - start)
}
parseTimesMs.sort((left, right) => left - right)

const welfare = Float64Array.from(document.points, (point) => Number(point[0]))
const cumulative = Float64Array.from(document.points, (point) => Number(point[1]))
const total = cumulative.at(-1)

function firstIndexAtLeast(target) {
  let low = 0
  let high = welfare.length
  while (low < high) {
    const middle = low + Math.floor((high - low) / 2)
    if (welfare[middle] < target) low = middle + 1
    else high = middle
  }
  return low
}

let checksum = 0
const lookupStart = performance.now()
for (let index = 0; index < 100_000; index += 1) {
  const target = welfare[index % welfare.length]
  const position = firstIndexAtLeast(target)
  const below = position === 0 ? 0 : cumulative[position - 1]
  checksum += below / total
}
const lookupMs = performance.now() - lookupStart

const runtimeSources = await Promise.all(
  ['src/world/domain.ts', 'src/world/loader.ts'].map(async (relativePath) => ({
    relativePath,
    source: await readFile(resolve(root, relativePath), 'utf8'),
  })),
)
const transpiledRuntime = runtimeSources.map(({ relativePath, source }) => (
  `// ${relativePath}\n${stripTypeScriptTypes(source, { mode: 'transform', sourceMap: false })}`
)).join('\n')
const runtimeBytes = Buffer.from(transpiledRuntime)

const distAssets = resolve(root, 'dist/assets')
let activeBundleContainsWorldRuntime = false
try {
  const assets = await readdir(distAssets)
  for (const asset of assets.filter((name) => name.endsWith('.js'))) {
    const content = await readFile(resolve(distAssets, asset), 'utf8')
    if (content.includes('world-income-engine-manifest.json')) activeBundleContainsWorldRuntime = true
  }
} catch {
  // O build é uma precondição opcional somente para medir inclusão no bundle ativo.
}

process.stdout.write(`${JSON.stringify({
  cdf: {
    rawSizeBytes: bytes.byteLength,
    gzipSizeBytes: gzipSync(bytes, { level: 9 }).byteLength,
    brotliSizeBytes: brotliCompressSync(bytes, {
      params: { [constants.BROTLI_PARAM_QUALITY]: 11 },
    }).byteLength,
    parseMedianMs: parseTimesMs[2],
    parseRunsMs: parseTimesMs,
  },
  lookup: { count: 100_000, elapsedMs: lookupMs, checksum },
  isolatedRuntimeTranspiled: {
    rawSizeBytes: runtimeBytes.byteLength,
    gzipSizeBytes: gzipSync(runtimeBytes, { level: 9 }).byteLength,
    brotliSizeBytes: brotliCompressSync(runtimeBytes, {
      params: { [constants.BROTLI_PARAM_QUALITY]: 11 },
    }).byteLength,
  },
  activeBuild: {
    containsWorldRuntime: activeBundleContainsWorldRuntime,
    approximateAddedBytes: activeBundleContainsWorldRuntime ? null : 0,
  },
}, null, 2)}\n`)
