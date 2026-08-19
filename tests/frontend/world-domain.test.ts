import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import {
  calculateWorldIncomePosition,
  internationalPppDailyToNominalHouseholdIncome,
  lookupWorldIncome,
  nominalHouseholdIncomeToInternationalPppDaily,
  presentWorldPosition,
  validateWorldInputs,
} from '../../src/world/domain.ts'
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

async function loadRuntime() {
  const files = await canonicalBytes()
  const manifestBytes = files.get(paths.manifest)!
  const bootstrap: WorldRuntimeBootstrap = {
    publicBasePath: '/data/world',
    engineManifest: { publicPath: paths.manifest, sha256: hash(manifestBytes), sizeBytes: manifestBytes.byteLength },
  }
  return createWorldEngineLoader(mockFetcher(files, []), bootstrap).load()
}

test('valida renda e moradores sem aceitar negativos, zero ou frações', () => {
  assert.deepEqual(validateWorldInputs(0, 1), { ok: true, householdIncome: 0, residents: 1 })
  assert.equal(validateWorldInputs(-1, 1).ok, false)
  assert.equal(validateWorldInputs(Number.NaN, 1).ok, false)
  assert.equal(validateWorldInputs(1000, 0).ok, false)
  assert.equal(validateWorldInputs(1000, -1).ok, false)
  assert.equal(validateWorldInputs(1000, 2.5).ok, false)
})

test('conversão D069 reproduz R$ 6.500 / 3 e faz round-trip', async () => {
  const runtime = await loadRuntime()
  const daily = nominalHouseholdIncomeToInternationalPppDaily(runtime, 6500, 3)
  assert.ok(Math.abs(daily - 22.127980281368043) < 1e-13)
  assert.ok(Math.abs(internationalPppDailyToNominalHouseholdIncome(runtime, daily, 3) - 6500) < 1e-10)
  assert.equal(runtime.priceReferenceMonth, '2026-07')
  assert.equal(runtime.brlPerIntl2024Derived, 2.922489790253104)
})

test('runtime reproduz os 11 golden cases canônicos', async () => {
  const runtime = await loadRuntime()
  const golden = JSON.parse(await readFile(new URL('validation/world/world-income-golden-cases-d070-candidate.json', root), 'utf8'))
  assert.equal(golden.cases.length, 11)
  for (const expected of golden.cases) {
    const lookup = lookupWorldIncome(runtime, Number(expected.internationalPppDaily))
    assert.ok(Math.abs(lookup.shareBelow - expected.shareBelow) < 2e-15, expected.name)
    assert.ok(Math.abs(lookup.shareAtOrBelow - expected.shareAtOrBelow) < 2e-15, expected.name)
    assert.ok(Math.abs(lookup.topShare - expected.topShare) < 2e-15, expected.name)
  }
})

test('classifica mínimo, máximo, acima do máximo e empates sem extrapolar', async () => {
  const runtime = await loadRuntime()
  const minimum = lookupWorldIncome(runtime, runtime.cdf.minWelfare)
  const maximum = lookupWorldIncome(runtime, runtime.cdf.maxWelfare)
  const above = lookupWorldIncome(runtime, runtime.cdf.maxWelfare + 1)
  assert.equal(minimum.supportStatus, 'at-minimum')
  assert.equal(maximum.supportStatus, 'at-maximum')
  assert.equal(above.supportStatus, 'above-maximum')
  assert.equal(above.shareBelow, 1)
  assert.equal(above.shareAtOrBelow, 1)
  assert.equal(above.topShare, 0)
  assert.equal(presentWorldPosition(above.topShare, runtime.maxAbsoluteErrorPp, above.supportStatus).extrapolated, false)
})

test('apresentação D070 cobre caudas e nunca produz TOP 0% ou TOP 100% como headline', () => {
  assert.equal(presentWorldPosition(0.01, 0.022516991848920, 'inside').kind, 'main')
  assert.equal(presentWorldPosition(0.009999, 0.022516991848920, 'inside').kind, 'upper-tail')
  assert.deepEqual(
    presentWorldPosition(0.0009, 0.022516991848920, 'inside'),
    { kind: 'upper-extreme', headline: 'aproximadamente 0,1%', extrapolated: false },
  )
  assert.deepEqual(
    presentWorldPosition(0.0007, 0.022516991848920, 'inside'),
    { kind: 'upper-extreme', headline: 'menos de 0,1%', extrapolated: false },
  )
  const minimum = presentWorldPosition(1, 0.022516991848920, 'at-minimum')
  const upper = presentWorldPosition(0, 0.022516991848920, 'at-maximum')
  assert.equal('headline' in minimum && minimum.headline.includes('TOP 100%'), false)
  assert.equal('headline' in upper && upper.headline.includes('TOP 0%'), false)
})

test('resultado de domínio é estruturado e usa linguagem canônica', async () => {
  const runtime = await loadRuntime()
  const result = calculateWorldIncomePosition(runtime, 6500, 3)
  assert.equal(result.language, 'posição monetária global estimada')
  assert.equal(result.supportStatus, 'inside')
  assert.equal(result.presentation.kind, 'main')
  assert.ok(Math.abs(result.shareBelow - 0.7460604158641307) < 2e-15)
})
