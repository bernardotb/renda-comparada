import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'

const root = new URL('../../', import.meta.url)

function attribute(tag: string, name: string): string | null {
  const match = tag.match(new RegExp(`\\b${name}\\s*=\\s*(["'])(.*?)\\1`, 'i'))
  return match?.[2] ?? null
}

test('o caminho ativo não contém motor legado nem fallback mundial', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const domain = await readFile(new URL('src/brazil/domain.ts', root), 'utf8')
  const activeSource = `${app}\n${domain}`

  for (const forbidden of [
    'BRAZIL_THRESHOLDS',
    'WORLD_CURVE',
    'PPP_2021_BRL',
    'BRAZIL_CPI_2024',
    'interpolateLog',
  ]) {
    assert.equal(activeSource.includes(forbidden), false, forbidden)
  }

  assert.match(app, /worldEngineLoader\.load\(\)/)
  assert.match(app, /Nenhum número provisório ou fallback legado é exibido/)
  assert.match(app, /posição monetária global estimada/i)
  assert.match(app, /World Bank — Poverty and Inequality Platform/)
  assert.match(app, /runtime\.referenceYear/)
  assert.match(app, /runtime\.pppBase/)
  assert.match(app, /setBrazilCalculation\(\{ status: 'unavailable'/)
  assert.match(app, /setWorldCalculation\(\{ status: 'unavailable'/)
})

test('o frontend não persiste nem transmite entradas ou resultados', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const loader = await readFile(new URL('src/brazil/loader.ts', root), 'utf8')
  const analytics = await readFile(new URL('src/analytics.ts', root), 'utf8')
  const activeSource = `${app}\n${loader}\n${analytics}`

  for (const forbidden of [
    'localStorage',
    'sessionStorage',
    'indexedDB',
    'document.cookie',
    'navigator.sendBeacon',
    'console.log',
  ]) {
    assert.equal(activeSource.includes(forbidden), false, forbidden)
  }

  for (const forbidden of ['household_size', 'per_capita', 'percentile', 'top_percent', 'RDPC']) {
    assert.equal(analytics.includes(forbidden), false, forbidden)
  }
})

test('a CDF é referenciada somente como artefato estático sob demanda', async () => {
  const loader = await readFile(new URL('src/brazil/loader.ts', root), 'utf8')
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.equal(app.includes('brazil-income-cdf-2025.json'), false)
  assert.equal(/import\s+.*brazil-income-cdf-2025\.json/.test(loader), false)
  assert.match(app, /brazilEngineLoader\.load\(\)/)
})

test('erros de validação recebem anúncio e foco no primeiro campo inválido', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.match(app, /incomeInputRef\.current\?\.focus\(\)/)
  assert.match(app, /householdInputRef\.current\?\.focus\(\)/)
  assert.equal((app.match(/className="field-error"[^>]*role="alert"/g) ?? []).length, 2)
})

test('o marcador visual permanece contido sem limitar o percentil estatístico', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.match(app, /clamp\(6\.5px, \$\{markerPercent\}%, calc\(100% - 6\.5px\)\)/)
  assert.equal(app.includes('99.7'), false)
})

test('a home possui exatamente uma ocorrência de cada metadata canônica D073', async () => {
  const html = await readFile(new URL('index.html', root), 'utf8')
  const titles = [...html.matchAll(/<title\b[^>]*>([\s\S]*?)<\/title>/gi)]
    .map((match) => match[1].trim())
  const metaTags = html.match(/<meta\b[^>]*>/gi) ?? []

  const expected = [
    {
      attribute: 'name',
      key: 'description',
      content: 'Descubra onde a renda da sua casa está na distribuição do Brasil e, de forma estimada, no mundo. Comparação de renda, não de patrimônio.',
    },
    {
      attribute: 'property',
      key: 'og:title',
      content: 'Você é mais rico do que quantos brasileiros?',
    },
    {
      attribute: 'property',
      key: 'og:description',
      content: 'Descubra onde a renda da sua casa está no Brasil e, de forma estimada, no mundo.',
    },
  ] as const

  assert.deepEqual(titles, ['Você é mais rico do que quantos brasileiros? | Renda Comparada'])

  for (const field of expected) {
    const matches = metaTags.filter(
      (tag) => attribute(tag, field.attribute)?.toLowerCase() === field.key,
    )
    assert.equal(matches.length, 1, `${field.attribute}=${field.key}`)
    assert.equal(attribute(matches[0], 'content'), field.content, field.key)
  }
})
