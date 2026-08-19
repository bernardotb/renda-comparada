import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile, readdir } from 'node:fs/promises'
import test from 'node:test'
import { createWorldEngineLoader, type WorldRuntimeBootstrap } from '../../src/world/loader.ts'

const root = new URL('../../', import.meta.url)
const paths = {
  manifest: '/data/world/world-income-engine-manifest.json',
  price: '/data/world/world-price-alignment.json',
  cdf: '/data/world/world-income-cdf-2024.json',
}

async function canonicalBytes() {
  return new Map<string, Uint8Array>([
    [paths.manifest, await readFile(new URL('data/production/world/world-income-engine-manifest.json', root))],
    [paths.price, await readFile(new URL('data/production/world/world-price-alignment.json', root))],
    [paths.cdf, await readFile(new URL('data/production/world/world-income-cdf-2024.json', root))],
  ])
}

function hash(bytes: Uint8Array): string {
  return createHash('sha256').update(bytes).digest('hex').toUpperCase()
}

function mockFetcher(files: Map<string, Uint8Array>, calls: Array<{ url: string; init?: RequestInit }>) {
  return async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input)
    calls.push({ url, init })
    const bytes = files.get(url)
    return bytes ? new Response(bytes, { status: 200 }) : new Response('not found', { status: 404 })
  }
}

function bootstrap(manifestBytes: Uint8Array): WorldRuntimeBootstrap {
  return {
    publicBasePath: '/data/world',
    engineManifest: { publicPath: paths.manifest, sha256: hash(manifestBytes), sizeBytes: manifestBytes.byteLength },
  }
}

test('loader valida o pacote completo e reutiliza runtime em memória', async () => {
  const files = await canonicalBytes()
  const calls: Array<{ url: string; init?: RequestInit }> = []
  const loader = createWorldEngineLoader(mockFetcher(files, calls), bootstrap(files.get(paths.manifest)!))
  const first = await loader.load()
  const second = await loader.load()
  assert.equal(first, second)
  assert.equal(loader.getCached(), first)
  assert.deepEqual(calls.map(({ url }) => url), [paths.manifest, paths.price, paths.cdf])
  await loader.load()
  assert.equal(calls.length, 3)
})

test('requisições de artefato são GET estáticos sem renda, moradores ou resultado', async () => {
  const files = await canonicalBytes()
  const calls: Array<{ url: string; init?: RequestInit }> = []
  await createWorldEngineLoader(mockFetcher(files, calls), bootstrap(files.get(paths.manifest)!)).load()
  for (const { url, init } of calls) {
    assert.match(url, /^\/data\/world\/[a-z0-9-]+\.json$/)
    assert.equal(url.includes('?'), false)
    assert.equal(init?.method, 'GET')
    assert.equal(init?.body, undefined)
    assert.equal(init?.headers, undefined)
    assert.equal(init?.credentials, 'same-origin')
    for (const forbidden of ['householdIncome', 'residents', 'percentile', 'topShare', '6500']) {
      assert.equal(url.includes(forbidden), false)
    }
  }
})

test('ausência de artefato falha fechada e não mantém resultado anterior', async () => {
  const files = await canonicalBytes()
  files.delete(paths.cdf)
  const calls: Array<{ url: string; init?: RequestInit }> = []
  const loader = createWorldEngineLoader(mockFetcher(files, calls), bootstrap(files.get(paths.manifest)!))
  await assert.rejects(loader.load(), /indisponível/)
  assert.equal(loader.getCached(), null)
  await assert.rejects(loader.load(), /indisponível/)
  assert.equal(calls.filter(({ url }) => url === paths.cdf).length, 2)
})

test('alteração de um byte causa falha de integridade', async () => {
  const files = await canonicalBytes()
  const changed = Uint8Array.from(files.get(paths.price)!)
  changed[Math.floor(changed.length / 2)] ^= 1
  files.set(paths.price, changed)
  await assert.rejects(
    createWorldEngineLoader(mockFetcher(files, []), bootstrap(files.get(paths.manifest)!)).load(),
    /SHA-256 incompatível/,
  )
})

test('manifesto divergente em versão, ano, PPP ou autorização é rejeitado', async () => {
  const base = await canonicalBytes()
  for (const mutate of [
    (manifest: any) => { manifest.methodology.pipVersion = 'wrong' },
    (manifest: any) => { manifest.methodology.productionBuild = 'wrong' },
    (manifest: any) => { manifest.methodology.referenceYear = 2025 },
    (manifest: any) => { manifest.methodology.pppBase = 2017 },
    (manifest: any) => { manifest.integration.worldFrontendIntegrationAllowed = false },
    (manifest: any) => { manifest.status = 'CANONICAL_PRODUCTION_FRONTEND_BLOCKED' },
  ]) {
    const files = new Map(base)
    const manifest = JSON.parse(new TextDecoder().decode(files.get(paths.manifest)))
    mutate(manifest)
    const bytes = new TextEncoder().encode(JSON.stringify(manifest))
    files.set(paths.manifest, bytes)
    await assert.rejects(
      createWorldEngineLoader(mockFetcher(files, []), bootstrap(bytes)).load(),
      /Manifesto Mundo incompatível/,
    )
  }
})

test('runtime Mundo está integrado sem embutir a CDF ou publicar golden cases', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const packageJson = await readFile(new URL('package.json', root), 'utf8')
  const publicFiles = (await readdir(new URL('public/data/world/', root))).sort()
  assert.match(app, /worldEngineLoader/)
  assert.match(packageJson, /sync:world-runtime/)
  assert.deepEqual(publicFiles, [
    'world-income-cdf-2024.json',
    'world-income-engine-manifest.json',
    'world-price-alignment.json',
  ])
  assert.equal(publicFiles.some((name) => name.includes('golden')), false)
})

test('JSON inválido, tamanho divergente e referências cruzadas falham fechados', async () => {
  const base = await canonicalBytes()

  const invalidJson = new Map(base)
  const invalidManifest = new TextEncoder().encode('{')
  invalidJson.set(paths.manifest, invalidManifest)
  await assert.rejects(
    createWorldEngineLoader(mockFetcher(invalidJson, []), bootstrap(invalidManifest)).load(),
    /JSON inválido/,
  )

  const manifestBytes = base.get(paths.manifest)!
  const wrongSize = bootstrap(manifestBytes)
  wrongSize.engineManifest.sizeBytes = manifestBytes.byteLength + 1
  await assert.rejects(
    createWorldEngineLoader(mockFetcher(base, []), wrongSize).load(),
    /Tamanho incompatível/,
  )

  const crossed = new Map(base)
  const manifest = JSON.parse(new TextDecoder().decode(manifestBytes))
  manifest.artifacts.cdf.version = 'wrong'
  const crossedBytes = new TextEncoder().encode(JSON.stringify(manifest))
  crossed.set(paths.manifest, crossedBytes)
  await assert.rejects(
    createWorldEngineLoader(mockFetcher(crossed, []), bootstrap(crossedBytes)).load(),
    /CDF Mundo incompatível/,
  )
})

test('SHA ou tamanho divergente de qualquer artefato falha fechado', async () => {
  const base = await canonicalBytes()

  const wrongManifestHash = bootstrap(base.get(paths.manifest)!)
  wrongManifestHash.engineManifest.sha256 = '0'.repeat(64)
  await assert.rejects(
    createWorldEngineLoader(mockFetcher(base, []), wrongManifestHash).load(),
    /SHA-256 incompatível/,
  )

  for (const artifact of ['priceAlignment', 'cdf'] as const) {
    const files = new Map(base)
    const manifest = JSON.parse(new TextDecoder().decode(files.get(paths.manifest)))
    manifest.artifacts[artifact].sha256 = '0'.repeat(64)
    const bytes = new TextEncoder().encode(JSON.stringify(manifest))
    files.set(paths.manifest, bytes)
    await assert.rejects(
      createWorldEngineLoader(mockFetcher(files, []), bootstrap(bytes)).load(),
      /SHA-256 incompatível/,
    )

    manifest.artifacts[artifact].sha256 = artifact === 'cdf'
      ? hash(base.get(paths.cdf)!)
      : hash(base.get(paths.price)!)
    manifest.artifacts[artifact].sizeBytes += 1
    const wrongSizeBytes = new TextEncoder().encode(JSON.stringify(manifest))
    files.set(paths.manifest, wrongSizeBytes)
    await assert.rejects(
      createWorldEngineLoader(mockFetcher(files, []), bootstrap(wrongSizeBytes)).load(),
      /Tamanho incompatível/,
    )
  }
})

test('404 de manifesto, price ou CDF deixa o runtime indisponível', async () => {
  const base = await canonicalBytes()
  for (const missing of [paths.manifest, paths.price, paths.cdf]) {
    const files = new Map(base)
    files.delete(missing)
    await assert.rejects(
      createWorldEngineLoader(mockFetcher(files, []), bootstrap(base.get(paths.manifest)!)).load(),
      /indisponível/,
      missing,
    )
  }
})

test('bootstrap Mundo referencia exatamente o SHA final do manifesto', async () => {
  const config = JSON.parse(await readFile(new URL('config/world-frontend-runtime.json', root), 'utf8'))
  const manifest = await readFile(new URL('data/production/world/world-income-engine-manifest.json', root))
  assert.equal(config.engineManifest.sha256, hash(manifest))
  assert.deepEqual(Object.keys(config).sort(), ['engineManifest', 'publicBasePath', 'schemaVersion'])
})
