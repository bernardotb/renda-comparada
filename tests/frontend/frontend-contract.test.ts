import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'

const root = new URL('../../', import.meta.url)

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

  assert.match(app, /Indisponível nesta versão/)
  assert.match(app, /Nenhum número provisório ou curva antiga é exibido/)
})

test('o frontend não persiste nem transmite entradas ou resultados', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const loader = await readFile(new URL('src/brazil/loader.ts', root), 'utf8')
  const activeSource = `${app}\n${loader}`

  for (const forbidden of [
    'localStorage',
    'sessionStorage',
    'indexedDB',
    'document.cookie',
    'navigator.sendBeacon',
    'analytics',
    'console.log',
  ]) {
    assert.equal(activeSource.includes(forbidden), false, forbidden)
  }
})

test('a CDF é referenciada somente como artefato estático sob demanda', async () => {
  const loader = await readFile(new URL('src/brazil/loader.ts', root), 'utf8')
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.equal(app.includes('brazil-income-cdf-2025.json'), false)
  assert.equal(/import\s+.*brazil-income-cdf-2025\.json/.test(loader), false)
  assert.match(app, /brazilEngineLoader\.load\(\)/)
})
