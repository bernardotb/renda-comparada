import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import { calculateBrazilIncomePosition } from '../../src/brazil/domain.ts'
import {
  createBrazilEngineLoader,
  type BrazilRuntimeBootstrap,
} from '../../src/brazil/loader.ts'

const root = new URL('../../', import.meta.url)
const publicPaths = {
  engine: '/data/brazil/brazil-income-engine-manifest.json',
  price: '/data/brazil/brazil-price-alignment.json',
  cdf: '/data/brazil/brazil-income-cdf-2025.json',
}

const bootstrap: BrazilRuntimeBootstrap = {
  publicBasePath: '/data/brazil',
  engineManifest: {
    publicPath: publicPaths.engine,
    sha256: '5BE810FA4ED0BA1A1842239CA8FF4CAD65DB5EB9ED71EF1AC7B5228589DDD15F',
  },
}

async function canonicalBytes() {
  return new Map<string, Uint8Array>([
    [publicPaths.engine, await readFile(new URL('data/production/brazil/brazil-income-engine-manifest.json', root))],
    [publicPaths.price, await readFile(new URL('data/production/brazil/brazil-price-alignment.json', root))],
    [publicPaths.cdf, await readFile(new URL('data/production/brazil/brazil-income-cdf-2025.json', root))],
  ])
}

function hash(bytes: Uint8Array): string {
  return createHash('sha256').update(bytes).digest('hex').toUpperCase()
}

function mockFetcher(
  files: Map<string, Uint8Array>,
  calls: Array<{ url: string; init?: RequestInit }>,
) {
  return async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input)
    calls.push({ url, init })
    const bytes = files.get(url)
    return bytes ? new Response(bytes, { status: 200 }) : new Response('not found', { status: 404 })
  }
}

test('carrega o pacote canônico, reproduz o golden atual e reutiliza a CDF em memória', async () => {
  const calls: Array<{ url: string; init?: RequestInit }> = []
  const loader = createBrazilEngineLoader(mockFetcher(await canonicalBytes(), calls), bootstrap)

  assert.equal(loader.getCached(), null)
  const runtime = await loader.load()
  const result = calculateBrazilIncomePosition(runtime, 6500, 3)

  assert.equal(runtime.datasetVersion, '2025-20260508-v1')
  assert.equal(runtime.referenceMonth, '2026-07')
  assert.equal(runtime.priceReference, 'preços médios de 2025')
  assert.ok(Math.abs(result.comparableHouseholdIncome - 6197.067647113874) < 1e-9)
  assert.ok(Math.abs(result.comparableRdpc - 2065.689215704624) < 1e-9)
  assert.ok(Math.abs(result.shareBelow - 0.6866910622833815) < 1e-15)
  assert.equal(result.shareBelow, result.shareAtOrBelow)

  const reused = await loader.load()
  assert.equal(reused, runtime)
  assert.deepEqual(calls.map(({ url }) => url), [publicPaths.engine, publicPaths.price, publicPaths.cdf])
})

test('as únicas requisições são GET estáticos sem renda, query, corpo ou headers personalizados', async () => {
  const calls: Array<{ url: string; init?: RequestInit }> = []
  const loader = createBrazilEngineLoader(mockFetcher(await canonicalBytes(), calls), bootstrap)
  await loader.load()

  assert.equal(calls.length, 3)
  for (const { url, init } of calls) {
    assert.match(url, /^\/data\/brazil\/[a-z0-9-]+\.json$/)
    assert.equal(url.includes('?'), false)
    assert.equal(url.includes('6500'), false)
    assert.equal(init?.method, 'GET')
    assert.equal(init?.body, undefined)
    assert.equal(init?.headers, undefined)
    assert.equal(init?.credentials, 'same-origin')
  }
})

test('falha de modo seguro quando a CDF está ausente e permite nova tentativa', async () => {
  const files = await canonicalBytes()
  files.delete(publicPaths.cdf)
  const calls: Array<{ url: string; init?: RequestInit }> = []
  const loader = createBrazilEngineLoader(mockFetcher(files, calls), bootstrap)

  await assert.rejects(loader.load(), /Artefato indisponível/)
  assert.equal(loader.getCached(), null)
  await assert.rejects(loader.load(), /Artefato indisponível/)
  assert.equal(calls.filter(({ url }) => url === publicPaths.cdf).length, 2)
})

test('rejeita manifesto não autorizado antes de carregar os demais artefatos', async () => {
  const files = await canonicalBytes()
  const manifest = JSON.parse(new TextDecoder().decode(files.get(publicPaths.engine)))
  manifest.integration.brazilFrontendIntegrationAllowed = false
  const invalidBytes = new TextEncoder().encode(JSON.stringify(manifest))
  files.set(publicPaths.engine, invalidBytes)
  const calls: Array<{ url: string; init?: RequestInit }> = []
  const invalidBootstrap = {
    ...bootstrap,
    engineManifest: { ...bootstrap.engineManifest, sha256: hash(invalidBytes) },
  }

  await assert.rejects(
    createBrazilEngineLoader(mockFetcher(files, calls), invalidBootstrap).load(),
    /não está aprovado/,
  )
  assert.deepEqual(calls.map(({ url }) => url), [publicPaths.engine])
})

test('rejeita SHA-256 incompatível sem acionar fallback', async () => {
  const files = await canonicalBytes()
  const corrupted = Uint8Array.from(files.get(publicPaths.engine) ?? [])
  corrupted[0] ^= 1
  files.set(publicPaths.engine, corrupted)
  const calls: Array<{ url: string; init?: RequestInit }> = []

  await assert.rejects(
    createBrazilEngineLoader(mockFetcher(files, calls), bootstrap).load(),
    /SHA-256 incompatível/,
  )
  assert.deepEqual(calls.map(({ url }) => url), [publicPaths.engine])
})
