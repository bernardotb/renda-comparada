import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import {
  ANALYTICS_EVENTS,
  buildPlausibleInitOptions,
  initializePlausible,
  sanitizeAnalyticsUrl,
  trackAnalyticsEvent,
} from '../../src/analytics.ts'
import {
  GENERIC_SHARE_MESSAGE,
  buildSharePayload,
  buildShareUrl,
  buildWhatsAppUrl,
} from '../../src/share.ts'

const root = new URL('../../', import.meta.url)
const sentinelIncome = '12345678'
const sentinelResidents = '7'

type BrowserGlobals = {
  document?: unknown
  window?: unknown
}

function withBrowserGlobals<T>(windowValue: unknown, documentValue: unknown, action: () => T): T {
  const globals = globalThis as typeof globalThis & BrowserGlobals
  const previousWindow = Object.getOwnPropertyDescriptor(globals, 'window')
  const previousDocument = Object.getOwnPropertyDescriptor(globals, 'document')
  Object.defineProperty(globals, 'window', { configurable: true, writable: true, value: windowValue })
  Object.defineProperty(globals, 'document', { configurable: true, writable: true, value: documentValue })

  try {
    return action()
  } finally {
    if (previousWindow) Object.defineProperty(globals, 'window', previousWindow)
    else delete globals.window
    if (previousDocument) Object.defineProperty(globals, 'document', previousDocument)
    else delete globals.document
  }
}

test('taxonomia expõe somente os cinco eventos autorizados', () => {
  assert.deepEqual(ANALYTICS_EVENTS, [
    'calculation_started',
    'calculation_completed',
    'result_viewed',
    'share_clicked',
    'recalculate_clicked',
  ])
})

test('todos os eventos são enviados sem custom properties nem dados financeiros', () => {
  const calls: unknown[][] = []
  const fakeWindow = {
    plausible: (...args: unknown[]) => calls.push(args),
  }

  withBrowserGlobals(fakeWindow, {}, () => {
    trackAnalyticsEvent('calculation_started')
    trackAnalyticsEvent('calculation_completed')
    trackAnalyticsEvent('result_viewed')
    trackAnalyticsEvent('share_clicked')
    trackAnalyticsEvent('recalculate_clicked')
  })

  assert.equal(calls.length, 5)
  assert.deepEqual(calls, ANALYTICS_EVENTS.map((eventName) => [eventName]))
  const serialized = JSON.stringify(calls)
  for (const forbidden of [
    sentinelIncome,
    sentinelResidents,
    'income',
    'household_size',
    'per_capita',
    'percentile',
    'top_percent',
    'RDPC',
  ]) assert.equal(serialized.includes(forbidden), false, forbidden)

  withBrowserGlobals(fakeWindow, {}, () => {
    const runtimeCall = trackAnalyticsEvent as unknown as (...args: unknown[]) => void
    runtimeCall('share_clicked', {
      props: { share_channel: 'whatsapp', share_mode: `position-${sentinelIncome}` },
    })
  })
  assert.equal(calls.length, 6)
  assert.deepEqual(calls[5], ['share_clicked'])
})

test('falha ou ausência do Plausible nunca propaga erro funcional', () => {
  assert.doesNotThrow(() => withBrowserGlobals({}, {}, () => {
    trackAnalyticsEvent('calculation_started')
  }))
  assert.doesNotThrow(() => withBrowserGlobals({
    plausible: () => { throw new Error('provider unavailable') },
  }, {}, () => {
    trackAnalyticsEvent('calculation_completed')
  }))
})

test('falha do analytics não interrompe a preparação do compartilhamento', () => {
  assert.doesNotThrow(() => withBrowserGlobals({
    plausible: () => { throw new Error('provider unavailable') },
  }, {}, () => {
    trackAnalyticsEvent('share_clicked')
    const shareUrl = buildShareUrl('https://rendacomparada.com.br/', 'whatsapp')
    const payload = buildSharePayload(shareUrl, false, null)
    assert.match(buildWhatsAppUrl(payload), /^https:\/\/wa\.me\/\?text=/)
  }))
})

test('sanitização conserva somente atribuição genérica de compartilhamento', () => {
  const dirty = `https://rendacomparada.com.br/?income=${sentinelIncome}&household_size=${sentinelResidents}&utm_source=share&utm_medium=whatsapp&utm_campaign=organic_share#resultado-${sentinelIncome}`
  const sanitized = new URL(sanitizeAnalyticsUrl(dirty))

  assert.equal(sanitized.origin, 'https://rendacomparada.com.br')
  assert.equal(sanitized.pathname, '/')
  assert.equal(sanitized.hash, '')
  assert.deepEqual([...sanitized.searchParams.entries()], [
    ['utm_source', 'share'],
    ['utm_medium', 'whatsapp'],
    ['utm_campaign', 'organic_share'],
  ])
  assert.equal(sanitized.toString().includes(sentinelIncome), false)
  assert.equal(sanitized.toString().includes(`=${sentinelResidents}`), false)

  const maliciousCampaign = sanitizeAnalyticsUrl(
    `https://rendacomparada.com.br/?utm_source=share&utm_medium=copy&utm_campaign=${sentinelIncome}`,
  )
  assert.equal(maliciousCampaign, 'https://rendacomparada.com.br/')
})

test('inicialização usa snippet individual, não cria persistência e sanitiza payload', () => {
  const appended: Array<Record<string, unknown>> = []
  let cookieWrites = 0
  let localWrites = 0
  let sessionWrites = 0
  const fakeDocument: Record<string, unknown> = {
    querySelector: () => null,
    createElement: () => ({ async: false, src: '', dataset: {} }),
    head: { append: (node: Record<string, unknown>) => appended.push(node) },
  }
  Object.defineProperty(fakeDocument, 'cookie', {
    configurable: true,
    get: () => '',
    set: () => { cookieWrites += 1 },
  })
  const fakeWindow: Record<string, unknown> = {
    location: {
      href: `https://rendacomparada.com.br/?income=${sentinelIncome}&household_size=${sentinelResidents}`,
    },
    localStorage: { setItem: () => { localWrites += 1 } },
    sessionStorage: { setItem: () => { sessionWrites += 1 } },
  }

  withBrowserGlobals(fakeWindow, fakeDocument, () => {
    assert.equal(initializePlausible('https://plausible.io/js/pa-renda123.js'), true)
    const plausible = fakeWindow.plausible as {
      o?: { transformRequest: (payload: Record<string, unknown>) => Record<string, unknown> }
    }
    const payload = plausible.o?.transformRequest({ u: 'unsafe', n: 'pageview' })
    assert.equal(payload?.u, 'https://rendacomparada.com.br/')
  })

  assert.equal(appended.length, 1)
  assert.equal(appended[0].src, 'https://plausible.io/js/pa-renda123.js')
  assert.equal(cookieWrites, 0)
  assert.equal(localWrites, 0)
  assert.equal(sessionWrites, 0)
  assert.equal(initializePlausible('https://example.com/analytics.js'), false)
  assert.equal(initializePlausible('https://plausible.io/js/script.js'), false)
})

test('UTMs e shares genérico/posição não vazam a sentinela financeira', () => {
  for (const channel of ['native', 'whatsapp', 'copy'] as const) {
    const shareUrl = buildShareUrl(
      `https://rendacomparada.com.br/path?income=${sentinelIncome}&household_size=${sentinelResidents}#resultado`,
      channel,
    )
    const url = new URL(shareUrl)
    assert.deepEqual([...url.searchParams.keys()].sort(), ['utm_campaign', 'utm_medium', 'utm_source'])
    assert.equal(url.searchParams.get('utm_source'), 'share')
    assert.equal(url.searchParams.get('utm_medium'), channel)
    assert.equal(url.searchParams.get('utm_campaign'), 'organic_share')
    assert.equal(shareUrl.includes(sentinelIncome), false)
    assert.equal(shareUrl.includes(`=${sentinelResidents}`), false)

    const generic = buildSharePayload(shareUrl, false, `TOP ${sentinelResidents}% — posição`)
    const position = buildSharePayload(shareUrl, true, 'TOP 12% — minha posição aproximada')
    assert.equal(generic.text, GENERIC_SHARE_MESSAGE)
    for (const serialized of [JSON.stringify(generic), JSON.stringify(position), buildWhatsAppUrl(generic), buildWhatsAppUrl(position)]) {
      assert.equal(serialized.includes(sentinelIncome), false)
      assert.equal(serialized.includes('moradores'), false)
    }
  }
})

test('App dispara eventos somente nos marcos do funil, sem tracking de teclado ou render', async () => {
  const app = await readFile(new URL('src/App.tsx', root), 'utf8')
  const submit = app.indexOf('async function handleSubmit')
  const invalidGate = app.indexOf('if (!income.ok || !household.ok)')
  const started = app.indexOf("trackAnalyticsEvent('calculation_started')")
  const loader = app.indexOf('const cachedBrazilRuntime')

  assert.equal(submit >= 0 && started > submit && invalidGate > started && loader > invalidGate, true)
  assert.equal((app.match(/trackAnalyticsEvent\('calculation_started'\)/g) ?? []).length, 1)
  assert.match(app, /useEffect\(\(\) => \{\s+if \(!showSharing\) return[\s\S]*?trackAnalyticsEvent\('calculation_completed'\)/)
  assert.match(app, /setActiveCalculationRequest\(request\)/)
  assert.equal((app.match(/\[activeCalculationRequest, showSharing\]/g) ?? []).length, 2)
  assert.match(app, /if \(completedCalculationRequest\.current === request\) return\s+completedCalculationRequest\.current = request\s+trackAnalyticsEvent\('calculation_completed'\)/)
  const viewedEffect = app.slice(
    app.indexOf('const trackResultViewed'),
    app.indexOf('function trackShareClick'),
  )
  assert.match(viewedEffect, /trackAnalyticsEvent\('result_viewed'\)/)
  assert.match(viewedEffect, /IntersectionObserver/)
  assert.match(viewedEffect, /if \(viewedCalculationRequest\.current === request\) return\s+viewedCalculationRequest\.current = request/)
  assert.match(app, /function trackShareClick\(\) \{\s+trackAnalyticsEvent\('share_clicked'\)\s+\}/)
  assert.equal(app.includes('share_channel'), false)
  assert.equal(app.includes('share_mode'), false)
  assert.match(app, /function handleRecalculate\(\) \{\s+trackAnalyticsEvent\('recalculate_clicked'\)/)

  const updateIncome = app.slice(app.indexOf('function updateIncome'), app.indexOf('function updateHousehold'))
  const updateHousehold = app.slice(app.indexOf('function updateHousehold'), app.indexOf('function changeHousehold'))
  assert.equal(updateIncome.includes('trackAnalyticsEvent'), false)
  assert.equal(updateHousehold.includes('trackAnalyticsEvent'), false)
})

test('pageviews das três rotas carregam a mesma entrada mínima do Plausible', async () => {
  const pages = await Promise.all([
    readFile(new URL('index.html', root), 'utf8'),
    readFile(new URL('metodologia/index.html', root), 'utf8'),
    readFile(new URL('privacidade/index.html', root), 'utf8'),
  ])
  for (const html of pages) {
    assert.match(html, /<script type="module" src="\/src\/analytics-entry\.ts"><\/script>/)
  }
})

test('transformRequest não depende do payload original para compor URL segura', () => {
  const options = buildPlausibleInitOptions(
    () => `https://rendacomparada.com.br/metodologia?income=${sentinelIncome}#${sentinelResidents}`,
  )
  const transformed = options.transformRequest({
    u: `https://unsafe.example/?income=${sentinelIncome}`,
    n: 'pageview',
  })
  assert.equal(transformed.u, 'https://rendacomparada.com.br/metodologia')
  assert.equal(JSON.stringify(transformed).includes(sentinelIncome), false)
})
