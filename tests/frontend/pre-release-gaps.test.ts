import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import {
  datasetYearFromVersion,
  formatReferenceMonth,
  shouldShowSharing,
} from '../../src/presentation.ts'

const root = new URL('../../', import.meta.url)

test('share só aparece depois que Brasil e Mundo estão settled', () => {
  assert.equal(shouldShowSharing('success', 'loading'), false)
  assert.equal(shouldShowSharing('loading', 'success'), false)
  assert.equal(shouldShowSharing('success', 'success'), true)
  assert.equal(shouldShowSharing('success', 'unavailable'), true)
  assert.equal(shouldShowSharing('unavailable', 'success'), true)
  assert.equal(shouldShowSharing('unavailable', 'unavailable'), false)
})

test('metadata temporal é formatada a partir dos valores do runtime', () => {
  assert.equal(formatReferenceMonth('2026-07'), 'julho de 2026')
  assert.equal(formatReferenceMonth('2026-13'), null)
  assert.equal(datasetYearFromVersion('2025-20260508-v1'), 2025)
  assert.equal(datasetYearFromVersion('versao-sem-ano'), null)
})

test('App não duplica o mês operacional e apresenta metadata carregada', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.equal(app.includes('2026-07'), false)
  assert.equal(app.includes('julho de 2026'), false)
  assert.match(app, /brazilRuntime\.referenceMonth/)
  assert.match(app, /brazilRuntime\.priceReference/)
  assert.match(app, /worldRuntime\.referenceYear/)
  assert.match(app, /worldRuntime\.pppBase/)
  assert.equal((app.match(/EngineLoader\.load\(\)/g) ?? []).length, 2)
})

test('metodologia pública cobre o mínimo sem implementar fórmula no domínio', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const brazilDomain = await readFile(new URL('src/brazil/domain.ts', root), 'utf8')
  const worldDomain = await readFile(new URL('src/world/domain.ts', root), 'utf8')

  for (const concept of [
    /não medem patrimônio/i,
    /PNAD Contínua/,
    /IPCA nacional/,
    /pessoas elegíveis/,
    /não há interpolação nem extrapolação/,
    /Poverty and Inequality Platform/,
    /PPP/,
    /estimativa monetária/,
    /renda ou consumo/,
    /diferenças regionais de preços não são modeladas/,
  ]) assert.match(app, concept)

  const domains = `${brazilDomain}\n${worldDomain}`
  assert.equal(domains.includes('formatReferenceMonth'), false)
  assert.equal(domains.includes('shouldShowSharing'), false)
})

test('Open Graph padrão preserva a copy canônica e publica apenas a URL disponível', async () => {
  const html = await readFile(new URL('index.html', root), 'utf8')
  const source = `${html}\n${await readFile(new URL('src/App.tsx', root), 'utf8')}`
  const ogTags = (html.match(/<meta\b[^>]*property=["']og:[^>]*>/gi) ?? []).join('\n')

  for (const forbidden of ['12345678', '7 moradores', 'TOP 12%', 'Percentil 88']) {
    assert.equal(ogTags.includes(forbidden), false)
  }
  assert.equal(/property=["']og:image["']/i.test(html), false)
  assert.match(html, /<meta property="og:url" content="https:\/\/rendacomparada\.com\.br\/" \/>/)
  assert.equal(source.includes('DEFAULT_OG_IMAGE'), false)
  assert.equal(source.includes('PRODUCTION_DOMAIN'), false)
})

test('divulgação metodológica expõe estado e painel controlado semanticamente', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.match(app, /aria-expanded=\{showMethod\}/)
  assert.match(app, /aria-controls="method-details"/)
  assert.match(app, /id="method-details" hidden=\{!showMethod\}/)
})
