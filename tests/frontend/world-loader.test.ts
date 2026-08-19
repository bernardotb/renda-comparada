import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import { createWorldEngineLoader, type WorldRuntimeBootstrap } from '../../src/world/loader.ts'

const root = new URL('../../', import.meta.url)
const paths = {
  manifest: '/data/world/world-income-engine-manifest.json',
  price: '/data/world/world-price-alignment.json',
  cdf: '/data/world/world-income-cdf-2024.json',
  golden: '/data/world/world-income-golden-cases-d070-candidate.json',
}

async function canonicalBytes() {
  return new Map<string, Uint8Array>([
    [paths.manifest, await readFile(new URL('data/production/world/world-income-engine-manifest.json', root))],
    [paths.price, await readFile(new URL('data/production/world/world-price-alignment.json', root))],
    [paths.cdf, await readFile(new URL('data/production/world/world-income-cdf-2024.json', root))],
    [paths.golden, await readFile(new URL('validation/world/world-income-golden-cases-d070-candidate.json', root))],
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
  assert.deepEqual(calls.map(({ url }) => url), [paths.manifest, paths.price, paths.cdf, paths.golden])
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
    (manifest: any) => { manifest.methodology.referenceYear = 2025 },
    (manifest: any) => { manifest.methodology.pppBase = 2017 },
    (manifest: any) => { manifest.integration.worldFrontendIntegrationAllowed = true },
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

test('runtime Mundo permanece isolado da aplicação e da área pública', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const packageJson = await readFile(new URL('package.json', root), 'utf8')
  const publicFiles = await readFile(new URL('public/data/brazil/brazil-income-engine-manifest.json', root))
  assert.equal(app.includes("./world/"), false)
  assert.equal(app.includes("world/loader"), false)
  assert.equal(packageJson.includes('sync:world'), false)
  assert.ok(publicFiles.byteLength > 0)
  await assert.rejects(readFile(new URL('public/data/world/world-income-engine-manifest.json', root)))
})
