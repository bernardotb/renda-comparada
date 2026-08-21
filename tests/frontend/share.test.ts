import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import type { BrazilPositionDisplay } from '../../src/brazil/domain.ts'
import {
  GENERIC_SHARE_MESSAGE,
  buildPositionShareMessage,
  buildSharePayload,
  buildShareUrl,
  buildWhatsAppUrl,
} from '../../src/share.ts'

const root = new URL('../../', import.meta.url)

function display(overrides: Partial<BrazilPositionDisplay> = {}): BrazilPositionDisplay {
  return {
    kind: 'standard',
    topLabel: 'TOP 12%',
    percentileLabel: 'Percentil 88',
    interpretation: 'Posição de teste.',
    markerPercent: 88,
    ...overrides,
  } as BrazilPositionDisplay
}

test('identidade, headline, campos vazios e microcopy seguem o contrato canônico', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')

  assert.match(app, /RENDA<br \/>COMPARADA/)
  assert.match(app, /Você é mais rico do que/)
  assert.match(app, /quantos brasileiros\?/)
  assert.match(app, /Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo\./)
  assert.equal((app.match(/useState\(''\)/g) ?? []).length >= 2, true)
  assert.match(app, /Use a renda bruta mensal, antes de impostos e despesas\./)
  assert.match(app, /Quantas pessoas fazem parte deste domicílio\?/)
  assert.match(app, /Inclua adultos e crianças, mesmo que não tenham renda\./)
  assert.match(app, /“pensionista” é uma categoria técnica/)
})

test('URL e mensagem genéricas não carregam a sentinela nem dados individuais', () => {
  const sentinelIncome = '12345678'
  const sentinelResidents = '7'
  const url = buildShareUrl('https://renda.example/path?income=12345678#top-7')
  const payload = buildSharePayload(url, false, 'TOP 12% — posição')
  const serialized = JSON.stringify(payload)

  assert.equal(url, 'https://renda.example/')
  assert.equal(payload.text, GENERIC_SHARE_MESSAGE)
  for (const forbidden of [sentinelIncome, sentinelResidents, 'TOP 12%', 'Percentil']) {
    assert.equal(serialized.includes(forbidden), false, forbidden)
  }
  assert.deepEqual(Object.keys(payload).sort(), ['text', 'title', 'url'])
})

test('posição Brasil já formatada só entra depois do opt-in', () => {
  const position = buildPositionShareMessage(display())
  assert.match(position ?? '', /^TOP 12%/)
  assert.equal(buildSharePayload('https://renda.example/', false, position).text, GENERIC_SHARE_MESSAGE)
  assert.equal(buildSharePayload('https://renda.example/', true, position).text, position)
})

test('limites não inventam TOP 0%, TOP 100% ou posição fora do suporte', () => {
  assert.equal(buildPositionShareMessage(display({ kind: 'zero', topLabel: null, markerPercent: 0 })), null)
  assert.equal(buildPositionShareMessage(display({ kind: 'above-maximum', topLabel: null, markerPercent: null })), null)
  assert.equal(buildPositionShareMessage(display({ topLabel: 'TOP 0%' })), null)
  assert.equal(buildPositionShareMessage(display({ topLabel: 'TOP 100%' })), null)
  assert.match(buildPositionShareMessage(display({ kind: 'upper-tail', topLabel: 'TOP 0,6%' })) ?? '', /^TOP 0,6%/)
  assert.match(buildPositionShareMessage(display({ kind: 'upper-tail', topLabel: 'TOP < 0,1%' })) ?? '', /^TOP < 0,1%/)
})

test('WhatsApp contém somente texto visível e URL genérica', () => {
  const payload = buildSharePayload('https://renda.example/', false, null)
  const whatsapp = new URL(buildWhatsAppUrl(payload))
  const visible = whatsapp.searchParams.get('text') ?? ''

  assert.equal(whatsapp.origin, 'https://wa.me')
  assert.equal(visible, `${GENERIC_SHARE_MESSAGE}\nhttps://renda.example/`)
  assert.equal(visible.includes('12345678'), false)
  assert.equal(visible.includes('moradores'), false)
})

test('bloco de share vem após interpretação, inicia privado e mantém fallback', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const interpretation = app.indexOf('className="interpretation"')
  const sharing = app.indexOf('className="sharing"')

  assert.equal(interpretation >= 0 && sharing > interpretation, true)
  assert.match(app, /const \[includePosition, setIncludePosition\] = useState\(false\)/)
  assert.match(app, /disabled=\{!positionShareMessage\}/)
  assert.match(app, /typeof navigator\.share !== 'function'/)
  assert.match(app, /navigator\.share\(sharePayload\)/)
  assert.match(app, /navigator\.clipboard\.writeText\(shareUrl\)/)
  assert.match(app, /Compartilhamento nativo indisponível\. Link copiado\./)
  assert.match(app, /shouldShowSharing\(brazilCalculation\.status, worldCalculation\.status\)/)
})

test('compartilhamento não introduz persistência, analytics ou dados na URL', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const share = await readFile(new URL('src/share.ts', root), 'utf8')
  const active = `${app}\n${share}`

  for (const forbidden of [
    'localStorage',
    'sessionStorage',
    'indexedDB',
    'document.cookie',
    'sendBeacon',
    'analytics',
    'console.',
    'URLSearchParams',
  ]) {
    assert.equal(active.includes(forbidden), false, forbidden)
  }
})
